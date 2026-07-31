#!/bin/bash

set_MNT(){
    mnt_input=$(dialog --stdout --backtitle "$BACK_TITLE" --inputbox "Please specify the mountpoint on $1" 10 $WIDTH)

    echo $mnt_input
}

set_FS(){
    choose=$(dialog --stdout --cancel-label "Back" --backtitle "$BACK_TITLE" --title "Select the filesystem for $1" --menu "$LABEL" $HEIGHT $WIDTH 5 "btrfs" "Oracle's Btrfs" "ext2" "Linux ext2" "ext3" "Linux ext3" "ext4" "Linux ext4" "f2fs" "Flash-Friendly Filesystem" "swap" "Linux swap" "vfat" "FAT32" "xfs" "SGI'S XFS")

    if [ $? -eq 1 ]; then
        filesystem_menu
    fi

    case $choose in 
        "btrfs")
            echo "btrfs"
            set_MNT $1
            ;;
        "ext2")
            echo "ext2"
            set_MNT $1
            ;;
        "ext3")
            echo "ext3"
            set_MNT $1
            ;;
        "ext4")
            echo "ext4"
            set_MNT $1
            ;;
        "f2fs")
            echo "f2fs"
            set_MNT $1
            ;;
        "swap")
            echo "swap"
            set_MNT $1
            ;;
        "vfat")
            echo "vfat"
            set_MNT $1
            ;;
        "xfs")
            echo "xfs"
            set_MNT $1
            ;;
    esac
}

function filesystem_menu {
    partitions=()

    while IFS= read -r line; do
        eval "$line"

        partitions+=("$NAME" "fstype:${FSTYPE};mnt:${MOUNTPOINT};size:${SIZE}")
    done < <(lsblk -pP -o NAME,FSTYPE,SIZE,TYPE,MOUNTPOINT | grep 'TYPE="part"')
 
    filesystem_dlg=$(dialog --stdout --backtitle "$BACK_TITLE" --title "Setting the filesystem & mountpoint" --menu "$LABEL" $HEIGHT $WIDTH 5 "${partitions[@]}")

    if [ $? -eq 1 ]; then
        menu
    fi

    set_FS $filesystem_dlg
}
