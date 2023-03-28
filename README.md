# image_filtering

# Setup

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

