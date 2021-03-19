import json

data = json.load(open('bjjt_totle.json', 'r'))
resource_data = json.load(open('data.json', 'r', encoding='utf-8'))
clear_data = {}
for key in data.keys():
    i = 1
    while i <= data[key]: 
        data_key = '{}_{}'.format(key,str(i))
        clear_data[data_key] = resource_data[data_key]
        i += 1

with open('data2.json', 'w+', encoding='utf-8') as f:
    json.dump(clear_data, f, ensure_ascii=False)