import sys, os
from platform import system
from pydub import AudioSegment
from math import log
if system() != "Windows":
    from pydub.playback import play

def find_end(arg, argnum, letternum):
    '''
    find_end
    finds the second ) in the sentence

    Parameters
    ----------
    arg : list
        the sentence as a list
    argnum : int
        word number in the sentence
    letternum : int
        letter number where the ( is at

    Returns
    -------
    out : str
        the words that were in ()
    len(out.split()) : int
        number of words in ()
    '''
    out = arg[argnum][letternum:]
    for argnum_new in range(argnum, len(arg)):
        if argnum_new != argnum:
            out += " " + arg[argnum_new]
        if arg[argnum_new][-1] == ")":
            break
    return(out, len(out.split()))

def get_control(control):
    '''
    get_control
    returs list of lists with control letter and value

    Parameters
    ----------
    control : list
        control string in (), word num and tmp flag

    Returns
    -------
    out : list
        control letter and value
    '''
    out = []
    tmp = control[0].split(" ")
    tmp[0] = tmp[0][1:]
    tmp[-1] = tmp[-1][:-1]
    for var in tmp:
        out += [[var[0], int(var[1:])]]
    return(out)

def control_dict(control):
    '''
    control_dict
    generates dictionary for control vars

    Parameters
    ----------
    control : list
        control string in (), word num and tmp flag

    Returns
    -------
    ctrl_dict : dict
        dictionary where key is word number, and value is list
        or int of control value numbers
    '''
    ctrl_dict = {}
    for controlnum in range(len(control)):
        if control[controlnum][2] in ctrl_dict:
            ctrl_dict[control[controlnum][2]] = [ctrl_dict[control[controlnum][2]], controlnum]
        else:
            ctrl_dict[control[controlnum][2]] = controlnum
    #print("dict", ctrl_dict)
    return(ctrl_dict)

def gen_control_arr(ctrl, control_arr):
    '''
    gen_control_arr
    generates control array

    Parameters
    ----------
    ctrl : list
        control letter and value

    Returns
    -------
    control_arr : list
        list of control var values
    '''
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
    '''
    timecompress
    time comression like in gold source

    Parameters
    ----------
    time_pr : int
       compression ratio in %
    sound : AudioSegment
        audio to be comressed

    Returns
    -------
    new_sound : AudioSegment
        comressed audio
    '''
    length = len(sound)
    step = length / 8
    cut_pr = step / 100 * time_pr
    current_pos = step
    new_sound = sound[:step]
    for _ in range(8):
        new_sound += sound[current_pos + cut_pr:current_pos + step]
        current_pos += step
    return(new_sound)

def postcontrol(infile, control_arr, prim_vox_dir, fallback_dir):
    '''
    postcontrol
    manupulates audio according to control_arr

    Parameters
    ----------
    infile : str
        name of the input file
    control_arr : list
        list of control var values
    prim_vox_dir : str
        path to primary vox directory
    fallback_dir : str
        path to fallback directory

    Returns
    -------
    sound : AudioSegment
        audio after the manipulations
    '''
    try:
        sound = AudioSegment.from_wav(infile) # cut end, 100 = 0.1s
    except:
        try:
            os.chdir(fallback_dir)
            sound = AudioSegment.from_wav(infile)
            os.chdir(prim_vox_dir)
        except:
            print("argument", infile[:-4], "does not exist in primary, or fallback dir")
            sys.exit(1)
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

def word_sound(control, ctrl_dict, filenum, infiles, control_arr, prim_vox_dir, fallback_dir):
    '''
    word_sound
    generates audio for a word

    Parameters
    ----------
    control : list
        control string in (), word num and tmp flag
    ctrl_dict : dict
        dictionary where key is word number, and value is list
        or int of control value numbers
    filenum : int
        number of the word in the infiles
    infiles : list
        list of words in the sentence
    control_arr : list
        list of control var values
    prim_vox_dir : str
        path to primary vox directory
    fallback_dir : str
        path to fallback directory

    Returns
    -------
    postcontrol(infiles[filenum]) : AudioSegment
        audio for the word
    control_arr : list
        list of control var values
    '''
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
            return(postcontrol(infiles[filenum], tmp_control_arr, prim_vox_dir, fallback_dir), control_arr)
        else:
            return(postcontrol(infiles[filenum], control_arr, prim_vox_dir, fallback_dir), control_arr)
        #print("control:", control_arr)
        #print("tmp control:", tmp_control_arr)
    else:
        return(postcontrol(infiles[filenum], control_arr, prim_vox_dir, fallback_dir), control_arr)

def out_gen(infiles, outfile, cwd, pl, control, syst, fallback_dir):
    '''
    out_gen
    generates the audio, expeorts/plays it

    Parameters
    ----------
    infiles : list
        list of words in the sentence
    outfile : str
        name of the file to export the audio to
    cwd : path
        path to dir where the program was launched
    pl : int
        whether the file will be exported or player (-p option)
    control : list
        control string in (), word num and tmp flag
    syst : str
        system name
    prim_vox_dir : str
        path to primary vox directory
    fallback_dir : str
        path to fallback directory
    '''
    prim_vox_dir = os.getcwd()
    ctrl_dict = control_dict(control)
    control_arr = [100, 0, 0, 100, 0] #end pitch start volume time
    sound, control_arr = word_sound(control, ctrl_dict, 0, infiles, control_arr, prim_vox_dir, fallback_dir)
    for filenum in range(1, len(infiles)):
        tmp = word_sound(control, ctrl_dict, filenum, infiles, control_arr, prim_vox_dir, fallback_dir)
        sound += tmp[0]
        control_arr = tmp[1]
    os.chdir(cwd)
    if pl != "pl":
        sound.export(outfile, format="wav")
    if pl != "gn" and syst != "Windows":
        try:
            play(sound)
        except:
            print("Looks like you don't have ffmpeg installed, but it is required for playback\nif you did not pass '-p 2' option the file has been generated\nif you don't want to install ffmpeg\nto disable this messege, change 'pl' variable value in the main() to 'gn'")
            sys.exit(1)

def main():
    syst = system()
    cwd = os.getcwd()
    try:
        if syst == "Windows":
            os.chdir("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Half-Life")
        else:
            os.chdir(os.path.expanduser("~/.local/share/Steam/steamapps/common/Half-Life"))
        hl_dir = os.getcwd()
    except:
        print("Looks like you dont have Half-Life 1 installed with steam, ether install it with steam, or\n change the os.chdir at the beggining of main to your Half-Life/valve/sound directory")
        sys.exit(1)
    game_dir = "valve"
    vox_dir = "./vox"
    arg = sys.argv[1:]
    swap_tup = (".", ",")
    outfile = "out.wav"
    options = []
    pl = "both" 
    if len(arg) < 1 or "--help" in arg or "-h" in arg:
        print("Half life vox generator\n")
        print('usage: python3 hl_vox_gen [option(s)] ["file_name[s]"] [option(s)]')
        print("supported optins [default in brackets]:")
        print("-v use different directory for .wav files [vox]")
        print("-o specify the name of the output file [out.wav]")
        print("--game specify the game: gearbox, bshift or valve [valve]")
        if syst != "Windows":
            print("--play play file after generating if 0, only generate if 'gn'")
            print("only play if 'pl' [0]")
        print("-h or --help print this message and exit")
        sys.exit(0)
    new_arg = []
    control = []
    new_arg.extend(arg)
    offset = 0
    for argnum in range(len(arg)):
        if arg[argnum][0] == "-":
            if arg[argnum] == "-o":
                if len(arg) < argnum + 1:
                    outfile = arg[argnum + 1]
                else:
                    print("No file specified after -o option")
                    sys.exit(1)
                new_arg.pop(argnum - offset)
                new_arg.pop(argnum - offset)
                offset += 2
            elif arg[argnum] == "-v":
                if len(arg) < argnum + 1:
                    vox_dir = arg[argnum + 1]
                else:
                    print("No path after -v option")
                    sys.exit(1)
                new_arg.pop(argnum - offset)
                new_arg.pop(argnum - offset)
                offset += 2
            elif arg[argnum] == "--play" and syst != "Windows":
                if len(arg) < argnum + 1:
                    pl = arg[argnum + 1]
                else:
                    print("No arguments after --play option")
                    sys.exit(1)
                if not pl in ("pl", "both", "gn"):
                    print(pl, "is not a valid play option")
                    sys.exit(1)
                new_arg.pop(argnum - offset)
                new_arg.pop(argnum - offset)
                offset += 2
                if pl == "pl":
                    outfile = "n/a"
            elif arg[argnum] == "--game":
                if len(arg) < argnum + 1:
                    game_dir = arg[argnum + 1]
                else:
                    print("No game specified after --game option")
                    sys.exit(1)
                if os.path.isdir(hl_dir + "/bshift") and game_dir == "bshift" or os.path.isdir(hl_dir + "/gearbox") and game_dir == "gearbox" or game_dir == "valve":
                    new_arg.pop(argnum - offset)
                    new_arg.pop(argnum - offset)
                    offset += 2
                else:
                    print(game_dir, "is not a valid game")
                    sys.exit(1)
    os.chdir(game_dir+"/sound")
    if len(new_arg) != 1:
        if len(new_arg) > 1:
            print("Too many arguments!")
        else:
            print("No arguments!")
        sys.exit(1)
    offset = 0
    new_arg = new_arg[0].split(" ")
    if new_arg[0][0] == "!":
        line_name = new_arg[0][1:]
        try:
            with open("sentences.txt", "r", encoding="cp1252") as file:
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
            sys.exit(1)
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
    try:
        os.chdir(os.path.expanduser(vox_dir))
    except:
        print(vox_dir, "is not a valid vox dir")
        sys.exit(1)
    vox_words = os.listdir()
    fallback_dir = hl_dir + "/valve/sound/" + vox_dir
    if not os.path.isdir(fallback_dir):
        fallback_dir = os.getcwd()
    fallback_vox_words = os.listdir(fallback_dir)
    arg_new = []
    for argument in new_arg:
        argument += ".wav"
        if argument in vox_words or argument in fallback_vox_words:
            arg_new += [argument]
        elif argument.lower() in vox_words or argument.lower() in fallback_vox_words:
            arg_new += [argument.lower()]
        else:
            print("invalid argument", argument, "does not exist")
            sys.exit(1)
    print("arguments: " + "".join(word + " " for word in arg_new) + f"\ncontrol: {control}\noutput file: {outfile}\nvoxdir: {vox_dir}")
    out_gen(arg_new, outfile, cwd, pl, control, syst, fallback_dir)
    print("Success")

if __name__ == "__main__":
    main()
