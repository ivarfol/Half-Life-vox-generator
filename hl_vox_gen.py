import sys
import os
from platform import system
from pydub import AudioSegment
from math import log
if system() != "Windows":
    from pydub.playback import play

def find_end(arg, argnum, letternum):
    out = arg[argnum][letternum:]
    for argnum_new in range(argnum, len(arg)):
        if argnum_new != argnum:
            out += " " + arg[argnum_new]
        if arg[argnum_new][-1] == ")":
            break
    return(out, len(out.split()))

def get_control(control):
    out = []
    tmp = control[0].split(" ")
    tmp[0] = tmp[0][1:]
    tmp[-1] = tmp[-1][:-1]
    for var in tmp:
        out += [[var[0], int(var[1:])]]
    return(out)

def control_dict(control):
    ctrl_dict = {}
    for controlnum in range(len(control)):
        if control[controlnum][2] in ctrl_dict:
            ctrl_dict[control[controlnum][2]] = [ctrl_dict[control[controlnum][2]], controlnum]
        else:
            ctrl_dict[control[controlnum][2]] = controlnum
    #print("dict", ctrl_dict)
    return(ctrl_dict)

def gen_control_arr(ctrl, control_arr):
    #print("ctrl:", ctrl)
    for contr_var in ctrl:
        if contr_var[0] == "e":
            control_arr[0] = contr_var[1]
        elif contr_var[0] == "p":
            control_arr[1] = contr_var[1]
        elif contr_var[0] == "s":
            control_arr[2] = contr_var[1]
        elif contr_var[0] == "v":
            control_arr[3] = contr_var[1]
        elif contr_var[0] == "t":
            control_arr[4] = contr_var[1]
    #print("ctrl arr", control_arr)
    return(control_arr)

def timecompress(time_pr, sound):
    length = len(sound)
    step = length / 8
    cut_pr = step / 100 * time_pr
    current_pos = step
    new_sound = sound[:step]
    for _ in range(8):
        new_sound += sound[current_pos + cut_pr:current_pos + step]
        current_pos += step
    return(new_sound)

def postcontrol(infile, control_arr):
    sound = AudioSegment.from_wav(infile) # cut end, 100 = 0.1s
    if control_arr[0] != 100:
        sound = sound[:control_arr[0] - 100]
    if control_arr[2] != 0:
        sound = sound[control_arr[2]*10:] # cut start, 100 = 0.1s
    if control_arr[1] != 0 and control_arr[1] != 100:
        octaves = (control_arr[1] - 100) / 50 # change pitch, 255 = 1 octave
        new_sample_rate = int(sound.frame_rate * (2 ** octaves))
        hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        hipitch_sound = hipitch_sound.set_frame_rate(11025)
        sound = hipitch_sound
    if control_arr[3] != 100:
        sound += 10 * log(control_arr[3] / 100, 10) # change volume, 0 = -10db
    if control_arr[4] != 0:
        sound = timecompress(control_arr[4], sound) # time compression
    return(sound)

def word_sound(control, ctrl_dict, filenum, infiles, control_arr):
    tmp_control_arr = []
    temp = []
    if filenum in ctrl_dict.keys():
        tmp = ctrl_dict.get(filenum)
        if not type(tmp) == int:
            if control[tmp[0]][1]:
                ctrlt = get_control(control[tmp[0]])
                ctrlf = get_control(control[tmp[1]])
            else:
                ctrlt = get_control(control[tmp[1]])
                ctrlf = get_control(control[tmp[0]])
        else:
            if control[tmp][1]:
                ctrlt = get_control(control[tmp])
                ctrlf = 0
            else:
                ctrlf = get_control(control[tmp])
                ctrlt = 0
        #print("ctrl t:", ctrlt)
        #print("ctrl f:", ctrlf)
        if ctrlt:
            control_arr = gen_control_arr(ctrlt, control_arr)
        if ctrlf:
            temp.extend(control_arr)
            tmp_control_arr = gen_control_arr(ctrlf, temp)
            return(postcontrol(infiles[filenum], tmp_control_arr), control_arr)
        else:
            return(postcontrol(infiles[filenum], control_arr), control_arr)
        #print("control:", control_arr)
        #print("tmp control:", tmp_control_arr)
    else:
        return(postcontrol(infiles[filenum], control_arr), control_arr)

def out_gen(infiles, outfile, cwd, pl, control, syst):
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
    if pl != 1 and syst != "Windows":
        play(sound)

def main():
    syst = system()
    cwd = os.getcwd()
    if syst == "Windows":
        os.chdir("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Half-Life\\valve\\sound")
    else:
        os.chdir(os.path.expanduser("~/.local/share/Steam/steamapps/common/Half-Life/valve/sound/"))
    vox_dir = "./vox"
    arg = sys.argv[1:]
    swap_tup = (".", ",")
    outfile = "out.wav"
    options = []
    pl = 0
    if len(arg) < 1 or "--help" in arg or "-h" in arg:
        print("Half life vox generator\n")
        print('usage: python3 hl_vox_gen [option(s)] ["file_name[s]"] [option(s)]')
        print("supported optins [default in brackets]:")
        print("-v use different directory for .wav files [vox]")
        print("-o specify the name of the output file [out.wav]")
        if syst != "Windows":
            print("-p play file after generating if 0, only generate if one")
            print("only play if 2 [0]")
        print("-h or --help print this message and exit")
        sys.exit(0)
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
                vox_dir = arg[argnum + 1]
                new_arg.pop(argnum - offset)
                new_arg.pop(argnum - offset)
                offset += 2
            elif arg[argnum] == "-p" and syst != "Windows":
                pl = int(arg[argnum + 1])
                new_arg.pop(argnum - offset)
                new_arg.pop(argnum - offset)
                offset += 2
                if pl == 2:
                    outfile = "n/a"
    if len(new_arg) != 1:
        if len(new_arg) > 1:
            print("Too many arguments!")
        else:
            print("No arguments!")
        sys.exit(0)
    offset = 0
    new_arg = new_arg[0].split(" ")
    if new_arg[0][0] == "!":
        line_name = new_arg[0][1:]
        try:
            with open("sentences.txt", "r") as file:
                for line in file:
                    if line.strip().split(" ")[0] == line_name:
                        sentence_output = line.strip()
                        for add_word in new_arg[1:]:
                            sentence_output += " " + add_word
                        print(sentence_output)
                        new_arg = line.strip().split(" ")[1:] + new_arg[1:]
                        break
        except:
            print("No sentence called", line_name)
            sys.exit(0)
    if "/" in new_arg[0]:
        vox_dir = new_arg[0].split("/")[0]
        new_arg = [new_arg[0].split("/")[1]] + new_arg[1:]
    tmp_arg = []
    for word in new_arg:
        if word != "":
            if word[-1] in swap_tup:
                tmp_arg += [word[:-1]]
                if word[-1] == ".":
                    tmp_arg += ["_period"]
                else:
                    tmp_arg += ["_comma"]
            else:
                tmp_arg += [word]
    new_arg = []
    new_arg.extend(tmp_arg)
    for argnum in range(len(tmp_arg)):
        flag = False
        for letternum in range(len(tmp_arg[argnum])):
            if tmp_arg[argnum][letternum] == "(":
                if letternum == 0:
                    temp, cut = find_end(tmp_arg, argnum, 0)
                    control += [[temp, True, argnum - offset]]
                    if cut == argnum:
                        new_arg.pop(argnum - offset)
                        offset += 1
                    else:
                        for i in range(cut):
                            new_arg.pop(argnum + i - offset)
                            offset += 1
                else:
                    if new_arg[argnum - offset][-1] == ")":
                        temp = new_arg[argnum - offset][letternum:]
                        cut = 1
                    else:
                        temp, cut = find_end(tmp_arg, argnum, letternum)
                    new_arg[argnum - offset] = new_arg[argnum - offset][:letternum]
                    control += [[temp, False, argnum - offset]]
                    #print(cut)
                    for j in range(cut - 1):
                        new_arg.pop(argnum + j - offset + 1)
                        offset += 1
                flag = True
                break
            if flag:
                break
    os.chdir(os.path.expanduser(vox_dir))
    vox_words = os.listdir()
    arg_new = []
    for argument in new_arg:
        argument += ".wav"
        if argument in vox_words:
            arg_new += [argument]
        else:
            print(f"invalid argument {argument} does not exist")
            sys.exit(0)
    print("arguments: " + "".join(word + " " for word in arg_new) + f"\ncontrol: {control}\noutput file: {outfile}\nvoxdir: {vox_dir}")
    out_gen(arg_new, outfile, cwd, pl, control, syst)
    print("Success")

if __name__ == "__main__":
    main()
