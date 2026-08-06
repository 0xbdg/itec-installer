#!/bin/bash

source "cores/config.sh"
source "menus/keyboard.sh"
source "menus/timezone.sh"
source "menus/locale.sh"
source "menus/user.sh"
source "menus/partition.sh"
source "menus/network.sh"
source "menus/filesystem.sh"
source "menus/install.sh"

function welcome_menu {
    dialog --yes-label "Next" --no-label "Cancel" --backtitle "$BACK_TITLE" --title "Welcome to ITEC-OS Installer" --yesno "\nWelcome to the itec-os Installer.\n\nThis installer will guide you through the steps required to install itec-os on your computer. During the installation, you will choose the installation drive, configure your system settings, and create your user account.\n\nBefore continuing, ensure you have backed up any important data if you plan to modify existing partitions.\n\nClick Next to continue or Cancel to exit the installer." $HEIGHT $WIDTH

    if [[ $? -eq 1 ]]; then
        exit
    fi

}

function exit_menu {
    dialog --yes-label "Exit" --no-label "Back" --backtitle "$BACK_TITLE" --title "Exit Installer" --yesno "\nThe installation has been canceled.\n\nNo further changes will be made to your system. If any installation steps were completed before cancellation, you may need to restart the installer to begin again.\n\nClick Exit to close the installer." $HEIGHT $WIDTH

    if [[ $? -eq 0 ]]; then
        exit
    elif [[ $? -eq 1 ]]; then
        menu
    fi
}

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
                dialog --backtitle "$BACK_TITLE" --title "Network Configuration" --msgbox "You have connected to internet, press ok to continue." 10 80

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
        "Install")
            install
            ;;
        "Quit" )
            exit_menu
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
