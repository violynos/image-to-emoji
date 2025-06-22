import math
from PIL import Image
import argparse

#------------- Parser

parser = argparse.ArgumentParser(
    description="Process an image file."
)

parser.add_argument(
    "image_file",
    type=str,
    help="The path to the image file (e.g., image.png)"
)

args = parser.parse_args()

Inimg = args.image_file

#------------- Get img

img = Image.open(Inimg)

imgw, imgh = img.size

if imgw >53:
    print("EE: Image too wide")
    exit()

imgL = list(img.getdata())

#------------- Funcs

def hex_to_rgb(hex_color):
    
    if len(hex_color) != 6:
        print("EE: Hex color must be 6 characters long (e.g., 'RRGGBB').")
        hex_color=000000 
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r},{g},{b}"
    except ValueError:
        raise ValueError("Invalid hexadecimal color value. Please provide a valid hex string.")

def find_closest_rgb(file_path, curr_rgb_tuple):
    min_distance = float('inf')
    closest_color_name = None
    closest_color_rgb = None

    with open(file_path) as Inem:
        for line in Inem:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" | ")
            if len(parts) != 2:
                print(f"Warning: Skipping malformed line: {line}")
                continue

            name = parts[0].strip()
            rgb_str = hex_to_rgb(parts[1].strip())

            try:
                r, g, b = map(int, rgb_str.split(','))
                file_rgb_tuple = (r, g, b)
            except ValueError:
                print(f"Warning: Skipping line with invalid RGB values: {line}")
                continue

            distance = (
                (curr_rgb_tuple[0] - file_rgb_tuple[0])**2 +
                (curr_rgb_tuple[1] - file_rgb_tuple[1])**2 +
                (curr_rgb_tuple[2] - file_rgb_tuple[2])**2
            )**0.5

            if distance < min_distance:
                min_distance = distance
                closest_color_name = name
                closest_color_rgb = file_rgb_tuple

    return closest_color_name, closest_color_rgb

#------------- Get emoji for each pixel

ret=[]

iii = 0
for curr in imgL:
    if iii%imgw == 0:
        ret.append("\n")
    closest_name, closest_rgb = find_closest_rgb("emoji.txt", curr)
    ret.append(closest_name)
    iii+=1

#------------- Print in chat

print("".join(ret))
