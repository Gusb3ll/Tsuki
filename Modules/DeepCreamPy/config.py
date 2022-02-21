import argparse

def str2floatarr(v):
    if type(v) == str:
        try:
            return [float(v) for v in v.split(',')]
        except:
            raise argparse.ArgumentTypeError('Integers seperated by commas expected.')
    else:
        raise argparse.ArgumentTypeError('Integers seperated by commas expected.')

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1', True):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', False):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_args():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--decensor_input_path', dest='decensor_input_path', default='./decensor_input/', help='Input images with censored regions colored green to be decensored by decensor.py path')
	parser.add_argument('--decensor_output_path', dest='decensor_output_path', default='./decensor_output/', help='Output images generated from running decensor.py path')
	parser.add_argument('--mask_color_red', dest='mask_color_red', default=0, help='Red channel of mask color in decensoring')
	parser.add_argument('--mask_color_green', dest='mask_color_green', default=255, help='Green channel of mask color in decensoring')
	parser.add_argument('--mask_color_blue', dest='mask_color_blue', default=0, help='Blue channel of mask color in decensoring')
	parser.add_argument('--is_mosaic', dest='is_mosaic', default='False', type=str2bool, help='True if image has mosaic censoring, false otherwise')

	args = parser.parse_args()
	return args

if __name__ == '__main__':
	get_args()
