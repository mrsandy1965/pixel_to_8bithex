#!/usr/bin/env python3

import os
from PIL import Image

# Path to images folder.
image_path = "images"

def color_to_bit_string(c, nbits):
    """Convert color value to a bit string of specified length."""
    newc = bin(int(round(c / (256 // 2 ** nbits))))
    return newc[2:].zfill(nbits)

def images_folder_exists():
    """Check if the images folder exists."""
    return os.path.exists(image_path)

def is_valid_image(file_name):
    """Check if the file is a valid image."""
    try:
        with Image.open(os.path.join(image_path, file_name)) as img:
            return img
    except IOError:
        print(f"{file_name} is not a valid image.")
        return None

def process_image(img, file_name, openfile):
    """Process the image and write the converted data to the output file."""
    pix = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            if img.mode == "RGBA":
                r, g, b, a = pix[x, y]
            else:
                r, g, b = pix[x, y]
                a = 255  # Assume fully opaque if not RGBA

            r_bits = color_to_bit_string(r, 3)
            g_bits = color_to_bit_string(g, 3)
            b_bits = color_to_bit_string(b, 2)
            num = int(r_bits + g_bits + b_bits, 2)

            if img.mode == "RGBA" and a == 0:  # If pixel is transparent
                openfile.write('x"TR",')
            else:
                openfile.write(f'x"{num:02x}",')

        if y == 7:  # Add file name as comment on row 7
            openfile.write(f"    -- {file_name}")
        openfile.write("\n")
    openfile.write("\n")  # Empty line after image has been converted
    print(f"Successfully wrote {file_name} to output.")

def main():
    """Main function to convert images."""
    total_images = 0

    with open('output.txt', 'w') as openfile:
        for file_name in sorted(os.listdir(image_path)):
            img = is_valid_image(file_name)
            if img:
                process_image(img, file_name.split(".")[0], openfile)
                total_images += 1

    if total_images == 0:
        print("No images in folder. 0 Images converted.")
    else:
        print(f"Finished converting {total_images} images.")

if __name__ == "__main__":
    if images_folder_exists():
        main()
    else:
        os.makedirs(image_path)
        print('\033[91m' + "Image folder does not exist. An empty folder, 'images', has been created. Please add your images and rerun the script.")
