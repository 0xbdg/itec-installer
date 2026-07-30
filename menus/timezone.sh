#!/bin/bash

timezone_menu(){
    mapfile -t timezones < <(timedatectl list-timezones)

    tzmenu=()

    for timezone in "${timezones[@]}"; do
        tzmenu+=("$timezone" "" "off")
    done

    timezone_dlg=$(dialog --stdout --backtitle "$BACK_TITLE" --title "Select Time Zone" --radiolist "$LABEL" $HEIGHT $WIDTH 10 "${tzmenu[@]}")

    if [ $? -eq 1 ]; then
        menu
    fi

    echo $timezone_dlg
}
