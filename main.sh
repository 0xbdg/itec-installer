#!/bin/bash

source "cores/config.sh"
source "cores/colors.sh"
source "menus/keyboard.sh"
source "menus/timezone.sh"
source "menus/locale.sh"
source "menus/user.sh"
source "menus/partition.sh"
source "menus/network.sh"
source "menus/filesystem.sh"
source "menus/profile.sh"
source "menus/install.sh"

function welcome_menu {
    MODE=$([ -d "/sys/firmware/efi/efivars" ] && echo "UEFI" || echo "BIOS")
    dialog --colors --yes-label "Next" --no-label "Cancel" --backtitle "$BACK_TITLE" --title "${BLACK}Welcome to ITEC-OS Installer" --yesno "\nWelcome to the ITEC-OS Installer.\n\nThis installer will guide you through the steps required to install ITEC-OS on your computer. During the installation, you will choose the installation drive, configure your system settings, and create your user account.\n\nBefore continuing, ensure you have backed up any important data if you plan to modify existing partitions.\n\nClick ${BOLD}Next${NORMAL} to continue or ${BOLD}Cancel${NORMAL} to exit the installer." $HEIGHT $WIDTH

    if [[ $? -eq 0 ]]; then
        menu
    elif [[ $? -eq 1 ]]; then
        exit
    fi

}

function exit_menu {
    dialog --colors --yes-label "Exit" --no-label "Back" --backtitle "$BACK_TITLE" --title "${BLACK}Exit Installer" --yesno "\nThe installation has been canceled.\n\nNo further changes will be made to your system. If any installation steps were completed before cancellation, you may need to restart the installer to begin again.\n\nClick ${BOLD}Exit ${NORMAL}to close the installer." 15 $WIDTH

    if [[ $? -eq 0 ]]; then
        echo $LOCALE
        echo $TIMEZONE
        echo $KEYBOARD
        echo $HOST
        echo $USERNAME
        echo $PASSWORD
        echo $SELECTED_PART
        echo $MODE
        exit
    elif [[ $? -eq 1 ]]; then
        menu
    fi
}

function menu {
    menu_dlg=$(dialog --stdout --colors --no-cancel --backtitle "$BACK_TITLE" --title "${BLACK}ITEC-OS Installer Menu" --menu "$LABEL" $HEIGHT $WIDTH 10 "Network" "Set up the network" "Keyboard" "Set system keyboard" "Timezone" "Set system time zone" "Locale" "Set system locale" "User" "Set hostname, username and password" "Partition" "Partition disk(s)" "Filesystems" "Configure filesystem and mount point" "Profile" "Set DEWM, Drivers & Display Manager" "Install" "Start installation" "Quit" "Exit installer")
    exit=$?

    case $exit in  
        255)
            menu
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
                dialog --no-lines --colors --backtitle "$BACK_TITLE" --msgbox "You have connected to internet, press ${BOLD}OK${NORMAL} to continue." 5 80

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
        "Profile")
            profile_menu
            ;;
        "Install")
            install
            ;;
        "Quit" )
            exit_menu
            ;;
    esac
}

trap '' SIGINT SIGTSTP SIGQUIT
welcome_menu
menu
