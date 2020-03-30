import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

req = Request('https://www.worldometers.info/coronavirus/country/south-korea/', headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()

f = open('html.txt', 'w', encoding = 'utf-8')
content = html.decode(encoding = 'utf-8')
f.write(content)
f.close()
soup = BeautifulSoup(html, 'html.parser')

rawdata = soup.get_text().strip()

f = open('rawdata.txt', 'w')
f.write(re.sub(r'\s$', '', rawdata, flags=re.MULTILINE))
f.close()

dataList = []
with open('rawdata.txt', 'rt') as f:
    flag = 0
    for l in f:
        if flag:
            dataList.append(l.strip())
            break
        if l == '        xAxis: {\n':
            flag = 1

lineList = []
with open('rawdata.txt', 'rt') as myfile:
    for line in myfile:
        lineList.append(line)



for _ in range(len(lineList)):
    if lineList[_].strip() == "name: 'New Recoveries',":
        dataList.append('New Recoveries')
        dataList.append(lineList[_ + 4].strip())
    if lineList[_].strip() == "name: 'New Cases',":
        dataList.append('New Cases')
        dataList.append(lineList[_ + 3].strip())
    if lineList[_].strip() == "name: 'Daily Deaths',":
        dataList.append('Daily Deaths')
        dataList.append(lineList[_ + 3].strip())

for _ in range(len(dataList)):
    if (_ % 2 == 0 and _ != 0):
        dataList[_] = (dataList[_].split()[1])


temp = dataList[0].split()
temp[0] = 'Dates\n'
dataList[0] = ''.join(i for i in temp)


with open('data.csv', 'w') as myfile:
    for line in dataList:
        myfile.write(line)
        myfile.write('\n')
