#!/bin/bash

function network_menu {
    dialog --backtitle "$BACK_TITLE" --infobox "Scanning all wifi, please wait..." 10 60
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
            echo "ok"
            break
            ;;
        1)
            echo "cancel"
            ;;
        3)
            network_menu
            ;;
    esac

    echo "$network_dlg"
    
}
