import os
import numpy as np
from PIL import Image

def imgToArray(img):
  array = np.asarray(img)
  return np.array(array / 255.0)

def findRegions(img, mask_color):
  pixel = img.load()
  neighbors = dict()
  width, height = img.size
  for x in range(width):
    for y in range(height):
      if isRightColor(pixel[x, y], *mask_color):
        neighbors[x, y] = {(x, y)}
  for x, y in neighbors:
    candidates = (x + 1, y), (x, y + 1)
    for i in candidates:
        if i in neighbors:
          neighbors[x, y].add(i)
          neighbors[i].add((x, y))
  closedList = set()

  def connectedComponent(pixel):
    region = set()
    openList = { pixel }
    while openList:
      pixel = openList.pop()
      closedList.add(pixel)
      openList |= neighbors[pixel] - closedList
      region.add(pixel)
    return region
  
  regions = []
  for pixel in neighbors:
    if pixel not in closedList:
      regions.append(connectedComponent(pixel))
  regions.sort(key = len, reverse = True)
  return regions

def expandBounding(img, region, expand_factor, minSize = 256):
  x, y = zip(*region)
  minX, minY, maxX, maxY = min(x), min(y), max(x), max(y)
  width, height = img.size
  boundingWidth = maxX - minX
  boundingHeight = maxY - minY
  xCenter = (maxX + minX) // 2
  yCenter = (maxY + minY) // 2
  currentSize = int(max(boundingWidth, boundingHeight) * expand_factor)
  maxSize = min(width, height)
  if currentSize > maxSize:
    currentSize = maxSize
  elif currentSize < minSize:
    currentSize = minSize
  x1 = xCenter - currentSize // 2
  x2 = xCenter + currentSize // 2
  y1 = yCenter - currentSize // 2
  y2 = yCenter + currentSize // 2
  if (y1 < 0 or y2 > (height - 1)) and (x1 < 0 or x2 > (width - 1)):
    if x1 < 0 and y1 < 0:
      x1 = 0
      y1 = 0
      x2 = currentSize
      y2 = currentSize
    elif x2 > (width - 1) and y1 < 0:
      x1 = width - currentSize - 1
      y1 = 0
      x2 = width - 1
      y2 = currentSize
    elif x1 < 0 and y2 > (height - 1):
      x1 = 0
      y1 = height - currentSize - 1
      x2 = currentSize
      y2 = height -1
    elif x2 > (width - 1) and y2 > (height - 1):
      x1 = width - currentSize - 1
      y1 = height - currentSize - 1
      x2 = width - 1
      y2 = height - 1
  else:
    if x1 < 0:
      diff = x1
      x1 -= diff
      x2 -= diff
    if x2 > (width - 1):
      diff = x2 - width + 1
      x1 -= diff
      x2 -= diff
    if y1 < 0:
      diff = y1
      y1 -= diff
      y2 -= diff
    if y2 > (height - 1):
      diff = y2 - height + 1
      y1 -= diff
      y2 -= diff
  return x1, y1, x2, y2

def isRightColor(pixel, r2, g2, b2):
    r1, g1, b1 = pixel
    return r1 == r2 and g1 == g2 and b1 == b2

class Decensor:
  def __init__(self):
    self.is_mosaic = False
    self.mask_color = [0/255.0, 255/255.0, 0/255.0]
    self.input_path = os.path.join(os.getcwd(),'src/data/input/')
    self.output_path = os.path.join(os.getcwd(),'src/data/output/')
  
  def getMask(self, img):
    mask = np.ones(img.shape, np.uint8)
    i, j = np.where(np.all(img[0] == self.mask_color, axis=-1))
    mask[0, i, j] = 0
    return mask

  def decensorImg(self, orignalImage, img, filename):
    alpha = False
    if (orignalImage.mode == 'RGBA'):
      alpha = True
      alpha_channel = np.expand_dims(np.asarray(orignalImage)[:, :, 3], axis=-1)
      orignalImage = orignalImage.convert('RGB')
    orignalImageArray = np.expand_dims(imgToArray(orignalImage), axis=0)
    
    if self.is_mosaic:
      orignalImage = orignalImage.convert('RGB')
      orignalImageArray = np.expand_dims(imgToArray(orignalImage), axis=0)
      mask = self.getMask(orignalImageArray)
      maskReshaped = mask[0, :, :, :] * 255.0
      maskImage = Image.fromarray(maskReshaped.astype(np.uint8))
    else:
      mask = self.getMask(orignalImageArray)

    regions = findRegions(img.convert('RGB'), [i * 255 for i in self.mask_color])
    print(f'Found {len(regions)} green regions in this image')

    if len(regions) == 0 and not self.is_mosaic:
      print('No green regions detected')

    outputImageArray = orignalImageArray[0].copy()

    for regionCounter, region in enumerate(regions, 1):
      boundingBox = expandBounding(orignalImage, region, expand_factor=1.5)
      cropImage = orignalImage.crop(boundingBox)
      maskReshaped = mask[0, :, :, :] * 255.0
      maskImage = Image.fromarray(maskReshaped.astype(np.uint8))
      cropImage = cropImage.resize((256, 256))
      cropImageArray = imgToArray(cropImage)
      maskImage = maskImage.crop(boundingBox)
      maskImage = maskImage.resize((256, 256))
      maskArray = imgToArray(maskImage)

      if not self.is_mosaic:
        a, b = np.where(np.all(maskArray == 0, axis=-1))
        cropImageArray[a, b, :] = 0.
      cropImageArray = np.expand_dims(cropImageArray, axis=0)
      maskArray = np.expand_dims(maskArray, axis=0)
      cropImageArray = cropImageArray * 2.0 - 1.0
      predictionImageArray = [] #! WORK ON THIS
      predictionImageArray = np.squeeze(predictionImageArray, axis=0)
      predictionImageArray = (255.0 * ((predictionImageArray + 1.0) / 2.0)).astype(np.uint8)
      boundingWidth = boundingBox[2] - boundingBox[0]
      boundingHeight = boundingBox[3] - boundingBox[1]
      predictedImage = Image.fromarray(predictionImageArray.astype(np.unit8))
      predictedImage = predictedImage.resize((boundingWidth, boundingHeight), resample=Image.BICUBIC)
      predictedImageArray = np.expand_dims(imgToArray(predictedImage), axis=0)

      for i in range(len(orignalImageArray)):
        for col in range(boundingWidth):
          for row in range(boundingHeight):
            boundingWidthIndex = col + boundingBox[0]
            boundingHeightIndex = row + boundingBox[1]
            if (boundingWidthIndex, boundingHeightIndex) in region:
              outputImageArray[boundingHeightIndex][boundingWidthIndex] = predictedImageArray[i, :, :, :][row][col]
      print(f'{regionCounter} out of {len(regions)} regions decensored')

    outputImageArray = outputImageArray * 255.0

    if alpha:
      outputImageArray = np.concatenate((outputImageArray, alpha_channel), axis=2)
    outputImage = Image.fromarray(outputImageArray.astype(np.uint8))

    if filename:
      savePath = os.path.join(self.output_path, filename)
      outputImage.save(savePath)
      return print(f'Decensored image saved to {savePath}')

  def decensorImgFolder(self):
    input_path = self.input_path
    output_path = self.output_path
    
    for filename in os.listdir(input_path):
      if filename.endswith('.png'):
        try:
          img = Image.open(input_path + filename)
          print(f'Decensoring {filename} -', end=' ')
          self.decensorImg(img, img, filename)
        except:
          print('Error opening file: ' + filename)
        print('All image has been decensored')

if __name__ == '__main__':
  decensor = Decensor()
  decensor.decensorImgFolder()
