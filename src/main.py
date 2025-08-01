import os

from subprocess import *
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
ROOT_PASSWORD = ""
USERNAME = ""
USER_PASSWORD = ""

def detect_boot_mode():
    return "UEFI" if os.path.exists("/sys/firmware/efi/efivars") else "BIOS"

def timezone():
    global TIMEZONE
    timezones = sorted(available_timezones())
    formatted_timezones = [(tz, "", False) for tz in timezones]

    if TIMEZONE == "" or TIMEZONE == None:
        code, tag =d.radiolist(text="Select timezone", choices=formatted_timezones)

        if code == d.OK:
 
            if tag == "" or tag == None:
                d.msgbox("Belum memilih")
                timezone()
            TIMEZONE=tag
            d.msgbox(f"{TIMEZONE} set success")
            menu()

        elif code == d.CANCEL:
            menu()

    else:
        d.msgbox(f"{TIMEZONE}, do you want to change?")
        menu()

def locale():
    a = [(i, "", False) for i in locales]

    code, tag = d.radiolist(text="Select locale (recommend is en_US.UTF-8)", choices=a)

    if code == d.OK:
        d.msgbox(tag)
        menu()

    elif code == d.CANCEL:
        menu()

def keyboard():
    keymap = [(k, "", False) for k in keymaps]

    code, tag = d.radiolist(text="Select keymaps", choices=keymap)

def select_disk():
    pass

def welcome():
     if d.msgbox("Welcome to ITEC installer. Minimum installer for ITEC-OS Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua", width=50, height=10) == d.OK: 
        menu()

def menu(): 
    code, tags = d.menu(
            text=f"Detected boot {detect_boot_mode()}",
            choices=[("Timezone", "Set location"),
                     ("Locale", "Set locale"),
                     ("Keyboard", "Keyboard layout"), 
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

        elif tags == "Locale":
            locale()

        elif tags == "Keyboard":
            keyboard()

    elif code == d.CANCEL:
        exit()

if __name__ == "__main__":
    welcome()
