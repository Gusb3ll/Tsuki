![Tsuki](https://user-images.githubusercontent.com/77166960/154808873-1bdd3aab-1aa4-4fcd-a3e6-17dfcde3b720.png)


### Manga uncensoring script based on
- [DeepCreamPy](https://github.com/liaoxiong3x/DeepCreamPy)
- [HentAI](https://github.com/natethegreate/hent-AI)
- [ToneRemover](https://github.com/natethegreate/Screentone-Remover) (For non-colored manga)

# Installiation

### System requirements

- CUDA Compatible GPU
- [CUDA (latest version) (current working one is 11.5)](https://developer.nvidia.com/cuda-downloads)
- [CUDNN (latest version compatible with CUDA) (current working one is 8.3.2)](https://developer.nvidia.com/rdp/cudnn-download)
- Python 3.9.7

If you have others CUDA versions installed, make sure you set the system variable "CUDA_PATH" to your latest CUDA path

## Install the requirements for each module

### Converter
```bash
cd tsukiu
cd modules
cd convert
virtualenv env --python=3.9.7
pip install -r requirements.txt
```

### DeepCreamPy
```bash
cd tsuki
cd modules
cd DeepCreamPy
virtualenv env --python=3.9.7
pip install -r requirements.txt
```

### HentAI
  - You need to download pytorch 0.4.1 wheel and put it in the HentAI folder first
  - Download it [here](https://download.pytorch.org/whl/cpu/torch-0.4.1-cp35-cp35m-win_amd64.whl)
#### after that run
```bash
cd tsuki
cd modules
cd HentAI
virtualenv env --python=3.9.7
pip install -r requirements.txt
```

### ToneRemover
```bash
cd tsuki
cd modules
cd ToneRemover
virtualenv env --python=3.9.7
pip install -r requirements.txt
```

## Download the required models

### DeepCreamPy
  - [Models.zip](https://drive.google.com/file/d/1ZJ5x-lVnouTv-OL8jp_ClDD1A7QgDwoa/view?usp=sharing)
    - Extract the file then put it in DeepCreamPy/models folder

### HentAI
  - [4x_FatalPixels_340000_G.pth](https://de-next.owncube.com/index.php/s/mDGmi7NgdyyQRXL)
  - [Weights.h5](https://www.dropbox.com/s/zvf6vbx3hnm9r31/weights268.zip?dl=0)
    - Put these two files in HentAI folder
  - [RRDB](https://drive.google.com/file/d/1pJ_T-V1dpb1ewoEra1TGSWl5e6H7M4NN/view) 
    - Put this in HentAI/ColabESRGAN/models folder

# Usage

### First time running the scripts

```
.\init.bat
```
The scripts will create "INPUT" and "OUTPUT" folder for each modules to use

### For black & white manga
Put the manga images in "INPUT" folder (Both PNG & JPG are acceptable)
```
.\run-blackwhite.bat
```

### For colored manga
Put the manga images in "INPUT" folder (Both PNG & JPG are acceptable)
```
.\run-color.bat
```

# Demo
![Demo](https://cdn.discordapp.com/attachments/858334807561863221/944618448540033064/test-output.png)
