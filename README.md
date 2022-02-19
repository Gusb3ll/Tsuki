# Tsuki

### Manga uncensoring script based on
- [DeepCreamPy](https://github.com/liaoxiong3x/DeepCreamPy)
- [HentAI](https://github.com/natethegreate/hent-AI)
- [ToneRemover](https://github.com/natethegreate/Screentone-Remover) (For non-colored manga)

# Installiation

### System requirements

- CUDA Compatible GPU
- [CUDA 9.0](https://developer.nvidia.com/cuda-90-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exenetwork)
- [CUDNN 7.6.5](https://developer.nvidia.com/rdp/cudnn-archive)
- Python 3.9.7
- Python 3.5.2 (Used for HentAI) <- Reworking to work with python 3.9

If you have cuda 10 or 11 install, install cuda 9 and set the system variable "CUDA_PATH" to your CUDA 9.0 Path

## Install the requirements for each module

### Converter
```bash
cd tsukiuncen
cd modules
cd convert
virtualenv env --python=3.9.7
pip install -r requirements.txt
```

### DeepCreamPy
```bash
cd tsukiuncen
cd modules
cd DeepCreamPy
virtualenv env --python=3.9.7
pip install -r requirements.txt
```

### HentAI
  - You need to download pytorch 0.4.1 wheel and put it in the HentAI folder first
  - Download it [here](https://download.pytorch.org/whl/cpu/torch-0.4.1-cp35-cp35m-win_amd64.whl)
after that run
```bash
cd tsukiuncen
cd modules
cd HentAI
virtualenv env --python=3.5.2
pip install -r requirements.txt
```
Ignore any invaild syntax error

### ToneRemover
```bash
cd tsukiuncen
cd modules
cd ToneRemover
virtualenv env --python=3.9.7
pip install -r requirements.txt
```

## Download the required models

### DeepCreamPy
  - [Models.zip](https://drive.google.com/file/d/1ZJ5x-lVnouTv-OL8jp_ClDD1A7QgDwoa/view?usp=sharing)
    - Extract the file then put in DeepCreamPy/models folder

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
First put the manga images in "INPUT" folder
```
.\run-blackwhite.bat
```

### For colored manga
First put the manga images in "INPUT" folder
```
.\run-color.bat
```

# Demo
![Demo](https://cdn.discordapp.com/attachments/858334807561863221/944618448540033064/test-output.png)
