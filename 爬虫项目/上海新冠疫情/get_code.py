import json
f = open('local.json',encoding='utf-8') #打开json文件
res = f.read()
temp = json.loads(res)
num = 1
code_list = []
for j in temp:
    tt = j
    if not(tt['result']['level'] == '区县' or tt['result']['level'] == 'UNKNOWN'):
        lng = tt['result']['location']['lng']
        lat = tt['result']['location']['lat']
        address = tt['address']
        str_point = 'var point'+str(num)+' = new BMapGL.Point('+str(lng)+','+str(lat)+');'
        str_marker = 'var marker'+str(num)+' = new BMapGL.Marker(point'+str(num)+');'
        str_add_marker = 'map.addOverlay(marker'+str(num)+');'
        str_infoWindow = 'var infoWindow'+str(num)+' = new BMapGL.InfoWindow('+"'"+address+"'"+',opts);'
        str_Listerener = 'marker'+str(num)+'.addEventListener('+"'click'"+',function(){map.openInfoWindow(infoWindow'+str(num)+',point'+str(num)+');});'
        #print(str_point)
        #print(str_marker)
        #print(str_add_marker)
        #print(str_infoWindow)
        #print(str_Listerener)
        num+=1
        code_list.append(str_point)
        code_list.append(str_marker)
        code_list.append(str_add_marker)
        code_list.append(str_infoWindow)
        code_list.append(str_Listerener)
with open('js_code.txt','w',encoding='UTF-8') as f:
    for i in code_list:
        f.write(i)