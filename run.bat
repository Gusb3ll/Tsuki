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

echo y  | del .\OUTPUT\*

move .\INPUT\* .\convert\input\ 

cd convert
.\env\Scripts\python.exe .\JPG_to_PNG_converter.py

cd ..

move .\convert\output\*.png .\hent\input\
echo y | del .\convert\input\*

cd hent
.\env\Scripts\python.exe .\main.py

cd ..

move .\hent\output\decensor_input\*.png .\DeepCreamPy\decensor_input\
echo y | del .\hent\input\*

cd DeepCreamPy
.\env\Scripts\python.exe .\decensor.py

cd ..

move .\DeepCreamPy\decensor_output\*.png .\OUTPUT
echo y | del .\DeepCreamPy\decensor_input\*
