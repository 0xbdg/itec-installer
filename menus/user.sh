#!/bin/bash

set_HOSTNAME(){
    hostname=$(dialog --stdout --colors --cancel-label "Back" --backtitle "$BACK_TITLE" --title "${BLACK}Create User Account" --inputbox "Enter your hostname" 10 $WIDTH)

    if [[ $? -eq 1 ]]; then
        menu
    fi

    HOST=$hostname
}

set_USERNAME(){
    username=$(dialog --stdout --colors --cancel-label "Back" --backtitle "$BACK_TITLE" --title "${BLACK}Create User Account" --inputbox "Enter your username" 10 $WIDTH)

    if [[ $? -eq 1 ]]; then
        set_HOSTNAME
    fi

    USERNAME=$username
}

set_PASSWORD(){
    password=$(dialog --stdout --colors --cancel-label "Back" --backtitle "$BACK_TITLE" --title "${BLACK}Create User Account" --passwordbox "Enter your password" 10 $WIDTH)

    if [[ $? -eq 1 ]]; then
        set_USERNAME
    fi

    confirm=$(dialog --stdout --colors --cancel-label "Back" --backtitle "$BACK_TITLE" --title "${BLACK}Create User Account" --passwordbox "Confirm password" 10 $WIDTH)

    if [[ $? -eq 1 ]]; then
        set_PASSWORD
    else
        if [[ "$confirm" = "$password" ]]; then
            PASSWORD=$confirm
        else
            dialog --colors --no-lines --backtitle "$BACK_TITLE" --msgbox "Password not matching, try again!!" 5 $WIDTH

            if [[ $? -eq 0 ]]; then
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
