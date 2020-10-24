from glob import glob
import json
import sys
import os

cwd = os.getcwd()

os.chdir('/Users/griffin/Dropbox/_Courses/5443-Spatial-Data-Structures/Data/plane_crashes')

files = glob("./crash_data/*.json")

sum = 0
for f in files:
    data = json.loads(open(f).read())
    sum += len(data)

print(sum)
