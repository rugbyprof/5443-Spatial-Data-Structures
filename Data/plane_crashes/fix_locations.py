import json
import glob 
import os

base_path = '/Users/griffin/Dropbox/_Courses/5443-Spatial-Data-Structures/Data/'

crash_files = glob.glob(os.path.join(base_path,"plane_crashes/crash_data/*.json"))

with open(os.path.join(base_path,"countries_states/country-json/country-by-name.json")) as f:
    countries = json.loads(f.read())
    
with open(os.path.join(base_path,"countries_states/states.json")) as f:
    states = json.loads(f.read())

CRASHES = []
locations = []
terms = []
found = []

count = 0

for cfile in crash_files:
    data = json.loads(open(cfile,'r').read())
    CRASHES.extend(data)

letters = "abcdefghijklmnopqrstuvwxyz "


fixed = {}

for crash in CRASHES:
    if not crash['year'] in fixed:
        fixed[crash['year']] = []

    fixed[crash['year']].append(crash)

    loc = crash['Location']
    newloc = ""
    for l in loc:
        if l.lower() in letters:
            newloc += l

    for country in countries:
        
        if country['country'].lower() in loc.lower():
            fixed[crash['year']][-1]['Country'] = country['country']
        elif 'alias' in country:
            for alias in country['alias']:
                if alias.lower() in loc.lower():
                    fixed[crash['year']][-1]['Country'] = country['country']


    for s in states:
        if s['name'].lower() in loc.lower():
            fixed[crash['year']][-1]['State'] = s['name']
            fixed[crash['year']][-1]['Country'] = 'United States'

        # elif not 'Country' in fixed[crash['year']][-1] and s['abbreviation'].lower() in loc.lower():
        #     fixed[crash['year']][-1]['State'] = s['name']
        #     fixed[crash['year']][-1]['Country'] = 'United States'

    # words = l.split()
    # for word in words:
    #     if not word in terms:
    #         terms.append(word)
    #     for country in countries:
            
    #         if word.lower() in country['name'].lower():
    #             fixed[crash['year']][-1]['Country'] = country['name']


# has = 0
# total = 0
# for crash in CRASHES:
#     if 'Country' in crash:
#         has += 1
#     else:
#         print(crash)
#     total += 1

# print(has)
# print(total)

with open('crash_data_fixed.json','w') as f:
    f.write(json.dumps(fixed,indent=4))

missed = []

with open('crash_data_fixed.json') as f:
    data = json.loads(f.read())

count = 0
total = 0
for year in data:
    for d in data[year]:
        if 'Country' in d:
            count += 1
        else:
            missed.append(d)
        total += 1

for m in missed:
    print(m)

with open('crash_data_missed.json','w') as f:
    f.write(json.dumps(missed,indent=4))

with open('crash_data_missed_summary.txt','w') as f:
    for m in missed:
        f.write(f"{m['year']} : {m['Location']} : {m['Route']}\n")
    
print(len(missed))
print(count)
print(total)