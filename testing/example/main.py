import PIL
import math
from PIL import Image

#-----------------------------------------------
#  
#  max width is 53; height dont matter
#  max char count 2k(def) or 4k
#  
#  import
#  check width
#  turn pixels into a list of vec4
#  for each item compare it with all emojis and find closest matching
#  append it to stdout
#  write
#  
#  
#  
#  
#  
#  
#  
#-----------------------------------------------

#--- import

Inimg = input("What image should i use? ")


print(Inimg)

img=Image.open(Inimg)

#--- width

imgw, imgh = img.size


if (53 == imgw):
    exit()

#--- list

imgL=list(img.getdata())


#--- compare





def hex_to_rgb(hex_color):
    """
    Converts a hex color string (e.g., "#RRGGBB" or "RRGGBB") to an RGB tuple.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))




def find_closest_rgb(file_path, curr_rgb_tuple):
    """
    Finds the closest RGB color from a text file to a given RGB tuple.

    Args:
        file_path (str): The path to the text file containing color names and RGB values.
                         Each line should be in the format "Name|R,G,B".
        curr_rgb_tuple (tuple): A tuple representing the RGB value (R, G, B)
                                 to find the closest color to.

    Returns:
        tuple: A tuple containing the name and the RGB tuple of the closest color.
               Returns None if the file is empty or no valid RGB values are found.
    """
    min_distance = float('inf')
    closest_color_name = None
    closest_color_rgb = None

    with open(file_path, 'r') as Inem:
        for line in Inem:
            line = line.strip()  # Remove leading/trailing whitespace
            if not line:  # Skip empty lines
                continue

            parts = line.split('|')
            if len(parts) != 2:
                print(f"Warning: Skipping malformed line: {line}")
                continue

            name = parts[0].strip()
            rgb_str = hex_to_rgb(parts[1].strip())



            try:
                # Convert RGB string "R,G,B" to a tuple of integers
                r, g, b = map(int, rgb_str.split(','))
                file_rgb_tuple = (r, g, b)
            except ValueError:
                print(f"Warning: Skipping line with invalid RGB values: {line}")
                continue

            # Calculate Euclidean distance between the two RGB colors
            # Distance = sqrt((R1-R2)^2 + (G1-G2)^2 + (B1-B2)^2)
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

# --- Example Usage ---

# 1. Create a dummy file for demonstration
file_content = """
Red|255,0,0
Green|0,255,0
Blue|0,0,255
Yellow|255,255,0
Cyan|0,255,255
Magenta|255,0,255
Black|0,0,0
White|255,255,255
Light Gray|200,200,200
Dark Blue|0,0,100
Orange|255,165,0
"""

with open("colors.txt", "w") as f:
    f.write(file_content.strip())

# 2. Define your 'curr' pixel value (as an RGB tuple)
curr = (10, 10, 150)  # Example: A dark blueish color

# 3. Call the function
closest_name, closest_rgb = find_closest_rgb("colors.txt", curr)

if closest_name:
    print(f"The 'curr' color {curr} is closest to:")
    print(f"  Name: {closest_name}")
    print(f"  RGB: {closest_rgb}")
else:
    print("No valid colors found in the file or an error occurred.")

# Another example: A greenish color
curr_2 = (50, 200, 70)
closest_name_2, closest_rgb_2 = find_closest_rgb("colors.txt", curr_2)
if closest_name_2:
    print(f"\nThe 'curr' color {curr_2} is closest to:")
    print(f"  Name: {closest_name_2}")
    print(f"  RGB: {closest_rgb_2}")
