import sys, os, json
import pandas as pd

def getgatimecourse(id):
    fh = open(os.path.join('../experiments/',id,"generations.log"))
    newlines = []
    # newlines.append("i,j,x,y,z,g,f")
    tmp = fh.readlines()
    fh.close()
    lines = [x.strip() for x in tmp]
    gen_size=str.split(lines[1],',')[0]
    gen_size=int(str.split(gen_size,' ')[3])
    # print(lines[4])
    # df = pd.DataFrame(columns=["i","j","x","y","z","g","f"])
    for line in range(4, len(lines)):
        if not lines[line].startswith('0,') and not lines[line].startswith('-1,'):
            continue
        else:
            lines[line] = lines[line].replace(' ','')
            lines[line] = lines[line].replace('[','')
            lines[line] = lines[line].replace('],(',',')
            lines[line] = lines[line].replace(',)','')
            # df = df.append(str.split(lines[line],','), ignore_index=True)
            newlines.append(lines[line])
    # print(newlines)
    scores = [];
    for line in range(0,len(newlines)):
        # print(newlines[line])
        scores.append(str.split(newlines[line],',')[6])
    # print(scores[2*gen_size::2*gen_size])
    # print(scores)
    return json.dumps(scores[2*gen_size::2*gen_size])