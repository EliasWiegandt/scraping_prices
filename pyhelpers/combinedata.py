import glob
import os

base_dir = "H:/HBS Data/Crawlers/pricebot/pricedata_test/"
pattern = '*/*'
name_list = [
    'bilka', 'elgiganten', 'power', 'punkt1', 'skousen', 'whiteaway', 'wupti'
]

for pathAndFilename in glob.glob(os.path.join(base_dir, pattern)):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    print(pathAndFilename)
