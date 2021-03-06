# coding: utf-8
rules = {'if (.*)': ["Do you really think it's likely that {0}", 'Do you wish that {0}',
                     'What do you think about {0}', 'Really--if {0}'],
         'do you think (.*)': ['if {0}? Absolutely.', 'No chance'],
         '(.*)what can you do(.*)':['Well, I\'m your _music bot_. \n \n*1)* You can ask me for some *music recommendations*\
         \n*2)* or you can tell me *your preferences*, for instance, the *title*, the *kind*, the *artist*, the *genera*, and even your *mood* right now! \n\n _So, Why not have a try~_'],
         '(.*)your name(.*)':['Hh i\'m kangkang, I\'m Xuanhe\'s music chatbot! How nice to meet you!',
                              'my name is Kangkang, Xuanhe\'s music chatbot! Glad meeting you!'],
         'do you remember (.*)': ['Did you think I would forget {0}', "How could I forget {0}"]}

responses={
    'want more':['Would u like tell me more?',
                 'And..Any other preferences?'],
    'wait':['OK~ a moment please, I\'ll back soon',
            'would you mind waiting a short while? I\'ll be right back',
            'Let me check..',
            'humm, moment please~'],
    'offer choices':['How about this song!',
                    'OK, I\'ve found sth for you~',
                    'How do you like {0}, a great song by {1}',
                    'What do you think of {0},by {1}'],
    'sad':['Sorry to hear that, No matter what happens, I\'ll always here for you, here is a sad song {0} by {1}',
           'oh, sorry to know you are down, Maybe a sad song will help you release'],
    'happy':['Wow, glad to know that! May the good mood always with you'],
    'offer choices when no answer':['Sorry I can\'t help, but how about this song:',
                    'How do you like {0}, a great song by {1}',
                    'What do you think of {0}, by {1}'],
    'recommend choices':['How about that song!',
                    'Got it, I\'ve found for you~',
                    'How do you like {0}, a great song by {1}',
                    'What do you think of {0}, by {1}'],
    'no answer':['Sorry, I can\'t find song like you said',
                 'Sorry, I don\'t know song you want... But later I surely will!'],
    'affirm':['Yeah~ but I\'m still making progress','Wow, I\'m flattered','Glad to hear that~','Haha, I\'ll keep making progress'],
    'pleasure':['You are welcome~','It\'s my pleasure! ^o^'],
    'about_teacher':['Oh, you mean Fan Zhang? He\'s my teacher and he\'s very great! \nHere I have a farewell song for him, you know, since the remote research has ended. If you meet him someday~, please send him my BEST WISHES ^_^'],
    'bye':['Bye~~','See you','Glad talking to you, see you next time!'],
    'distinguish_songs':['Why not send me a piece and let me check?','Good, you can now send a voice to me, even there are noises'],
    'greet':['Hi, my friend','Wow, long time no see~','Hello, I\' Kangkang, I\'m Xuanhe\'s music chatbot!']
    }