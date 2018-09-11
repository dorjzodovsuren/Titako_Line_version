from __future__ import unicode_literals
import random
import errno
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
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


# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    text1 = text.lower()
    zassan=shortcut(text1)

    if text1 == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Display name: ' + profile.display_name),
                    TextSendMessage(text='Status message: ' + profile.status_message)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text1 == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))
    elif text1 == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageAction(label='Yes', text='Yes!'),
            MessageAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text1 in ['hi','hello','sainu','launch']:
        buttons_template = ButtonsTemplate(
            title='Services', text='Hello. I am TiTAX LINE assistant.Please choose your service', actions=[
                URIAction(label='Go to TokyoTech Web', uri='https://www.titech.ac.jp/english/'),
                PostbackAction(label='Search room', data='ping', text='Please enter room number:'),
                PostbackAction(label='Search building', data='ping', text='Please enter bulding number'),
                MessageAction(label='Report Problem', text='Please describe problems:')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text1 == 'instruction':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='English version', title='Instruction', actions=[
                URIAction(label='Go to Instruction', uri='https://www.dropbox.com/s/xjvc90mbxvfs41k/Instruction.pdf?raw=1'),
                PostbackAction(label='Comment', data='comment')
            ]),
            CarouselColumn(text='Japanese version', title='Instruction', actions=[
                URIAction(label='Go to Instruction', uri='https://www.dropbox.com/s/xjvc90mbxvfs41k/Instruction.pdf?raw=1'),
                PostbackAction(label='Comento', data='comment')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text1 == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='datetime',
                                                            data='datetime_postback',
                                                            mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='date',
                                                            data='date_postback',
                                                            mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text1 == 'imagemap':
        pass
    elif text1 in ["h121","h111","h112","h113","h114","h115","h116","h118","z14","z16","71-2"]:
        zurag={"h121":"https://www.dropbox.com/s/lc94cqfzttgx7mv/h121.jpg?raw=1","h111":"https://www.dropbox.com/s/rn9sn5ylimphdir/h111.jpg?raw=1","hoh":"https://www.dropbox.com/s/hpxkwcq9ej6sskz/hoh.jpg?raw=1","h112":"https://www.dropbox.com/s/29xlk7clggixhfz/h112.jpg?raw=1","h113":"https://www.dropbox.com/s/nsxcdaycm0b2lyi/h113.jpg?raw=1","h114":"https://www.dropbox.com/s/718s7wtk4uopjni/h114.jpg?raw=1","h115":"https://www.dropbox.com/s/und4scgb7ae69l5/h115.jpg?raw=1","h116":"https://www.dropbox.com/s/lcvum4xr5p3o7l0/h116.jpg?raw=1","h118":"https://www.dropbox.com/s/vq2oqeglcb5t161/h118.jpg?raw=1","71-2":"https://www.dropbox.com/s/q8ev4t9gm1pxlxk/71-2.jpg?raw=1","z10":"https://www.dropbox.com/s/96eglhjxn073vi0/10.JPG?raw=1","z11":"https://www.dropbox.com/s/c14fimzx9pj9zpr/11.JPG?raw=1","z12":"https://www.dropbox.com/s/0atiryca1466iki/12.JPG?raw=1","z14":"https://www.dropbox.com/s/v585jlwpuxzoy0d/14.JPG?raw=1","z15":"https://www.dropbox.com/s/2cct5tumg415s2u/15.jpg?raw=1","z16":"https://www.dropbox.com/s/arn15usdhqufq6n/16.jpg?raw=1"}
        building_pic={"h121":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","h111":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","h112":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","h113":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","h114":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","h115":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","h116":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","h118":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1"}
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url=building_pic[text1],
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri=zurag[text1], label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='%s room location'%text1.upper(), weight='bold', size='xl'),
                    # review
#                     BoxComponent(
#                         layout='baseline',
#                         margin='md',
#                         contents=[
#                             IconComponent(size='sm', url=zurag[text1]),
#                             IconComponent(size='sm', url='https://example.com/grey_star.png'),
#                             IconComponent(size='sm', url='https://example.com/gold_star.png'),
#                             IconComponent(size='sm', url='https://example.com/gold_star.png'),
#                             IconComponent(size='sm', url='https://example.com/grey_star.png'),
#                             TextComponent(text='4.0', size='sm', color='#999999', margin='md',
#                                           flex=0)
#                         ]
#                     ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='%s, Tokyo Institute of Technology'%text1.upper(),
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="07:00 - 20:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:08088923385'),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='Click to see location', uri=zurag[text1])
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif text1 in ["w1","w2","w3","w4","w7","w8","w9","e1","e2","e8","s1","s1","s2","s3","s4","s5","s6","s7","s8","s9","i1","i2","i3","i4","i5","i6","i7","i8","i9","n1","n2","m1","m2","m3","m4","m5","m6"]:

        tatemono={"w1":"https://www.google.com/maps/place/35%C2%B036'16.7%22N+139%C2%B041'01.2%22E/@35.6046431,139.6748992,15z/data=!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6046443!4d139.6836544","w2":"https://www.google.com/maps/place/35%C2%B036'17.2%22N+139%C2%B040'55.6%22E/@35.6047961,139.6645685,14z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6047627!4d139.6821211","main":"https://www.google.com/maps/place/35%C2%B036'16.1%22N+139%C2%B041'01.9%22E/@35.6044811,139.6751022,15z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6044824!4d139.6838569","w1":"https://www.google.com/maps/place/35%C2%B036'19.4%22N+139%C2%B040'58.4%22E/@35.6053704,139.6478786,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6053761!4d139.6828977","w3":"https://www.google.com/maps/place/35%C2%B036'17.2%22N+139%C2%B040'55.6%22E/@35.6047961,139.6645685,14z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6047627!4d139.6821211","w4":"https://www.google.com/maps/place/35%C2%B036'15.7%22N+139%C2%B040'57.8%22E/@35.6043574,139.6477066,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6043627!4d139.6827263",
                                "w7":"https://www.google.com/maps/place/35%C2%B036'15.0%22N+139%C2%B040'57.7%22E/@35.6041634,139.6476796,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6041693!4d139.6826986","w8":"https://www.google.com/maps/place/35%C2%B036'17.7%22N+139%C2%B040'57.2%22E/@35.6049094,139.6475246,13967m/data=!3m2!1e3!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6049153!4d139.6825438","w9":"https://www.google.com/maps/place/35%C2%B036'21.0%22N+139%C2%B040'57.7%22E/@35.6058134,139.6476866,13967m/data=!3m2!1e3!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6058189!4d139.6827061","e1":"https://www.google.com/maps/place/35%C2%B036'13.6%22N+139%C2%B041'03.7%22E/@35.6037614,139.6494324,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6037673!4d139.6843664","e2":"https://www.google.com/maps/place/35%C2%B036'13.8%22N+139%C2%B041'02.5%22E/@35.6038385,139.6490974,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6038436!4d139.6840311","e8":"https://www.google.com/maps/place/35%C2%B036'17.9%22N+139%C2%B040'56.1%22E/@35.6049694,139.6472286,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6049752!4d139.6822484",
                                "s1":"https://www.google.com/maps/place/35%C2%B036'13.2%22N+139%C2%B041'00.3%22E/@35.6036484,139.6484884,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6036539!4d139.6834222","s2":"https://www.google.com/maps/place/35%C2%B036'10.9%22N+139%C2%B041'03.1%22E/@35.6030285,139.6492634,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6030345!4d139.6841974","s3":"https://www.google.com/maps/place/35%C2%B036'11.3%22N+139%C2%B041'02.1%22E/@35.6031405,139.6489764,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6031461!4d139.6839096","s4":"https://www.google.com/maps/place/35%C2%B036'12.0%22N+139%C2%B041'03.3%22E/@35.6033315,139.6493124,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6033375!4d139.684246","s5":"https://www.google.com/maps/place/35%C2%B036'09.5%22N+139%C2%B041'01.9%22E/@35.6026295,139.6489274,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.602635!4d139.6838608","s6":"https://www.google.com/maps/place/35%C2%B036'09.4%22N+139%C2%B041'04.2%22E/@35.6026125,139.6495754,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.602618!4d139.6845085","s7":"https://www.google.com/maps/place/35%C2%B036'12.4%22N+139%C2%B040'59.6%22E/@35.6034325,139.6482984,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.603438!4d139.6832318","s8":"https://www.google.com/maps/place/35%C2%B036'11.4%22N+139%C2%B041'00.4%22E/@35.6031705,139.6485024,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6031763!4d139.6834357",
                                "s9":"https://www.google.com/maps/place/35%C2%B036'10.6%22N+139%C2%B041'01.0%22E/@35.6029475,139.6486864,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6029526!4d139.6836196","i1":"https://www.google.com/maps/place/35%C2%B036'04.2%22N+139%C2%B041'04.1%22E/@35.6011484,139.6494646,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6011541!4d139.6844837","i2":"https://www.google.com/maps/place/35%C2%B036'06.4%22N+139%C2%B041'04.1%22E/@35.6017754,139.6494586,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6017808!4d139.6844782","i3":"https://www.google.com/maps/place/35%C2%B036'05.6%22N+139%C2%B041'05.8%22E/@35.6015564,139.6499196,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6015617!4d139.6849389","i4":"https://www.google.com/maps/place/35%C2%B036'04.1%22N+139%C2%B041'06.1%22E/@35.6011234,139.6500026,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.601129!4d139.6850217","i5":"https://www.google.com/maps/place/35%C2%B036'02.3%22N+139%C2%B041'04.4%22E/@35.6006294,139.6495246,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6006349!4d139.6845441","i6":"https://www.google.com/maps/place/35%C2%B036'02.7%22N+139%C2%B041'02.9%22E/@35.6007444,139.6491126,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6007505!4d139.6841325",
                                "i7":"https://www.google.com/maps/place/35%C2%B036'07.0%22N+139%C2%B041'04.8%22E/@35.6019504,139.6496556,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6019556!4d139.6846755","i8":"https://www.google.com/maps/place/35%C2%B036'03.1%22N+139%C2%B041'05.8%22E/@35.6008424,139.6499166,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6008483!4d139.6849365","i9":"https://www.google.com/maps/place/35%C2%B036'02.2%22N+139%C2%B041'06.0%22E/@35.6006104,139.6499666,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6006156!4d139.6849865",
                                "n1":"https://www.google.com/maps/place/35%C2%B036'24.2%22N+139%C2%B040'51.8%22E/@35.6067034,139.6460346,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6067089!4d139.6810535","n2":"https://www.google.com/maps/place/35%C2%B036'23.9%22N+139%C2%B040'49.7%22E/@35.6066194,139.6454636,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6066249!4d139.680483",
                                "m1":"https://www.google.com/maps/place/35%C2%B036'31.6%22N+139%C2%B040'44.1%22E/@35.6087704,139.6438886,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6087765!4d139.6789083","m2":"https://www.google.com/maps/place/35%C2%B036'30.8%22N+139%C2%B040'45.9%22E/@35.6085624,139.6444036,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6085676!4d139.6794225","m3":"https://www.google.com/maps/place/35%C2%B036'29.1%22N+139%C2%B040'46.0%22E/@35.6080644,139.6444136,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6080696!4d139.6794333","m4":"https://www.google.com/maps/place/35%C2%B036'27.5%22N+139%C2%B040'46.1%22E/@35.6076314,139.6444426,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.607637!4d139.679462","m5":"https://www.google.com/maps/place/35%C2%B036'32.6%22N+139%C2%B040'41.5%22E/@35.6090484,139.6431756,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6090541!4d139.6781948","m6":"https://www.google.com/maps/place/35%C2%B036'29.1%22N+139%C2%B040'44.6%22E/@35.6080794,139.6440226,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6080845!4d139.6790421"}     
        building_pic={"w1":"https://www.dropbox.com/s/rtv2k8b8sa77gsn/w1.jpg?raw=1","w2":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","w3":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","w7":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","w4":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","w7":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","w8":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","w9":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1"}
        web={"w1":"http://js.ila.titech.ac.jp/~web/japanese.html","w2":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html","w3":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html","w7":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html","w4":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html","w7":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html","w8":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html","w9":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html","s1":"https://www.dropbox.com/s/ovo0h48cr5a8t9s/S1.jpg?raw=1","s2":"https://www.dropbox.com/s/oo6vh1jqs8ddsjy/S2.jpg?raw=1","s3":"https://www.dropbox.com/s/febfx46obyg2nzq/S3.jpg?raw=1","s4":"https://www.dropbox.com/s/hp59mv0kw4b9m0f/S4.jpg?raw=1","s5":"https://www.dropbox.com/s/5ma2v75blf1fv77/S5.jpg?raw=1","s6":"https://www.dropbox.com/s/0ajsq48mg7y8crm/S6.jpg?raw=1","s7":"https://www.dropbox.com/s/p1kpr4scoeahenc/S7.jpg?raw=1","s8":"https://www.dropbox.com/s/nuqsy6j5wk2fu2q/S8.jpg?raw=1","s9":"https://www.dropbox.com/s/td1bfzgtvidar1l/S9.jpg?raw=1","administration buraeu 1":"https://www.dropbox.com/s/nvdzun2bhcw2pe4/Administration%20buraeu%201.jpg?raw=1","administration buraeu 4":"https://www.dropbox.com/s/l13gdtmicx9jqnd/Administration%20buraeu%204.jpg?raw=1","gsic":"https://www.dropbox.com/s/yldh85w4jqvhlf9/Gsic.jpg?raw=1","e1":"https://www.dropbox.com/s/h3dg36v3xsf00td/E1.jpg?raw=1"}
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url=building_pic[text1],
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri=tatemono[text1], label='label') 
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='%s building location'%text1.upper(), weight='bold', size='xl'),
                    # review
#                     BoxComponent(
#                         layout='baseline',
#                         margin='md',
#                         contents=[
#                             IconComponent(size='sm', url=zurag[text1]),
#                             IconComponent(size='sm', url='https://example.com/grey_star.png'),
#                             IconComponent(size='sm', url='https://example.com/gold_star.png'),
#                             IconComponent(size='sm', url='https://example.com/gold_star.png'),
#                             IconComponent(size='sm', url='https://example.com/grey_star.png'),
#                             TextComponent(text='4.0', size='sm', color='#999999', margin='md',
#                                           flex=0)
#                         ]
#                     ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='%s, Tokyo Institute of Technology'%text1.upper(),
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="07:00 - 20:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='Go to %s website'%text1.upper(), uri=web[text1]),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='Click to see on map', uri=tatemono[text1]) #zurag
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif text1 == 'quick_reply':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='Quick reply',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="label1", data="data1")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="label2", text="text2")
                        ),
                        QuickReplyButton(
                            action=DatetimePickerAction(label="label3",
                                                        data="data3",
                                                        mode="date")
                        ),
                        QuickReplyButton(
                            action=CameraAction(label="label4")
                        ),
                        QuickReplyButton(
                            action=CameraRollAction(label="label5")
                        ),
                        QuickReplyButton(
                            action=LocationAction(label="label6")
                        ),
                    ])))
    elif zassan in ["library","main","w2 lecture","sport center","gymnasium","lecture theater","environmental safety management","70th anniversary auditorium","cafeteria","extracurricular bldg 1","extracurricular bldg 2","extracurricular bldg 3","extracurricular bldg 4","administration bureau 1","administration bureau 2","administration bureau 3","administration bureau 4","administration bureau 5","gsic","global scientific information and computing center","library","centennial hall","south lecture","south lab 2","south lab 4","south lab 1","south lab 3","south lab 5","ishikawadai lab 1","elsi 1","elsi 2","international house","north lab 1","north lab 2a","north lab 2b","north lab 3a","north lab 3b","north lab 4","north lab 5","north lab 6","north lab 7","north lab 8","health service center","80th anniversary hall","extracurricular 5","tokyo tech front","n3","extracurricular 6","midorigaoka lecture"]:
         building={"library":"https://www.google.com/maps/place/Tokyo+Institute+of+Technology+Library/@35.6063984,139.68306,18z/data=!3m1!4b1!4m5!3m4!1s0x6018f531bfbef27f:0x4f3bc391a397d081!8m2!3d35.6063984!4d139.6840261","main":"https://www.google.com/maps/place/35%C2%B036'16.1%22N+139%C2%B041'01.9%22E/@35.6044811,139.6751022,15z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6044824!4d139.6838569",
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
         building_pic={"library":"https://www.dropbox.com/s/i7l5utqtr7jfs0r/library.jpg?raw=1","main":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1","sport center":"https://www.dropbox.com/s/0o3d513711z9nmb/sport%20hall.jpg?raw=1","gymnasium":"https://www.titech.ac.jp/english/enrolled/facilities/sports.html"}
         web={"library":"https://www.libra.titech.ac.jp/en","main":"https://www.titech.ac.jp/english/about/campus_maps/campus_highlights/main.html","sport center":"https://www.titech.ac.jp/english/enrolled/facilities/sports.html","gymnasium":"https://www.titech.ac.jp/english/enrolled/facilities/sports.html"}
         bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url=building_pic[zassan],
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri=building[zassan], label='label') 
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='%s building location'%zassan.upper(), weight='bold', size='xl'),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='%s, Tokyo Institute of Technology'%zassan.upper(),
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="07:00 - 20:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='Go to %s website'%zassan.upper(), uri=web[zassan]),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='Click to see on map', uri=building[zassan]) 
                    )
                ]
            ),
        )
         message = FlexSendMessage(alt_text="hello", contents=bubble)
         line_bot_api.reply_message(
            event.reply_token,
            message
        )
    else:
        pass
        


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id )
    )


# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        #ext = 'jpg'
        pass
    elif isinstance(event.message, VideoMessage):
        #ext = 'mp4'
        pass
    elif isinstance(event.message, AudioMessage):
        #ext = 'm4a'
        pass
    else:
        return

    #message_content = line_bot_api.get_message_content(event.message.id)
    #with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        #for chunk in message_content.iter_content():
            #tf.write(chunk)
        #tempfile_path = tf.name

    #dist_path = tempfile_path + '.' + ext
    #dist_name = os.path.basename(dist_path)
    #os.rename(tempfile_path, dist_path)

    #line_bot_api.reply_message(
        #event.reply_token, [
            #TextSendMessage(text='Save content.'),
            #TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        #])

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save file.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow event")


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        pass
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))
#     elif event.postback.data == 'comment':
#      line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text='Hello')


@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()

    app.run(debug=options.debug, port=options.port)
