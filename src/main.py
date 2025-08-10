import os, subprocess, socket, time

from dialog import Dialog
from zoneinfo import available_timezones
from lists import keymaps, locales

d = Dialog(dialog="dialog")

d.set_background_title("ITEC-OS Installer (0xbdg)") 

DISK = ""
HOSTNAME = ""
TIMEZONE = ""
LOCALE = ""
KEYMAP = ""
USERNAME = ""
USER_PASSWORD = ""
SELECTED_FS = []

MENU_LABEL = "Use <UP> and <DOWN> key to navigate menus, Use <TAB> to switch between buttons."

check_internet = lambda: not socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(("8.8.8.8", 53))

def run_command(cmd, exit_on_error=True):
    """Run shell command with error handling"""
    result = subprocess.run(cmd, shell=True)
    if exit_on_error and result.returncode != 0:
        d.msgbox(f"Command failed: {cmd}")
        exit(1)

def detect_boot_mode():
    return "UEFI" if os.path.exists("/sys/firmware/efi/efivars") else "BIOS"

def network():
    if not check_internet():
        d.infobox("Scanning WiFi...")
        result = subprocess.run(
            ['nmcli', '-f', 'SSID', 'd', 'w', 'l'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdout.strip().split('\n')

        net = []
        
        for n in result[1:]:
            net.append((n,""))

        if len(net) <= 0:
            if d.msgbox("WiFi not found!")==d.OK:
                menu()

        code, tag = d.menu(title="Select WiFi Network", text=MENU_LABEL,choices=net) 

        if code == d.OK:
            code, password = d.passwordbox(text=f"Enter password for {tag}", insecure=True)

            if code == d.OK:
                print(password)

        else:
            menu()


    else:
        d.infobox("You have connected to internet!")
        time.sleep(2)
        menu()


def timezone():
    global TIMEZONE
    timezones = sorted(available_timezones())
    formatted_timezones = [(tz, "", False) for tz in timezones]

    code, tag =d.radiolist(title="Select timezone", text=MENU_LABEL, choices=formatted_timezones)

    if code == d.OK:
 
        if tag == "" or tag == None:
            d.msgbox("Belum memilih")
            timezone()
        TIMEZONE=tag 
        menu()

    elif code == d.CANCEL:
        menu()

def keyboard():
    global KEYMAP
    keymap = [(k, "", False) for k in keymaps]

    code, tag = d.radiolist(title="Select keymaps", text=MENU_LABEL,choices=keymap)

    if code == d.OK:
        KEYMAP = tag
        menu()

    else:
        menu()


def locale():
    global LOCALE
    loc = [(l, "", False) for l in locales]

    code, tag = d.radiolist(title="Select locale", text=MENU_LABEL,choices=loc)

    if code == d.OK:
        LOCALE=tag
        menu()

    else:
        menu()

def partition():
    global DISK
    get_disk = subprocess.run(
        ["lsblk", "-dno", "NAME,SIZE,TYPE"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True).stdout.strip().split('\n')

    choose = []
    for disk in get_disk:
        dev  = disk.split(None, 3) 
        if dev[2] == "disk":
            choose.append((f"/dev/{dev[0]}", "size:"+dev[1])) 

    code, disk = d.menu(title="Select the disk of partition",text=MENU_LABEL,choices=choose)

    if code == d.OK:
        if d.msgbox(title=f"Modify Partition Table on {disk}",text=f"cfdisk will be executed for disk {disk}.\n\nTo use GPT on PC BIOS systems an empty partition of 1MB must be added\nat the first 2GB of the disk with the TOGGLE 'bios_grub' enabled.\nNOTE: you don't need this on EFI systems.\n\nFor EFI systems GPT is mandatory and a FAT32 partition with at least\n512MB must be created with the TOGGLE 'boot', this will be used as\nEFI System Partition. This partition must have mountpoint as '/boot/efi'.\n\nAt least 2 partitions are required: swap and rootfs (/).\nFor swap, RAM*2 must be really enough. For / 600MB are required.\n\nWARNING: /usr is not supported as a separate partition.\nWARNING: changes made by parted are destructive, you've been warned.\n", width=60, height=50) == d.OK:
            DISK=disk

            if detect_boot_mode() == "UEFI":
                run_command(f"parted {disk} mklabel gpt")
                run_command(f"cfdisk {disk}")
                menu()
            elif detect_boot_mode() == "BIOS":
                run_command(f"parted {disk} mklabel msdos")
                run_command(f"cfdisk {disk}")
                menu()

    elif code == d.CANCEL:
        menu()

def filesystem():
    global SELECTED_FS
    fs = subprocess.run(["lsblk", '-ln','-o', 'NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE'],stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True, check=True).stdout.strip().split('\n')

    fs_disk = []

    for f in fs:
        dev = f.split(None,4) 
        if dev[2] == "part":
            fs_disk.append(("/dev/"+dev[0] if not len(dev) < 1 else "None", f"size:{dev[1] if not len(dev) < 2 else "None"}|fstype:{"None" if len(dev) < 5 else dev[4]}|mnt:{"None" if len(dev) < 4 else dev[3]}"))

    if len(fs_disk) <= 0:
        if d.msgbox("Disk part not found!"):
            partition()

    code, tag = d.menu(title="Setting the filesystem and mountpoint",text=MENU_LABEL, choices=fs_disk)

    if code == d.OK:
        s, fs_type = d.menu(
            title=f"Select the filesystem for {tag}", 
            text=MENU_LABEL,
            choices=[
                ("btrfs", "Oracle's Btrfs"),
                ("ext2", "Linux ext2"),
                ("ext3", "Linux ext3"),
                ("ext4", "Linux ext4"),
                ("f2fs", "Flash-Friendly Filesystem"),
                ("swap", "Linux swap"),
                ("vfat", "FAT32"),
                ("xfs", "SGI's XFS")
            ]
        )

        if s == d.OK:
            if fs_type == "swap":
                run_command(f"mkswap {tag}")
                run_command(f"swapon {tag}")
                d.msgbox(f"swap on {tag} success")
                filesystem()

            else:
                inp, val = d.inputbox(f"Please specify the mountpoint on {tag}")

                if inp == d.OK:
                    os.makedirs("/mnt", exist_ok=True)
                    if fs_type == "vfat":
                        run_command(f"mkfs.fat -F32 {tag}")
                    else:
                        run_command(f"mkfs.{fs_type} {tag}")

                    os.makedirs(str(val), exist_ok=True)
                    run_command(f"mount {tag} {val}")
                    SELECTED_FS.append(tag)
                    filesystem()
        else:
            filesystem()
    else:
        menu()

def user_acc():
    global HOSTNAME, USERNAME, USER_PASSWORD
    h_code , hostname = d.inputbox("Enter your hostname: ", init=HOSTNAME)

    if h_code == d.OK:
        HOSTNAME = hostname

    else:
        menu()

    name_code, username = d.inputbox("Enter your username: ", init=USERNAME)

    if name_code == d.OK:
        USERNAME = username

    else:
        user_acc()

    pass_code, password = d.passwordbox("Enter your password: ", init=USER_PASSWORD,insecure=True)

    if pass_code == d.OK:
        if len(str(password)) < 4:
            d.msgbox("")
            user_acc()
        USER_PASSWORD = password
    else:
        user_acc()

    confirm_code, confirm = d.passwordbox("Confirm your password: ",insecure=True)

    if confirm_code == d.OK:
        if confirm == password:
            menu()
        else:
            d.msgbox("Password not match!")
            user_acc()

def install_system():
    packages = "base base-devel linux linux-firmware vim sudo grub git efibootmgr os-prober networkmanager alsa-utils openbox lightdm lightdm-gtk-greeter xorg xorg-xauth xorg-server xorg-xinit xdg-utils tint2 caja firefox kitty feh conky rofi perl perl-gtk3 perl-data-dump"
    d.infobox("Installing package to system, please wait...")
    run_command(f"pacstrap /mnt {packages}")
    run_command("genfstab -U /mnt >> /mnt/etc/fstab")

    d.infobox("Configuring system, please wait...")
    chroot_commands = f"""#!/bin/bash
ln -sf /usr/share/zoneinfo/{TIMEZONE} /etc/localtime
hwclock --systohc
echo "{HOSTNAME}" > /etc/hostname
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
echo "LANG={LOCALE}" > /etc/locale.conf
localectl set-keymap {KEYMAP}
echo "KEYMAP={KEYMAP}" > /etc/vconsole.conf
echo "root:{USER_PASSWORD}" | chpasswd
useradd -m -G wheel {USERNAME}
echo "{USERNAME}:{USER_PASSWORD}" | chpasswd
sed -i 's/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers
mkinitcpio -P
"""
    if detect_boot_mode() == "UEFI":
        chroot_commands += f"""
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
"""
    elif detect_boot_mode() == "BIOS":
        chroot_commands += f"""
grub-install --target=i386-pc {DISK}
"""
    chroot_commands += """
grub-mkconfig -o /boot/grub/grub.cfg
systemctl enable NetworkManager.service
systemctl start NetworkManager.service
systemctl enable lightdm.service
exit
"""
    with open("/mnt/chroot_script.sh", "w") as f:
        f.write(chroot_commands)

    run_command("chmod +x /mnt/chroot_script.sh")
    run_command("arch-chroot /mnt /chroot_script.sh")
    os.remove("/mnt/chroot_script.sh") 
 
    run_command("umount -R /mnt", exit_on_error=False)
    d.msgbox("Installation complete, restart your computer")

def welcome():
     
    if os.geteuid() != 0:
        d.msgbox("must be run as root!")
        exit(1)
    
    d.infobox(text=f"Detect boot mode: {detect_boot_mode()}")
    time.sleep(1)
    if d.msgbox(title="ITEC Installer",text="Welcome to ITEC-OS. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua", width=50, height=10) == d.OK: 
        menu()

def menu(): 
    code, tags = d.menu(
            text=MENU_LABEL,
            choices=[("Network", "Connected" if check_internet() else "Disconnected"),
                     ("Timezone", TIMEZONE), 
                     ("Keyboard", KEYMAP),
                     ("Locale", LOCALE),
                     ("Partition", DISK),
                     ("Filesystem", SELECTED_FS),
                     ("User Account", HOSTNAME),
                     ("Install", "")
            ],
            title="ITEC-OS Installation Menu",
            width=50, 
    )
    if code == d.OK:
        if tags == "Network":
            network()

        elif tags == "Timezone":
            timezone()

        elif tags == "Keyboard":
            keyboard()

        elif tags == "Locale":
            locale()

        elif tags == "Partition":
            partition()

        elif tags == "Filesystem":
            filesystem()

        elif tags == "User Account":
            user_acc()

        elif tags == "Install":
            install_system()

    elif code == d.CANCEL:
        if d.yesno("Are yo sure?") == d.OK:
            exit(1)

        else:
            menu()

if __name__ == "__main__":
    welcome()
