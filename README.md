# image_filtering

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

Specify paths to your directories and other parameters at the bottom of the `image_filtering.py` file

```
if __name__ == "__main__":
    main(
        source_img_dir = '/media/vova/data/viz/preprocessed',
        selected_img_dir = '/media/vova/data/viz/preprocessed_selected',

        window_height = 1280,
        window_width = 720,
        
        short_delay_ms = 5,
        normal_delay_ms = 40,
        long_delay_ms = 100,
    )
```

Save file and run script with command

```
python image_filtering.py
```

Controls:

```
w - forward with short delay
s - forward with normal delay
x - forward with long delay
a - backward short delay
c - select image
p - close window
```

