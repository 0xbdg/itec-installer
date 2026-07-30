#!/bin/bash

function user_menu {
    hostname=$(dialog --stdout --cancel-label "BACK" --backtitle "$BACK_TITLE" --title "Create User Account" --inputbox "Enter hostname" 10 80)

    if [ $? -eq 1 ]; then
        menu
    fi

    echo $hostname

    username=$(dialog --stdout --cancel-label "BACK" --backtitle "$BACK_TITLE" --title "Create User Account" --inputbox "Enter username" 10 80)

    if [ $? -eq 1 ]; then
        user_menu
    fi

    echo $username

    password=$(dialog --stdout cancel-label "BACK" --backtitle "$BACK_TITLE" --title "Create User Account" --passwordbox "Enter your password" 10 80)

    echo $password

    if [ $? -eq 1 ]; then
        user_menu
    fi

    confirm=$(dialog --stdout --cancel-label "BACK" --backtitle "$BACK_TITLE" --title "Create User Account" --passwordbox "Confirm password" 10 80)

    echo $confirm

    if [ $? -eq 1 ]; then
        user_menu 
    fi
}
