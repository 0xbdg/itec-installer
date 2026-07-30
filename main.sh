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
    menu_dlg=$(dialog --stdout --colors --no-cancel --backtitle "$BACK_TITLE" --title "ITEC-OS Installation Menu" --menu "$LABEL" $HEIGHT $WIDTH 5 "Network" "Set up the network" "Keyboard" "Set system keyboard" "Timezone" "Set system time zone" "Locale" "Set system locale" "User" "Set hostname, username and password" "Partition" "Partition disk(s)" "Filesystems" "Configure filesystem and mount point" "Install" "Start installation" "Quit" "Exit installation")
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
            network_menu
            ;;
        "Partition")
            partition_menu
            ;;
        "Filesystems")
            filesystem_menu
            ;;
        "Quit" )
            exit
            ;;
    esac
}


#if ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1; then
        welcome_menu
        menu
#else
#       dialog --backtitle "$BACK_TITLE" --title "Connection failed" --msgbox "if you want to run ITEC-OS Installer, you must connect to internet first!!" 10 60
#fi

