import requests
import json
import os
import execjs

from requests.packages import urllib3

urllib3.disable_warnings()

query = input('Input query...\n')
#query = 'happy'

with open(r'sign_func.js', 'r', encoding='utf-8') as f:
    ctx = execjs.compile(f.read())

sign = ctx.call('e', query)

#print(sign)

def colorFormat(string,color):
    if color == 'green':
        return '\033[32m'+string+'\033[0m'
    if color == 'blue':
        return '\033[34m'+string+'\033[0m'
    if color == 'red':
        return '\033[31m'+string+'\033[0m'
    if color == 'yellow':
        return '\033[33m'+string+'\033[0m'
    if color == 'cyan':
        return '\033[36m'+string+'\033[0m'

parms = {
    'from': 'en',
    'to': 'zh',
    'query': query,
    # 'transtype': 'realtime',
    # 'simple_means_flag': 3,
    'sign': sign,
    'token': '89c45df3fa96182536ebe95c4d600662',
    # 'token': '3733199e9e43abb34bcf7949a81a96fc',
    # 'domain': 'common'
}


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
    'Host': 'fanyi.baidu.com',
    'Connection': 'keep-alive',
    'Content-Length': '134',
    'Accept': '*/*',
    'DNT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded;charset = UTF-8',
    'Origin': 'https://fanyi.baidu.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://fanyi.baidu.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US, en;q = 0.9, zh-CN;q = 0.8, zh;q = 0.7, sl;q = 0.6, ja;q = 0.5, es;q = 0.4',
    'Cookie': 'BAIDUID=0F94C5139F9BAE72C26E8926EB899A44:FG=1; BIDUPSID=0F94C5139F9BAE72C26E8926EB899A44; PSTM=1563287630; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_SPD_SWITCH=1; HISTORY_SWITCH=1; SOUND_PREFER_SWITCH=1; BDUSS=FZQ0VhSFNrdkpKb1lkT1d0M1FKdkRIUEIxQ3BJMkUyOWtTckgyQjBXT1NFaGhnRVFBQUFBJCQAAAAAAAAAAAEAAACKAd6bU2FtZHlTbm93AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKF8F-ShfBfNV; BDUSS_BFESS=FZQ0VhSFNrdkpKb1lkT1d0M1FKdkRIUEIxQ3BJMkUyOWtTckgyQjBXT1NFaGhnRVFBQUFBJCQAAAAAAAAAAAEAAACKAd6bU2FtZHlTbm93AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKF8F-ShfBfNV; BAIDUID_BFESS=0F94C5139F9BAE72C26E8926EB899A44:FG=1; __yjs_duid=1_b0a28cd6865cedbf3261d45a2639362a1615269123655; H_PS_PSSID=33511_33257_33273_31253_33693_33594_33570_33618_33590_26350; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=3; BA_HECTOR=04042k85a50ga020j31g4ohbq0r; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1615611260; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1615611260; __yjsv5_shitong=1.0_7_9cd58b90fb36c37b3649a3e7858844abfe70_300_1615611263631_112.10.131.225_714f98e7; ab_sr=1.0.0_MGUyY2UwMjBmZTNmNzVlOThjOWFjYmJkOWMyZmIzZjVhYzZlNzI1ZmI0YTFhNzk0MDFkZWVlOThhZTQzZTUzNzkwMmIxOTAwZjgyMTRmZmZjN2EwODU3Njk0MzQ0Yzg5'
}

url = 'https://fanyi.baidu.com/v2transapi'

print('\nSending Requests to Baidu Translate Sever Host...')


response = requests.post(url= url, data= parms, headers= headers,verify=False)

#print(response.status_code)

if(response.status_code == 200):
    print("Status Code: \033[32m●\033[0m 200 Host %s\n"%colorFormat('Online','green'))
#print(response.json())

def isWord(string):
    for i in range(len(string)):
        if string[i] == ' ':
            return False
    return True


def dataAna_trans_result(dict):

    trans_result = dict['trans_result']

    #print(trans_result)
    #print(type(trans_result))

    data = trans_result['data']
    data_dict = data[0]
    src = data_dict['src'] #Ori
    dst = data_dict['dst'] #Trans Result

    print('Query        : %s'%colorFormat(src,'green'))
    print('Trans_result : %s'%colorFormat(dst,'green'))

    phonetic_list = trans_result['phonetic']
    s = ''
    for i in phonetic_list:
        s = s + i['trg_str'] + ' '
    print('Phonetic     : %s'%colorFormat(s,'green'))

def print_word_exchange(exchange_dict):

    print(colorFormat('Word_Exchanges :','cyan'))

    if exchange_dict.__contains__('word_third'):
        s = exchange_dict['word_third']
        word = ''
        for i in s[0:-1]:
            word += i + ','
        word += s[-1]
        print('  --> %s: %s' % (colorFormat('Third Person Singular ','blue'),
                                colorFormat(word, 'green'),))

    if exchange_dict.__contains__('word_ing'):
        s = exchange_dict['word_ing']
        word = ''
        for i in s[0:-1]:
            word += i + ','
        word += s[-1]
        print('  --> %s: %s' % (colorFormat('Present Progressive   ', 'blue'),
                                colorFormat(word, 'green'),))
    
    if exchange_dict.__contains__('word_past'):
        s = exchange_dict['word_past']
        word = ''
        for i in s[0:-1]:
            word += i + ','
        word += s[-1]
        print('  --> %s: %s' % (colorFormat('Simple Past           ', 'blue'),
                                colorFormat(word, 'green'),))

    if exchange_dict.__contains__('word_done'):
        s = exchange_dict['word_done']
        word = ''
        for i in s[0:-1]:
            word += i + ','
        word += s[-1]
        print('  --> %s: %s' % (colorFormat('Pluperfect            ', 'blue'),
                                colorFormat(word, 'green'),))

    if exchange_dict.__contains__('word_pl'):
        s = exchange_dict['word_pl']
        word = ''
        for i in s[0:-1]:
            word += i + ','
        word += s[-1]
        print('  --> %s: %s' % (colorFormat('Plural                ', 'blue'),
                                colorFormat(word, 'green'),))
    
    if exchange_dict.__contains__('word_er'):
        s = exchange_dict['word_er']
        word = ''
        for i in s[0:-1]:
            word += i + ','
        word += s[-1]
        print('  --> %s: %s' % (colorFormat('Comparative           ', 'blue'),
                                colorFormat(word, 'green'),))
    
    if exchange_dict.__contains__('word_est'):
        s = exchange_dict['word_est']
        word = ''
        for i in s[0:-1]:
            word += i + ','
        word += s[-1]
        print('  --> %s: %s' % (colorFormat('Superlative           ', 'blue'),
                                colorFormat(word, 'green'),))

def printUsecase(usecase_dict):

    if usecase_dict.__contains__('collocation'):

        print(colorFormat('Word_Usecase :','cyan'))
        print('  --> %s'%colorFormat('Word_with_Listed_Part_of_Speech :','cyan'))

        collocation_dict = usecase_dict['collocation']
        data_list = collocation_dict['data']

        for data_dict in data_list:
            print('    --> %s'%colorFormat(data_dict['p'],'blue'))
            ex_list = data_dict['ex']
            for ex_dict in ex_list:
                print('      --> %s'%colorFormat(ex_dict['en'],'green'))
                print('      --> %s'%colorFormat(ex_dict['zh'],'yellow'))

    


def printSanyms(sanyms_list):
        print(colorFormat('Synonyms_and_Antonyms :','cyan'))

        for sanyms_dict in sanyms_list:
            if sanyms_dict['type'] == 'synonym':
                print('  --> %s :'%colorFormat('Synonym','yellow'))
                data_list = sanyms_dict['data']

                for data_dict in data_list:
                    output = colorFormat(data_dict['p'] + ' ','blue')

                    for i in data_dict['d']:
                        output += colorFormat(i + ', ','green')
                    
                    print('    --> %s'%output)

            if sanyms_dict['type'] == 'antonym':
                print('  --> %s :' % colorFormat('Antonym', 'yellow'))
                data_list = sanyms_dict['data']

                for data_dict in data_list:
                    output = colorFormat(data_dict['p'] + ' ','blue')

                    for i in data_dict['d']:
                        output += colorFormat(i + ', ','green')
                    
                    print('    --> %s'%output)

def dataAna_dict_result(dict):
    try:
        dict_result = dict['dict_result']
    except:
        print('%s'%colorFormat('\n-----No Dict Result Avalible-----\n','red'))
        return

    simple_means = dict_result['simple_means']
    word_name = simple_means['word_name']

    print('%s'%colorFormat('\n-----Simple_Means----\n','blue'))
    symbols = simple_means['symbols'][0]

    ph_en = symbols['ph_en']
    ph_am = symbols['ph_am']

    print(colorFormat(word_name,'yellow'),'(enE: %s ; amE: %s) :'%(colorFormat(ph_en,'green'),colorFormat(ph_am,'green')))

    #word_name += ' (enE: %s ; amE: %s)'%(ph_en,ph_am)

    #print(colorFormat('%s :' % word_name, 'green'))

    word_means_list = simple_means['word_means']
    word_means = ''
    for i in word_means_list:
        word_means += i + ','
    #print('Word_Means : %s' % colorFormat(word_means, 'green'))
    print(colorFormat('Word_Means :','cyan'))
    print('  --> %s'%colorFormat(word_means,'green'))

    parts = symbols['parts']

    print(colorFormat('Word_Means_in_Details :','cyan'))
    
    for i in parts:
        means = ''
        for j in i['means']:
            means += j + ','
        print('  --> %s %s'%(colorFormat(i['part'],'blue'),colorFormat(means,'green')))

    print(colorFormat('World_Means_in_English :','cyan'))

    edict_dict = dict_result['edict']
    item_list = edict_dict['item']

    for item_dict in item_list:
        tr_group_list = item_dict['tr_group']

        for tr_group in tr_group_list:

            tr = colorFormat(item_dict['pos'] + '. ', 'blue')
            example = ''
            similar_word = ''

            for tr_i in tr_group['tr']:
                tr += colorFormat((tr_i + ', '),'green')
            
            print('  --> %s'%tr)

            for sw_i in tr_group['similar_word']:
                similar_word += sw_i + ', '
            
            print('    --> %s : %s'%(colorFormat('Similar','yellow'),colorFormat(similar_word,'green')))

            for ex_i in tr_group['example']:
                example += ex_i + '; '
            
            print('    --> %s : %s'%(colorFormat('Example','yellow'),colorFormat(example,'green')))


    exchange_dict = simple_means['exchange']
    print_word_exchange(exchange_dict)

    if simple_means.__contains__('derivative'):
        derivative_list = simple_means['derivative']
        print(colorFormat('Word_Derivative :','cyan'))

        for i in derivative_list:
            print('  -->',end= ' ')
            print(colorFormat(i['data'][1]['p_text'],'blue'),end=' ')
            print(colorFormat(i['data'][0]['data'][0]['text'],'green'))

    if dict_result.__contains__('sanyms'):

        sanyms_list = dict_result['sanyms']
        printSanyms(sanyms_list)

    if dict_result.__contains__('usecase'):

        usecase_dict = dict_result['usecase']
        printUsecase(usecase_dict)


# fp = open(r'python\Trans Tool\test.json', 'w', encoding='utf-8')
# json.dump(response.json(), fp = fp,ensure_ascii=False)
# fp.close()

dict_json = response.json()

if isWord(query):
    dataAna_trans_result(dict_json)
    dataAna_dict_result(dict_json)
else:
    dataAna_trans_result(dict_json)


#over

#print(type(dict_json))

