import glob
from pathlib import Path
from PIL import Image

OUTPUT_DIR = 'screenshots_cropped/'

def extract_bridge_from_screenshot(screenshot_filename: str, output_filename: str):
    """
    Crops a screenshot of Link next to the bridge so only the bridge is in focus.
    
    This helps the image group analysis script be more accurate.
    """
    image = Image.open(screenshot_filename)

    # width, height = image.size
    width, height = 256, 384

    left = 0
    top = 128 # height/2
    right = (width * 0.6) - 25 #(3/5)
    bottom = height
    image_cropped = image.crop((left, top, right, bottom))
    image_cropped.save(output_filename, quality=1)

filelist = glob.glob('../screenshots_ram/*.png')
filelist.sort()
Path.mkdir(Path(OUTPUT_DIR), parents=True, exist_ok=True)

for i, imagepath in enumerate(filelist):
    print(f'    Status: {i} / {len(filelist)}', end='\r')
    extract_bridge_from_screenshot(imagepath, f'screenshots_cropped/{Path(imagepath).name}')
