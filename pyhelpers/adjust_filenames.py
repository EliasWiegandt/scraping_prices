import glob
import os

base_dir = "H:/HBS Data/Crawlers/pricebot/pricedata_test/"
pattern = '*/*'

dir = base_dir

for pathAndFilename in glob.glob(os.path.join(dir, pattern)):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    # print(pathAndFilename)
    # first_letter = title[0]
    # new_title = first_letter.lower() + title[1:]
    new_title = title.replace("_prices_", "_")
    new_pathAndFilename = os.path.join(pathAndFilename, new_title + ext)
    new_pathAndFilename = new_pathAndFilename.replace("\\", "/")
    print(new_pathAndFilename)
    # os.rename(pathAndFilename, os.path.join(pathAndFilename, new_title + ext))
