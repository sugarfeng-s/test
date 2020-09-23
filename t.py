import json
import numpy as np
# load_f =  open("./1.txt",'r',encoding='utf-8')
# papers = []
# for line in load_f.readlines():
#     line=line[:-1]
#     temp_list = line.split(' ',line.count(' '))
#     for i in temp_list:
#         papers.append(int(i))
# print(sorted(papers))
#     # for i in temp_list:

# papers=papers[0]
# for i in range(0,3):
#     for paper in papers:
#         if str(i) == list(paper.keys())[0]:
#             print(paper[str(i)])
print('input score')
score = float(input())
assert(score>=0)
assert(score<=100)
if score>=0 and score<25:
    print('D')
elif score>=25 and score<50:
    print('C')
elif score>=50 and score<75:
    print('B')
elif score>=75 and score<100:
    print('A')


