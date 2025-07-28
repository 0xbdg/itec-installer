from dialog import Dialog

d = Dialog(dialog="dialog",autowidgetsize=True)

d.set_background_title("ITEC-OS")

if d.yesno("Welcome to ITEC-OS installer\nDo you want to continue?") == d.OK: 

    code, tags = d.menu("What sandwich toppings do you like?",
                             choices=[("Timezone", "Set location"),
                                      ("Locale", "Set locale"),
                                      ("Keyboard", "Keyboard layout"),
                                      ("Mirror", "Set mirror"),
                                      ("Partition", "Disk configuration"),
                                      ("User", "User account"),
                                      ("Install", "")
                            ],
                             title="ITEC-OS Installer",)
    if code == d.OK:
        if tags == "Timezone":
            d.msgbox("test")
        print(tags)
