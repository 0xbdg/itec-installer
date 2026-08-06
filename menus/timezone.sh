#!/bin/bash

timezone_menu(){
    mapfile -t timezones < <(timedatectl list-timezones)

    tzmenu=()

    for timezone in "${timezones[@]}"; do
        if [[ "$timezone" = "$TIMEZONE" ]]; then
            tzmenu+=("$timezone" "" "on")
        else 
            tzmenu+=("$timezone" "" "off")
        fi
    done

    timezone_dlg=$(dialog --stdout --backtitle "$BACK_TITLE" --title "Select Time Zone" --radiolist "$LABEL" $HEIGHT $WIDTH 10 "${tzmenu[@]}")

    if [[ $? -eq 1 ]]; then
        menu
    fi

    TIMEZONE=$timezone_dlg
    menu
}
