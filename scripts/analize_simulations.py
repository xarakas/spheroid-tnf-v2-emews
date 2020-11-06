import pandas as pd
import os
import glob

fname = "time_course.tsv"

count = 0
good = 0
not_bad = 0
alive_count = []
for i in glob.glob("./instance_*/"):
    if not os.path.isfile(i + fname):
        continue
    count += 1
    df = pd.read_csv(i + fname, sep='\t')
    alive_s = df.alive.iloc[0]
    alive_e = df.alive.iloc[-1]
    if alive_e < alive_s:
        not_bad += 1
        print(i, alive_s, alive_e)
    if alive_e < 300:
        good += 1
    alive_count.append(alive_e)
print(count, not_bad, good)
for i in np.logspace(0,5,num=5):
    print("Talive < %.2e : %i" % (i, (alive_count<i).sum()))
