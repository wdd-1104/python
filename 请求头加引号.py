import re

headers_str = '''
pageNo: 1
pageSize: 15
ipAddress: 119.57.164.251
count: 450
searchword: 
searchword2: 
hotword: 
provinceId: 1
provinceName: 安徽
areaId: 34
areaName: 巢湖
infoType: 2
infoTypeName: 中标
noticeTypes: 
noticeTypesName: 
secondInfoType: 1
secondInfoTypeName: 采购中标
timeType: 0
timeTypeName: 
searchType: 2
clearAll: false
e_keywordid: 
e_creative: 
flag: 0
source: 360so
firstTime: 1
'''

pattern = '^(.*?): (.*)$'
for i in headers_str.splitlines():
    print(re.sub(pattern,'\'\\1\': \'\\2\',',i))