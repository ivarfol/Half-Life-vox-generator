import sys
import wave
from pathlib import Path
import os
def out_gen(infiles, outfile, cwd):
    data = []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()
    os.chdir(cwd)
    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()

def main():
    cwd = os.getcwd()
    os.chdir(os.path.expanduser("~/.local/share/Steam/steamapps/common/Half-Life/valve/sound/vox/"))
    arg = sys.argv[1:]
    outfile = "out.wav"
    error_flag = True
    if arg[-1] == "--help" or arg[-1] == "-h":
        print("help")
    else:
        if arg[-2] == "-o":
            outfile= arg[-1]
            arg = arg[:-2]
        vox_words = os.listdir()
        for argument in arg:
            if not argument + ".wav" in vox_words:
                print(f"invalid argument {argument}.wav does not exist")
                error_flag = False
                break
        print(f"arguments: {arg}\noutput file: {outfile}")
        if error_flag:
            arg_new = []
            for argument in arg:
                arg_new += [argument + ".wav"]
            out_gen(arg_new, outfile, cwd)

if __name__ == "__main__":
    main()
