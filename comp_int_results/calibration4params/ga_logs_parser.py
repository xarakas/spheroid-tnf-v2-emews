import sys, os, re

'''
    Usage:

        $ python3 ga_logs_parser.py <exp_folder1> <exp_folder2> ... <exp_folderN>

    where exp_folderx is a (relative) path to a folder containing the generations.log files
'''

for i in range(1,len(sys.argv)):
    generations_orig = os.path.join(os.path.dirname(os.path.realpath(__file__)),sys.argv[i],"generations.log")
    generations_new = os.path.join(os.path.dirname(os.path.realpath(__file__)),sys.argv[i],"generations.csv")
    newlines = []
    newlines.append("i,j,x,y,z,g,f\n")
    fh = open(generations_orig)
    fw = open(generations_new, 'w')
    tmp = fh.readlines()
    fh.close()
    lines = [x.strip() for x in tmp]
    gen_size=str.split(lines[1],',')[0]
    gen_size=int(str.split(gen_size,' ')[3])
    # print(lines[4])
    for line in range(4, len(lines)):
        if not lines[line].startswith('0,') and not lines[line].startswith('-1,'):
            continue
        else:
            lines[line] = lines[line].replace(' ','')
            lines[line] = lines[line].replace('[','')
            lines[line] = lines[line].replace('],(',',')
            lines[line] = lines[line].replace(',)','')
            newlines.append(lines[line]+"\n")
    fw.writelines(newlines)
    fw.close()

