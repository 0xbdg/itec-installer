#!/bin/bash

log=""
sudo pacman -S --noconfirm neofetch 2>&1 | while read -r line; do
    log="${log}${line}\n"
    dialog --infobox "$(printf "%b" "$log" | tail -n 25)" 30 80
done

sudo pacman -S --noconfirm htop btop fastfetch linux 2>&1 | {
    lines=()
    count=0

    while IFS= read -r line; do
        lines+=("$line")
        ((${#lines[@]} > 15)) && lines=("${lines[@]: -15}")

        ((count++))
        if (( count % 5 == 0 )); then
            dialog --infobox "$(printf '%s\n' "${lines[@]}")" 20 80
        fi
    done

    dialog --infobox "$(printf '%s\n' "${lines[@]}")" 20 80
}
sleep 1
