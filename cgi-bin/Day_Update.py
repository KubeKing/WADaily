#!/home/jamwal77/opt/python-3.6.2/bin/python3
#Created by Trey W.
import PyPDF2
import requests
import json
from datetime import datetime, date
from lxml import html

year = int(datetime.now().year)
day = str(datetime.now().day)
weekdays = {'0':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}
months = {'1':'January','2':'February','3':'March','4':'April','5':'May',
'6':'June','7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
inv_months = {v: k for k, v in months.items()}
month = months[str(datetime.now().month)]
weekday = weekdays[str(datetime.today().weekday())]
date = [(month),(day),(str(year))]
storedSchedule = eval(open('ScheduleDictStorage.txt', 'r').read())

def getLongDate(x):
    date = x.timetuple()
    year = str(date.tm_year)
    month = str(date.tm_mon)
    day = str(date.tm_mday)
    return([(months[month]),(day),(str(year))])

def getLunch():
    foodList = []
    page = requests.get('https://www.woodward.edu/parents/menu')
    tree = html.fromstring(page.content)
    try:
        for x, y in enumerate('//div[@class="fsNotes"]/p/text()'):
            try:
                food = str((tree.xpath('//div[@class="fsNotes"]/p/text()')[x]))
                if food in foodList:
                    return(foodList)
                else:
                    foodList.append(food)
            except:
                return('')
    except:
        return('')
    return(foodList)

def getAun():
    try:
        page = requests.get('https://www.woodward.edu/parents/upper-school/newsletter')
        tree = html.fromstring(page.content)
        dates = []
        aunList = []
        for x in range(5):
            try:
                dates.append(tree.xpath('//*[@id="fsEl_24434"]/div/div[2]/div[1]/article['+str(x+1)+']/time/span[2]/text()')[0])
            except:
                break
        for x, y in enumerate(dates):
            aunList.append((tree.xpath('//*[@class="fsDayContainer"]/article/div/a[1]/text()')[x]))
        if dates[0] == day:
            return(aunList)
        else:
            return('')
    except:
        return('')

def whatDay(m,d,y):
    try:
        day = storedSchedule[m+' '+d+' '+y]
    except KeyError as error:
        day = 'Key Error'
    except Exception as exception:
        day = 'Unknown Error'
    return(day)

def makeImage(rotation, scale):
    if rotation != 'Unknown Error' and rotation != '' and rotation != 'Key Error':
        if rotation == 'DAY 8' or rotation == 'DAY 9':
            image = {'src':('../images/'+rotation.replace(' ', '')+'.jpg'),'alt':rotation.replace(' ', ''),'width':str(353*scale),'height':str(604* scale),
            'bottomPadding':str((604* scale)/2)+'px'}
        elif rotation == 'XDAY':
            image = {'src':('../images/'+rotation.replace(' ', '')+'.jpg'),'alt':rotation.replace(' ', ''),'width':str(353* scale),'height':str(740* scale),
            'bottomPadding':str((740* scale)/2)+'px'}
        elif rotation == 'SPRING':
            image = {'src':('../images/'+rotation.replace(' ', '')+'.jpg'),'alt':rotation.replace(' ', ''),'width':str(401*0.5),'height':str(804*0.5),
            'bottomPadding':str((804* scale)/2)+'px'}
        elif rotation == 'EXAM REVIEW':
            image = {'src':('../images/EXAM_REVIEW.jpg'),'alt':'EXAM REVIEW','width':str(352* scale),'height':str(736* scale),
            'bottomPadding':str((736* scale)/2)+'px'}
        else:
            image = {'src':'../images/'+rotation.replace(' ', '')+'.jpg','alt':rotation.replace(' ', ''),'width':str(350* scale),'height':str(713* scale),
            'bottomPadding':str((713* scale)/2)+'px'}
        rotation = ('a '+rotation)
    else:
        image = {'src':'', 'bottomPadding':'-10px'}
    return(image)
