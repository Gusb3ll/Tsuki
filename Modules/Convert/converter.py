# import sys
import os
from PIL import Image
from cmyui import log, Ansi

input_path = './input'
output_path = './output'

try:
    os.mkdir(os.getcwd() + '\\' + output_path)
    log(f'The output folder - {output_path}, has been created!', Ansi.GREEN)
except FileExistsError:
    log(f'The folder {output_path} already exists! All the PNG files will be saved in it!', Ansi.GREEN)

for filename in os.listdir(input_path):
    current_img = Image.open(input_path + '\\' + filename)
    log("--------------------------------------------------------------------------", Ansi.GRAY)
    log('Working on image: ' + os.path.splitext(filename)[0], Ansi.CYAN)
    log(f'Format: {current_img.format}, Size: {current_img.size}, Mode: {current_img.mode}', Ansi.WHITE)
    current_img.save('.\\' + output_path + '\\' +
        os.path.splitext(filename)[0] + '.png', 'PNG')
