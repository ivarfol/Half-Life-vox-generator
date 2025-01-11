# Half-Life-vox-generator
This is a program for joining and manipulating half life audio files  
You will need pydub library installed  
```
pip install pydub
```
  
if you have a copy installed with steam, but would want to uninstall it and  
keep this program working you can run ``copy_files.sh`` if you are on linux  
or ``copy_files.bat`` if you are on windows  
  
if the game was not installed with steam  
create directory ``sound`` in the same directory as this program, then create dirctory ``valve``  
in there, if you also wounld like to have acces to blue shift and opposing forece sound files  
create ``bshift`` directory for blue shift and ``gearbox`` directory for opposing force  
then copy directories named ``sound`` form your half life location into the corresponding dirs   
directories you will need to copy from your game files:
```
Half-Life
\_valve
| \_sound <- copy this to sound/valve in the program directory
\_gearbox
| \_sound <- copy this to sound/gearbox in the program directory
\_bshift
  \_sound <- copy this to sound/bshift in the program directory
```
at the end the file tree shound look like this:  
```
hl_vox_gen.py
copy_files.sh
copy_files.bat
README.md
sound
\_valve
| \_sound
\_gearbox
| \_sound
\_bshift
  \_sound
```
or like this (if you only copied valve sounds):
```
hl_vox_gen.py
copy_files.sh
copy_files.bat
README.md
sound
\_valve
  \_sound
```
note that valve sounds are required for the expansios, as some phrases rely on the vanilla sounds  
[link to a repo with sound files](https://github.com/sourcesounds/hl1)  
## Usage
python3 hl\_vox\_gen.py \[option(s)\] \["sentence"\] \[option(s)\]  
supported options \[default in brackets\]:  
-v use different directory for .wav files [vox]  
-o specify output file name  
--game specify the game: gearbox, bshift or valve [valve]
-h or --help print help  

if you are using linux you can also use --play option  
to specify whether the file will be generated and played (--play both default),  
generated only (--play gn), or played only (--play pl)  

an example:  
``python3 hl_vox_gen.py -o hello_world.wav "(p130) bizwarn bizwarn bizwarn (e95 p95) attention  this announcement system now(e100) under military command"``

You can use sintax from sentences.txt in your  
~/.local/share/Steam/steamapps/common/Half-Life/valve/sound/  
directory for linux, or  
C:\\Program Files (x86)\\Steam\\steamapps\\common\\Half-Life\\valve\\sound  
for windows  
to change pitch from (p1) to (p255) (reset is (p0), same as (p100))  
ending point from (e100) to (e0) (default is (e100),  
(e0) cuts one second off the end)  
starting point from (s0) to (s100) (default (s0),  
(s100) cuts one second off the start)  
volume in % from (v100) to (v0) (default (v100))  
and time compression from (t0) to (t100) default is (t0)  

the above options can be ether appended to a word ``test(p90)`` to  
only change the word, or used separetly to change all words after the option:  
``test (p95) test test`` in this example the first ``test`` will sound  
differently to the two after the ```p95```  

the program outputs the files in wav format, but you can convert it to mp3 with ffmpeg:  
```
ffmpeg -i input.wav -vn -ar 11025 -ac 1 -b:a 88.2k output.mp3
```

for more information visit [this article](https://twhl.info/wiki/page/sentences.txt)  

### New features
now -v option accepts paths to any location, not just the Half-Life/sound directory  
now you can specify vox directory like in sentences.txt, example: ``python3 hl_vox_gen.py "hgrunt/freeman!"``  
is the same as ``python3 hl_vox_gen.py -v hgrunt "freeman!"``  
now you can pass the sentence name instead of the whole sentence ``python3 hl_vox_gen.py "!HG_ALERT5"``  
is the same as ``python3 hl_vox_gen.py "hgrunt/(t20) clik squad!, neutralize!(e90) freeman! clik"``  
you will find the sentence name at the start of each sentence in sentences.txt  
when using this feature on linux you will have to use ``''`` instead of ``""`` as the ``!`` will cause an error  
you can now use --game option to use voicelines from opposing force (--game gearbox) or blue shift (--game bshift)  
the voice lines from the original game will still be accesible if the vox directory with the same name exists  
example: ``python3 hl_vox_gen.py "otis/reputation beer" -o reputation.wav --game gearbox``  
  
now you can have several sentence names/voxdirs per sentence  
examples:  
``python3 hl_vox_gen.py "!HG_QUEST9 !C1A3_5"``  
``python3 hl_vox_gen.py "hgrunt/hostiles! scientist/yees"``  
``python3 hl_vox_gen.py "hgrunt/hostiles! scientist/yees !HG_QUEST9"``  
note that the control variables (the letter+number in brackets) are reset each time  
there is a new vox dir or sentence name in the input  
  
Now pitch control works as intended  
There is still a small discrepancy when joining words with different pitch values,  
but it's well within the acceptable bounds
