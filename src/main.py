import os, subprocess, socket, time

from dialog import Dialog
from zoneinfo import available_timezones
from lists import keymaps, locales

d = Dialog(dialog="dialog",autowidgetsize=True)

d.set_background_title("ITEC-OS Installer (0xbdg)") 

DISK = ""
BOOT_MODE = ""
ROOT_SIZE = ""
SWAP_SIZE = ""
HOSTNAME = ""
TIMEZONE = ""
LOCALE = ""
KEYMAP = ""
ROOT_PASSWORD = ""
USERNAME = ""
USER_PASSWORD = ""

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
    if check_internet():
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

        code, tag = d.menu(title="Select WiFi Network", text=MENU_LABEL,choices=net) 

        if code == d.OK:
            code, password = d.passwordbox(text=f"Enter password for {tag}", width=70, insecure=True)

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
    get_disk = subprocess.run(
        ["lsblk", "-dno", "NAME,SIZE", "-e7,11"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True).stdout.strip().split('\n')

    if not get_disk:
        d.msgbox("no disk found")
        exit(1)

    choose = []
    for disk in get_disk:
        dev, size = disk.split()
        choose.append((f"/dev/{dev}", "size:"+size))

    code, disk = d.menu(title="Select the disk of partition",text=MENU_LABEL,choices=choose)

    if code == d.OK:
        if d.msgbox(title=f"Modify Partition Table on {disk}",text=f"cfdisk will be executed for disk {disk}.\n\nTo use GPT on PC BIOS systems an empty partition of 1MB must be added\nat the first 2GB of the disk with the TOGGLE 'bios_grub' enabled.\nNOTE: you don't need this on EFI systems.\n\nFor EFI systems GPT is mandatory and a FAT32 partition with at least\n100MB must be created with the TOGGLE 'boot', this will be used as\nEFI System Partition. This partition must have mountpoint as '/boot/efi'.\n\nAt least 2 partitions are required: swap and rootfs (/).\nFor swap, RAM*2 must be really enough. For / 600MB are required.\n\nWARNING: /usr is not supported as a separate partition.\nWARNING: changes made by parted are destructive, you've been warned.\n") == d.OK:
            #run_command(f"cfdisk {disk}")
            print("success")

    elif code == d.CANCEL:
        menu()


def welcome():
    """
    if os.geteuid() != 0:
        d.msgbox("This script must be run as root!")
        exit(1)
    """
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
                     ("Partition", ""),
                     ("User", ""),
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

    elif code == d.CANCEL:
        if d.yesno("Are yo sure?") == d.OK:
            exit(1)

        else:
            menu()

if __name__ == "__main__":
    welcome()
