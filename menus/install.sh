#!/bin/bash

function summary(){
    dialog --backtitle "$BACK_TITLE" --title "" --yesno "" $HEIGHT $WIDTH
}

log=""
sudo pacman -S --noconfirm neofetch 2>&1 | while read -r line; do
    log="${log}${line}\n"
    dialog --progressbox "$(printf "%b" "$log" | tail -n 25)" 30 80
done

sudo pacman -S --noconfirm htop btop fastfetch linux 2>&1 | {
    lines=()
    count=0

    while IFS= read -r line; do
        lines+=("$line")
        ((${#lines[@]} > 15)) && lines=("${lines[@]: -15}")

        ((count++))
        if (( count % 5 == 0 )); then
            dialog --progressbox "$(printf '%s\n' "${lines[@]}")" 20 80
        fi
    done

    dialog --progressbox "$(printf '%s\n' "${lines[@]}")" 20 80
}

sudo pacman -S --noconfirm neofetch 2>&1 | dialog --programbox "Installing Package..." 20 80
dialog --programbox "Installing Package..." 20 80 < <(sudo pacman -S --noconfirm neofetch 2>&1)
