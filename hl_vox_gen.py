import sys
import wave
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
    os.chdir(os.path.expanduser("~/.local/share/Steam/steamapps/common/Half-Life/valve/sound/"))
    vox_dir = "./vox"
    arg = sys.argv[1:]
    outfile = "out.wav"
    error_flag = True
    options = []
    if arg[-1] == "--help" or arg[-1] == "-h":
        print("help")
    else:
        new_arg = []
        new_arg.extend(arg)
        offset = 0
        for argnum in range(len(arg)):
            if arg[argnum][0] == "-":
                if arg[argnum] == "-o":
                    outfile = arg[argnum + 1]
                    new_arg.pop(argnum - offset)
                    new_arg.pop(argnum - offset)
                    offset += 2
                elif arg[argnum] == "-v":
                    if not arg[argnum + 1] in os.listdir():
                        print(arg[argnum + 1], "is not a directory")
                        error_flag = False
                        break
                    else:
                        vox_dir = "./" + arg[argnum + 1]
                        new_arg.pop(argnum - offset)
                        new_arg.pop(argnum - offset)
                        offset += 2
        if error_flag:
            os.chdir(vox_dir)
            vox_words = os.listdir()
            arg_new = []
            for argument in new_arg:
                argument += ".wav"
                if argument in vox_words:
                    arg_new += [argument]
                else:
                    print(f"invalid argument {argument} does not exist")
                    error_flag = False
                    break
            print("arguments: " + "".join(word + " " for word in arg_new) + f"\noutput file: {outfile}\nvoxdir: {vox_dir[2:]}")
            if error_flag:
                out_gen(arg_new, outfile, cwd)

if __name__ == "__main__":
    main()
