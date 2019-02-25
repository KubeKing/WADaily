#!/home/jamwal77/opt/python-3.6.2/bin/python3
#Created by Trey W.
import requests
import json
from ics import Calendar
from datetime import datetime, date, timedelta
from lxml import html
from PIL import Image

#year = int(datetime.now().year)
#month = months[str(datetime.now().month)]
#day = str(datetime.now().day)
#weekday = weekdays[str(datetime.today().weekday())]
#date = [(month),(day),(str(year))]
weekdays = {'0':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}
months = {'1':'January','2':'February','3':'March','4':'April','5':'May',
'6':'June','7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
inv_months = {v: k for k, v in months.items()}
months_abv = {'January':'Jan', 'February':'Feb'}
storedSchedule = eval(open('ScheduleDictStorage.txt', 'r').read())

def getLongDate(x):
    date = x.timetuple()
    year = str(date.tm_year)
    month = str(date.tm_mon)
    day = str(date.tm_mday)
    return([(months[month]),(day),(str(year))])

def getShortDate(m,d,y):
    return(datetime((int(y)), (int(inv_months[str(m)])), (int(d))))

def getLunch(d, m, y):
    try:
        with open('lunchList.json') as json_file: 
            data = json.load(json_file) 
            return(data[str(m)+'/'+str(d)+'/'+str(y)])
    except:
        try:
            c = Calendar(requests.get('https://woodward.finalsite.com/calendar/calendar_400.ics').text)
            c, foodDict = c.events, {}
            c.reverse()
            for item in c:
                if item.description:
                    dateMod = getLongDate(item.begin)
                    food = (item.description).split('\n')
                    food = [value for value in food if value != '']
                    foodDict[str(dateMod[0])+'/'+str(dateMod[1])+'/'+str(dateMod[2])] = food
            try:
                with open('lunchList.json', 'w') as outfile:
                    json.dump(foodDict, outfile)
                return(foodDict[str(m)+'/'+str(d)+'/'+str(y)])
            except:
                return('')
        except:
            return('')

def getAun(day):
    try:
        page = requests.get('https://www.woodward.edu/parents/upper-school/newsletter')
        tree = html.fromstring(page.content)
        aunDict = {}
        dates = tree.xpath('//span[@class="fsDay"]/text()')
        aunList = tree.xpath('//a[@class="fsCalendarEventLink"]/text()')
        for i in range(len(dates)):
            aunDict[dates[i]] = aunList[i]
        try:
            return(aunDict[str(day)])
        except:
            return('')
    except:
        return('')

def whatDay(m,d,y,doMath):
    try:
        longDate = [m,d,y]
        day = storedSchedule[m+' '+d+' '+y]
    except KeyError:
        if doMath == True:
            shortDate = getShortDate(m,d,y)
            if shortDate.weekday() == 6:
                longDate = getLongDate(shortDate + timedelta(days=-2))
                try:
                    day = storedSchedule[longDate[0]+' '+longDate[1]+' '+longDate[2]]
                except:
                    day = 'Key Error'
            elif shortDate.weekday() == 5 or shortDate.weekday() == '5':
                longDate = getLongDate(shortDate + timedelta(days=2))
                try:
                    day = storedSchedule[longDate[0]+' '+longDate[1]+' '+longDate[2]]
                except:
                    day = 'Key Error'
            else:
                day = 'Key Error'
        else:
            day = 'Key Error'
    except:
        day = 'Unknown Error'
    return(day, longDate)

def makeImage(rotation, scale):
    if rotation != 'Unknown Error' and rotation != '' and rotation != 'Key Error':
        size = (Image.open('images/'+rotation.replace(' ', '')+'.jpg')).size
        image = {'src':('../images/'+rotation.replace(' ', '')+'.jpg'),'alt':rotation,'width':str(size[0]* scale),'height':str(size[1]* scale),
            'bottomPadding':str((size[1]* scale)/2)+'px','halfWidth':str((size[0]* scale)/2)}
        rotation = ('a '+rotation)
    else:
        image = {'src':'', 'bottomPadding':'-10px', 'halfWidth':'0', 'height':'0'}
    return(image)

def week_range(date):
    weekData = {'rotations': [], 'misc': {}}
    year, week, dow = date.isocalendar()
    if dow == 7:
        start_date = date
    else:
        start_date = date - timedelta(dow)

    n = start_date + timedelta(1)
    for i in range(5):
        try:
            loDa = getLongDate(n)
            x = {'rotation':(makeImage((whatDay(loDa[0], loDa[1], loDa[2], False))[0], 0.65)), 'day':weekdays[str(n.weekday())][:3]}
            if x['rotation']['src']:
                weekData['rotations'].append(x)
        except:
            pass
        n = n + timedelta(1)
    tallest = 0
    days = weekData['rotations']
    for i in days:
        try:
            if float(i['rotation']['height']) > tallest:
                tallest = float(i['rotation']['height'])
        except:
            pass
    for i in days:
        i['rotation']['bottomPadding'] = ((str((tallest - float(i['rotation']['height']))/2))+'px')
    weekData['misc']['tallest'] = ((str(tallest/2))+'px')
    return(weekData)

if __name__ == "__main__":
    print(getLunch('25', 'February', '2019'))