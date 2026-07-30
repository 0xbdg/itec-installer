#!/bin/bash

function filesystem_menu {
    partitions=()

    while IFS= read -r line; do
        eval "$line"

        partitions+=("$NAME" "size:${SIZE};fstype:${FSTYPE:-unknown};mnt:${MOUNTPOINT}")
    done < <(lsblk -pP -o NAME,FSTYPE,SIZE,TYPE,MOUNTPOINT | grep 'TYPE="part"')
 
    filesystem_dlg=$(dialog --stdout --backtitle "$BACK_TITLE" --title "Setting the filesystem & mountpoint" --menu "$LABEL" $HEIGHT $WIDTH 5 "${partitions[@]}")

    echo $filesystem_dlg
}
