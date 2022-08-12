import os
import exiftool
import argparse
import configparser
from pyail import PyAIL
import hashlib

dir_path = os.path.dirname(os.path.realpath(__file__))
uuid = "1552b4bb-067b-403a-8a2f-e4c8b36b5c6e"

## Config
pathConf = '../etc/ail-feeder-image.cfg'

if os.path.isfile(pathConf):
    config = configparser.ConfigParser()
    config.read(pathConf)
else:
    print("[-] No conf file found")
    exit(-1)

if 'general' in config:
    uuid = config['general']['uuid']

if 'ail' in config:
    ail_url = config['ail']['url']
    ail_key = config['ail']['apikey']


def pushToAIl(data, meta):
    """Push json to AIL"""
    default_encoding = 'UTF-8'

    json_pdf = dict()
    json_pdf['data'] = data
    json_pdf['meta'] = meta

    source = 'image-feeder'
    source_uuid = uuid

    if debug:
        print(json_pdf)
    else:
        pyail.feed_json_item(data, meta, source, source_uuid, default_encoding)


def extractMeta(image):
    """Extract metadata from a given image"""

    if verbose:
        print(f"\n{image}")

    ####################
    # Extract Metadata #
    ####################

    meta = dict()

    if verbose:
        print("[+] Extract Metadata")

    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image)

    # Openstreetmap url generation
    if "EXIF:GPSLatitude" in metadata.keys():
        lat = metadata["EXIF:GPSLatitude"]
        lon = metadata["EXIF:GPSLongitude"]
        meta[f"image_feeder:openstreetmap"] = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=12"
    
    for key in metadata.keys():
        meta[f"image_feeder:{key}"] = metadata[key]

    with open(image, 'rb') as read_image:
        i = read_image.read()
        b = bytearray(i)
    
    data = b

    pushToAIl(data, meta)


def recursiveFolder(folder):
    """Recursive folder exploration"""
    for file in os.listdir(folder):
        image = os.path.join(folder, file)
        if os.path.isdir(image):
            recursiveFolder(image)
        else:
            extractMeta(image)


#############
# Arg Parse #
#############

parser = argparse.ArgumentParser()
parser.add_argument('-i', "--image", nargs='+', help="list of images to analyse")
parser.add_argument('-fi', "--folder_image", help="folder containing images")
parser.add_argument("-d", "--debug", help="debug mode", action="store_true")
parser.add_argument("-v", "--verbose", help="display more info", action="store_true")
args = parser.parse_args()

debug = args.debug
verbose = args.verbose

if not args.image and not args.folder_image:
    print("[-] Error passing image")
    exit(0)
elif args.image:
    flag = True
elif args.folder_image:
    flag = False

## Ail
if not debug:
    try:
        pyail = PyAIL(ail_url, ail_key, ssl=False)
    except Exception as e:
        print("\n\n[-] Error during creation of AIL instance")
        exit(0)


if flag:
    for image in args.image:
        extractMeta(image)
else:
    if not os.path.isdir():
        print("[-]Error, try to open other than a directory")
        exit(0)
    else:
        recursiveFolder(args.folder_image)
