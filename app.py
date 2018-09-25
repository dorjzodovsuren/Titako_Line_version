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
 a=["main","@@","@","","@@@","@@@@","@@@@@","@@@@@@","@@@@@@@","w2 lecture","sport center","gymnasium","lecture theater","environmental safety management","70th anniversary auditorium","extracurricular 1","extracurricular 2","extracurricular 3","extracurricular 4","administration bureau 1","administration bureau 2","administration bureau 3","administration bureau 4","administration bureau 5","gsic","global scientific information and computing center","library","centennial hall","south lecture","south lab 2","south lab 4","south lab 1","south lab 3","south lab 5","ishikawadai lab 1","international house","health service center","80th anniversary hall","extracurricular 5","tokyo tech front","extracurricular 6","midorigaoka lecture"]
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
                
    elif text1 in ['hi','hello','sainu','launch']:
        buttons_template = ButtonsTemplate(
            title='Services', text='Hello. I am TiTAX LINE assistant.Please choose your service', actions=[
                URIAction(label='Go to TokyoTech Web', uri='https://www.titech.ac.jp/english/'),
                PostbackAction(label='Search room', data='ping', text='Please enter room number:'),
                PostbackAction(label='Search building', data='ping', text='Please enter bulding number'),
                MessageAction(label='Report Problem', text='Please describe problems:')
            ])
        template_message = TemplateSendMessage(
            alt_text='TiTAX is greeting', template=buttons_template)
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
            CarouselColumn(text='Mongolian version', title='Instruction', actions=[
                URIAction(label='Go to Instruction', uri='https://www.dropbox.com/s/xjvc90mbxvfs41k/Instruction.pdf?raw=1'),
                PostbackAction(label='Setgegdel', data='comment')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Instructions', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    
    elif text1 == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://www.dropbox.com/s/urhqywhgfyk1829/Share%20QR.png?raw=1',
                                action=DatetimePickerAction(label='image',
                                                            data='image',
                                                            mode='image')),
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
        zurag={"h121":"https://www.dropbox.com/s/lc94cqfzttgx7mv/h121.jpg?raw=1","h111":"https://www.dropbox.com/s/rn9sn5ylimphdir/h111.jpg?raw=1","hoh":"https://www.dropbox.com/s/hpxkwcq9ej6sskz/hoh.jpg?raw=1","h112":"https://www.dropbox.com/s/29xlk7clggixhfz/h112.jpg?raw=1","h113":"https://www.dropbox.com/s/nsxcdaycm0b2lyi/h113.jpg?raw=1","h114":"https://www.dropbox.com/s/718s7wtk4uopjni/h114.jpg?raw=1","h115":"https://www.dropbox.com/s/und4scgb7ae69l5/h115.jpg?raw=1","h116":"https://www.dropbox.com/s/lcvum4xr5p3o7l0/h116.jpg?raw=1","h118":"https://www.dropbox.com/s/vq2oqeglcb5t161/h118.jpg?raw=1"}
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
                    SpacerComponent(size='sm'),
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
    elif text1 in ["w1","w2","w3","w4","w5","w6","w7","w8e","w8w","w9","cafeteria 1","cafeteria 2","west lecture 1","west lecture 2","e1","e2","e8","s1","s2","s3","s4","s5","s6","s7","s8","s9","south lab 1","south lab 2","south lab 3","south lab 4","south lab 5","i1","i2","i3","i4","i5","i6","i7","i8","i9","elsi 1","elsi 2","n1","n2","n3","north lab 1","north lab 2a","north lab 2b","north lab 3a","north lab 3b","north lab 4","north lab 5","north lab 6","north lab 7","north lab 8","m1","m2","m3","m4","m5","m6"]:

        tatemono={"w1":"https://www.google.com/maps/place/35%C2%B036'19.4%22N+139%C2%B040'58.4%22E/@35.6053704,139.6478786,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6053761!4d139.6828977",
"w2":"https://www.google.com/maps/place/35%C2%B036'16.7%22N+139%C2%B040'57.3%22E/@35.6046301,139.6820325,19z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6046289!4d139.6825812",
"w3":"https://www.google.com/maps/place/35%C2%B036'16.7%22N+139%C2%B040'58.2%22E/@35.6046431,139.6822795,19z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6046417!4d139.6828282",
"w4":"https://www.google.com/maps/place/35%C2%B036'15.7%22N+139%C2%B040'57.8%22E/@35.6043574,139.6477066,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6043627!4d139.6827263",
"w5":"https://www.google.com/maps/place/35%C2%B036'16.3%22N+139%C2%B040'56.3%22E/@35.6045284,139.6472956,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6045342!4d139.6823149",
"w6":"https://www.google.com/maps/place/35%C2%B036'15.9%22N+139%C2%B040'56.2%22E/@35.6044004,139.6472606,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6044062!4d139.6822797",
"w7":"https://www.google.com/maps/place/35%C2%B036'15.0%22N+139%C2%B040'57.7%22E/@35.6041634,139.6476796,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6041693!4d139.6826986",
"w8e":"https://www.google.com/maps/place/35%C2%B036'17.6%22N+139%C2%B040'58.2%22E/@35.6049011,139.6822755,19z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6049004!4d139.6828243",
"w8w":"https://www.google.com/maps/place/35%C2%B036'17.8%22N+139%C2%B040'57.0%22E/@35.6049321,139.6819565,19z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6049313!4d139.6825046",
"w9":"https://www.google.com/maps/place/35%C2%B036'21.0%22N+139%C2%B040'57.7%22E/@35.6058134,139.6476866,13967m/data=!3m2!1e3!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6058189!4d139.6827061",
"cafeteria 1":"https://www.google.com/maps/place/35%C2%B036'22.4%22N+139%C2%B040'58.2%22E/@35.6062281,139.6822915,19z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6062271!4d139.6828397",
"cafeteria 2":"https://www.google.com/maps/place/Second+Cafeteria/@35.6047977,139.6828778,19.68z/data=!4m5!3m4!1s0x6018f53056737891:0x96922e6237b5f769!8m2!3d35.6045703!4d139.6831396",
"west lecture 1":"https://www.google.com/maps/place/35%C2%B036'16.3%22N+139%C2%B040'56.3%22E/@35.6045284,139.6472956,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6045342!4d139.6823149",
"west lecture 2":"https://www.google.com/maps/place/35%C2%B036'15.9%22N+139%C2%B040'56.2%22E/@35.6044004,139.6472606,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6044062!4d139.6822797",
"e1":"https://www.google.com/maps/place/35%C2%B036'13.6%22N+139%C2%B041'03.7%22E/@35.6037614,139.6494324,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6037673!4d139.6843664",
"e2":"https://www.google.com/maps/place/35%C2%B036'13.8%22N+139%C2%B041'02.5%22E/@35.6038385,139.6490974,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6038436!4d139.6840311",
"e8":"https://www.google.com/maps/place/35%C2%B036'17.9%22N+139%C2%B040'56.1%22E/@35.6049694,139.6472286,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6049752!4d139.6822484",
"s1":"https://www.google.com/maps/place/35%C2%B036'13.2%22N+139%C2%B041'00.3%22E/@35.6036484,139.6484884,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6036539!4d139.6834222",
"s2":"https://www.google.com/maps/place/35%C2%B036'10.9%22N+139%C2%B041'03.1%22E/@35.6030285,139.6492634,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6030345!4d139.6841974",
"s3":"https://www.google.com/maps/place/35%C2%B036'11.3%22N+139%C2%B041'02.1%22E/@35.6031405,139.6489764,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6031461!4d139.6839096",
"s4":"https://www.google.com/maps/place/35%C2%B036'12.0%22N+139%C2%B041'03.3%22E/@35.6033315,139.6493124,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6033375!4d139.684246",
"s5":"https://www.google.com/maps/place/35%C2%B036'09.5%22N+139%C2%B041'01.9%22E/@35.6026295,139.6489274,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.602635!4d139.6838608",
"s6":"https://www.google.com/maps/place/35%C2%B036'09.4%22N+139%C2%B041'04.2%22E/@35.6026125,139.6495754,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.602618!4d139.6845085",
"s7":"https://www.google.com/maps/place/35%C2%B036'12.4%22N+139%C2%B040'59.6%22E/@35.6034325,139.6482984,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.603438!4d139.6832318",
"s8":"https://www.google.com/maps/place/35%C2%B036'11.4%22N+139%C2%B041'00.4%22E/@35.6031705,139.6485024,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6031763!4d139.6834357",
"s9":"https://www.google.com/maps/place/35%C2%B036'10.6%22N+139%C2%B041'01.0%22E/@35.6029475,139.6486864,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6029526!4d139.6836196",
"south lab 1":"https://www.google.com/maps/place/35%C2%B036'10.7%22N+139%C2%B041'00.1%22E/@35.6029715,139.6484324,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6029768!4d139.6833664",
"south lab 2":"https://www.google.com/maps/place/35%C2%B036'11.5%22N+139%C2%B041'04.5%22E/@35.6031985,139.6496504,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6032038!4d139.6845842",
"south lab 3":"https://www.google.com/maps/place/35%C2%B036'14.0%22N+139%C2%B041'01.4%22E/@35.6038795,139.6487754,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6038852!4d139.6837088",
"south lab 4":"https://www.google.com/maps/place/35%C2%B036'12.3%22N+139%C2%B041'01.0%22E/@35.6034195,139.6486814,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6034253!4d139.6836152",
"south lab 5":"https://www.google.com/maps/place/35%C2%B036'14.0%22N+139%C2%B040'59.5%22E/@35.6038835,139.6482604,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6038893!4d139.6831935",
"i1":"https://www.google.com/maps/place/35%C2%B036'04.2%22N+139%C2%B041'04.1%22E/@35.6011484,139.6494646,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6011541!4d139.6844837",
"i2":"https://www.google.com/maps/place/35%C2%B036'06.4%22N+139%C2%B041'04.1%22E/@35.6017754,139.6494586,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6017808!4d139.6844782",
"i3":"https://www.google.com/maps/place/35%C2%B036'05.6%22N+139%C2%B041'05.8%22E/@35.6015564,139.6499196,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6015617!4d139.6849389",
"i4":"https://www.google.com/maps/place/35%C2%B036'04.1%22N+139%C2%B041'06.1%22E/@35.6011234,139.6500026,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.601129!4d139.6850217",
"i5":"https://www.google.com/maps/place/35%C2%B036'02.3%22N+139%C2%B041'04.4%22E/@35.6006294,139.6495246,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6006349!4d139.6845441",
"i6":"https://www.google.com/maps/place/35%C2%B036'02.7%22N+139%C2%B041'02.9%22E/@35.6007444,139.6491126,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6007505!4d139.6841325",
"i7":"https://www.google.com/maps/place/35%C2%B036'07.0%22N+139%C2%B041'04.8%22E/@35.6019504,139.6496556,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6019556!4d139.6846755",
"i8":"https://www.google.com/maps/place/35%C2%B036'03.1%22N+139%C2%B041'05.8%22E/@35.6008424,139.6499166,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6008483!4d139.6849365",
"i9":"https://www.google.com/maps/place/35%C2%B036'02.2%22N+139%C2%B041'06.0%22E/@35.6006104,139.6499666,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6006156!4d139.6849865",
"elsi 1":"https://www.google.com/maps/place/35%C2%B036'07.0%22N+139%C2%B041'04.8%22E/@35.6019504,139.6496556,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6019556!4d139.6846755",
"elsi 2":"https://www.google.com/maps/place/35%C2%B036'03.1%22N+139%C2%B041'05.8%22E/@35.6008424,139.6499166,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6008483!4d139.6849365",
"n1":"https://www.google.com/maps/place/35%C2%B036'24.2%22N+139%C2%B040'51.8%22E/@35.6067034,139.6460346,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6067089!4d139.6810535",
"n2":"https://www.google.com/maps/place/35%C2%B036'23.9%22N+139%C2%B040'49.7%22E/@35.6066194,139.6454636,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6066249!4d139.680483",
"n3":"https://www.google.ru/maps/place/35%C2%B036'22.9%22N+139%C2%B040'50.6%22E/@35.606356,139.6797136,18z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6063542!4d139.680722",
"north lab 1":"https://www.google.com/maps/place/35%C2%B036'25.1%22N+139%C2%B040'49.6%22E/@35.6069514,139.6454286,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6069574!4d139.6804477",
"north lab 2a":"https://www.google.com/maps/place/35%C2%B036'25.9%22N+139%C2%B040'49.3%22E/@35.6071814,139.6453476,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.607187!4d139.6803671",
"north lab 2b":"https://www.google.com/maps/place/35%C2%B036'25.9%22N+139%C2%B040'49.3%22E/@35.6071814,139.6453476,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.607187!4d139.6803671",
"north lab 3a":"https://www.google.com/maps/place/35%C2%B036'26.8%22N+139%C2%B040'49.1%22E/@35.6074334,139.6452966,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6074387!4d139.6803156",
"north lab 3b":"https://www.google.com/maps/place/35%C2%B036'27.1%22N+139%C2%B040'48.7%22E/@35.6075154,139.6451716,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6075207!4d139.6801908",
"north lab 4":"https://www.google.com/maps/place/35%C2%B036'26.7%22N+139%C2%B040'51.0%22E/@35.6074014,139.6458046,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6074075!4d139.680824",
"north lab 5":"https://www.google.com/maps/place/35%C2%B036'26.8%22N+139%C2%B040'51.8%22E/@35.6074464,139.6460446,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6074516!4d139.6810636",
"north lab 6":"https://www.google.com/maps/place/35%C2%B036'25.3%22N+139%C2%B040'51.3%22E/@35.6070204,139.6458886,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6070256!4d139.680908",
"north lab 7":"https://www.google.com/maps/place/35%C2%B036'27.5%22N+139%C2%B040'48.9%22E/@35.6076454,139.6452416,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6076507!4d139.6802611",
"north lab 8":"https://www.google.com/maps/place/35%C2%B036'26.1%22N+139%C2%B040'52.0%22E/@35.6072294,139.6460976,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6072355!4d139.6811175",
"m1":"https://www.google.com/maps/place/35%C2%B036'31.6%22N+139%C2%B040'44.1%22E/@35.6087704,139.6438886,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6087765!4d139.6789083",
"m2":"https://www.google.com/maps/place/35%C2%B036'30.8%22N+139%C2%B040'45.9%22E/@35.6085624,139.6444036,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6085676!4d139.6794225",
"m3":"https://www.google.com/maps/place/35%C2%B036'29.1%22N+139%C2%B040'46.0%22E/@35.6080644,139.6444136,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6080696!4d139.6794333",
"m4":"https://www.google.com/maps/place/35%C2%B036'27.5%22N+139%C2%B040'46.1%22E/@35.6076314,139.6444426,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.607637!4d139.679462",
"m5":"https://www.google.com/maps/place/35%C2%B036'32.6%22N+139%C2%B040'41.5%22E/@35.6090484,139.6431756,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6090541!4d139.6781948",
"m6":"https://www.google.com/maps/place/35%C2%B036'29.1%22N+139%C2%B040'44.6%22E/@35.6080794,139.6440226,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6080845!4d139.6790421" }     
        building_pic={"w1":"https://www.dropbox.com/s/rtv2k8b8sa77gsn/w1.jpg?raw=1",
"w2":"https://www.dropbox.com/s/v2kkuf59rze1vgm/W2%263.jpg?raw=1",
"w3":"https://www.dropbox.com/s/v2kkuf59rze1vgm/W2%263.jpg?raw=1",
"w4":"https://www.dropbox.com/s/zj1fhbs1ljgoyqi/West%204.jpg?raw=1",
"w5":"https://www.dropbox.com/s/6pjc3kpx7vt5ps3/West%20lecture%201.jpg?raw=1",
"w6":"https://www.dropbox.com/s/wt44xn3nnpvcssa/West%20lecture%202.jpg?raw=1",
"w7":"https://www.dropbox.com/s/l90anftneygvqtw/West%207.jpg?raw=1",
"w8e":"https://www.dropbox.com/s/e4fag1qfji0v05x/W8E.jpg?raw=1",
"w8w":"https://www.dropbox.com/s/kylfwqh770t8rok/W8W.jpg?raw=1",
"w9":"https://www.dropbox.com/s/r1q788p9nt1i77a/West%209.jpg?raw=1",
"cafeteria 1":"https://www.dropbox.com/s/arko24qxpizl2fp/Cafeteria%201.jpg?raw=1",
"cafeteria 2":"https://www.dropbox.com/s/lsx6b9vltikv2ot/Cafeteria%202.jpg?raw=1",
"west lecture 1":"https://www.dropbox.com/s/6pjc3kpx7vt5ps3/West%20lecture%201.jpg?raw=1",
"west lecture 2":"https://www.dropbox.com/s/wt44xn3nnpvcssa/West%20lecture%202.jpg?raw=1",
"e1":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
"e2":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
"e8":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
"s1":"https://www.dropbox.com/s/ovo0h48cr5a8t9s/S1.jpg?raw=1",
"s2":"https://www.dropbox.com/s/oo6vh1jqs8ddsjy/S2.jpg?raw=1",
"s3":"https://www.dropbox.com/s/febfx46obyg2nzq/S3.jpg?raw=1",
"s4":"https://www.dropbox.com/s/hp59mv0kw4b9m0f/S4.jpg?raw=1",
"s5":"https://www.dropbox.com/s/5ma2v75blf1fv77/S5.jpg?raw=1",
"s6":"https://www.dropbox.com/s/0ajsq48mg7y8crm/S6.jpg?raw=1",
"s7":"https://www.dropbox.com/s/p1kpr4scoeahenc/S7.jpg?raw=1",
"s8":"https://www.dropbox.com/s/nuqsy6j5wk2fu2q/S8.jpg?raw=1",
"s9":"https://www.dropbox.com/s/td1bfzgtvidar1l/S9.jpg?raw=1",
"south lab 1":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
"south lab 2":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
"south lab 3":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
"south lab 4":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
"south lab 5":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
"i1":"https://www.dropbox.com/s/8zsbckwcyqpl8lo/I1.jpg?raw=1",
"i2":"https://www.dropbox.com/s/mv6ue8x81fu71lh/I2.jpg?raw=1",
"i3":"https://www.dropbox.com/s/2me9984qo6badpa/I3.jpg?raw=1",
"i4":"https://www.dropbox.com/s/ohw8itgo5ojnm4u/I4.jpg?raw=1",
"i5":"https://www.dropbox.com/s/ssaqtygxowwequc/I5.jpg?raw=1",
"i6":"https://www.dropbox.com/s/z1vqesr1uqzg9h9/I6.jpg?raw=1",
"i7":"https://www.dropbox.com/s/r50vh4j8s1zt1ou/Elsi%201.jpg?raw=1",
"i8":"https://www.dropbox.com/s/70nf8nd05sbnts1/I8.jpg?raw=1",
"i9":"https://www.dropbox.com/s/zq4k2pk5pa0g4g8/I9.jpg?raw=1",
"elsi 1":"https://www.dropbox.com/s/r50vh4j8s1zt1ou/Elsi%201.jpg?raw=1",
"elsi 2":"https://www.dropbox.com/s/70nf8nd05sbnts1/I8.jpg?raw=1",
"n1":"https://www.dropbox.com/s/qt8a5vzzgshrbd0/N1.jpg?raw=1",
"n2":"https://www.dropbox.com/s/kl5tqnpw4w76omj/N2.jpg?raw=1",
"n3":"https://www.dropbox.com/s/lj2o0e03bagwe5k/EEI.jpg?raw=1",
"north lab 1":"https://www.dropbox.com/s/aj7j4shcrt1ohk2/North%20lab%201.jpg?raw=1",
"north lab 2a":"https://www.dropbox.com/s/59zk3x9yt0emsty/North%20lab%202a.jpg?raw=1",
"north lab 2b":"https://www.dropbox.com/s/59zk3x9yt0emsty/North%20lab%202a.jpg?raw=1",
"north lab 3a":"https://www.dropbox.com/s/9dii8skvm3y1cre/North%20lab%203a.jpg?raw=1",
"north lab 3b":"https://www.dropbox.com/s/vezxczg0xzwnuay/North%20lab%203b.jpg?raw=1",
"north lab 4":"https://www.dropbox.com/s/kvin13cs2vbjjz7/North%20lab%204.jpg?raw=1",
"north lab 5":"https://www.dropbox.com/s/82u5bxnwgbs6rys/North%20lab%205.jpg?raw=1",
"north lab 6":"https://www.dropbox.com/s/xfxiaojip0ve9t7/North%20lab%206.jpg?raw=1",
"north lab 7":"https://www.dropbox.com/s/40eu9ykl0w42pjw/North%20lab%207.jpg?raw=1",
"north lab 8":"https://www.dropbox.com/s/i4xv7xxc9r7i662/North%20lab%208.jpg?raw=1",
"m1":"https://www.dropbox.com/s/ef92hsy6yz1spph/M1.jpg?raw=1",
"m2":"https://www.dropbox.com/s/j22xnhnkj8awyy9/M2.jpg?raw=1",
"m3":"https://www.dropbox.com/s/8un108x33jz5pob/M3.jpg?raw=1",
"m4":"https://www.dropbox.com/s/6m5o41deubgjd9r/M4.jpg?raw=1",
"m5":"https://www.dropbox.com/s/sxtblhxpt62owd8/M5.jpg?raw=1",
"m6":"https://www.dropbox.com/s/bz7hr0fw09c2lng/M6.jpg?raw=1"}
        web={"w1":"http://js.ila.titech.ac.jp/~web/japanese.html",
"w2":"https://www.titech.ac.jp/english/maps/ookayama/",
"w3":"https://www.titech.ac.jp/english/maps/ookayama/",
"w4":"https://www.titech.ac.jp/english/maps/ookayama/",
"w5":"https://www.titech.ac.jp/english/maps/ookayama/",
"w6":"https://www.titech.ac.jp/english/maps/ookayama/",
"w7":"https://www.titech.ac.jp/english/maps/ookayama/",
"w8e":"https://www.titech.ac.jp/english/maps/ookayama/",
"w8w":"https://www.titech.ac.jp/english/maps/ookayama/",
"w9":"https://www.titech.ac.jp/english/maps/ookayama/",
"cafeteria 1":"https://www.titech.ac.jp/english/about/campus_maps/cafeterias.html",
"cafeteria 2":"https://www.titech.ac.jp/english/about/campus_maps/cafeterias.html",
"west lecture 1":"https://www.titech.ac.jp/english/news/2015/031639.html",
"west lecture 2":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"e1":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"e2":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"e8":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"s1":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"s2":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"s3":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"s4":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"s5":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"s6":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"s7":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"s8":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"s9":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"south lab 1":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"south lab 2":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"south lab 3":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"south lab 4":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"south lab 5":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"i1":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"i2":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"i3":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"i4":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"i5":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"i6":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"i7":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"i8":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"i9":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"elsi 1":"http://www.elsi.jp/en/",
"elsi 2":"http://www.elsi.jp/en/",
"n1":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"n2":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"n3":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 1":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 2a":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 2b":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 3a":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 3b":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 4":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 5":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 6":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 7":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"north lab 8":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"m1":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"m2":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"m3":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"m4":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"m5":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"m6":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html"}
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
                                        text="----",
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
                        action=URIAction(label='Click to see on map', uri=tatemono[text1]) 
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
    elif zassan in ["administration bureau 1","administration bureau 2","administration bureau 3","administration bureau 4","administration bureau 5","gsic","global scientific information and computing center","library","main","centennial hall","lecturehall","lecture theater","safety management","70th anniversary auditorium","sports center","gymnasium","health service center","80th anniversary hall","tokyo tech front","environmental energy innovation","south lecture","ishikawadai lab 1","international house","midorigaoka lecture"]:
         building={"administration bureau 1":"https://www.google.com/maps/place/35%C2%B036'18.7%22N+139%C2%B041'03.9%22E/@35.6052005,139.6494834,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6052063!4d139.6844169",
"administration bureau 2":"https://www.google.com/maps/place/35%C2%B036'18.7%22N+139%C2%B041'03.9%22E/@35.6052005,139.6494834,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6052063!4d139.6844169",
"administration bureau 3":"https://www.google.com/maps/place/35%C2%B036'18.3%22N+139%C2%B041'05.7%22E/@35.6050655,139.6499744,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6050714!4d139.6849082",
"administration bureau 4":"https://www.google.com/maps/place/35%C2%B036'20.5%22N+139%C2%B041'06.1%22E/@35.6056745,139.6501004,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6056798!4d139.6850342",
"administration bureau 5":"https://www.google.com/maps/place/35%C2%B036'20.5%22N+139%C2%B041'06.1%22E/@35.6056745,139.6501004,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6056798!4d139.6850342",
"gsic":"https://www.google.com/maps/place/35%C2%B036'20.2%22N+139%C2%B041'04.8%22E/@35.6055955,139.6497194,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6056013!4d139.6846534",
"global scientific information and computing center":"https://www.google.com/maps/place/35%C2%B036'20.2%22N+139%C2%B041'04.8%22E/@35.6055955,139.6497194,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6056013!4d139.6846534",
"library":"https://www.google.com/maps/place/Tokyo+Institute+of+Technology+Library/@35.6063984,139.68306,18z/data=!3m1!4b1!4m5!3m4!1s0x6018f531bfbef27f:0x4f3bc391a397d081!8m2!3d35.6063984!4d139.6840261",
"main":"https://www.google.com/maps/place/35%C2%B036'16.1%22N+139%C2%B041'01.9%22E/@35.6044811,139.6751022,15z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6044824!4d139.6838569",
"centennial hall":"https://www.google.com/maps/place/35%C2%B036'24.9%22N+139%C2%B041'05.6%22E/@35.6069085,139.6499504,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6069141!4d139.684884",
"lecturehall":"https://www.google.ru/maps/place/35%C2%B036'16.0%22N+139%C2%B041'01.9%22E/@35.60443,139.6833168,19z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6044304!4d139.6838642",
"lecture theater":"https://www.google.com/maps/place/35%C2%B036'16.3%22N+139%C2%B040'56.3%22E/@35.6045284,139.6472956,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6045342!4d139.6823149",
"safety management":"https://www.google.com/maps/place/35%C2%B036'21.6%22N+139%C2%B040'54.6%22E/@35.6059814,139.6468176,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6059866!4d139.681837",
"70th anniversary auditorium":"https://www.google.com/maps/place/35%C2%B036'21.3%22N+139%C2%B041'00.8%22E/@35.6059164,139.6485256,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6059219!4d139.6835447",
"sports center":"https://www.google.com/maps/place/35%C2%B036'19.6%22N+139%C2%B040'56.3%22E/@35.6054424,139.6472916,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6054482!4d139.6823113",
"gymnasium":"https://www.google.com/maps/place/35%C2%B036'19.6%22N+139%C2%B040'56.3%22E/@35.6054424,139.6472916,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6054482!4d139.6823113",
"health service center":"https://www.google.com/maps/place/35%C2%B036'26.1%22N+139%C2%B041'01.3%22E/@35.6072424,139.6486846,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6072477!4d139.6837039",
"80th anniversary hall":"https://www.google.com/maps/place/35%C2%B036'25.5%22N+139%C2%B041'00.0%22E/@35.6070714,139.6483236,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6070767!4d139.6833428",
"tokyo tech front":"https://www.google.com/maps/place/35%C2%B036'26.8%22N+139%C2%B041'04.2%22E/@35.6074504,139.6494686,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6074556!4d139.6844877",
"environmental energy innovation":"https://www.google.com/maps/place/35%C2%B036'22.9%22N+139%C2%B040'50.4%22E/@35.6063414,139.6456436,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.606347!4d139.6806627",
"south lecture":"https://www.google.com/maps/place/35%C2%B036'08.9%22N+139%C2%B041'03.0%22E/@35.6024515,139.6492394,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6024568!4d139.6841734",
"ishikawadai lab 1":"https://www.google.com/maps/place/35%C2%B036'06.1%22N+139%C2%B041'03.3%22E/@35.6016814,139.6492336,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6016865!4d139.684253",
"international house":"https://www.google.com/maps/place/35%C2%B036'01.0%22N+139%C2%B041'03.5%22E/@35.6002734,139.6492956,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6002789!4d139.684315",

"library":"https://www.google.com/maps/place/35%C2%B036'23.0%22N+139%C2%B041'02.5%22E/@35.6063824,139.6490934,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6063883!4d139.6840266",
"midorigaoka lecture":"https://www.google.com/maps/place/35%C2%B036'28.5%22N+139%C2%B040'45.7%22E/@35.6079114,139.6443346,13z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d35.6079171!4d139.6793542"}
         building_pic={"administration bureau 1":"https://www.dropbox.com/s/nvdzun2bhcw2pe4/Administration%20buraeu%201.jpg?raw=1",
"administration bureau 2":"https://www.dropbox.com/s/nvdzun2bhcw2pe4/Administration%20buraeu%201.jpg?raw=1",
"administration bureau 3":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
"administration bureau 4":"https://www.dropbox.com/s/l13gdtmicx9jqnd/Administration%20buraeu%204.jpg?raw=1",
"administration bureau 5":"https://www.dropbox.com/s/l13gdtmicx9jqnd/Administration%20buraeu%204.jpg?raw=1",
"gsic":"https://www.dropbox.com/s/yldh85w4jqvhlf9/Gsic.jpg?raw=1",
"global scientific information and computing center":"https://www.dropbox.com/s/yldh85w4jqvhlf9/Gsic.jpg?raw=1",
"library":"https://www.dropbox.com/s/i7l5utqtr7jfs0r/library.jpg?raw=1",
"main":"https://www.dropbox.com/s/gknlyhdaxw5mfdj/main%20building.jpg?raw=1",
"centennial hall":"https://www.dropbox.com/s/09d2j66275rgjkc/centennial%20hall.jpg?raw=1",
"lecturehall":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
#WEST
"lecture theater":"https://www.dropbox.com/s/6pjc3kpx7vt5ps3/West%20lecture%201.jpg?raw=1",
"safety management":"https://www.dropbox.com/s/oksvyk1f72bu3g8/Environmental%20safety%20management.jpg?raw=1",
"70th anniversary auditorium":"https://www.dropbox.com/s/njdrmcugxqeqoux/70th%20anniversary%20Auditorium.jpg?raw=1",
"sports center":"https://www.dropbox.com/s/0o3d513711z9nmb/sport%20hall.jpg?raw=1",
"gymnasium":"https://www.dropbox.com/s/0o3d513711z9nmb/sport%20hall.jpg?raw=1",
#NORTH
"health service center":"https://www.dropbox.com/s/dm720e5f02ha85v/Health%20service%20center.jpg?raw=1",
"80th anniversary hall":"https://www.dropbox.com/s/xxionlp5qap7eaz/80th%20anniversary%20hall.jpg?raw=1",
"tokyo tech front":"https://www.dropbox.com/s/0m7nqghbm5p6ase/Tokyo%20Tech%20Front.jpg?raw=1",
"environmental energy innovation":"https://www.dropbox.com/s/lj2o0e03bagwe5k/EEI.jpg?raw=1",
#South
"south lecture":"https://www.dropbox.com/s/ihn336paj1hgq1i/logo.jpg?raw=1",
#Ishikawadai
"ishikawadai lab 1":"https://www.dropbox.com/s/s23kuxfp9dn78w2/Ishikawadai%20lab%201.jpg?raw=1",
"international house":"https://www.dropbox.com/s/uu9ghsxbu1d9zfl/International%20house.jpg?raw=1",
#Midorigaoka
"midorigaoka lecture":"https://www.dropbox.com/s/ftys9nu05813xqd/Midorigaoka%20lecture.jpg?raw=1"}
         web={"administration bureau 1":"https://www.titech.ac.jp/english/about/overview/administration/",
"administration bureau 2":"https://www.titech.ac.jp/english/about/overview/administration/",
"administration bureau 3":"https://www.titech.ac.jp/english/about/overview/administration/",
"administration bureau 4":"https://www.titech.ac.jp/english/about/overview/administration/",
"administration bureau 5":"https://www.titech.ac.jp/english/about/overview/administration/",
"gsic":"http://www.gsic.titech.ac.jp/en",
"global scientific information and computing center":"http://www.gsic.titech.ac.jp/en",
"library":"https://www.libra.titech.ac.jp/en",
"main":"https://www.titech.ac.jp/english/about/campus_maps/campus_highlights/main.html",
"centennial hall":"https://www.titech.ac.jp/english/about/campus_maps/campus_highlights/museum.html",
"lecturehall":"https://www.titech.ac.jp/english/enrolled/facilities/rooms/",
#WEST
"lecture theater":"https://www.titech.ac.jp/english/news/2015/031639.html",
"safety management":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"70th anniversary auditorium":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
"sports center":"https://www.titech.ac.jp/english/enrolled/facilities/sports.html",
"gymnasium":"https://www.titech.ac.jp/english/enrolled/facilities/sports.html",
#NORTH
"health service center":"https://www.titech.ac.jp/english/about/organization/institute_wide_support_centers/organization01.html",
"80th anniversary hall":"http://www.iad.titech.ac.jp/80th/english/",
"tokyo tech front":"http://www.somuka.titech.ac.jp/ttf/",
"environmental energy innovation":"https://www.titech.ac.jp/english/research/featured/environmental.html",
#South
"south lecture":"https://www.titech.ac.jp/english/maps/ookayama/ookayama.html",
#Ishikawadai
"ishikawadai lab 1":"https://www.titech.ac.jp/english/maps/ookayama/ishikawadai.html",
"international house":"http://www.iad.titech.ac.jp/accommodations/english/",
#Midorigaoka
"midorigaoka lecture":"https://www.titech.ac.jp/english/maps/ookayama/midorigaoka.html"}
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

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    sticker_ids = [ 2, 4, 10, 11, 13, 14, 15, 100, 103, 106,
                   107, 114, 115, 119, 120, 122, 124, 125,
                   126, 130, 134, 402]
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
    pass
  #   message_content = line_bot_api.get_message_content(event.message.id)
#     with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
#         for chunk in message_content.iter_content():
#             tf.write(chunk)
#         tempfile_path = tf.name
# 
#     dist_path = tempfile_path + '-' + event.message.file_name
#     dist_name = os.path.basename(dist_path)
#     os.rename(tempfile_path, dist_path)
# 
#     line_bot_api.reply_message(
#         event.reply_token, [
#             TextSendMessage(text='Save file.'),
#             TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
#         ])


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
        TextSendMessage(text='TiTAX joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Good bye. I hope see you again")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        pass
    elif event.postback.data == 'datetime_postback':
        pass
    elif event.postback.data == 'date_postback':
        pass

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
