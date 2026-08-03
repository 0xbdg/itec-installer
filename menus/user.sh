#!/bin/bash

set_HOSTNAME(){
    hostname=$(dialog --stdout --cancel-label "BACK" --backtitle "$BACK_TITLE" --title "Create User Account" --inputbox "Enter your hostname" 10 $WIDTH)

    if [ $? -eq 1 ]; then
        menu
    fi

    HOST=$hostname
}

set_USERNAME(){
    username=$(dialog --stdout --cancel-label "BACK" --backtitle "$BACK_TITLE" --title "Create User Account" --inputbox "Enter your username" 10 $WIDTH)

    if [ $? -eq 1 ]; then
        set_HOSTNAME
    fi

    USERNAME=$username
}

set_PASSWORD(){
    password=$(dialog --stdout --cancel-label "BACK" --backtitle "$BACK_TITLE" --title "Create User Account" --passwordbox "Enter your password" 10 $WIDTH)

    if [ $? -eq 1 ]; then
        set_USERNAME
    fi

    confirm=$(dialog --stdout --cancel-label "BACK" --backtitle "$BACK_TITLE" --title "Create User Account" --passwordbox "Confirm password" 10 $WIDTH)

    if [ $? -eq 1 ]; then
        set_PASSWORD
    else
        if [[ "$confirm" = "$password" ]]; then
            PASSWORD=$confirm
        else
            dialog --backtitle "$BACK_TITLE" --msgbox "Password not matching, try again!!" 10 $WIDTH

            if [ $? -eq 0 ]; then
                set_PASSWORD
            fi
        fi
    fi
}

function user_menu { 
    set_HOSTNAME
    set_USERNAME
    set_PASSWORD

    menu
}
