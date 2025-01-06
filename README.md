# Half-Life-vox-generator
This is a program for joining and manipulating half life audio files
## Usage
python3 hl\_vox\_gen.py \[option(s)\] \["sentence"\] \[option(s)\]
supported options \[default in brackets\]:
-v use different directory for .wav files [vox]
-o specify outpyt file name
-h or --help print help

if you are using linux you can also use -p option
to specify whether the file will be generated and played (-p 0 default),
generated only (-p 1), or played only (-p 2)

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

the above options can be ether appended to a word ```test(p90)``` to 
only change the word, or used separetly to change all words after the option:
for more information visit [this article](https://twhl.info/wiki/page/sentences.txt)
```test (p95) test test``` in this example the first ```test``` will sound
differently to the following two
### todo
swap ```,``` and ```.``` at the end of a word for _comma and _period
get more precise values for pitch
