import os
from PIL import Image

TARGET_SIZE_KB = 150
RESIZE_FACTOR = 0.9
WEBP_QUALITY = 85

def resize_image(img_path, output_path, resize_factor):
    with Image.open(img_path) as img:
        width, height = img.size
        img = img.resize((int(width * resize_factor), int(height * resize_factor)))
        img.save(output_path, "WEBP", quality=WEBP_QUALITY)

def convert_to_webp(img_path, output_path):
    with Image.open(img_path) as img:
        img.save(output_path, "WEBP", quality=WEBP_QUALITY)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, filename)
                output_path = os.path.splitext(img_path)[0] + '.webp'

                # Check image orientation
                with Image.open(img_path) as img:
                    width, height = img.size
                    if width > height:  # landscape
                        resize_factor = RESIZE_FACTOR
                        resize_image(img_path, output_path, resize_factor)

                        while os.path.getsize(output_path) > TARGET_SIZE_KB * 1024:
                            resize_factor *= 0.9
                            resize_image(img_path, output_path, resize_factor)
                    else:
                        convert_to_webp(img_path, output_path)

if __name__ == '__main__':
    directory = input("Enter the directory path: ")
    process_directory(directory)
    print("Conversion complete!")