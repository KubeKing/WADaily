#Created by Trey W.
import PyPDF2
from datetime import datetime
from lxml import html
import requests
import json
pdfFileObj = open('Schedule.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
year = int(datetime.now().year)
day = str(datetime.now().day)
weekdays = {'0':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}
months = {'1':'January','2':'February','3':'March','4':'April','5':'May',
'6':'June','7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
month = months[str(datetime.now().month)]
weekday = weekdays[str(datetime.today().weekday())]
date = (month+' '+day+' '+str(year))
storedSchedule = eval(open('ScheduleDictStorage.txt', 'r').read())
def validate():
    try:
        if storedSchedule['lastUpdate'] == date:
            validate = True
        else:
            validate = False
    except:
        validate = False
    return(validate)
def getLunch():
    foodList = []
    try:
        page = requests.get('https://www.woodward.edu/parents/menu')
        tree = html.fromstring(page.content)
        for x in range(0,5):
            food = str((tree.xpath('//div[@class="fsNotes"]/p/text()')[x]))
            foodList.append(food)
    except:
        foodList.append('Error connecting to Woodward Servers')
    return(foodList)
def whiteList():
    numbers = []
    for x in range(0,35):
        numbers.append(str(x))
    strings = ['August', 'September', 'October', 'November', 'December', 'January',
    'February', 'March', 'April', 'May', 'June', 'July', str(year), str(year-1), str(year+1),
     'DAY', 'XDAY', 'SPECIAL','ODD','EVEN']
    whiteList = strings + numbers
    return(whiteList)
def gatherText():
    allowed = whiteList()
    rawText = ''
    allText = []
    for x in range(0,pdfReader.numPages):
        pageObj = pdfReader.getPage(x)
        rawText = ((pageObj.extractText())+(rawText))
    rawText = rawText.replace('\n', '')
    rawText = rawText.replace('-', '')
    rawText = rawText.replace(',', '')
    textList = rawText.split(' ')
    for x in range(0,len(textList)):
        if textList[x] in allowed:
            allText.append(textList[x])
    return(allText)
def createSchedule():
    text = gatherText()
    schedule = {'lastUpdate':date}
    speicals = ['XDAY','SPECIAL','ODD','EVEN']
    for x in range(0,len(text)):
        if text[x] == 'DAY':
            add = {(text[x+2]+' '+text[x+3]+' '+text[x+4]):(text[x]+' '+text[x+1])}
            schedule.update(add)
        if text[x] in speicals:
            add = {(text[x+1]+' '+text[x+2]+' '+text[x+3]):(text[x])}
            schedule.update(add)
    with open('ScheduleDictStorage.txt', 'w') as file:
        file.write(json.dumps(schedule))
    file.close()
    return(schedule)
def whatDay(m,d,y):
    if validate() == False:
        schedule = createSchedule()
    else:
        schedule = storedSchedule
    try:
        day = schedule[m+' '+d+' '+y]
    except:
        day = 'Error'
    return(day)
def finalPrint():
    xy = whatDay(month,day,str(year))
    foodList = getLunch()
    final = ''
    if xy == 'Error':
        dayPrint = ('Can not find out the day.\nError no key stored as '+month+' '+day+' '+str(year))
    else:
        if xy == 'ODD' or xy == 'EVEN':
            dayPrint = ('Today is '+weekday+' and it\'s an '+xy+' rotation.')
        else:
            dayPrint = ('Today is '+weekday+' and it\'s a '+xy+' rotation.')
    if foodList[0] == 'Error connecting to Woodward Servers':
        foodPrint = (foodList[0])
    else:
        foodPrint = ('The lunch is: '+foodList[0]+', '+foodList[1]+', '+foodList[2]+', '+foodList[3]+', '+foodList[4])
    final = (dayPrint+'\n'+foodPrint)
    return(final)
print(finalPrint())
