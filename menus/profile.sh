#!/bin/bash

function dewm_menu {
    $dewm_dlg=$(dialog --stdout --colors --backtitle "$BACK_TITLE" --title "${BLACK}Choose DE & WM" --radiolist "$LABEL" $HEIGHT $WIDTH 5 "XFCE" "" "off" "KDE" "" "off" "i3wm" "" "off" "Sway" "" "off")

    if [[ $? -eq 1 ]]; then
        profile_menu
    fi

    case $dewm_dlg in 
        "XFCE")
            ;;
        "KDE")
            ;;
        "i3wm")
            ;;
        "Sway")
            ;;
        *)
            profile_menu
            ;;
    esac
}

function driver_menu {
    driver_dlg=$(dialog --stdout --colors --backtitle "$BACK_TITLE" --title "${BLACK}Choose Graphic Driver" --radiolist "$LABEL" $HEIGHT $WIDTH 5 "All Open Source" "Default" "on" "AMD / ATI" "Open Source" "off" "Intel" "Open Source" "off" "Nvidia" "noveau driver etc" "off" "VMWare / Virtualbox" "Open Source" "off")

    if [[ $? -eq 1 ]]; then
        profile_menu
    fi
}

function display_menu {
    display_dlg=$(dialog --stdout --colors --backtitle "$BACK_TITLE" --title "${BLACK}Choose Display Manager" --radiolist "$LABEL" $HEIGHT $WIDTH 5 "" "" "")

    if [[ $? -eq 1 ]]; then
        profile_menu
    fi
}

function profile_menu {
    profile_dlg=$(dialog --stdout --colors --backtitle "$BACK_TITLE" --title "${BLACK}Profile Configuration" --menu "$LABEL" $HEIGHT $WIDTH 5 "DEWM" "Manage desktop environment & window manager" "Drivers" "Manage drivers for graphics hardware" "Display" "Manage the login screen session startup")

    if [[ $? -eq 1 ]]; then
        menu
    fi

    case $profile_dlg in 
        "DEWM")
            dewm_menu
            ;;
        "Drivers")
            driver_menu
            ;;
        "Display")
            display_menu
            ;;
    esac
}
