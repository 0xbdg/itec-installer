#!/bin/bash

partition_MBR(){
    dialog --colors --backtitle "$BACK_TITLE" --title "${BLACK}Modify Partition Table on $1" --msgbox "\n${BOLD}cfdisk${NORMAL} will be executed for disk ${BOLD}$1${NORMAL}.\n\nAt least 2 partitions are required: swap and rootfs (/).\nFor swap, RAM*2 must be really enough. For / 600MB are required.\n\nWARNING: /usr is not supported as a separate partition.\nWARNING: changes made by parted are destructive, you've been warned." $HEIGHT $WIDTH

    if [[ $? -eq 0 ]]; then
        echo "cfdisk $1"
    fi
}

partition_GPT(){
    dialog --colors --backtitle "$BACK_TITLE" --title "${BLACK}Modify Partition Table on $1" --msgbox "\n${BOLD}cfdisk${NORMAL} will be executed for disk ${BOLD}$1${NORMAL}.\n\nTo use GPT on PC BIOS systems an empty partition of 1MB must be added\nat the first 2GB of the disk with the TOGGLE 'bios_grub' enabled.\nNOTE: you don't need this on EFI systems.\n\nFor EFI systems GPT is mandatory and a FAT32 partition with at least\n512MB must be created with the TOGGLE 'boot', this will be used as\nEFI System Partition. This partition must have mountpoint as '/boot/efi'.\n\nAt least 2 partitions are required: swap and rootfs (/).\nFor swap, RAM*2 must be really enough. For / 600MB are required.\n\nWARNING: /usr is not supported as a separate partition.\nWARNING: changes made by parted are destructive, you've been warned.\n" $HEIGHT $WIDTH

    if [[ $? -eq 0 ]]; then
        echo "cfdisk $1"
    fi

}

function partition_menu {
    mapfile -t parts < <(lsblk -d -n -o NAME) 
    part=()

    for device in "${parts[@]}"; do
        part+=("/dev/$device" "size:$(lsblk /dev/$device -d -n -o SIZE);type:$(lsblk /dev/$device -d -n -o TYPE)")
    done

    partition_dlg=$(dialog --stdout --colors --cancel-label "BACK" --backtitle "$BACK_TITLE" --title "${BLACK}Select the disk of partition" --menu "$LABEL" $HEIGHT $WIDTH 8 "${part[@]}")

    if [[ $? -eq 1 ]]; then
        menu
    fi
    
    if [[ "$MODE" == "UEFI" ]]; then
        partition_GPT $partition_dlg
    elif [[ "$MODE" == "MBR" ]]; then
        partition_MBR $partition_dlg
    fi

    SELECTED_PART=$partition_dlg
    menu
}
