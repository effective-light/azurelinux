#!/bin/bash
if [ "$EUID" -ne 0 ]; then
  echo "error: this script must be run as root."
  exit 1
fi

set -e

scriptPath=$(realpath ${BASH_SOURCE[0]})
scriptDir=$(dirname "$scriptPath")

# ---- constants ----

tftpLocalDir="/var/lib/tftpboot"
httpLocalDir="/etc/httpd/azl-os"

# If a place holder string is used for `pxe|pxeImageUrl`, to replace it in
# grub.cfg at build time, set 'httpRootPlaceHolder' to the place holder string.
httpRootPlaceHolder=""
httpRoot=""

# ---- Commnad Line ----

function show_usage() {
    echo
    echo "$(basename ${BASH_SOURCE[0]}) -s <source-path> [-p <iso-url-place-holder> -r <iso-url>]"
    echo
    echo "  Sample script that deploys the Azure Linux PXE artifacts to a PXE server."
    echo "  It assumes a tftp and an http servers are running on the local machine where:"
    echo "  - tftp root is at /var/lib/tftpboot"
    echo "  - http root is at /etc/httpd"
    echo
    echo "  -s <source-path>         : local path to the source of the artifacts to deploy."
    echo "                             It accepts either:"
    echo "                             - a full path to an iso image file."
    echo "                             - a full path to a local folder populated by the imagecustomizer --output-pxe-artifacts-dir"
    echo
    echo "  -p <iso-url-place-holder>: place-holder string in grub.cfg to be replaced with the http server ip and root path at deployment time."
    echo "                             This string can be specified in the Image Customizer configuration under pxe | isoImageUrl"
    echo "                             For example:"
    echo
    echo "                             -p iso-publish-path"
    echo
    echo "                             where the Image Customizer config file has:"
    echo
    echo "                             pxe:"
    echo "                               isoImageUrl: http://iso-publish-path/my-os.iso"
    echo
    echo "  -r <iso-url>             : string holding the http server ip and root path to replace the place holder string specified by <iso-url-place-holder>."
    echo "                             For example:"
    echo
    echo "                             -r 192.168.0.1/azl-os"
    echo
}

# -s -> input iso or input directory containing the PXE artifacts.
while getopts ":s:p:r:" OPTIONS; do
  case "${OPTIONS}" in
    s ) sourcePath=$OPTARG ;;
    p ) httpRootPlaceHolder=$OPTARG ;;
    r ) httpRoot=$OPTARG ;;

    \? )
        echo "Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

if [[ -z "$sourcePath" ]]; then
    echo "error: missing required parameter 'source-path'."
    show_usage
    exit 1
fi

if [[ -z "$httpRootPlaceHolder" && -n "$httpRoot" ]]; then
    echo "error: 'iso-url-place-holder' must be specified if 'iso-url' is specified."
    show_usage
    exit 1
fi

if [[ -n "$httpRootPlaceHolder" && -z "$httpRoot" ]]; then
    echo "error: 'iso-url' must be specified if 'iso-url-place-holder' is specified."
    show_usage
    exit 1
fi

# ---- helper functions ----

function mount_iso() {
    local isoPath=$1
    local mountDir=$2
    rm -rf $mountDir
    mkdir -p $mountDir
    mount $isoPath $mountDir
}

function unmount_iso() {
    local mountDir=$1    
    umount $mountDir
    rm -r $mountDir
}

function clean_tftp_folder() {
    rm -rf $tftpLocalDir/boot
    rm -rf $tftpLocalDir/liveos
    rm -f  $tftpLocalDir/bootx64.efi
    rm -f  $tftpLocalDir/grubx64.efi
}

function clean_http_folder() {
    rm -rf $httpLocalDir/liveos
}

function copy_file () {
    local source_file=$1
    local target_file=$2
    cp $source_file $target_file
    chmod 755 $target_file
    chown root:root $target_file
}

function deploy_tftp_folder() {
    local artifactsRootDir=$1
    local tftpLocalDir=$2

    copy_file $artifactsRootDir/efi/boot/grubx64.efi $tftpLocalDir/grubx64.efi
    copy_file $artifactsRootDir/efi/boot/bootx64.efi $tftpLocalDir/bootx64.efi

    mkdir -p $tftpLocalDir/boot
    copy_file $artifactsRootDir/boot/vmlinuz $tftpLocalDir/boot/vmlinuz
    copy_file $artifactsRootDir/boot/initrd.img $tftpLocalDir/boot/initrd.img

    mkdir -p $tftpLocalDir/boot/grub2
    if [[ -f $artifactsRootDir/boot/grub2/grub-pxe.cfg ]]; then
        copy_file $artifactsRootDir/boot/grub2/grub-pxe.cfg $tftpLocalDir/boot/grub2/grub.cfg
    else
        copy_file $artifactsRootDir/boot/grub2/grub.cfg $tftpLocalDir/boot/grub2/grub.cfg
    fi
    copy_file $artifactsRootDir/boot/grub2/grubenv $tftpLocalDir/boot/grub2/grubenv    

    # If grub.cfg has been generated with a placeholder, make sure you update it
    # now with the real URL.
    set -x
    sed -i "s|$httpRootPlaceHolder|$httpRoot|g" $tftpLocalDir/boot/grub2/grub.cfg
    set +x
}

function deploy_http_folder() {
    local sourceIsoPath=$1
    local httpLocalDir=$2

    mkdir -p $httpLocalDir/liveos
    chmod 755 $httpLocalDir/liveos
    copy_file $sourceIsoPath $httpLocalDir/$(basename $sourceIsoPath)
}

function deploy() {
    local artifactsRootDir=$1
    local sourceIsoPath=$2

    deploy_http_folder $sourceIsoPath $httpLocalDir
    deploy_tftp_folder $artifactsRootDir $tftpLocalDir
    systemctl restart httpd
}

function clean() {
    clean_tftp_folder
    clean_http_folder
}

function list_deployed_files() {
    find $tftpLocalDir -type f
    find $httpLocalDir -type f
}

# ---- main ----

clean

# if sourcePath is a file, we assume it's the path to the iso image.
if [[ -f "$sourcePath" ]]; then
    isoMountDir=/mnt/$(basename $sourcePath)
    sourceIsoPath=$sourcePath

    mount_iso $sourceIsoPath $isoMountDir
    deploy $isoMountDir $sourceIsoPath
    unmount_iso $isoMountDir

elif [[ -d "$sourcePath" ]]; then

    sourceIsoPath=$(find "$sourcePath" -name "*.iso")
    deploy $sourcePath $sourceIsoPath
fi

list_deployed_files
