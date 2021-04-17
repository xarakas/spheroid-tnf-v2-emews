import sys, os, json
import pandas as pd
import glob

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

def getexpdetails(id):
    fh = open(os.path.join('../experiments/',id,"generations.log"))
    tmp = fh.readlines()
    fh.close()
    lines = [x.strip() for x in tmp]
    return json.dumps([lines[0],lines[1],lines[2]])
    

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


def getga3d(id, limit):
    fh = open(os.path.join('../experiments/',id,"generations.log"))
    if limit=="max":
        limit=1000000
    else:
        limit=float(limit)
    newlines = []
    # newlines.append("i,j,x,y,z,g,f")
    tmp = fh.readlines()
    fh.close()
    lines = [x.strip() for x in tmp]
    gen_size=str.split(lines[1],',')[0]
    if '[None]' in lines[2]:
        scores_index=5
    else:
        scores_index=6
    gen_size=int(str.split(gen_size,' ')[3])
    # print(lines[4])
    # df = pd.DataFrame(columns=["i","j","x","y","z","g","f"])
    for line in range(4, len(lines)):
        if not lines[line].startswith('0,'):
            continue
        else:
            lines[line] = lines[line].replace(' ','')
            lines[line] = lines[line].replace('[','')
            lines[line] = lines[line].replace('],(',',')
            lines[line] = lines[line].replace(',)','')
            # df = df.append(str.split(lines[line],','), ignore_index=True)
            newlines.append(lines[line])
    # print(newlines)
    x = []
    y = []
    z = []
    g = []
    f = []
    for line in range(0,len(newlines)):
        # print(newlines[line])
        temp=str.split(newlines[line],',')
        
        if scores_index == 5:
            # scores.append([temp[scores_index-3],temp[scores_index-2],temp[scores_index-1],temp[scores_index]])
            if float(temp[5])>=limit:
                continue
            else:
                # print(newlines[line])
                # print(temp)
                x.append(temp[2])
                y.append(temp[3])
                z.append(temp[4])
                f.append(temp[5])
        else:
            # scores.append([temp[scores_index-4],temp[scores_index-3],temp[scores_index-2],temp[scores_index-1],temp[scores_index]])
            if float(temp[6])>=limit:
                continue
            else:
                x.append(temp[2])
                y.append(temp[3])
                z.append(temp[4])
                g.append(temp[5])
                f.append(temp[6])
    if scores_index == 5:
        # print([x,y,z,f])
        # print(len(x))
        return json.dumps([x,y,z,f])
    else:
        # print([x,y,z,g,f])
        return json.dumps([x,y,z,g,f])


def getindividuals(id):
    n = []
    k1 = []
    k2 = []
    k3 = []
    k4 = []
    score = []
    geta = []
    g = glob.glob("../experiments/"+id+"/figures/*ki_values.tsv")
    for file in g:
        fh = open(file)
        tmp = fh.readlines()
        fh.close()
        temp=str.split(tmp[1],'\t')
        if len(temp)==4:
            n.append(str.replace(str.replace(file,"../experiments/"+id+"/figures/",""),"ki_values.tsv",""))
            k1.append(temp[1])
            k2.append(temp[2])
            k3.append(temp[3])
            tmp2 = [temp[1],temp[2],temp[3]]
            score.append(getindscore(id,temp[1],temp[2],temp[3]))
            geta.append("<input type=\"submit\" id=\"" + str.replace(str.replace(file,"../experiments/"+id+"/figures/","") \
                ,"ki_values.tsv","") + "\" value=\"PNG\" onclick=\"getpng(this.id," + str(tmp2) + ")\">" + \
                 "<input type=\"submit\" id=\"" + str.replace(str.replace(file,"../experiments/"+id+"/figures/",""),"ki_values.tsv","") \
                  + "\" value=\"CSV\" onclick=\"getcsv(this.id)\">")
            return json.dumps([n,k1,k2,k3,score,geta])

        elif len(temp)==5:
            n.append(str.replace(str.replace(file,"../experiments/"+id+"/figures/",""),"ki_values.tsv",""))
            k1.append(temp[1])
            k2.append(temp[2])
            k3.append(temp[3])
            k4.append(temp[4])
            tmp2 = [temp[1],temp[2],temp[3],temp[4]]
            score.append(getindscore(id,temp[1],temp[2],temp[3],temp[4]))
            geta.append("<input type=\"submit\" id=\"" + str.replace(str.replace(file,"../experiments/"+id+"/figures/","") \
                ,"ki_values.tsv","") + "\" value=\"PNG\" onclick=\"getpng(this.id," + str(tmp2) + ")\">" + \
                 "<input type=\"submit\" id=\"" + str.replace(str.replace(file,"../experiments/"+id+"/figures/",""),"ki_values.tsv","") \
                  + "\" value=\"CSV\" onclick=\"getcsv(this.id)\">")
            return json.dumps([n,k1,k2,k3,k4,score,geta])

    


def getindscore(id, k1, k2, k3):
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
        if not (k1 in lines[line] and k2 in lines[line] and k3 in lines[line]):
            continue
        else:
            lines[line] = lines[line].replace(' ','')
            lines[line] = lines[line].replace('[','')
            lines[line] = lines[line].replace('],(',',')
            lines[line] = lines[line].replace(',)','')
            # df = df.append(str.split(lines[line],','), ignore_index=True)
            return str.split(lines[line],',')[score_index]
    # print(newlines)
    # print(finallines)
    # return json.dumps(finallines)
