import os
from PIL import Image



class Converter:

  def __init__(self):
    self.input_path = os.path.join(os.getcwd(),'src/data/input/')

  def toPng(self):
    for filename in os.listdir(self.input_path):
      if filename.endswith(".jpg"):
          img = Image.open(self.input_path + filename)
          img.save(self.input_path + filename.strip('.jpg') + '.png')
          os.remove(self.input_path + filename)