import sys
import os
from pydub import AudioSegment
from pydub.playback import play

def get_control(control):
    out = []
    out += [control[0][1:-2], control[1]]
    print(out)
    return(out)

def control_dict(control):
    ctrl_dict = {}
    for controlnum in range(len(control)):
        ctrl_dict[control[controlnum][2]] = controlnum
    return(ctrl_dict)

def word_sound(control, ctrl_dict, filenum, infiles):
    if filenum in ctrl_dict.keys():
        ctrl = get_control(control[ctrl_dict.get(filenum)])
        return(AudioSegment.from_wav(infiles[filenum])) #placeholder
    else:
        return(AudioSegment.from_wav(infiles[filenum]))

def out_gen(infiles, outfile, cwd, pl, control):
    ctrl_dict = control_dict(control)
    sound = word_sound(control, ctrl_dict, 0, infiles)
    for filenum in range(1, len(infiles)):
        sound += word_sound(control, ctrl_dict, filenum, infiles)
    os.chdir(cwd)
    if pl != 2:
        sound.export(outfile, format="wav")
    if pl != 1:
        play(sound)

def main():
    cwd = os.getcwd()
    os.chdir(os.path.expanduser("~/.local/share/Steam/steamapps/common/Half-Life/valve/sound/"))
    vox_dir = "./vox"
    arg = sys.argv[1:]
    outfile = "out.wav"
    error_flag = True
    options = []
    pl = 0
    if arg[-1] == "--help" or arg[-1] == "-h":
        print("Half life vox generator\n")
        print("usage: python3 hl_vox_gen [option(s)] [file(s)]")
        print("supported optins [default in brackets]:")
        print("-v use different directory for .wav files [vox]")
        print("-o specify the name of the output file [out.wav]")
        print("-p play file after generating if 0, only generate if one")
        print("only play if 2 [0]")
        print("-h or --help print this message and exit")
    else:
        new_arg = []
        control = []
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
                elif arg[argnum] == "-p":
                    pl = int(arg[argnum + 1])
                    new_arg.pop(argnum - offset)
                    new_arg.pop(argnum - offset)
                    offset += 2
            elif arg[argnum][-1] == "}":
                if arg[argnum][0] == "{":
                    new_arg.pop(argnum - offset)
                    offset += 1
                    control += [[arg[argnum], True, argnum - offset]]
                else:
                    for letternum in range(len(arg[argnum])):
                        if arg[argnum][letternum] == "{":
                            new_arg[argnum - offset] = new_arg[argnum - offset][:letternum]
                            control += [[arg[argnum][letternum:], False, argnum - offset]]
                            break
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
            print("arguments: " + "".join(word + " " for word in arg_new) + f"\ncontrol: {control}\noutput file: {outfile}\nvoxdir: {vox_dir[2:]}")
            if error_flag:
                out_gen(arg_new, outfile, cwd, pl, control)
                print("Success")

if __name__ == "__main__":
    main()
