import os, subprocess

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

def run_command(cmd, exit_on_error=True):
    """Run shell command with error handling"""
    result = subprocess.run(cmd, shell=True)
    if exit_on_error and result.returncode != 0:
        d.msgbox(f"Command failed: {cmd}")
        exit(1)

def detect_boot_mode():
    return "UEFI" if os.path.exists("/sys/firmware/efi/efivars") else "BIOS"

def timezone():
    global TIMEZONE
    timezones = sorted(available_timezones())
    formatted_timezones = [(tz, "", False) for tz in timezones]

    code, tag =d.radiolist(text="Select timezone", choices=formatted_timezones)

    if code == d.OK:
 
        if tag == "" or tag == None:
            d.msgbox("Belum memilih")
            timezone()
        TIMEZONE=tag 
        menu()

    elif code == d.CANCEL:
        menu()

def keyboard():
    keymap = [(k, "", False) for k in keymaps]

    code, tag = d.radiolist(text="Select keymaps", choices=keymap)



def locale():
    loc = [(l, "", False) for l in locales]

    code, tag = d.radiolist(text="Select locale", choices=loc)

def partition():
    get_disk = subprocess.check_output(
        "lsblk -dno NAME,SIZE -e7,11",
        shell=True,
        text=True).strip().splitlines()

    if not get_disk:
        d.msgbox("no disk found")
        exit(1)

    choose = []
    for disk in get_disk:
        choose.append(("/dev/"+disk[0], disk[1:]))

    code, disk = d.menu(text="test",choices=choose)

    if code == d.CANCEL:
        menu()


def welcome():
     if d.msgbox("Welcome to ITEC installer. Minimum installer for ITEC-OS Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua", width=50, height=10) == d.OK: 
        menu()

def menu(): 
    code, tags = d.menu(
        text=f"Detected boot mode: {detect_boot_mode()}",
            choices=[("Timezone", TIMEZONE), 
                     ("Keyboard", KEYMAP),
                     ("Locale", LOCALE),
                     ("Partition", "Disk configuration"),
                     ("User", "User account"),
                     ("Install", "")
            ],
            title="ITEC-OS Installer",
            width=50, 
    )
    if code == d.OK:
        if tags == "Timezone":
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
