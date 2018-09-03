from flask import Flask, request
from pymessenger2.bot import Bot
import os
import random
from pymessenger2.buttons import URLButton, PostbackButton
from pymessenger2 import Element, QuickReply
import time


app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN, api_version='2.12')

welcome_msg = '''
Hello {}! I’m  TiTAX. I can offer you free guide service inside Tokyo Tech main-building and around Ookayama campus at any time. Also, You can send me about issues around the campus. 
'''
global dialogue
global story
global q
global b
dialogue = []
story = []
timeline = 0
seq = []
q=[]
b=[]
def shortcut(utga):
 q=[]
 b=[]
 a=["main","@@","@","","@@@","@@@@","@@@@@","@@@@@@","@@@@@@@","w2 lecture","sport center","gymnasium","lecture theater","environmental safety management","70th anniversary auditorium","cafeteria","extracurricular 1","extracurricular 2","extracurricular 3","extracurricular 4","administration bureau 1","administration bureau 2","administration bureau 3","administration bureau 4","administration bureau 5","gsic","global scientific information and computing center","library","centennial hall","south lecture","south lab 2","south lab 4","south lab 1","south lab 3","south lab 5","ishikawadai lab 1","elsi 1","elsi 2","international house","north lab 1","north lab 2a","north lab 2b","north lab 3a","north lab 3b","north lab 4","north lab 5","north lab 6","north lab 7","north lab 8","health service center","80th anniversary hall","extracurricular 5","tokyo tech front","extracurricular 6","midorigaoka lecture"]
 data=list(utga)
 n=len(data)
 if n<51:
  for i in range(len(a)):
   if len(data)==len(a[i]):
    q.append(str(a[i]))

  for m in range(len(q)):
    k=0
    p=0
    while p<len(data):
      if data[p]== list(q[m])[p]: 
       p+=1  
       k+=1
      else:
       p+=1
    b.append(k)
  if len(b)!=0:
   tom=max(b)
   if tom>=n-2 and tom<=n:
    o=b.index(tom) 
    return (q[o])
   else: 
    return ("a")
  else:
   return ("a")
 else:
  return ("a")

@app.route("/hello", methods=['GET'])
def helloTest():
	return "hello"
@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'This website is under construction !!!'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            if event.get('messaging'):
                messaging = event['messaging']
                print(messaging)
                for x in messaging:
                    if x.get('message'):
                        recipient_id = x['sender']['id']
                        if x['message'].get('text'):
                            message = x['message']['text']
                            text1 = message.casefold()
                            zassan=shortcut(text1)
                            if text1 in ["hi", "hi there", "hello", "sain bainuu", "сайн уу", "hey", "yo","hey titax","titax","こんにちは"]:
                                buttons = []
                                button = URLButton(title='University web', url="https://www.titech.ac.jp/english/")
                                buttons.append(button)
                                button = PostbackButton(title='Room&Building search', payload='roomsearch')
                                buttons.append(button)
                                button = PostbackButton(title="Problems", payload= "problem")
                                buttons.append(button)
                                text = 'Choose a service please:' 
                                #bot.send_image_url(recipient_id, "https://www.dropbox.com/s/214z9ospup78eyp/Tseej%20zurag.jpg?raw=1") 			
                                bot.send_text_message(recipient_id, welcome_msg.format(bot.get_user_info(recipient_id)['first_name']))
                                bot.send_button_message(recipient_id, text, buttons)
                            elif text1 in ["h121","h111","h112","h113","h114","h115","h116","h118","z14","z16","71-2"]:
                                zurag={"h121":"https://www.dropbox.com/s/lc94cqfzttgx7mv/h121.jpg?raw=1","h111":"https://www.dropbox.com/s/rn9sn5ylimphdir/h111.jpg?raw=1","hoh":"https://www.dropbox.com/s/hpxkwcq9ej6sskz/hoh.jpg?raw=1","h112":"https://www.dropbox.com/s/29xlk7clggixhfz/h112.jpg?raw=1","h113":"https://www.dropbox.com/s/nsxcdaycm0b2lyi/h113.jpg?raw=1","h114":"https://www.dropbox.com/s/718s7wtk4uopjni/h114.jpg?raw=1","h115":"https://www.dropbox.com/s/und4scgb7ae69l5/h115.jpg?raw=1","h116":"https://www.dropbox.com/s/lcvum4xr5p3o7l0/h116.jpg?raw=1","h118":"https://www.dropbox.com/s/vq2oqeglcb5t161/h118.jpg?raw=1","71-2":"https://www.dropbox.com/s/q8ev4t9gm1pxlxk/71-2.jpg?raw=1","z10":"https://www.dropbox.com/s/96eglhjxn073vi0/10.JPG?raw=1","z11":"https://www.dropbox.com/s/c14fimzx9pj9zpr/11.JPG?raw=1","z12":"https://www.dropbox.com/s/0atiryca1466iki/12.JPG?raw=1","z14":"https://www.dropbox.com/s/v585jlwpuxzoy0d/14.JPG?raw=1","z15":"https://www.dropbox.com/s/2cct5tumg415s2u/15.jpg?raw=1",
                                "z16":"https://www.dropbox.com/s/arn15usdhqufq6n/16.jpg?raw=1"}
                                bot.send_image_url(recipient_id, zurag[text1]) 
                            elif text1 in ["w1","w2","w3","w4","w7","w8","w9","e1","e2","e8","s1","s1","s2","s3","s4","s5","s6","s7","s8","s9","i1","i2","i3","i4","i5","i6","i7","i8","i9","n1","n2","m1","m2","m3","m4","m5","m6"]:
                                del story[:]	
                                tatemono={"w1":"https://www.google.com/maps/place/35%C2%B036'16.7%22N+139%C2%B041'01.2%22E/@35.6046431,139.6748992,15z/data=!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6046443!4d139.6836544","w2":"https://www.google.com/maps/place/35%C2%B036'17.2%22N+139%C2%B040'55.6%22E/@35.6047961,139.6645685,14z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6047627!4d139.6821211","main":"https://www.google.com/maps/place/35%C2%B036'16.1%22N+139%C2%B041'01.9%22E/@35.6044811,139.6751022,15z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6044824!4d139.6838569","w1":"https://www.google.com/maps/place/35%C2%B036'19.4%22N+139%C2%B040'58.4%22E/@35.6053704,139.6478786,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6053761!4d139.6828977","w3":"https://www.google.com/maps/place/35%C2%B036'17.2%22N+139%C2%B040'55.6%22E/@35.6047961,139.6645685,14z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6047627!4d139.6821211","w4":"https://www.google.com/maps/place/35%C2%B036'15.7%22N+139%C2%B040'57.8%22E/@35.6043574,139.6477066,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6043627!4d139.6827263",
                                "w7":"https://www.google.com/maps/place/35%C2%B036'15.0%22N+139%C2%B040'57.7%22E/@35.6041634,139.6476796,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6041693!4d139.6826986","w8":"https://www.google.com/maps/place/35%C2%B036'17.7%22N+139%C2%B040'57.2%22E/@35.6049094,139.6475246,13967m/data=!3m2!1e3!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6049153!4d139.6825438","w9":"https://www.google.com/maps/place/35%C2%B036'21.0%22N+139%C2%B040'57.7%22E/@35.6058134,139.6476866,13967m/data=!3m2!1e3!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6058189!4d139.6827061","e1":"https://www.google.com/maps/place/35%C2%B036'13.6%22N+139%C2%B041'03.7%22E/@35.6037614,139.6494324,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6037673!4d139.6843664","e2":"https://www.google.com/maps/place/35%C2%B036'13.8%22N+139%C2%B041'02.5%22E/@35.6038385,139.6490974,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6038436!4d139.6840311","e8":"https://www.google.com/maps/place/35%C2%B036'17.9%22N+139%C2%B040'56.1%22E/@35.6049694,139.6472286,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6049752!4d139.6822484",
                                "s1":"https://www.google.com/maps/place/35%C2%B036'13.2%22N+139%C2%B041'00.3%22E/@35.6036484,139.6484884,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6036539!4d139.6834222","s2":"https://www.google.com/maps/place/35%C2%B036'10.9%22N+139%C2%B041'03.1%22E/@35.6030285,139.6492634,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6030345!4d139.6841974","s3":"https://www.google.com/maps/place/35%C2%B036'11.3%22N+139%C2%B041'02.1%22E/@35.6031405,139.6489764,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6031461!4d139.6839096","s4":"https://www.google.com/maps/place/35%C2%B036'12.0%22N+139%C2%B041'03.3%22E/@35.6033315,139.6493124,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6033375!4d139.684246","s5":"https://www.google.com/maps/place/35%C2%B036'09.5%22N+139%C2%B041'01.9%22E/@35.6026295,139.6489274,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.602635!4d139.6838608","s6":"https://www.google.com/maps/place/35%C2%B036'09.4%22N+139%C2%B041'04.2%22E/@35.6026125,139.6495754,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.602618!4d139.6845085","s7":"https://www.google.com/maps/place/35%C2%B036'12.4%22N+139%C2%B040'59.6%22E/@35.6034325,139.6482984,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.603438!4d139.6832318","s8":"https://www.google.com/maps/place/35%C2%B036'11.4%22N+139%C2%B041'00.4%22E/@35.6031705,139.6485024,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6031763!4d139.6834357",
                                "s9":"https://www.google.com/maps/place/35%C2%B036'10.6%22N+139%C2%B041'01.0%22E/@35.6029475,139.6486864,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6029526!4d139.6836196","i1":"https://www.google.com/maps/place/35%C2%B036'04.2%22N+139%C2%B041'04.1%22E/@35.6011484,139.6494646,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6011541!4d139.6844837","i2":"https://www.google.com/maps/place/35%C2%B036'06.4%22N+139%C2%B041'04.1%22E/@35.6017754,139.6494586,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6017808!4d139.6844782","i3":"https://www.google.com/maps/place/35%C2%B036'05.6%22N+139%C2%B041'05.8%22E/@35.6015564,139.6499196,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6015617!4d139.6849389","i4":"https://www.google.com/maps/place/35%C2%B036'04.1%22N+139%C2%B041'06.1%22E/@35.6011234,139.6500026,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.601129!4d139.6850217","i5":"https://www.google.com/maps/place/35%C2%B036'02.3%22N+139%C2%B041'04.4%22E/@35.6006294,139.6495246,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6006349!4d139.6845441","i6":"https://www.google.com/maps/place/35%C2%B036'02.7%22N+139%C2%B041'02.9%22E/@35.6007444,139.6491126,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6007505!4d139.6841325",
                                "i7":"https://www.google.com/maps/place/35%C2%B036'07.0%22N+139%C2%B041'04.8%22E/@35.6019504,139.6496556,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6019556!4d139.6846755","i8":"https://www.google.com/maps/place/35%C2%B036'03.1%22N+139%C2%B041'05.8%22E/@35.6008424,139.6499166,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6008483!4d139.6849365","i9":"https://www.google.com/maps/place/35%C2%B036'02.2%22N+139%C2%B041'06.0%22E/@35.6006104,139.6499666,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6006156!4d139.6849865",
                                "n1":"https://www.google.com/maps/place/35%C2%B036'24.2%22N+139%C2%B040'51.8%22E/@35.6067034,139.6460346,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6067089!4d139.6810535","n2":"https://www.google.com/maps/place/35%C2%B036'23.9%22N+139%C2%B040'49.7%22E/@35.6066194,139.6454636,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6066249!4d139.680483",
                                "m1":"https://www.google.com/maps/place/35%C2%B036'31.6%22N+139%C2%B040'44.1%22E/@35.6087704,139.6438886,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6087765!4d139.6789083","m2":"https://www.google.com/maps/place/35%C2%B036'30.8%22N+139%C2%B040'45.9%22E/@35.6085624,139.6444036,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6085676!4d139.6794225","m3":"https://www.google.com/maps/place/35%C2%B036'29.1%22N+139%C2%B040'46.0%22E/@35.6080644,139.6444136,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6080696!4d139.6794333","m4":"https://www.google.com/maps/place/35%C2%B036'27.5%22N+139%C2%B040'46.1%22E/@35.6076314,139.6444426,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.607637!4d139.679462","m5":"https://www.google.com/maps/place/35%C2%B036'32.6%22N+139%C2%B040'41.5%22E/@35.6090484,139.6431756,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6090541!4d139.6781948","m6":"https://www.google.com/maps/place/35%C2%B036'29.1%22N+139%C2%B040'44.6%22E/@35.6080794,139.6440226,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6080845!4d139.6790421"}
                                text = "The building you looking for is %s building, right?"%text1.upper()
                                buttons = []  
                                button = URLButton(title='Yes, it is', url=tatemono[text1])
                                buttons.append(button)
                                bot.send_button_message(recipient_id, text, buttons)
                            elif text1=="the coolest teacher":
                                data=["https://www.dropbox.com/s/8e1kqixb7tjnko9/Super%20Tilma.jpg?raw=1"]
                                smile=random.choice(data)
                                bot.send_image_url(recipient_id, smile)
                                bot.send_text_message(recipient_id, "Full name: Todd Tilma\n1.Word he like to say: Ningenwa BAKA\n2.Never assume")#hogjiltei fact hiih
                            elif text1=="family":
                                bot.send_image_url(recipient_id, "https://www.dropbox.com/s/th184qbyyyb3g9m/Gsep%20Family.png?raw=1")
                                bot.send_text_message(recipient_id, "I'm Bro")#hogjiltei fact hiih


                            elif zassan in ["main","w2 lecture","sport center","gymnasium","lecture theater","environmental safety management","70th anniversary auditorium","cafeteria","extracurricular bldg 1","extracurricular bldg 2","extracurricular bldg 3","extracurricular bldg 4","administration bureau 1","administration bureau 2","administration bureau 3","administration bureau 4","administration bureau 5","gsic","global scientific information and computing center","library","centennial hall","south lecture","south lab 2","south lab 4","south lab 1","south lab 3","south lab 5","ishikawadai lab 1","elsi 1","elsi 2","international house","north lab 1","north lab 2a","north lab 2b","north lab 3a","north lab 3b","north lab 4","north lab 5","north lab 6","north lab 7","north lab 8","health service center","80th anniversary hall","extracurricular 5","tokyo tech front","n3","extracurricular 6","midorigaoka lecture"]:
                                del story[:]
                                building={"main":"https://www.google.com/maps/place/35%C2%B036'16.1%22N+139%C2%B041'01.9%22E/@35.6044811,139.6751022,15z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6044824!4d139.6838569",
                                "sport center":"https://www.google.com/maps/place/35%C2%B036'19.6%22N+139%C2%B040'56.3%22E/@35.6054424,139.6472916,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6054482!4d139.6823113",
                                "lecture theater":"https://www.google.com/maps/place/35%C2%B036'16.3%22N+139%C2%B040'56.3%22E/@35.6045284,139.6472956,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6045342!4d139.6823149","w2 lecture":"https://www.google.com/maps/place/35%C2%B036'15.9%22N+139%C2%B040'56.2%22E/@35.6044004,139.6472606,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6044062!4d139.6822797",
                                "environmental safety management":"https://www.google.com/maps/place/35%C2%B036'21.6%22N+139%C2%B040'54.6%22E/@35.6059814,139.6468176,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6059866!4d139.681837","70th anniversary auditorium":"https://www.google.com/maps/place/35%C2%B036'21.3%22N+139%C2%B041'00.8%22E/@35.6059164,139.6485256,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6059219!4d139.6835447","cafeteria":"https://www.google.com/maps/place/35%C2%B036'22.4%22N+139%C2%B040'58.1%22E/@35.6062114,139.6477946,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6062167!4d139.6828145",
                                "extracurricular bldg 1":"https://www.google.com/maps/place/35%C2%B036'23.3%22N+139%C2%B040'59.1%22E/@35.6064534,139.6480616,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6064592!4d139.6830811","extracurricular bldg 2":"https://www.google.com/maps/place/35%C2%B036'22.6%22N+139%C2%B041'00.4%22E/@35.6062734,139.6484166,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6062789!4d139.6834356","extracurricular bldg 3":"https://www.google.com/maps/place/35%C2%B036'22.7%22N+139%C2%B040'59.8%22E/@35.6062914,139.6482496,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6062968!4d139.6832693","extracurricular bldg 4":"https://www.google.com/maps/place/35%C2%B036'21.4%22N+139%C2%B040'52.2%22E/@35.6059264,139.6461546,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6059321!4d139.6811745", #sport 
                                "administration bureau 1":"https://www.google.com/maps/place/35%C2%B036'18.7%22N+139%C2%B041'03.9%22E/@35.6052005,139.6494834,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6052063!4d139.6844169","administration bureau 2":"https://www.google.com/maps/place/35%C2%B036'18.7%22N+139%C2%B041'03.9%22E/@35.6052005,139.6494834,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6052063!4d139.6844169","administration bureau 3":"https://www.google.com/maps/place/35%C2%B036'18.3%22N+139%C2%B041'05.7%22E/@35.6050655,139.6499744,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6050714!4d139.6849082","gsic":"https://www.google.com/maps/place/35%C2%B036'20.2%22N+139%C2%B041'04.8%22E/@35.6055955,139.6497194,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6056013!4d139.6846534","global scientific information and computing center":"https://www.google.com/maps/place/35%C2%B036'20.2%22N+139%C2%B041'04.8%22E/@35.6055955,139.6497194,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6056013!4d139.6846534","library":"https://www.google.com/maps/place/35%C2%B036'23.0%22N+139%C2%B041'02.5%22E/@35.6063824,139.6490934,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6063883!4d139.6840266",
                                "centennial hall":"https://www.google.com/maps/place/35%C2%B036'24.9%22N+139%C2%B041'05.6%22E/@35.6069085,139.6499504,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6069141!4d139.684884","administration bureau 4":"https://www.google.com/maps/place/35%C2%B036'20.5%22N+139%C2%B041'06.1%22E/@35.6056745,139.6501004,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6056798!4d139.6850342","administration bureau 5":"https://www.google.com/maps/place/35%C2%B036'20.5%22N+139%C2%B041'06.1%22E/@35.6056745,139.6501004,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6056798!4d139.6850342","south lecture":"https://www.google.com/maps/place/35%C2%B036'08.9%22N+139%C2%B041'03.0%22E/@35.6024515,139.6492394,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6024568!4d139.6841734","south lab 2":"https://www.google.com/maps/place/35%C2%B036'11.5%22N+139%C2%B041'04.5%22E/@35.6031985,139.6496504,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6032038!4d139.6845842","south lab 4":"https://www.google.com/maps/place/35%C2%B036'12.3%22N+139%C2%B041'01.0%22E/@35.6034195,139.6486814,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6034253!4d139.6836152","south lab 1":"https://www.google.com/maps/place/35%C2%B036'10.7%22N+139%C2%B041'00.1%22E/@35.6029715,139.6484324,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6029768!4d139.6833664","south lab 3":"https://www.google.com/maps/place/35%C2%B036'14.0%22N+139%C2%B041'01.4%22E/@35.6038795,139.6487754,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6038852!4d139.6837088","south lab 5":"https://www.google.com/maps/place/35%C2%B036'14.0%22N+139%C2%B040'59.5%22E/@35.6038835,139.6482604,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6038893!4d139.6831935",
                                "ishikawadai lab 1":"https://www.google.com/maps/place/35%C2%B036'06.1%22N+139%C2%B041'03.3%22E/@35.6016814,139.6492336,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6016865!4d139.684253",
                                "elsi 2":"https://www.google.com/maps/place/35%C2%B036'03.1%22N+139%C2%B041'05.8%22E/@35.6008424,139.6499166,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6008483!4d139.6849365","international house":"https://www.google.com/maps/place/35%C2%B036'01.0%22N+139%C2%B041'03.5%22E/@35.6002734,139.6492956,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6002789!4d139.684315","elsi 1":"https://www.google.com/maps/place/35%C2%B036'07.0%22N+139%C2%B041'04.8%22E/@35.6019504,139.6496556,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6019556!4d139.6846755",
                                "north lab 1":"https://www.google.com/maps/place/35%C2%B036'25.1%22N+139%C2%B040'49.6%22E/@35.6069514,139.6454286,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6069574!4d139.6804477","north lab 2a":"https://www.google.com/maps/place/35%C2%B036'25.9%22N+139%C2%B040'49.3%22E/@35.6071814,139.6453476,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.607187!4d139.6803671","north lab 3a":"https://www.google.com/maps/place/35%C2%B036'26.8%22N+139%C2%B040'49.1%22E/@35.6074334,139.6452966,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6074387!4d139.6803156","north lab 3b":"https://www.google.com/maps/place/35%C2%B036'27.1%22N+139%C2%B040'48.7%22E/@35.6075154,139.6451716,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6075207!4d139.6801908","north lab 4":"https://www.google.com/maps/place/35%C2%B036'26.7%22N+139%C2%B040'51.0%22E/@35.6074014,139.6458046,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6074075!4d139.680824","north lab 5":"https://www.google.com/maps/place/35%C2%B036'26.8%22N+139%C2%B040'51.8%22E/@35.6074464,139.6460446,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6074516!4d139.6810636",
                                "north lab 6":"https://www.google.com/maps/place/35%C2%B036'25.3%22N+139%C2%B040'51.3%22E/@35.6070204,139.6458886,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6070256!4d139.680908","north lab 7":"https://www.google.com/maps/place/35%C2%B036'27.5%22N+139%C2%B040'48.9%22E/@35.6076454,139.6452416,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6076507!4d139.6802611","north lab 8":"https://www.google.com/maps/place/35%C2%B036'26.1%22N+139%C2%B040'52.0%22E/@35.6072294,139.6460976,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6072355!4d139.6811175","health service center":"https://www.google.com/maps/place/35%C2%B036'26.1%22N+139%C2%B041'01.3%22E/@35.6072424,139.6486846,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6072477!4d139.6837039","80th anniversary hall":"https://www.google.com/maps/place/35%C2%B036'25.5%22N+139%C2%B041'00.0%22E/@35.6070714,139.6483236,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6070767!4d139.6833428","extracurricular 5":"https://www.google.com/maps/place/35%C2%B036'26.2%22N+139%C2%B040'57.2%22E/@35.6072724,139.6475456,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6072785!4d139.6825652","tokyo tech front":"https://www.google.com/maps/place/35%C2%B036'26.8%22N+139%C2%B041'04.2%22E/@35.6074504,139.6494686,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6074556!4d139.6844877","n3":"https://www.google.com/maps/place/35%C2%B036'22.9%22N+139%C2%B040'50.4%22E/@35.6063414,139.6456436,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.606347!4d139.6806627",
                                "17":"https://www.google.com/maps/place/35%C2%B036'28.1%22N+139%C2%B040'49.6%22E/@35.6077864,139.6454156,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6077916!4d139.6804345",
                                "midorigaoka lecture":"https://www.google.com/maps/place/35%C2%B036'28.5%22N+139%C2%B040'45.7%22E/@35.6079114,139.6443346,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6079171!4d139.6793542","gymnasium":"https://www.google.com/maps/place/35%C2%B036'19.6%22N+139%C2%B040'56.3%22E/@35.6054424,139.6472916,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6054482!4d139.6823113"}
                                text = "The building you looking for is %s building, right?"%zassan.upper()
                                print(story)
                                buttons = []  
                                button = URLButton(title='Yes, it is', url=building[zassan])
                                buttons.append(button)
                                bot.send_button_message(recipient_id, text, buttons)
                            elif zassan in ["a"] and story==[]:
                                bot.send_text_message(recipient_id, "Please enter correct text ")

                            elif text1 not in ["z1","z2","z3","z4","z5","z6","z7","z8","z9","z10","z11","z12","z14","z15","z16","hoh"] and story==["Problem"]:
                                del story[:]
                                print ("PROBLEM is " + text1)
                                bot.send_text_message(recipient_id, "Please submit the picture of problem: ")
                            else:
                                bot.send_text_message(recipient_id, "Please enter correct text")
                        if x['message'].get('attachments'):
                            print(x['message'])
                            if x['message']['attachments'][0]['type'] == 'image':
                                bot.send_text_message(recipient_id, 'Thank you for all your assistance.')
        

                               

                    if x.get('postback'):
                        if x['postback']['payload'] == 'roomsearch':
                            recipient_id = x['sender']['id']
                            bot.send_text_message(recipient_id, 'Please enter the room number or building number you looking for (e.g: W4, I4): ')
                           

                            
                    if x.get('postback'):
                        if x['postback']['payload'] == 'problem':
                            recipient_id = x['sender']['id']
                            story.append("Problem")
                            bot.send_text_message(recipient_id, 'Please describe the problem :')      
                    if x.get('postback'):
                        if x['postback']['payload'] == "HELP_PAYLOAD":
                            recipient_id = x['sender']['id']
                            bot.send_text_message(recipient_id, 'This is English Brief description of "How to use TiTAX chatbot".This bot give you free guiding service in Ookayama campus and help you find the building you looking for within short amount of time. ')
                    if x.get('postback'):
                        if x['postback']['payload'] == "CONTACT_INFO_PAYLOAD":
                            recipient_id = x['sender']['id']
                            bot.send_text_message(recipient_id, 'これは日本語です。「TiTAXチャットボットの使い方」の簡単な説明。このボットは大岡山キャンパス内の無料案内サービスを提供し、あなたが短時間で探している建物を見つけるのを手助けします.')
                            
                          
                              
    return "Success"


if __name__ == "__main__":
    app.run()
