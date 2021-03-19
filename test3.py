import fileinput
import json
data = []

with fileinput.input(files='bjjt.log') as f:
    for line in f:
        url = r'https://api.cntv.cn/NewVideo/getVideoListByColumn?id=TOPC1451557052519584&n=20&sort=desc&p={}&mode=0&serviceId=tvcctv&d={}'
        line = line.replace('\n', '').replace('error info key:','').replace('paging:', '')
        list = line.split('  ')
        url = url.format(list[1].replace(' ', ''),list[0])
        data.append({list[0]+'_'+list[1].replace(' ', ''):{}})
        with open('url.txt', 'a+') as f:
            f.write(list[0]+'_'+list[1].replace(' ', '')+'\n')
            f.write(url+'\n')
with open('bjjt_info3.json', 'w+') as f:
    json.dump(data, f)