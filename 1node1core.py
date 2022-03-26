import json
import sys

#this function read the coordinates of each grid
def read_grids(file_path):
    f = open(file_path,'r')
    grids = json.load(f)
    coordinates = []
    for i in grids['features']:
        #print(i['geometry']['coordinates'][0])
        coordinates.append(i['geometry']['coordinates'][0])
    return coordinates

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
    
#master node, combine all result
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

sydgrid = read_grids(sys.argv[1])

twitter = open(sys.argv[2],'r',errors='ignore')
first = twitter.readline().strip()
first = first[:-1]
first += '0}'
total_row = json.loads(first)['total_rows']
total_row -= 1 #first line has been read

main_dict = []
for i in range(0,len(sydgrid)):
    main_dict.append({})


while total_row>0:
    tweets = []
    lang = []
    if total_row>1000:
        tweets = read_tweets(twitter,1000)
        total_row-=1000
    else:
        tweets = read_tweets(twitter,total_row)
        total_row=0
    lang = get_language(tweets,sydgrid)
    main_dict = update_lang(main_dict,lang)
print(main_dict)



















