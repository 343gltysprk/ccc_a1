import json
import sys
from mpi4py import MPI
import time
import math

#this function read the coordinates of each grid
def read_grids(file_path):
    f = open(file_path,'r')
    grids = json.load(f)
    coordinates = []
    grid_id = []
    for i in grids['features']:
        #print(i['geometry']['coordinates'][0])
        coordinates.append(i['geometry']['coordinates'][0])
        grid_id.append(i['properties'])
    return coordinates,grid_id

#read n tweets
def read_tweets(file,n):
    output = []
    for i in range(0,n):
        tweet = file.readline().strip()
        if len(tweet)<1 :
            #skip blank line
            continue
        if tweet[-1] == ',':
            output.append(tweet[:-1])
        else:
            output.append(tweet[:-2])
    return output
    
#combine the results of each chunk of data
def update_lang(main,new):
    for i in range(0,len(main)):
        for j in new[i]:
            if j in main[i]:
                main[i][j]+=new[i][j]
            else:
                main[i][j]=new[i][j]
    return main    

#point inside the area
def inside(point,box):
    if point[0]>=box[0][0] and point[0]<=box[2][0] and point[1]>=box[2][1] and point[1]<=box[0][1]:
        return True
    return False

#the task each node work on
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
            for j in range(0,length):
                if inside(point,grid[j]) is True:
                    language = temp['doc']['lang']
                    if (language == 'zh-tw') or (language == 'zh-cn'):
                        language = 'zh'
                    valid[j].append(language)
                    break
    #count valid langauge in the area
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


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#language code to name mapping
code2name = {'en': 'English', 'ar': 'Arabic', 'bn': 'Bengali', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'es': 'Spanish', 'fa': 'Persian', 'fi': 'Finnish', 'fil': 'Filipino', 'fr': 'French', 'he': 'Hebrew', 'hi': 'Hindi', 'hu': 'Hungarian', 'in': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'msa': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sv': 'Swedish', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-cn': 'Chinese(Simplified)', 'zh-tw': 'Chinese(Traditional)','cy':'Welsh','ht':'Haitian','zh':'Chinese'}

#read grid information and id, not necessary sydney's grids
sydgrid,grid_id = read_grids(sys.argv[1])

#read first line of twitter,get general information
twitter = open(sys.argv[2],'r',errors='ignore')
first = twitter.readline().strip()
first = first[:-1]
first += '0}'
total_row = json.loads(first)['total_rows']
offset = 0
try:
    offset = json.loads(first)['offset']
    total_row -= offset
except:
    offset = 0
    
total_row -= 1 #first line has been read

main_dict = []
for i in range(0,len(sydgrid)):
    main_dict.append({})

#read file with rank0, then scatter the data and compute
while total_row>0:
    comm.Barrier()
    chunk = 1000
    data = []
    if rank == 0:
        for i in range(size):
            tweets = []
            if total_row>chunk:
                tweets = read_tweets(twitter,chunk)
                total_row-=chunk
            else:
                tweets = read_tweets(twitter,total_row)
                total_row=0
            data.append(tweets)
    else:
        data = []
        total_row-=(chunk*size)
    comm.Barrier()
    data = comm.scatter(data, root=0)
    lang = get_language(data,sydgrid)
    main_dict = update_lang(main_dict,lang)

#gather result
main_dict = comm.gather(main_dict,root=0)
if rank == 0:
    for i in range(1,size):
        main_dict[0] = update_lang(main_dict[0],main_dict[i])
    print('Cell     #Total Tweets   #Number of Languages Used    #Top 10 Languages & #Tweets')
    for i in range(len(sydgrid)):
        total_language = 0
        total_t = 0
        t_lan = []
        for j in main_dict[0][i]:
            if j == 'und' or j == None:
                continue
            total_language+=1
            total_t+=main_dict[0][i][j]
            t_lan.append((main_dict[0][i][j],j))
        t_lan.sort(reverse=True)
        t_lan = t_lan[:10]
        code_to_name = []
        for j in t_lan:
            temp = code2name.get(j[1])
            if temp == None:
                temp = j[1]
            code_to_name.append((temp,j[0]))
        print(grid_id[i],'      ',total_t,'                  ',total_language,'                     ',code_to_name)












