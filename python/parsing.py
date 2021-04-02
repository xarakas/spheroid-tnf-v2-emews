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
    if '[None]' in lines[2]:
        score_index=5
    else:
        score_index=6
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
        scores.append(str.split(newlines[line],',')[score_index])
    # print(scores[2*gen_size::2*gen_size])
    # print(scores)
    return json.dumps(scores[2*gen_size::2*gen_size])


def getgalogbook(id):
    fh = open(os.path.join('../experiments/',id,"generations.log"))
    tmp = fh.readlines()
    fh.close()
    lines = [x.strip() for x in tmp]
    gen_size=str.split(lines[1],',')[0]
    gen_size=int(str.split(gen_size,' ')[3])
    if '[None]' in lines[2]:
        score_index=5
    else:
        score_index=6
    newlines = []
    finallines = [] 
    j=0
    for line in range(4, len(lines)):
        if not lines[line].startswith('0,'):
            if 'Stored' in lines[line]:
                finallines.append(newlines)
                newlines = []
            continue
        else:
            lines[line] = lines[line].replace(' ','')
            lines[line] = lines[line].replace('[','')
            lines[line] = lines[line].replace('],(',',')
            lines[line] = lines[line].replace(',)','')
            # df = df.append(str.split(lines[line],','), ignore_index=True)
            newlines.append(str.split(lines[line],',')[score_index])
    # print(newlines)
    # print(finallines)
    return json.dumps(finallines)
    # print(gen_size)
    # print(lines[-1])