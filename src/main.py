from subprocess import *
from dialog import Dialog
from zoneinfo import available_timezones

d = Dialog(dialog="dialog",autowidgetsize=True)

d.set_background_title("ITEC-OS")

def timezone():
    timezones = sorted(available_timezones())
    formatted_timezones = [(tz, "", False) for tz in timezones]

    code, tag =d.radiolist(text="Select timezone", choices=formatted_timezones)

    if code == d.OK:
        d.msgbox(f"{tag} set success")
        menu()

    print(tag)

def welcome():
     if d.msgbox("Welcome to ITEC-OS installer. Minimum installer for archiso Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua", width=50, height=10) == d.OK: 
        menu()

def menu(): 
    code, tags = d.menu("",
            choices=[("Timezone", "Set location"),
                     ("Locale", "Set locale"),
                     ("Keyboard", "Keyboard layout"),
                     ("Mirror", "Set mirror"),
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

if __name__ == "__main__":
    welcome()
