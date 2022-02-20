mkdir .\INPUT
mkdir .\OUTPUT

mkdir .\modules\Convert\input
mkdir .\modules\Convert\output

mkdir .\modules\ToneRemover\input
mkdir .\modules\ToneRemover\output

mkdir .\modules\DeepCreamPy\decensor_input
mkdir .\modules\DeepCreamPy\decensor_output

mkdir .\modules\HentAI\input
mkdir .\modules\HentAI\output\
mkdir .\modules\HentAI\output\decensor_input

python -m pip install virtualenv

cd modules 

cd Convert
virtualenv env
.\env\Scripts\python.exe .\env\Scripts\pip.exe install -r ./requirements.txt

cd ..

cd DeepCreamPy
virtualenv env
.\env\Scripts\python.exe .\env\Scripts\pip.exe install -r ./requirements.txt

cd ..

cd HentAI
virtualenv env
.\env\Scripts\python.exe .\env\Scripts\pip.exe install -r ./requirements.txt

cd ..

cd ToneRemover
virtualenv env
.\env\Scripts\python.exe .\env\Scripts\pip.exe install -r ./requirements.txt