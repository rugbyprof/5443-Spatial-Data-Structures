from bs4 import BeautifulSoup
import requests
from time import sleep
import json 

years = [x for x in range(1921,2021)]

# counts = []
# for year in years:
#     print(year,end=" ",flush=True)
#     r = requests.get(f"http://www.planecrashinfo.com/{str(year)}/{str(year)}.htm")
#     if r.status_code == 200:
#         soup = BeautifulSoup(r.text, 'html.parser')

#         table = soup.find('table')

#         # trs = table.findall('tr')
#         count = 0
#         for row in table.find_all('tr'):
#            for td in row.find_all('td'):
#                 for link in td.find_all('a'):
#                     count += 1
#         counts.append(count)
#         print(counts,end=" ",flush=True)
#     sleep(.2)

# print("")
# keys = ['Date','Time','Location','Operator','Flight','Route','Type','Registration','Aboard','Fatalities','Ground','Summary']

with open("detail_counts.json","r") as f:
    counts = json.loads(f.read())

j = 1
for year in years:
    results = []
    print(year,end=" ",flush=True)
    for i in range(1,counts[j]+1):
        print(i,end=" ",flush=True)
        r = requests.get(f"http://www.planecrashinfo.com/{str(year)}/{str(year)}-{i}.htm")
        if r.status_code == 200:

            soup = BeautifulSoup(r.text, 'html.parser')

            table = soup.find('table')
            rows = table.find_all('tr')
            details = {'year':year,'count':i}
            for row in rows:
                key = row.contents[1].text.strip()
                key = ' '.join(key.split())
                key = key[:-1]
                val = row.contents[3].text.strip()
                val = ' '.join(val.split())
                if key == "":
                    continue
                details[key] = val
            results.append(details)
            sleep(.3)
    j += 1
    
    print("")
    with open(f"./crash_data/{year}_data.json","w") as out:
        out.write(json.dumps(results,indent=4))
