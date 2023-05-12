# image_filtering

Utility for image filtering

# Setup

## 1. Clone this repo

```
git clone https://github.com/vovaxnz/image_filtering.git
```

## 2. cd to repo
```
cd image_filtering
```

## 3. Install dependencies

```
pip install -r requirements.txt
```

## 4. Specify variables in the `.env` file

Create `.env` file in the root of repository and specify variables in it.

For example:
```
TOKEN=86b0b932
ADDRESS=username@123.12.0.123
DATA_DIR=/path/to/dir
```

`DATA_DIR` should be the path to the directory where the script will download the archives and store the images. There must be enough space in this directory. At least 150 GB. Do not use this folder as `DATA_DIR`.


# Usage

Take `project_id` of your FilteringProject from the https://eg-ml.com/tasks/my_tasks/ page. For example it is `123`

## 1. Download images

```
python3 download.py -n 123
```

## 2. Filter images

```
python3 filtering.py -n 123
```

## 3. Upload images and complete project

```
python3 complete.py -n 123
```

You don`t need to edit any files. Just run commands above with your filtering project id.

After succesfull execution of `complete.py` script, filtering project will disappear from your tasks page on eg-ml.com

# Controls:

```
w - forward with short delay
s - forward with normal delay
x - forward with long delay
a - backward short delay
c - select image
p - close window
```