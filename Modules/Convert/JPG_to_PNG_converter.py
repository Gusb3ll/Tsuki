# import sys
import os
from PIL import Image

input_path = './input' # sys.argv[1]
output_path = './output' # sys.argv[2]

# if the output folder does not exist - it creates it
try:
    os.mkdir(os.getcwd() + '\\' + output_path)
    print(f'The output folder - {output_path}, has been created! \n')
except FileExistsError:
    print(
        f'The folder {output_path} already exists! All the PNG files will be saved in it! \n')

# loops through the InputJPG
for filename in os.listdir(input_path):
    current_img = Image.open(input_path + '\\' + filename)
    print('Working on image: ' + os.path.splitext(filename)[0])
    print(
        f'Format: {current_img.format}, Size: {current_img.size}, Mode: {current_img.mode}')

    # coverts the images to PNG + saves to the output folder
    current_img.save('.\\' + output_path + '\\' +
        os.path.splitext(filename)[0] + '.png', 'PNG')
