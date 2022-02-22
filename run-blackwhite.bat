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

CALL .\env\Scripts\activate.bat

cd convert
python .\converter.py

cd ..

move .\convert\output\*.png .\ToneRemover\input\
echo y | del .\convert\input\*

cd ToneRemover
python .\toneremove.py

cd ..

move .\ToneRemover\output\*.png .\HentAI\input\
echo y | del .\ToneRemover\input\*

cd HentAI
python .\main.py

cd ..

move .\HentAI\output\*.png .\DeepCreamPy\decensor_input\
echo y | del .\HentAI\input\*

cd DeepCreamPy
python .\decensor.py

cd ..
cd ..

move .\modules\DeepCreamPy\decensor_output\*.png .\OUTPUT
echo y | del .\modules\DeepCreamPy\decensor_input\*

echo.
echo.
echo.
echo.
echo.
echo DECENSORING COMPETED, ENJOY!
echo.
echo.
echo.
echo.
echo.