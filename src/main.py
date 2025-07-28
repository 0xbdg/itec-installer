from dialog import Dialog

d = Dialog(dialog="dialog",autowidgetsize=True)

d.set_background_title("ITEC-OS")

def menu():
    if d.msgbox("Welcome to ITEC-OS installer. Minimum installer for archiso Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua", width=50, height=10) == d.OK: 
 
        code, tags = d.menu("What sandwich toppings do you like?",
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
                d.msgbox("test")
                print(tags)

if __name__ == "__main__":
    menu()
