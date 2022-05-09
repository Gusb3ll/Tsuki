import os
# import file
import numpy as np
from PIL import Image

# from utils import *
# from model import InpaintNN

class Decensor:
  def __init__(self):
    self.mask_color = [0, 255, 0]
    self.input_path = os.path.join(os.getcwd(),'src/data/input/')
    self.output_path = os.path.join(os.getcwd(),'src/data/output/')
  
  def get_mask(self, colored):
    mask = np.ones(colored.shape, dtype=np.uint8)
    i, j = np.where(np.all(colored[0] == self.mask_color, axis=-1))
    mask[0, i, j] = 0
    return mask

  def decensorImg(self):
    input_path = self.input_path
    output_path = self.output_path
    files = os.listdir(input_path)
    print(files)

if __name__ == '__main__':
  decensor = Decensor()
  decensor.decensorImg()
