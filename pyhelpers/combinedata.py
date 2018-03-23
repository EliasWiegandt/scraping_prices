import glob
import os
import csv
import pandas as pd
import datetime

base_dir = "H:/HBS Data/Crawlers/pricebot/pricedata/"
pattern = '*/*'

now = datetime.datetime.now()
date = now.strftime("%Y%m%d")

frame = pd.DataFrame()
df_list = []

for pathAndFilename in glob.glob(os.path.join(base_dir, pattern)):
    with open(pathAndFilename) as f:
        df = pd.read_csv(f, index_col=None, header=0)
        df_list.append(df)
frame = pd.concat(df_list).reset_index(drop=True)

name = "prices_%s.csv" % (date)
frame.to_csv(base_dir + name, sep=",")
