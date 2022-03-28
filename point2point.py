#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
#this function read the coordinates of each grid

    


# In[51]:


# 读取json文件
twitter = open('smallTwitter.json','r',errors='ignore')
first = twitter.readline().strip()
print(first)
first = first[:-1]
first += '0}'
print(first)
total_row = json.loads(first)['total_rows']
total_row -= 1


# In[3]:


total_row


# In[11]:


# 读取网格规划图
def read_grids(file_path):
    f = open(file_path,'r')
    grids = json.load(f)
    coordinates = []
    for i in grids['features']:
        print(i['geometry']['coordinates'][0])
        coordinates.append(i['geometry']['coordinates'][0])
    return coordinates


# In[12]:


sydgrid = read_grids('sydGrid.json')


# In[14]:


main_dict = []
for i in range(0,len(sydgrid)):
    main_dict.append({})


# In[4]:


#read n tweets
def read_tweets(file,n):
    output = []
    for i in range(0,n):
        tweet = file.readline().strip()
        if tweet[-1] == ',':
            output.append(tweet[:-1])
        else:
            output.append(tweet[:-2])
    return output


# In[6]:


tweets = read_tweets(twitter,total_row)


# In[7]:


def get_language(tweet,grid):
    valid = []
    length = len(grid)
    for i in range(0,length):
        valid.append([])
    for i in tweet:
        try:
            temp = json.loads(i)
        except:
            continue
        if temp['doc']['coordinates'] != None:
            point = temp['doc']['coordinates']['coordinates']
            print(point)
            for j in range(0,length):
                if inside(point,grid[j]) is True:
                    valid[j].append(temp['doc']['lang'])
                    break
    lang_count = []
    for i in range(0,len(valid)):
        lang_dict = {}
        for j in valid[i]:
            if j in lang_dict:
                lang_dict[j]+=1
            else:
                lang_dict[j]=1
        lang_count.append(lang_dict)
    return lang_count


# In[8]:


#master node, combine all result
def update_lang(main,new):
    for i in range(0,len(main)):
        for j in new[i]:
            if j in main[i]:
                main[i][j]+=new[i][j]
            else:
                main[i][j]=new[i][j]
    return main


# In[9]:


def inside(point,box):
    if point[0]>=box[0][0] and point[0]<=box[2][0] and point[1]>=box[2][1] and point[1]<=box[0][1]:
        return True
    return False


# 
# #tweets = []
# lang = []
# #tweets = read_tweets(twitter,total_row)
#  
# lang = get_language(tweets,sydgrid)
# main_dict = update_lang(main_dict,lang)
# print(main_dict)

# In[30]:


from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()


# In[ ]:


#命令行执行
#mpiexec -n 8 python filename.py
#mpirun -n 8 python3 filename.py


# In[31]:


print('We got process {} out of {}'.format(rank, nprocs))


# In[36]:


len(tweets)


# In[48]:


if rank == 0:
    data = tweets
    data_len = len(tweets)
    # master拆分发送data到所有的slave
    print('Process {} sent data:'.format(rank), len(data))
    for i in range(1, size):
        #按比例拆分
        each_procs = data_len%size
        j = 0
        comm.send(data[j:j+each_procs], dest=i, tag=i)
        j = j+each_procs
        

# slave收到master的数据
else:
    data = comm.recv(source=0, tag=rank)
    print('Process {} received data:'.format(rank), len(data))


# # 
# if rank == 0:
# 
#     sendbuf = np.arange(float(total_row))
#     ave, res = divmod(sendbuf.size, nprocs)
#     #  number of element in each procs
#     count = [ave + 1 if p < res else ave for p in range(nprocs)]
#     count = np.array(count)
# 
#     # starting point of each procs 
#     displ = [sum(count[:p]) for p in range(nprocs)]
#     displ = np.array(displ)
# else:
#     sendbuf = None
#     count = np.zeros(nprocs, dtype=np.int)
#     displ = None
# 
# comm.Bcast(count, root=0)
# 
# 
# recvbuf = np.zeros(count[rank])
# 
# comm.Scatterv([sendbuf, count, displ, MPI.DOUBLE], recvbuf, root=0)
# 
# print('After Scatterv, process {} has data:'.format(rank), recvbuf)

# In[49]:



#tweets = []
lang = []
#tweets = read_tweets(twitter,total_row)
 
lang = get_language(tweets,sydgrid)
main_dict = update_lang(main_dict,lang)
print(main_dict)

