#!/usr/bin/env python3
import os
import subprocess
import dialog
import re

# Initialize dialog
d = dialog.Dialog(dialog="dialog", autowidgetsize=True)
d.set_background_title("Arch Linux Installer")

# Global configuration variables
DISK = ""
BOOT_MODE = ""
ROOT_SIZE = ""
SWAP_SIZE = ""
HOSTNAME = ""
TIMEZONE = ""
ROOT_PASSWORD = ""
USERNAME = ""
USER_PASSWORD = ""

def detect_boot_mode():
    """Detect if system uses UEFI or BIOS"""
    return "UEFI" if os.path.exists("/sys/firmware/efi/efivars") else "BIOS"

def get_disks():
    """Retrieve available disks using lsblk"""
    try:
        output = subprocess.check_output(
            "lsblk -dno NAME,SIZE -e7,11",
            shell=True,
            text=True
        ).strip().splitlines()
        return [line.split() for line in output]
    except subprocess.CalledProcessError:
        return []

def select_disk():
    """Dialog menu for disk selection"""
    disks = get_disks()
    if not disks:
        d.msgbox("No disks found!")
        exit(1)
    
    choices = []
    for disk in disks:
        disk_name = disk[0]
        disk_size = ' '.join(disk[1:])
        choices.append((disk_name, disk_size))
    
    code, disk = d.menu(
        "Select installation disk:",
        choices=choices
    )
    
    if code != d.OK:
        d.msgbox("Installation canceled")
        exit(0)
    return disk

def validate_size(size):
    """Validate partition size format"""
    pattern = r'^\d+[GM]iB$'
    return re.match(pattern, size) is not None

def get_timezones():
    """Get available timezones"""
    try:
        return subprocess.check_output(
            "find /usr/share/zoneinfo -type f | sed 's|/usr/share/zoneinfo/||' | sort",
            shell=True,
            text=True
        ).splitlines()
    except:
        return []

def run_command(cmd, exit_on_error=True):
    """Run shell command with error handling"""
    result = subprocess.run(cmd, shell=True)
    if exit_on_error and result.returncode != 0:
        d.msgbox(f"Command failed: {cmd}")
        exit(1)

def partition_disk():
    """Create partitions based on boot mode"""
    if BOOT_MODE == "UEFI":
        run_command(f"parted /dev/{DISK} --script mklabel gpt")
        run_command(f"parted /dev/{DISK} --script mkpart ESP fat32 1MiB 513MiB")
        run_command(f"parted /dev/{DISK} --script set 1 esp on")
        run_command(f"parted /dev/{DISK} --script mkpart primary ext4 513MiB {ROOT_SIZE}")
        run_command(f"parted /dev/{DISK} --script mkpart primary linux-swap {ROOT_SIZE} 100%")
    else:  # BIOS
        run_command(f"parted /dev/{DISK} --script mklabel msdos")
        run_command(f"parted /dev/{DISK} --script mkpart primary ext4 1MiB {ROOT_SIZE}")
        run_command(f"parted /dev/{DISK} --script set 1 boot on")
        run_command(f"parted /dev/{DISK} --script mkpart primary linux-swap {ROOT_SIZE} 100%")

def format_mount():
    """Format partitions and mount filesystems"""
    if BOOT_MODE == "UEFI":
        run_command(f"mkfs.fat -F32 /dev/{DISK}1")
        run_command(f"mkfs.ext4 /dev/{DISK}2")
        run_command(f"mkswap /dev/{DISK}3")
        run_command(f"swapon /dev/{DISK}3")
        os.makedirs("/mnt", exist_ok=True)
        run_command(f"mount /dev/{DISK}2 /mnt")
        os.makedirs("/mnt/boot", exist_ok=True)
        run_command(f"mount /dev/{DISK}1 /mnt/boot")
    else:  # BIOS
        run_command(f"mkfs.ext4 /dev/{DISK}1")
        run_command(f"mkswap /dev/{DISK}2")
        run_command(f"swapon /dev/{DISK}2")
        run_command(f"mount /dev/{DISK}1 /mnt")

def install_system():
    """Install base system and generate fstab"""
    run_command("pacstrap /mnt base linux linux-firmware nano sudo grub efibootmgr os-prober")
    run_command("genfstab -U /mnt >> /mnt/etc/fstab")

def configure_system():
    """Chroot into system and configure"""
    chroot_commands = f"""#!/bin/bash
ln -sf /usr/share/zoneinfo/{TIMEZONE} /etc/localtime
hwclock --systohc
echo "{HOSTNAME}" > /etc/hostname
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
echo "root:{ROOT_PASSWORD}" | chpasswd
useradd -m -G wheel {USERNAME}
echo "{USERNAME}:{USER_PASSWORD}" | chpasswd
sed -i 's/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers
mkinitcpio -P
"""

    if BOOT_MODE == "UEFI":
        chroot_commands += f"""
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
"""
    else:
        chroot_commands += f"""
grub-install --target=i386-pc /dev/{DISK}
"""

    chroot_commands += """
grub-mkconfig -o /boot/grub/grub.cfg
systemctl enable dhcpcd
exit
"""

    with open("/mnt/chroot_script.sh", "w") as f:
        f.write(chroot_commands)
    
    run_command("chmod +x /mnt/chroot_script.sh")
    run_command("arch-chroot /mnt /chroot_script.sh")
    os.remove("/mnt/chroot_script.sh")

def main():
    global DISK, BOOT_MODE, ROOT_SIZE, SWAP_SIZE, HOSTNAME, TIMEZONE, ROOT_PASSWORD, USERNAME, USER_PASSWORD
    
    # Check root privileges
    if os.geteuid() != 0:
        d.msgbox("This script must be run as root!")
        exit(1)
    
    # Detect boot mode
    BOOT_MODE = detect_boot_mode()
    d.msgbox(f"Detected Boot Mode: {BOOT_MODE}")
    
    # Disk selection
    DISK = select_disk()
    
    # Partition sizes
    while True:
        code, size = d.inputbox("Enter root partition size (e.g., 20GiB):")
        if code != d.OK:
            exit(0)
        if validate_size(size):
            ROOT_SIZE = size
            break
        d.msgbox("Invalid format! Use like '20GiB'")
    
    # Swap size
    while True:
        code, size = d.inputbox("Enter swap size (e.g., 4GiB):")
        if code != d.OK:
            exit(0)
        if validate_size(size):
            SWAP_SIZE = size
            break
        d.msgbox("Invalid format! Use like '4GiB'")
    
    # System configuration
    code, HOSTNAME = d.inputbox("Enter hostname:")
    if code != d.OK:
        exit(0)
    
    # Timezone selection
    timezones = get_timezones()
    code, TIMEZONE = d.menu("Select timezone:", choices=[(tz, "") for tz in timezones])
    if code != d.OK:
        exit(0)
    
    # Root password
    code, ROOT_PASSWORD = d.passwordbox("Set root password:")
    if code != d.OK:
        exit(0)
    
    # User creation
    code, USERNAME = d.inputbox("Create admin username:")
    if code != d.OK:
        exit(0)
    
    code, USER_PASSWORD = d.passwordbox(f"Set password for {USERNAME}:")
    if code != d.OK:
        exit(0)
    
    # Confirmation
    if d.yesno(f"WARNING: This will erase ALL data on /dev/{DISK}!\n\nProceed with installation?") != d.OK:
        d.msgbox("Installation canceled")
        exit(0)
    
    # Installation process
    try:
        partition_disk()
        format_mount()
        install_system()
        configure_system()
        run_command("umount -R /mnt", exit_on_error=False)
        d.msgbox("Installation Complete!\n\nRemove installation media and reboot.")
    except Exception as e:
        d.msgbox(f"Installation failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
