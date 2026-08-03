#!/bin/bash/

source "cores/config.sh"
source "menus/welcome.sh"
source "menus/keyboard.sh"
source "menus/timezone.sh"
source "menus/locale.sh"
source "menus/user.sh"
source "menus/partition.sh"
source "menus/network.sh"
source "menus/filesystem.sh"

function menu {
    menu_dlg=$(dialog --stdout --colors --no-cancel --backtitle "$BACK_TITLE" --title "ITEC-OS Installation Menu" --menu "$LABEL" $HEIGHT $WIDTH 5 "Network" "Set up the network" "Keyboard" "Set system keyboard" "Timezone" "Set system time zone" "Locale" "Set system locale" "User" "Set hostname, username and password" "Partition" "Partition disk(s)" "Filesystems" "Configure filesystem and mount point" "Install" "Start installation" "Quit" "Exit installer")
    exit=$?

    case $exit in  
        255)
            exit
            ;;
    esac

    case $menu_dlg in
        "Keyboard")
            keyboard_menu
        ;;
        "Timezone")
            timezone_menu
        ;;
        "Locale")
            locale_menu
            ;;
        "User")
            user_menu
            ;;
        "Network")
            if ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1; then
                dialog --backtitle "$BACK_TITLE" --title "Network Configuration" --msgbox "You have connected to internet, press ok" 10 80

                if [ $? -eq 0 ]; then
                    menu
                fi
            else
                network_menu
            fi

            ;;
        "Partition")
            partition_menu
            ;;
        "Filesystems")
            filesystem_menu
            ;;
        "Quit" )
            echo $LOCALE
            echo $TIMEZONE
            echo $KEYBOARD
            echo $HOST
            echo $USERNAME
            echo $PASSWORD
            echo $SELECTED_PART

            exit
            ;;
    esac
}

welcome_menu
menu
