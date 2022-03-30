a = [{'en': 888, 'tl': 4, 'ht': 17, 'ja': 6, 'ca': 3, 'es': 5, 'in': 6, 'ro': 6, 'et': 5, 'sv': 1, 'da': 2, 'it': 5, 'nl': 2, 'ko': 1, 'de': 2, 'fr': 3, 'cy': 1, 'und': 7, 'cs': 1, 'pl': 1, 'no': 1, 'pt': 2}, {'en': 450, 'in': 1, 'de': 1, 'it': 2, 'es': 1, 'tr': 1, 'ja': 8, 'nl': 1, 'fr': 1, 'pt': 3, 'und': 1}, {'en': 80, 'tr': 2, 'es': 1, 'fr': 2}, {'en': 154, 'es': 1, 'et': 1, 'pt': 1, 'und': 2, 'th': 1, 'tl': 1, 'ca': 1}, {'en': 4186, 'pt': 15, 'ro': 11, 'ja': 56, 'ca': 24, 'es': 42, 'zh': 13, 'in': 32, 'tl': 13, 'und': 42, 'th': 8, 'fr': 8, 'tr': 5, 'it': 9, 'sv': 3, 'nl': 6, 'et': 7, 'cy': 3, 'da': 5, 'pl': 3, 'de': 12, 'cs': 2, 'ar': 2, 'vi': 4, 'ko': 4, 'ht': 2, 'fi': 1, 'fa': 1, 'bn': 1, 'no': 1, 'hu': 1}, {'en': 611, 'zh': 5, 'ca': 2, 'ro': 4, 'ja': 5, 'es': 3, 'in': 5, 'pt': 3, 'tl': 1, 'und': 1, 'da': 1, 'th': 1, 'de': 1}, {'en': 9, 'th': 1, 'in': 1}, {'en': 31, 'es': 2}, {'en': 84, 'es': 2, 'in': 6, 'zh': 1, 'ro': 1, 'und': 2, 'fr': 1}, {'en': 481, 'und': 4, 'de': 2, 'it': 4, 'ja': 3, 'pt': 1, 'tl': 2, 'zh': 5, 'fi': 1, 'es': 1, 'hi': 1, 'et': 1, 'in': 1}, {'en': 21, 'ja': 1, 'und': 1}, {'en': 90, 'pt': 2, 'und': 1, 'cy': 2, 'es': 1, 'ca': 1, 'lt': 1}, {'en': 42, 'de': 1, 'und': 1, 'fr': 2, 'ht': 1}, {'en': 179, 'tl': 2, 'da': 1, 'ca': 1, 'ht': 1}, {'fr': 1, 'en': 20}, {'en': 3}]
f = open('input.txt','r')
code2name = {'en': 'English', 'ar': 'Arabic', 'bn': 'Bengali', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'es': 'Spanish', 'fa': 'Persian', 'fi': 'Finnish', 'fil': 'Filipino', 'fr': 'French', 'he': 'Hebrew', 'hi': 'Hindi', 'hu': 'Hungarian', 'in': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'msa': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sv': 'Swedish', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-cn': 'Chinese(Simplified)', 'zh-tw': 'Chinese(Traditional)','cy':'Welsh','ht':'Haitian','zh':'Chinese'}
print('Cell     #Total Tweets   #Number of Languages Used    #Top 10 Languages & #Tweets')
for i in range(0,16):
    total_language = 0
    total_t = 0
    t_lan = []
    for j in a[i]:
        if j == 'und' or j == None:
            continue
        total_language+=1
        total_t+=a[i][j]
        t_lan.append((a[i][j],j))
    t_lan.sort(reverse=True)
    t_lan = t_lan[:10]
    code_to_name = []
    for j in t_lan:
        temp = code2name.get(j[1])
        if temp == None:
            temp = j[1]
        code_to_name.append((temp,j[0]))
    print(i,'      ',total_t,'                  ',total_language,'                     ',code_to_name)
    
