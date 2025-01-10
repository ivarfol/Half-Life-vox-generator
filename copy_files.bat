mkdir sound
cd sound
mkdir valve
mkdir gearbox
mkdir bshift
mkdir valve\sound
mkdir gearbox\sound
mkdir bshift\sound
xcopy /s/e "C:\Program Files (x86)\Steam\steamapps\common\Half-Life\valve\sound" ".\valve\sound"
xcopy /s/e "C:\Program Files (x86)\Steam\steamapps\common\Half-Life\gearbox\sound" ".\gearbox\sound"
xcopy /s/e "C:\Program Files (x86)\Steam\steamapps\common\Half-Life\bshift\sound\" ".\bshift\sound"
