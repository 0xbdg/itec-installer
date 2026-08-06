#!/bin/bash

locale_menu(){
    mapfile -t locales < <(grep '^#[a-z]' /etc/locale.gen | sed 's/^#//')

    locales_menu=()
    for locale in "${locales[@]}"; do
        if [[ "$locale" = "$LOCALE" ]]; then
            locales_menu+=("$locale" "" "on")
        else
            locales_menu+=("$locale" "" "off")
        fi
    done

    locale_dlg=$(dialog --stdout --backtitle "$BACK_TITLE" --title "Select Locale" --radiolist "$LABEL" $HEIGHT $WIDTH 10 "${locales_menu[@]}")

    if [[ $? -eq 1 ]]; then
        menu
    fi

    LOCALE="$locale_dlg"
    menu
}
