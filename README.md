# image_filtering

This script is used to browse images and copy selected images from `source_img_dir` to `selected_img_dir`.

# Setup

Clone this repo

```
git clone https://github.com/vovaxnz/image_filtering.git
```

Install dependencies

```
pip install opencv-contrib-python numpy
```

# Usage

## 1. Specify paths to your directories in the `filter.sh` file

```
SOURCE_IMG_DIR=
SELECTED_IMG_DIR=
```

## 2. Save `filter.sh` and run script with command

```
sh filter.sh
```

# Controls:

```
w - forward with short delay
s - forward with normal delay
x - forward with long delay
a - backward short delay
c - select image
p - close window
```

# Download/Upload data

For downloading and uploading data use `download.sh` and `upload.sh` scripts.

Set your values to this variables in `download.sh` and `upload.sh` files. For example:
```
ADDRES=username@123.23.23.23
REMOTE_DIR=/path/to/dir/on/server
LOCAL_DIR=/path/to/your/dir
```

And run script with command:
```
sh download.sh
```

or 
```
sh upload.sh
```