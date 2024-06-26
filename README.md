![Tsuki](https://user-images.githubusercontent.com/77166960/154808873-1bdd3aab-1aa4-4fcd-a3e6-17dfcde3b720.png)


### Manga/picture uncensoring script based on
- [DeepCreamPy](https://github.com/liaoxiong3x/DeepCreamPy)
- [Hent-AI](https://github.com/natethegreate/hent-AI)
- [Screentone-Remover](https://github.com/natethegreate/Screentone-Remover) (For black & white manga/picture)

![Demo](https://cdn.discordapp.com/attachments/858334807561863221/944618448540033064/test-output.png)

### Right now the program only works with bar censoring, mosaic and video uncensoring will be implemented later

# Google colab version

### If you want to use the google colab version, make a copy of [this](https://github.com/Gusb3ll/Tsuki/blob/main/Tsuki_colab.ipynb) in your own google drive and download the models from the section below

# Installiation

### System requirements

- CUDA Compatible GPU
- [CUDA](https://developer.nvidia.com/cuda-downloads) (latest version) (current working one is 11.5)
- [CUDNN](https://developer.nvidia.com/rdp/cudnn-download) (latest version compatible with CUDA) (current working one is 8.3.2)
- Python 3.9.7

#### Notes

- If you have others CUDA version installed, make sure you set the system variable "CUDA_PATH" to your latest CUDA path
- Make sure you install CUDNN with the zip not the exe
- If you doesn't have GPU that can support CUDA you can run the script with CPU capable of running tensorflow as well

## Automatic installation

```bash
.\init.bat
```

## Manual installation (Not recommended)

```bash
cd tsuki
cd modules
virtualenv env --python=3.9.7
pip install -r requirements.txt
```

- Create "input" and "output" folder in Converter folder

- Ceate "decensor_input" and "decensor_output" folder in DeepCreamPy folder

- Create "input" and "output" folder in HentAI folder

- Create "input" and "output" folder in the ToneRemover folder

## Download the models

### DeepCreamPy
  - [Models.zip](https://drive.google.com/open?id=1byrmn6wp0r27lSXcT9MC4j-RQ2R04P1Z)
    - Extract the file then put it in DeepCreamPy/models folder

### HentAI
  - [4x_FatalPixels_340000_G.pth](https://github.com/KutsuyaYuki/hent-ai/blob/master/4x_FatalPixels_340000_G.pth)
  - [Weights.h5](https://www.dropbox.com/s/zvf6vbx3hnm9r31/weights268.zip?dl=0)
    - Put these two files in HentAI folder
  - [RRDB](https://drive.google.com/file/d/1pJ_T-V1dpb1ewoEra1TGSWl5e6H7M4NN/view) 
    - Put this in HentAI/ColabESRGAN/models folder

# Usage (Automatic)

If you ran "init.bat" already, there should be "INPUT" and "OUTPUT" folder at the root of the project

### For black & white manga/picture
Put the images in "INPUT" folder (Both PNG & JPG are acceptable)
```
.\run-blackwhite.bat
```

### For colored manga/picture
Put the images in "INPUT" folder (Both PNG & JPG are acceptable)
```
.\run-color.bat
```

# Usage (Manual)

### Make sure you are using the correct environment when using each modules
1. Activate HentAI environment then put the image in the "png" format into the "input" folder you just created
2. Move the result from "output" folder from HentAI to "decensor_input" in DeepCreamPy folder
3. Run DeepCreamPy and done! you have your uncensored image
