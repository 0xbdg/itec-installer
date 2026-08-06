#!/bin/bash

function install(){
    dialog --yes-label "Install" --no-label "Back" --backtitle "$BACK_TITLE" --title "Ready to install" --yesno "The installer is now ready to install the application on your computer.\n\nClick Install to begin the installation. If you want to review or change your installation settings, click Back." 10 $WIDTH

    if [ $? -eq 1 ]; then
        menu
    fi
}

L="""
function ready {
    dialog --back-title "$BACK_TITLE" --title "Installing & Configure System" --programbox "Installing Package..." 20 80 < <(sudo pacman -S --noconfirm linux linux-firmware 2>&1)

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
    sudo pacman -S --noconfirm neofetch 2>&1 | dialog --programbox "Installing Package..." 20 80
    dialog --programbox "Installing Package..." 20 80 < <(sudo pacman -S --noconfirm neofetch 2>&1)
}"""
