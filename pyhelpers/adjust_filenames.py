import glob
import os

base_dir = "H:/HBS Data/Crawlers/pricebot/websitehistory/"
pattern = '*'
name_list = [
    'bilka', 'elgiganten', 'power', 'punkt1', 'skousen', 'whiteaway', 'wupti'
]

for name in name_list:
    dir = base_dir + name
    for pathAndFilename in glob.glob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        first_letter = title[0]
        new_title = first_letter.lower() + title[1:]
        os.rename(pathAndFilename, os.path.join(dir, new_title + ext))
