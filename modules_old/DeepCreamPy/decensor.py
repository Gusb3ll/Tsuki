import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import file
import config
import numpy as np
from PIL import Image
from libs.utils import *
from cmyui import log, Ansi
from model import InpaintNN

log('----- DeepCreamPy modified by Gusbell -----', Ansi.CYAN)

class Decensor:
    def __init__(self):
        self.args = config.get_args()
        self.is_mosaic = self.args.is_mosaic
        self.mask_color = [self.args.mask_color_red/255.0,
        self.args.mask_color_green/255.0, self.args.mask_color_blue/255.0]
        if not os.path.exists(self.args.decensor_output_path):
            os.makedirs(self.args.decensor_output_path)
        self.load_model()

    def get_mask(self, colored):
        mask = np.ones(colored.shape, np.uint8)
        i, j = np.where(np.all(colored[0] == self.mask_color, axis=-1))
        mask[0, i, j] = 0
        return mask

    def load_model(self):
        self.model = InpaintNN(bar_model_name="./models/bar/Train_775000.meta", bar_checkpoint_name="./models/bar/", mosaic_model_name="./models/mosaic/Train_290000.meta", mosaic_checkpoint_name="./models/mosaic/", is_mosaic=self.is_mosaic)

    def decensor_all_images_in_folder(self):
        color_dir = self.args.decensor_input_path
        file_names = os.listdir(color_dir)

        input_dir = self.args.decensor_input_path
        output_dir = self.args.decensor_output_path

        file_names, self.files_removed = file.check_file(input_dir, output_dir, False)
        for file_name in file_names:
            color_file_path = os.path.join(color_dir, file_name)
            color_bn, color_ext = os.path.splitext(file_name)
            if os.path.isfile(color_file_path) and color_ext.casefold() == ".png":
                log("--------------------------------------------------------------------------", Ansi.GRAY)
                log("Decensoring the image {}".format(color_file_path), Ansi.CYAN)
                try:
                    colored_img = Image.open(color_file_path)
                except:
                    log("Cannot identify image file (" + str(color_file_path)+")", Ansi.RED)
                    self.files_removed.append((color_file_path, 3))
                    continue
                if self.is_mosaic:
                    ori_dir = self.args.decensor_input_original_path
                    valid_formats = {".png", ".jpg", ".jpeg"}
                    for test_file_name in os.listdir(ori_dir):
                        test_bn, test_ext = os.path.splitext(test_file_name)
                        if (test_bn == color_bn) and (test_ext.casefold() in valid_formats):
                            ori_file_path = os.path.join(ori_dir, test_file_name)
                            ori_img = Image.open(ori_file_path)
                            self.decensor_image(ori_img, colored_img, file_name)
                            break
                    else:
                        log("Corresponding original, uncolored image not found in {}".format(color_file_path), Ansi.RED)
                        log("Check if it exists and is in the PNG or JPG format", Ansi.RED)
                else:
                    self.decensor_image(colored_img, colored_img, file_name)
            else:
                log("--------------------------------------------------------------------------", Ansi.GRAY)
                log("Irregular file detected : "+ str(color_file_path), Ansi.RED)
        log("--------------------------------------------------------------------------", Ansi.GRAY)
        if(self.files_removed is not None):
            file.error_messages(None, self.files_removed)
        log("Decensoring complete!", Ansi.GREEN)

    def decensor_image(self, ori, colored, file_name=None):
        width, height = ori.size
        has_alpha = False
        if (ori.mode == "RGBA"):
            has_alpha = True
            alpha_channel = np.asarray(ori)[:, :, 3]
            alpha_channel = np.expand_dims(alpha_channel, axis=-1)
            ori = ori.convert('RGB')
        ori_array = image_to_array(ori)
        ori_array = np.expand_dims(ori_array, axis=0)
        if self.is_mosaic:
            colored = colored.convert('RGB')
            color_array = image_to_array(colored)
            color_array = np.expand_dims(color_array, axis=0)
            mask = self.get_mask(color_array)
            mask_reshaped = mask[0, :, :, :] * 255.0
            mask_img = Image.fromarray(mask_reshaped.astype('uint8'))
        else:
            mask = self.get_mask(ori_array)
        regions = find_regions(colored.convert('RGB'), [v*255 for v in self.mask_color])
        log("Found {region_count} green regions in this image".format(region_count=len(regions)), Ansi.CYAN)

        if len(regions) == 0 and not self.is_mosaic:
            log("No green regions detected", Ansi.RED)
            return
        output_img_array = ori_array[0].copy()

        for region_counter, region in enumerate(regions, 1):
            bounding_box = expand_bounding(ori, region, expand_factor=1.5)
            crop_img = ori.crop(bounding_box)
            mask_reshaped = mask[0, :, :, :] * 255.0
            mask_img = Image.fromarray(mask_reshaped.astype('uint8'))
            crop_img = crop_img.resize((256, 256))
            crop_img_array = image_to_array(crop_img)
            mask_img = mask_img.crop(bounding_box)
            mask_img = mask_img.resize((256, 256))
            mask_array = image_to_array(mask_img)

            if not self.is_mosaic:
                a, b = np.where(np.all(mask_array == 0, axis=-1))
                crop_img_array[a, b, :] = 0.
            temp = Image.fromarray((crop_img_array * 255.0).astype('uint8'))
            crop_img_array = np.expand_dims(crop_img_array, axis=0)
            mask_array = np.expand_dims(mask_array, axis=0)
            crop_img_array = crop_img_array * 2.0 - 1
            pred_img_array = self.model.predict(crop_img_array, crop_img_array, mask_array)
            pred_img_array = np.squeeze(pred_img_array, axis=0)
            pred_img_array = (255.0 * ((pred_img_array + 1.0) / 2.0)).astype(np.uint8)
            bounding_width = bounding_box[2]-bounding_box[0]
            bounding_height = bounding_box[3]-bounding_box[1]
            pred_img = Image.fromarray(pred_img_array.astype('uint8'))
            pred_img = pred_img.resize((bounding_width, bounding_height), resample=Image.BICUBIC)
            pred_img_array = image_to_array(pred_img)
            pred_img_array = np.expand_dims(pred_img_array, axis=0)

            for i in range(len(ori_array)):
                for col in range(bounding_width):
                    for row in range(bounding_height):
                        bounding_width_index = col + bounding_box[0]
                        bounding_height_index = row + bounding_box[1]
                        if (bounding_width_index, bounding_height_index) in region:
                            output_img_array[bounding_height_index][bounding_width_index] = pred_img_array[i, :, :, :][row][col]
            log("{region_counter} out of {region_count} regions decensored.".format(region_counter=region_counter, region_count=len(regions)), Ansi.GRAY)

        output_img_array = output_img_array * 255.0

        if has_alpha:
            output_img_array = np.concatenate((output_img_array, alpha_channel), axis=2)
        output_img = Image.fromarray(output_img_array.astype('uint8'))

        if file_name != None:
            save_path = os.path.join(self.args.decensor_output_path, file_name)
            output_img.save(save_path)
            log("Decensored image saved to {save_path}!".format(save_path=save_path), Ansi.GREEN)
            return
        else:
            log("Decensored image", Ansi.GREEN)
            return output_img

if __name__ == '__main__':
    decensor = Decensor()
    decensor.decensor_all_images_in_folder()
