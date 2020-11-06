count = 0
for i in glob.glob("./instance_*/"):
    if not os.path.isfile(i + fname):
        continue
    count += 1
    df = pd.read_csv(i + fname, sep='\t')
    alive_s = df.alive.iloc[0]
    alive_e = df.alive.iloc[-1]
    if alive_e < alive_s:
        print(i, alive_s, alive_e)

print(count)
