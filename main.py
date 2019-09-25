# coding: utf-8
import telebot
from config import TOKEN
import scipy
import re
import spacy
import numpy as np
import pandas as pd
nlp=spacy.load('en')
import requests
import sqlite3
import json
from rasa.nlu.training_data import load_data
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.model import Trainer
from rasa.nlu import config
import random

bot = telebot.TeleBot(TOKEN)

trainer = Trainer(config.load("config_spacy.yml"))
# Load the training data
training_data = load_data('rasa_train.json')
# Create an interpreter by training the model
interpreter = trainer.train(training_data)


conn = sqlite3.connect('songs.db')
c = conn.cursor()
c.execute("select song_id from LOCAL_SONGS ")
preview_already=l=[i[0] for i in c.fetchall()]
conn.close()

#define states
INIT=0
SPECIFY=1
CHECK_ATT=2
ORDERED=0

chatid=None

from common_response import rules,responses

def setchatid(id):
    global chatid
    chatid=id
    return

def chitchat_response(message):
    response, match_var = match_rule(rules,message)
    if response == "default":
        return None
    if '{0}' in response:
        phrase = replace_pronouns(match_var)
        response = response.format(phrase)
    return response

def match_rule(rules, message):
    for pattern, responses in rules.items():
        match = re.search(pattern, message)
        if match is not None:
            response = random.choice(responses)
            var = match.group(1) if '{0}' in response else None
            return response, var
    return "default", None

def replace_pronouns(message):
    message = message.lower()
    if 'me' in message:
        return re.sub('me', 'you', message)
    if 'my' in message:
        return re.sub('my', 'your', message)
    elif 'i' in message:
        return re.sub('i', 'you', message)
    elif 'your' in message:
        return re.sub('your', 'my', message)
    elif 'you' in message:
        return re.sub('you', 'me', message)
    return message

def formatsongs(x):
    ans=[]
    if len(x) > 0:
        for i in x:
            song = {'title': i[0],
                    'song_id': i[1],
                    'artist': i[2],
                    'artist_id': i[3]}
            ans.append(song)
    return ans

def find_songs(params={}, neg_params={}):
    conn = sqlite3.connect('songs.db')
    # create a cursor
    c = conn.cursor()
    query = 'SELECT title,song_id,artist,artist_id FROM LOCAL_SONGS '
    if len(params)+len(neg_params) == 0:
        c.execute(query)
        x = c.fetchall()
        c.close()
        conn.close()
        ans = formatsongs(x)
        return ans

    elif len(params) > 0 and len(neg_params) > 0:
        filters = ["LOWER({})=LOWER(?)".format(str(k)) for k in params] + ["LOWER({})!=LOWER(?)".format(str(k)) for k in
                                                                           neg_params]
        query += " WHERE " + " and ".join(filters)
        print(query)
    elif len(neg_params) > 0:
        filters = ["LOWER({})!=LOWER(?)".format(str(k)) for k in neg_params]
        query += " WHERE " + " and ".join(filters)

    elif len(params) > 0:
        filters = ["LOWER({})=LOWER(?)".format(str(k)) for k in params]
        query += " WHERE " + " and ".join(filters)

    t=[]
    for i,j in params.items():
        t.append(j)
    for i,j in neg_params.items():
        t.append(j)
    t=tuple(t)
    c.execute(query, t)
    x = c.fetchall()
    c.close()
    conn.close()
    ans = formatsongs(x)
    return ans

def negated_ents(phrase, entities=[]):
    # ends = sorted([phrase.index(e) + e[] for e in ents])
    result =[]
    if len(entities)==0:
        return result

    new_ents = sorted(entities, key=lambda e: e.__getitem__('end'), reverse=False)
    ends = [e['end'] for e in new_ents]
    start = 0
    chunks = []
    for end in ends:
        chunks.append(phrase[start:end])
        start = end

    for i, chunk in enumerate(chunks):
        if 'not' in chunk or "n't" in chunk or 'no' in chunk or 'nor' in chunk:
            result.append(new_ents[i]['value'])
    return result

'''
INIT=0
SPECIFY=1
CHECK_ATT=2
ORDERED=0
'''
def clear():
    global params, neg_params, state, anslist, pending
    params={}
    neg_params={}
    state=INIT
    anslist=find_songs()
    pre_anslist=anslist.copy()
    pending=None
    return


def getsong_by_id(x):
    # 0 成功
    # 1 没有这首歌
    # 2 网络错误

    global preview_already
    if str(x) in preview_already:
        # send to message
        # get 这首歌的信息
        info = {}
        return 0, info
    url = "https://deezerdevs-deezer.p.rapidapi.com/track/{}".format(x)
    headers = {'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
               'x-rapidapi-key': <API KEY>}
    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        print(e)
        print(x, 'request 1 failed')
        return 2, None
    else:
        print(x, 'request 1 succceed')
    r = response.json()
    if ('error' not in r) and (len(r) > 5):
        print("downloading with requests")
        mus = r['preview']

        try:
            download = requests.get(mus)
        except Exception as e:
            print(e)
            print(x, 'request 1 failed')
            return 2, None

        with open("./previews/{}.mp3".format(r['id']), "wb") as song:
            song.write(download.content)
            preview_already.append(str(r['id']))
            preview_already = list(set(preview_already))
            print('succeed', x)
            info = {

            }
        return 0, info
    else:
        print('request 1 wrong data', x)
        return 1, None


def getsong_by_title(x):
    # 0 成功
    # 1 没有这首歌
    # 2 网络错误

    global preview_already
    if str(x) in preview_already:
        # send to message
        return True
    querystring = {"q": x}
    headers = {
        'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
        'x-rapidapi-key': <API KEY>
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
    except Exception as e:
        print(e)
        print(x, 'request 1 failed')
        return False
    else:
        print(x, 'request 1 succceed')
    r = response.json()
    if ('error' not in r) and (r['total'] > 0):
        print("downloading with requests")
        mus = r['data'][0]['preview']

        if getsong_by_id(r['data'][0])[0] == 0:
            t = r['data'][0]
            return True, {'song_id': t['id'], 'title': t['title'], 'artist': t['artist']['name'],
                          'artist_id': t['artist']['id']}
        # 可以改成搜索两首歌

        return False
    else:
        print(x, 'no such songs')
        return False

def simple_answer(intent):
    if intent=='about_teacher':
        x=responses['about_teacher'][0]
        song={
            'title':'See You Again',
            'artist':'Wiz Khalifa',
            'song_id':'95813354',
            'artist_id':'74804'
        }

        tosend = open('./previews/seeyouagain.mp3', 'rb')
        bot.send_message(chat_id=chatid,text=x)
        bot.send_audio(chat_id=chatid,
                       audio=tosend,
                       parse_mode='Markdown',
                       title=song['title'],
                       performer=song['artist'])
        send_details2(song)
        # caption='How do you like this song_    \n\n ',
        tosend.close()

        return
    elif intent=='affirm':
        x=random.choice(responses['affirm'])
    elif intent in responses:
        x=random.choice(responses[intent])
    else:
        x = "you intent is {}, let's pretend i've answered you!".format(intent)
    print(" ========BOT : {0}".format(x))
    bot.send_message(chat_id=chatid, parse_mode='Markdown',text=x)
    return

def simple_send(msg):
    print(" ========BOT : {}".format(msg))
    bot.send_message(chat_id=chatid, parse_mode='Markdown',text=msg)
    # bot.send_message(chat_id=message.chat.id, text='I can hear you! You said: {0}'.format(message.text))

    return

def send_details2(ans):
    print("the song is ")
    bot.send_message(chat_id=chatid,  parse_mode='Markdown',
                     text='*See You Again*\n_You can also listen to it on Deezer:_ [Deezer.com]({0}), \n'\
                          '_and for more infomation about the artist:_ [{1}]({2}) \n\n'.format('https://www.deezer.com/track/'+ans['song_id'],
                                                                         ans['artist'],'https://www.deezer.com/artist/'+ans['artist_id']))
    return

def send_details(ans):
    print("the song is ")
    bot.send_message(chat_id=chatid,  parse_mode='Markdown',
                     text='*SONG - {3} * \n_For copyright reasons, i cannot offer you the whole song_ \n'\
                          '_You can get the full version on Deezer:_ [Deezer.com]({0}), \n'\
                          '_and for more infomation about the artist:_ [{1}]({2}) '.format('https://www.deezer.com/track/'+ans['song_id'],
                                                                         ans['artist'],'https://www.deezer.com/artist/'+ans['artist_id'],ans['title']))
    return


def send_song(song={}):
    # bot.send_message(chat_id=chatid,text='the song\s id is '+str(c))
    if len(song) == 0:
        print('song info lost')
        return 0
    if getsong_by_id(song['song_id'])!=0:
        return 1
    # if get_song_byid...
    tosend = open('./previews/{0}.mp3'.format(song['song_id']), 'rb')
    bot.send_audio(chat_id=chatid, audio=tosend, parse_mode='Markdown', title=song['title'], performer=song['artist'])
                   #caption='How do you like this song_    \n\n ',

    tosend.close()

    msg = '***SONG**** {2} by {1}  SONG_ID{0}'.format(song['song_id'], song['artist'], song['title'])
    print(msg)
    return 0


def respond(message):
    global state, params, neg_params, anslist, pending, preview_already, ans

    print(" ========USER : {}".format(message))
    response = chitchat_response(message)
    if response is not None:
        simple_send(response)
        return  # state  # , None

    rasa_dict = interpreter.parse(message)
    intent = rasa_dict['intent']['name']
    print('intent:',intent)

    if intent=='about_teacher' or 'Fan' in message:
        simple_answer('about_teacher')
        return

    entities = interpreter.parse(message)["entities"]
    ent_v = [e['value'] for e in entities]

    # find negative entities
    negated = negated_ents(message, entities)

    for ent in entities:
        if ent['value'] in negated:
            if ent["entity"] == 'title':
                neg_params[ent["entity"]] = str(ent["value"])[2:-2]
            else:
                neg_params[ent["entity"]] = str(ent["value"])
        else:
            if ent["entity"] == 'title':
                params[ent["entity"]] = str(ent["value"])[2:-2]
            else:
                params[ent["entity"]] = str(ent["value"])

    # answer without state change   [thx, applaud, how to use, ...
    if intent not in ['affirm', 'search_songs', 'deny', 'recommend_songs']:
        simple_answer(intent)
        return  # state  # , None


    # intent:[ search_songs ]
    pnum = len(neg_params) + len(params)
    anslist = find_songs(params, neg_params)

    print('~~~~~ intent: ',intent,' ~~~ state ', state)

    # new_state=state
    if state == INIT:
        if intent == 'search_songs':
            if len(anslist) == 0:
                simple_send(random.choice(responses['no answer']))
                state = INIT
                clear()

                # set pending & recommend
                return

            elif pnum <= 1 and "title" not in params and 'title' not in neg_params:

                simple_send(random.choice(responses['want more']))
                state = SPECIFY
                return

            else:

                #simple_send(random.choice(responses['wait']))
                ans = random.choice(anslist)
                anslist.remove(ans)
                if ('sad' in ent_v and 'sad' not in negated ) or ('happy' in ent_v and 'happy' in negated):
                    x=random.choice(responses['sad'])
                elif ('happy' in ent_v and 'happy' not in negated ) or ('sad' in ent_v and 'sad' in negated):
                    x=random.choice(responses['happy'])
                else:
                    x = random.choice(responses['offer choices'])
                if '{0}' in x:
                    x = x.format(ans['title'], ans['artist'])
                simple_send(x)
                send_song(ans)
                state = CHECK_ATT
                return

        elif intent == 'recommend_songs':

            ans = random.choice(anslist)
            anslist.remove(ans)
            state = CHECK_ATT
            x = random.choice(responses['recommend choices'])
            if '{0}' in x:
                x = x.format(ans['title'], ans['artist'])
            simple_send(x)
            send_song(ans)
            return

        else:
            simple_answer(intent)
            pass
        return
    elif state == SPECIFY:
        if intent == 'affirm' and pnum == 0:
            simple_send('Yes...and?')
            return
        else:
            if len(anslist) == 0:
                simple_send(random.choice(responses['no answer']))
                anslist = find_songs()
                x = random.choice(responses['recommend choices'])
            else:
                if ('sad' in ent_v and 'sad' not in negated ) or ('happy' in ent_v and 'happy' in negated):
                    x=random.choice(responses['sad'])
                elif ('happy' in ent_v and 'happy' not in negated ) or ('sad' in ent_v and 'sad' in negated):
                    x=random.choice(responses['happy'])
                else:
                    x = random.choice(responses['offer choices'])
            # 如果存在答案 就发送一个
            # 如果答案不存在，道歉并且设置推荐  是否设置推荐轮次
            ans = random.choice(anslist)
            anslist.remove(ans)
            if '{0}' in x:
                x = x.format(ans['title'], ans['artist'])
            simple_send(x)
            send_song(ans)
            state = CHECK_ATT
            return

    elif state == CHECK_ATT:
        # 先判断有没有新增加条件
        if intent == 'affirm':
            state = INIT
            simple_send(random.choice(responses['pleasure']))
            send_details(ans)
            clear()
            return

        elif intent in ['deny', 'recommend_songs']:
            if len(anslist) == 0:
                simple_send(random.choice(responses['no answer']))
                state = INIT
                clear()
                return

            else:
                ans = random.choice(anslist)
                anslist.remove(ans)
                anslist = []
                x = random.choice(responses['offer choices when no answer'])
                if '{0}' in x:
                    x = x.format(ans['title'], ans['artist'])
                simple_send(x)
                send_song(ans)
                state = CHECK_ATT
                return

        elif intent == 'search_songs':
            if len(anslist) == 0:
                simple_send(random.choice(responses['no answer']))
                anslist = find_songs()
                x = random.choice(responses['offer choices when no answer'])
            else:
                if ('sad' in ent_v and 'sad' not in negated ) or ('happy' in ent_v and 'happy' in negated):
                    x=random.choice(responses['sad'])
                elif ('happy' in ent_v and 'happy' not in negated ) or ('sad' in ent_v and 'sad' in negated):
                    x=random.choice(responses['happy'])
                else:
                    x = random.choice(responses['offer choices'])
                #x = random.choice(responses['offer choices'])
            # 如果存在答案 就发送一个
            # 如果答案不存在，道歉并且设置推荐  是否设置推荐轮次
            ans = random.choice(anslist)
            anslist.remove(ans)
            if '{0}' in x:
                x = x.format(ans['title'], ans['artist'])
            simple_send(x)
            send_song(ans)
            state = CHECK_ATT
            return
    return


@bot.message_handler(commands=['start'])
def send_welcome(message):
    setchatid(message.chat.id)
    bot.send_message(chat_id=message.chat.id, parse_mode='Markdown',text='Hi~ I\'m *KangKang*.')

@bot.message_handler(content_types=['voice'])
def send_distinguish(message):
    print(message)
    setchatid(message.chat.id)
    file_id = message.voice.file_id
    # bot.send_voice(chat_id=message.chat.id,voice=file_id)


    file_info = bot.get_file(file_id)
    url = "https://audd.p.rapidapi.com/"
    url1='https://<MY API URL1>/{1}'.format(file_info.file_path)

    print(url1)
    querystring = {"return":"deezer","itunes_country":"us","url":url1}
    headers = {
    'x-rapidapi-host': "audd.p.rapidapi.com",
    'x-rapidapi-key': <MY_KEY_2>
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    r=response.json()
    #print(response.text)
    if r['staus']=='success':
        v={}
        v['artist']=r['artist']
        v['title']=r['title']
        v['song_id']=r['deezer']['id']
        v['artist_id']=r['deezer']['artist']['id']
    else:
        simple_send(random.choice(responses['no answer']))
    send_details(v)
    return


@bot.message_handler(commands=['help'])
def send_welcome(message):
    setchatid(message.chat.id)
    bot.send_message(reply_to_message_id=message.message_id, chat_id=message.chat.id, text='What can I do for you?')

@bot.message_handler()
def send_messaage(message):
    setchatid(message.chat.id)
    respond(message.text)

if __name__ == '__main__':
    #bot.polling()
    clear()
    bot.polling()

