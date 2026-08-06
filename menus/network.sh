#!/bin/bash

connect() {
    wifi_pass=$(dialog --stdout --backtitle "$BACK_TITLE" --title "Connect to the WiFi" --passwordbox "Enter $1 password" 10 80)

    if [[ $? -eq 1 ]]; then
        network_menu
    fi
    echo $wifi_pass
}

function network_menu {
    dialog --backtitle "$BACK_TITLE" --title "Scanning the network" --infobox "Scanning all wifi, please wait..." 10 60
    net=()
    while IFS=: read -r ssid security signal; do
        net+=("$ssid" "sig:$signal;sec:$security")
    done < <(
        nmcli -t -f SSID,SECURITY,SIGNAL device wifi list |
        awk -F: '$1 != ""'
    ) 

    network_dlg=$(dialog --stdout --backtitle "$BACK_TITLE" --title "Select & connect to network" --extra-button --extra-label "Rescan" --menu "$LABEL" $HEIGHT $WIDTH 5 "${net[@]}")

    case $? in 
        0)
            connect "\"$network_dlg\""
            ;;
        1)
            menu
            ;;
        3)
            network_menu
            ;;
    esac
}
