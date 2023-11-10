# ail-feeder-image
This AIL feeder is a generic piece of software to extract information from image files and feed AIL via its REST API.

## Requirements
- [PyExifTool==0.4.13](https://github.com/smarnach/pyexiftool)
- [pyail](https://github.com/ail-project/PyAIL)

## Usage
~~~bash
dacru@dacru:~/git/ail-feeder-image/bin$ python3 feeder-image.py --help  
usage: feeder-image.py [-h] [-i IMAGE [IMAGE ...]] [-fi FOLDER_IMAGE] [-d] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE [IMAGE ...], --image IMAGE [IMAGE ...]
                        list of images to analyse
  -fi FOLDER_IMAGE, --folder_image FOLDER_IMAGE
                        folder containing images
  -d, --debug           debug mode
  -v, --verbose         display more info
~~~

## JSON output format to AIL
- `source` is the name of the AIL feeder module
- `source-uuid` is the UUID of the feeder (unique per feeder)
- `data` is text found in pdf
- `meta` is the generic field where feeder can add the metadata collected

Using the AIL API, `data` will be compress in gzip format and encode with base64 procedure. Then a new field will created, `data-sha256` who will be the result of sha256 on data after treatment.

## Output
~~~json
{'data': bytes,
 'meta': {'image_feeder:ExifTool:ExifToolVersion': 12.43,
          'image_feeder:File:MIMEType': 'image/jpeg',
          ..., // Exif metadata
		}
}
~~~

## License
This software is licensed under [GNU Affero General Public License version 3](http://www.gnu.org/licenses/agpl-3.0.html)
Copyright (C) 2022-2023 CIRCL - Computer Incident Response Center Luxembourg
Copyright (C) 2022-2023 David Cruciani
