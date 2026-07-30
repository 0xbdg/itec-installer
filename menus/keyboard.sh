#!/bin/bash

function keyboard_menu {
    mapfile -t keys < <(localectl list-keymaps)
    keymenu=()
    for keymap in "${keys[@]}"; do
        keymenu+=("$keymap" "" "off")
    done
    keyboard_dlg=$(dialog --stdout --backtitle "$BACK_TITLE" --title "Select keyboard" --radiolist "$LABEL" $HEIGHT $WIDTH 10 "${keymenu[@]}") 
    is_exit=$?

    if [ $is_exit -eq 1 ]; then
        menu
    fi
    

    echo $keyboard_dlg
}
