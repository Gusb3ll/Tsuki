# TSUKIUNCEN

### YOU NEED CUDA >= 9.0 < 10 AND CUDNN >= 7.0 < 8 TO USE THIS

[CUDA](https://developer.nvidia.com/cuda-90-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exenetwork)

[CUDNN](https://developer.nvidia.com/rdp/cudnn-archive)

## Python environment for each module

### Convert : >= 3.9 < 3.10
### download : >= 3.9 < 3.10
### DeepCreamPy : >= 3.9 < 3.10
### Hent : 3.5.2 ONLY

## Download and put these files in DeepCreamPy models folder

### [model](https://drive.google.com/file/d/1ZJ5x-lVnouTv-OL8jp_ClDD1A7QgDwoa/view?usp=sharing)


## Download and put these files in HentAI folder

### [4x_FatalPixels_340000_G.pth](https://de-next.owncube.com/index.php/s/mDGmi7NgdyyQRXL)

### [Weights.h5](https://www.dropbox.com/s/zvf6vbx3hnm9r31/weights268.zip?dl=0)

### [PyTourch for python 3.5 (Windows)](http://download.pytorch.org/whl/cu92/torch-0.4.1-cp35-cp35m-win_amd64.whl)

### [RRDB](https://drive.google.com/file/d/1pJ_T-V1dpb1ewoEra1TGSWl5e6H7M4NN/view) - put this in HentAI/ColabESRGAN/models folder

## Init DeepCreamPy

```
cd DeepCreamPy
virtualenv env --python=3.9
.\env\scripts\activate
pip install -r requirements.txt
```

## Init HentAI

```
cd HentAI
virtualenv env --python=3.5.2
.\env\scripts\activate
pip install torch-0.4.1-cp35-cp35m-win_amd64
pip install -r requirements-gpu.txt
pip install ffmpeg
python setup.py install
```

## Usage

### Run init.bat for once and run.bat everytime you wish to use it
### Always put censored pictures in "INPUT" folder
