import sys
import os
from pydub import AudioSegment
from pydub.playback import play

def find_end(arg, argnum, letternum):
    out = arg[argnum][letternum:]
    for argnum_new in range(argnum, len(arg)):
        if argnum_new != argnum:
            out += " " + arg[argnum_new]
        if arg[argnum_new][-1] == "}":
            break
    return(out, argnum_new)

def get_control(control):
    out = []
    tmp = control[0].split(" ")
    tmp[0] = tmp[0][1:]
    tmp[-1] = tmp[-1][:-1]
    print(tmp)
    out += [control[0][1], int(control[0][2:-1]), control[1]]
    #print(out)
    return(out)

def control_dict(control):
    ctrl_dict = {}
    for controlnum in range(len(control)):
        ctrl_dict[control[controlnum][2]] = controlnum
    return(ctrl_dict)

def gen_control_arr(ctrl, control_arr):
    if ctrl[2]:
        if ctrl[0] == "e":
            control_arr[0] = ctrl[1]
        elif ctrl[0] == "p":
            control_arr[1] = ctrl[1]
        elif ctrl[0] == "s":
            control_arr[2] = ctrl[1]
        elif ctrl[0] == "v":
            control_arr[3] = ctrl[1]
        elif ctrl[0] == "t":
            control_arr[4] = ctrl[1]
    return(control_arr)

def postcontrol(infile, control_arr):
    if control_arr[0] != 100:
        pass # cut end
    elif control_arr[2] != 0:
        pass # cut start
    elif control_arr[1] != 0:
        pass # change pitch
    elif control_arr[3] != 100:
        pass # change volume
    elif control_arr[4] != 0:
        pass # time compression
    return()

def word_sound(control, ctrl_dict, filenum, infiles, control_arr):
    if filenum in ctrl_dict.keys():
        ctrl = get_control(control[ctrl_dict.get(filenum)])
        if ctrl[2]:
            control_arr = gen_control_arr(ctrl, control_arr)
        else:
            tmp_control_arr = gen_control_arr(ctrl, control_arr)
        print(control_arr)
        return(AudioSegment.from_wav(infiles[filenum]), control_arr) #placeholder
    else:
        return(AudioSegment.from_wav(infiles[filenum]), control_arr)

def out_gen(infiles, outfile, cwd, pl, control):
    ctrl_dict = control_dict(control)
    control_arr = [100, 0, 0, 100, 0] #epsvt
    sound, control_arr = word_sound(control, ctrl_dict, 0, infiles, control_arr)
    for filenum in range(1, len(infiles)):
        tmp = word_sound(control, ctrl_dict, filenum, infiles, control_arr)
        sound += tmp[0]
        control_arr = tmp[1]
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
            else:
                for letternum in range(len(arg[argnum])):
                    if arg[argnum][letternum] == "{":
                        if letternum == 0:
                            temp, cut = find_end(arg, argnum, 0)
                            control += [[temp, True, argnum - offset]]
                            if cut == argnum:
                                new_arg.pop(argnum - offset)
                                offset += 1
                            for i in range(cut - argnum - offset + 1):
                                new_arg.pop(argnum + i - offset)
                                offset += 1
                        else:
                            new_arg[argnum - offset] = new_arg[argnum - offset][:letternum]
                            temp, cut = find_end(arg, argnum, letternum)
                            control += [[temp, False, argnum - offset]]
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
