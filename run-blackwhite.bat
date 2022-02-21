@echo off

echo.
echo.
echo.
echo.
echo.
echo DECENSOR AUTOMATION SCRIPT BY GUSBELL
echo.
echo.
echo.
echo.
echo.

echo y | del .\OUTPUT\*

move .\INPUT\* .\modules\convert\input\ 

cd modules

cd convert
.\env\Scripts\python.exe .\converter.py

cd ..

move .\convert\output\*.png .\ToneRemover\input\
echo y | del .\convert\input\*

cd ToneRemover
.\env\Scripts\python.exe .\toneremove.py

cd ..

move .\ToneRemover\output\*.png .\HentAI\input\
echo y | del .\ToneRemover\input\*

cd HentAI
.\env\Scripts\python.exe .\main.py

cd ..

move .\HentAI\output\*.png .\DeepCreamPy\decensor_input\
echo y | del .\HentAI\input\*

cd DeepCreamPy
.\env\Scripts\python.exe .\decensor.py

cd ..
cd ..

move .\modules\DeepCreamPy\decensor_output\*.png .\OUTPUT
echo y | del .\modules\DeepCreamPy\decensor_input\*
