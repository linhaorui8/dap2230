

import re

line = "this hdr-biz 123 model server 456"
pattern = r"123"
matchObj = re.match(pattern, line)
print(matchObj)

import re

line = "this hdr-biz model server"
pattern = r"hdr-biz"
m = re.search(pattern, line)
print(m)

import re

line = "this hdr-biz model args= server"
patt = r'server'
pattern = re.compile(patt)
result = pattern.findall(line)
if result:
    print(True)
print(result)

id = [1,2,3]
for i in range(len(id)):
    print(id[i])

