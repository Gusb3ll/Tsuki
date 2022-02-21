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

move .\convert\output\*.png .\HentAI\input\
echo y | del .\convert\input\*

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