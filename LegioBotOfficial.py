#Legio Bot
#Made By:CookiEvee
from apscheduler.schedulers.background import BackgroundScheduler
#Module for scheduling tasks on a specific time(used for updating data dumps)
from datetime import *
#handling datetime data types
from discord.ext import commands
#Discord module to interact with the discord api
from pymongo import *
#Mongo Client
from time import *
#used for time.sleep()
from urllib.error import URLError, HTTPError
#urllib error catches errors in urllib

import asyncio
#asyncio integrates with discord in allowing multiple commands to be run at once using asyncio.sleep()
import aiofiles
import aiohttp
#handles files asyncroniously
import calendar
#allows showing the current date
import csv
#deals with csvs
import discord
#discord module(backs on previous one)
import gzip
#unzips gzip filetypes
import math
#math functions
import os
#os functions(file sizes)
import random
#generate random numbers(sev's trigger)
import shutil
#copying objects
import time
#time
import urllib.request
#urllib retrieves data from url's
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import *
#xml Etree is used to parse XML data
time.sleep(20)
os.chdir('/home/ubuntu/Legio_Bot')
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'CaveDweller or cookieveenpo@gmail.com')]
urllib.request.install_opener(opener)
#sets the user agent for all urlopenings
client=MongoClient()
db=client.admin
invent=db.inventory
#MongoDB settings
OP=[]
OPFile=[]
#lists for OP commands
help=None
#allows creation of command called help
coupregion = ['*the* Pacific', 'The South Pacific', 'The North Pacific', 'The East Pacific', 'The West Pacific', 'Osiris', 'Balder', 'The Rejected Realms', 'Lazarus']
sevlist=['The NPO severs fascist ties to the Pacifics.','Did you know that he came from several regions?',"Have you seen Sev lately? I feel like he hasn't been very expressev.",]
#lists for the sev trigger
currentid=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?q=lasteventid').read().decode('utf-8')
currentidtree=ET.fromstring(currentid)
currentidtext=currentidtree[0].text
#current event id(for the checksinc auto=mand
def update():
    urllib.request.urlretrieve('https://www.nationstates.net/pages/regions.xml.gz', 'regions.xml.gz')
    #pulls region data dump from site
    with gzip.open('regions.xml.gz', 'rb') as f_in:
        with open('region.xml', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    #unzips region datadump
    names = []
    numnation = []
    nations=[]
    tree = ET.parse('region.xml')
    root = tree.getroot()
    ExecList = []
    #parses the region datadump and gets a root to file through
    
    for region in root.findall('REGION'):
        name = region.find('NAME').text
        number = region.find('NUMNATIONS').text
        nations.append({'Region Name':name,'Number of Nations':number})
        numnation.append(number)
        if 'X' in region.find('DELEGATEAUTH').text:
            ExecList.append(name)
    invent.update({'ExecList':{'$exists':True}},{'ExecList':','.join(ExecList)},upsert = True)
    #adds region name and number of nations to dictionary,adds number of nations to list
    prevminor = int(invent.find_one({'PrevMinor':{'$exists':True}})['PrevMinor'])
    numnation = list(map(int, numnation))
    totalnations = sum(numnation)
    prevmajor = int(root[-1][13].text)-int(root[0][13].text)
    secminor = prevminor/totalnations
    secmajor = prevmajor/totalnations
    #calculates how long the previous major took, and splits numnation list into a list with integers rather than strings
    #also calculates total number of nations
    #works out how long the major and minor took per nation
    for i in range(0, len(numnation)):
        nations[i]['Cumulative Nations'] = sum(numnation[0:(i+1)])
        nations[i]['Major Update Time'] = (sum(numnation[0:(i+1)])*secmajor)/86400
        nations[i]['Minor Update Time'] = ((sum(numnation[0:(i+1)])*secminor)+43200)/86400
    #calculates cumulative andupdate times      

    with open('Sheet.csv', 'w', newline='') as csvfile:
        fieldnames = ['Region Name', 'Number of Nations','Cumulative Nations','Major Update Time','Minor Update Time',"Total Nations","Prev Major","Sec/Nation Maj","Prev Minor","Sec/Nation Min"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in nations:
            if nations.index(i)!=0:
                writer.writerow({'Region Name': i['Region Name'],'Number of Nations': i['Number of Nations'],'Cumulative Nations':i['Cumulative Nations'],'Major Update Time':i['Major Update Time'],'Minor Update Time':i['Minor Update Time']})
            else:
                writer.writerow({'Region Name': i['Region Name'],'Number of Nations': i['Number of Nations'],'Cumulative Nations':i['Cumulative Nations'],'Major Update Time':i['Major Update Time'],'Minor Update Time':i['Minor Update Time'],"Total Nations":totalnations,"Prev Major":prevmajor,"Sec/Nation Maj":secmajor,"Prev Minor":prevminor,"Sec/Nation Min":secminor})            
        #writes csv file   
def minortext():
    with open('Sheet.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        file=list(reader)
        first = file[0]['Region Name']
        last = file[-1]['Region Name']
    #finds first and last regions    

    firstupdate = urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?region={}&q=lastupdate'.format(first.replace(" ", "_")))
    firstupdate = firstupdate.read().decode("utf-8")
    tree = ET.fromstring(firstupdate)
    first = int(tree[0].text)

    lastupdate = urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?region={}&q=lastupdate'.format(last.replace(" ", "_")))
    lastupdate = lastupdate.read().decode("utf-8")
    tree = ET.fromstring(lastupdate)
    last = int(tree[0].text)
    #finds update time of first and last regions
    minorvalue = last-first
    
    invent.update({'PrevMinor':{'$exists':True}},{'PrevMinor':minorvalue},upsert = True)
    #calculates minor time and inputs it to database
                  

scheduler = BackgroundScheduler()
scheduler.add_job(update, 'cron', hour=7, minute=30, second=0)
scheduler.add_job(minortext, 'cron', hour=19, minute=0, second=0)
#schedules the 2 jobs to occur every day
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
#sets prefix and removes the default help command
async def Endorsing():
    await bot.wait_until_ready()
    #waits till bot is ready to run
    while True:
        try:
            channel=bot.get_channel(537349388096503808)
            #sets channel to output to
            CurrentEndos=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?nation=east_durthang&q=endorsements')
            OpenEndos=CurrentEndos.read().decode("utf-8")
            EndoTree=ET.fromstring(OpenEndos)
            CurrentString=EndoTree[0].text
            Current=CurrentString.split(',')
            #gets the list of endorsers on the emperor
            Old=invent.find_one({'EmperorEndos':{'$exists':True}})['EmperorEndos']
            #gets the list of people who endorsed the emperor 1 hour ago
            Change=set(Old)-set(Current)
            IterChange=set(Old)-set(Current)
            #calculates change
            invent.update({'EmperorEndos':{'$exists':True}},{'EmperorEndos':Current})
            #writes the new list to the file
            if len(list(Change)) ==0:
                pass
            #if empty nothing happens
            else:
                for nation in IterChange:
                    try:
                        Open1 = urllib.request.urlopen(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=region')
                        Open2 = Open1.read().decode("utf-8")
                        Regiontree=ET.fromstring(Open2)
                        Region=Regiontree[0].text
                        if Region != 'the Pacific':
                            Change.remove(nation)
                        #if region isn't in the pacific it's removed from change list
                    except HTTPError as e:
                        if hasattr(e, 'code'):
                            Change.remove(nation)
                    #if nations has CTE'd it's removed from list
                if len(list(Change))!=0:
                    await channel.send(f'Nations recently unendorsed the Emperor:{" ".join(list(Change))}\n-------------')
            await asyncio.sleep(3600)
            #list sent then occurs every hour
        except URLError:
            pass
async def WAMovement():
    await bot.wait_until_ready()
    #waits till bot is ready to run
    while True:
        try:
            channel=bot.get_channel(537349426675712010)
            Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=members')
            Open=Req.read().decode("utf-8")
            WATree=ET.fromstring(Open)
            WA=WATree[0].text.split(",")
            #calculates list of WA nations
            Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?region=the_pacific&q=nations')
            Open=Req.read().decode("utf-8")
            EndoTree2=ET.fromstring(Open)
            Nations=EndoTree2[0].text.split(":")
            #calculates nations in TP
            WANations=set(Nations) & set(WA)
            CurrentString= ",".join(WANations)
            OldWAFile=invent.find_one({'WAS':{'$exists':True}})['WAS']
            OldWA=OldWAFile.split(',')
            #calculates old and new WANations in TP
            Change=set(OldWA)-set(WANations)
            IterChange=set(OldWA)-set(WANations)
            invent.update({'WAS':{'$exists':True}},{'WAS':','.join(WANations)})
            #calculates changes and writes new file
            if len(list(Change)) ==0:
                pass
            else:
                for nation in IterChange:
                    try:
                        Open1 = urllib.request.urlopen(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=region')
                        Open2 = Open1.read().decode("utf-8")
                        Regiontree=ET.fromstring(Open2)
                        Region=Regiontree[0].text
                        if Region != 'the Pacific':
                            Change.remove(nation)
                    except HTTPError as e:
                        if hasattr(e, 'code'):
                            Change.remove(nation)
                if len(list(Change)) != 0:
                    await channel.send(f'Nations recently unsubscribed from WA:{" ".join(list(Change))}\n-------------')
            await asyncio.sleep(3600)
            #outputs list of WA nations in the pacific resently unWAd
        except URLError:
            pass
    
async def WA():
    await bot.wait_until_ready()
    channel=bot.get_channel(537349288678785055)
    #waits till bot is ready and gets channel
    while not bot.is_closed():
        try:
            WA=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=resolution')
            OpenWA=WA.read().decode("utf-8")
            WATree=ET.fromstring(OpenWA)
            #finds GA resolution
            WA=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?wa=2&q=resolution')
            OpenWA=WA.read().decode("utf-8")
            WATree2=ET.fromstring(OpenWA)
            #finds SC resolution
            try:
                Security=invent.find_one({'Security':{'$exists':True}})['Security']
                if Security!= WATree2[0][3].text:
                    invent.update({'Security':{'$exists':True}},{'Security':WATree2[0][3].text})
                    await channel.send("**NEW SC PROPOSAL**\nLink: https://www.nationstates.net/page=sc \nName: {}".format(WATree2[0][4].text))
                    #if new security resolution then output the new resolution
            except:
                pass

            try:
                General=invent.find_one({'General':{'$exists':True}})['General']
                if General!= WATree[0][3].text:
                    invent.update({'General':{'$exists':True}},{'General':WATree[0][3].text})
                    await channel.send("**NEW GA PROPOSAL**\nLink: https://www.nationstates.net/page=ga \nName: {}".format(WATree[0][4].text))
                    #if new security resolution then output the new resolution
            except:
                pass
            await asyncio.sleep(600)
        except URLError:
            pass

async def UpdateTime(ctx,Name,Time,counter,Maj,Update):
    try:
        TimeZone = datetime.utcnow() + timedelta(hours=-4)
        TimeZone = int(TimeZone.strftime("%H"))*3600 + int(TimeZone.strftime("%M"))*60 + int(TimeZone.strftime("%S"))
        CurrentTime=timedelta(seconds=TimeZone)
        Add=0
        count=1
        timer=15
        try:
            if Time[-1] == 'm':
                timer=int(Time[0:-1])*60
            elif Time[-1] == 's':
                timer=int(Time[0:-1])
            else:
                timer=int(Time[2])
            try:
                counter=int(counter)
            except:
                counter=4
        except:
             pass
        #calculates time of trigger
        with open('Sheet.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            file=list(reader)
        Cumulative=[]
        Done=False
        for i in file:
            if Name.lower() == i['Region Name'].lower().replace(" ","_") and Done==False:
                row=file.index(i)
                Done=True
            NationMed=i['Cumulative Nations']
            Cumulative.append(int(NationMed))
            #list of cumulative nations
        if Maj == 'Major Update Time':
            myNumber = (int(file[row]['Cumulative Nations']) * float(file[0]['Sec/Nation Maj'])-timer)/float(file[0]['Sec/Nation Maj'])
        else:
            myNumber = (int(file[row]['Cumulative Nations']) * float(file[0]['Sec/Nation Min'])-timer)/float(file[0]['Sec/Nation Min'])
        Cumulative.append(float(myNumber))
        Cumulative.sort()
        #sorts nations 
        Start=Cumulative.index(myNumber)
        GCRStart=Start
        Cumulative.remove(myNumber)
        #finds index of trigger
        TriggerTime = timedelta(seconds=float(file[row][Maj])*86400)
        TriggerTime = timedelta(seconds=math.ceil(TriggerTime.total_seconds() ))

        if TriggerTime<CurrentTime:
            TrigTime = TriggerTime+timedelta(days=1)
        else:
            TrigTime=TriggerTime
        #makes sure trigger time is on the right day
        await ctx.send("**...Trigger Setting...**\nUpdate: {4}\nTarget: https://www.nationstates.net/region={0}\nTarget Update Time: {1}\nTrigger Time: {2} Seconds\nApproximate  Time Till Target Updates: {3}\n\nSuggested Triggers:\n ".format(file[row]['Region Name'].replace(" ","_"),TriggerTime,timer,(TrigTime-CurrentTime),Update))
        while count<=counter:
            if int(file[Start]['Number of Nations']) <= 50:
                count+=1
                FirstName = file[Start]['Region Name'].replace(" ","_")
                if Update=='Major':
                    FirstTime= timedelta(seconds = float(file[Start][Maj])*86400)
                else:
                    FirstTime= timedelta(seconds = float(file[Start][Maj])*86400)
                if int(file[Start]['Number of Nations']) <= 5:
                    Tag="Miniscule"
                elif int(file[Start]['Number of Nations']) <=10:
                    Tag="Small"
                elif int(file[Start]['Number of Nations']) <=50:
                    Tag="Medium"
                await ctx.send("Link: https://www.nationstates.net/region={0}\nUpdate Time: {1}\nSize Tag: {2}\n-----\n".format(file[Start]['Region Name'].replace(" ","_"),timedelta(seconds=float(file[Start][Maj])*86400),Tag))
                Start-=1
            else:
                Start-=1
        #goes through list and finds trigger,and calculates size
        
        GCR=((int(file[row]['Cumulative Nations'])*float(file[0][Maj]))-120)/float(file[0][Maj])         

        Cumulative.append(GCR)
        Cumulative.sort()
        Start=Cumulative.index(GCR)
        Cumulative.remove(GCR)
        #dictates if there's a gcr in the way
        for i in range(GCRStart-1,row):
            if int(file[i]['Number of Nations'])>1500:
                await ctx.send("⚠ There is an GCR between the trigger and the target. {0} updates at {1}, {2} before your target. Please allow for variance ⚠ ".format(file[1]['Region Name'],timedelta(seconds=float(file[i][maj]*86400)),TriggerTime-(timedelta(seconds=float(file[i][maj])*86400)))) 
    except ValueError:
        await ctx.send("There are none suggested, this may be because:\n -The trigger is too long- if so  please select a shorter trigger and try again.\n -The target updates too early- if so proceed with a blind jump.")
    except UnboundLocalError:
        await ctx.send("Region not found, please try again. Please check you have spelt it correctly and that the target has not CTE. If this is still a problem please contact @CookiEvee#7944.")
        
async def checksinc():
    await bot.wait_until_ready()
    global currentidtext
    while True:
        try:
            ctx=bot.get_channel(535209653139931176)
            currentidtext=await checkbase(ctx,currentidtext,';sinceid='+currentidtext,False)
            await ctx.send('AutoMand over, next in one hour')
        except:
            pass
        await asyncio.sleep(3600)
async def checkbase(ctx,ids,link,move):
        #waits till bot works then gets channel
        Req1 = urllib.request.Request("https://www.nationstates.net/cgi-bin/api.cgi?q=happenings;view=region.the_pacific;filter=founding"+link)
        #checks since last id call
        Open1 = urllib.request.urlopen(Req1)
        Open2 = Open1.read().decode("utf-8")    
        tree = ET.fromstring(Open2)
        nonew = tree.find('HAPPENINGS/EVENT')
        if nonew==None:
            await ctx.send('No new nations have been founded')
        else:
            skip=0
            #checks happenings
            ids = tree.find('HAPPENINGS/EVENT').get('id')
            nation = tree.findall('HAPPENINGS/EVENT/TEXT')
            #checks happenings
            #gets currrentid to start next tag
            for n in nation:
                nationname = n.text.partition('@@')[-1].rpartition('@@')[0]
                try:
                    time.sleep(0.01)
                    Req1 = urllib.request.Request("https://www.nationstates.net/cgi-bin/api.cgi?nation=" + nationname)
                    try:
                        time.sleep(0.01)
                        Open1 = urllib.request.urlopen(Req1)
                        Open2 = Open1.read().decode("utf-8")    
                    except HTTPError as e:
                        if hasattr(e, 'code'):
                            await ctx.send("Nation " + nationname + " has ceased to exist.")
                            #if cte'd say it ceased to exist
                    else:
                        tree = ET.fromstring(Open2)
                        fullname = tree.find('FULLNAME')
                        unstatus = tree.find('UNSTATUS')
                        endos1 = tree.find('ENDORSEMENTS')
                        endos2 = str(str(endos1.text).count(",") + 1)
                        region = tree.find('REGION')
                        natflag = tree.find('FLAG')
                        motto = tree.find('MOTTO')
                        animal = tree.find('ANIMAL')
                        currency = tree.find('CURRENCY')
                        religion = tree.find('RELIGION')
                        demonym = tree.find('DEMONYM')    
                        demonym2 = tree.find('DEMONYM2')
                        demonym2p = tree.find('DEMONYM2PLURAL')
                        if region.text != "the Pacific" :
                            if move:
                                skip+=1
                            else:
                                await ctx.send ("**Nation " + nationname + " has moved to " + region.text + "**")
                        elif unstatus.text == "Non-member" :
                            await ctx.send("**" + fullname.text + "**" + "\n"
                                           "https://www.nationstates.net/nation=" + nationname + "\n"
                                           "**WA Status: **" + unstatus.text + "\n"
                                           "**Region:** " + region.text + "\n"
                                           "**Flag:** " + natflag.text + "\n"
                                           "**Motto:** " + motto.text + "\n"
                                           "**Animal:** " + animal.text + "\n"
                                           "**Currency:** " + currency.text + "\n"
                                           "**Demonyms:** " + demonym.text + ", " + demonym2.text + ", " + demonym2p.text)
                        elif int(endos2) > 10:
                            await ctx.send("**" + fullname.text + "**" + "\n"
                                           "https://www.nationstates.net/nation=" + nationname + "\n"
                                           "**WA Status: **" + unstatus.text + "** | Endorsements:** " + endos2 + "\n"
                                           "**Region:** " + region.text + "\n"
                                           "**Flag:** " + natflag.text + "\n"
                                           "**Motto:** " + motto.text + "\n"
                                           "**Animal:** " + animal.text + "\n"
                                           "**Currency:** " + currency.text + "\n"
                                           "**Demonyms:** " + demonym.text + ", " + demonym2.text + ", " + demonym2p.text + "\n"
                                           "**:warning: Nation has more than 10 endorsements. :warning: **")
           
                        else:
                            await ctx.send("**" + fullname.text + "**" + "\n"
                                           "https://www.nationstates.net/nation=" + nationname + "\n"
                                           "**WA Status: **" + unstatus.text + "** | Endorsements:** " + endos2 + "\n"
                                           "**Region:** " + region.text + "\n"
                                           "**Flag:** " + natflag.text + "\n"
                                           "**Motto:** " + motto.text + "\n"
                                           "**Animal:** " + animal.text + "\n"
                                           "**Currency:** " + currency.text + "\n"
                                           "**Demonyms:** " + demonym.text + ", " + demonym2.text + ", " + demonym2p.text)
                        time.sleep(0.3)
                        if region.text != "the Pacific" :
                            if move:
                                pass
                            else:
                                await ctx.send("**-----------------------------------------------**")
                        await asyncio.sleep(3)
                        #sends nation and it's flag demonyms etc...
                except:
                    await ctx.send(f'-----------\nhttps://www.nationstates.net/nation={nationname}\n----------')
            if move:
                await ctx.send(str(skip) + " out of " + str(str(nation).count(",") + 1) + " nations were skipped in this request because they no longer reside in the Pacific. To show these nation names, use !check instead.")
        #sets current id
        return(ids)        

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
#activates when logged in
@bot.command()
async def api(ctx):
    link=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?a=useragent')
    await ctx.send(link.read().decode("utf-8"))
#command for checking api

@bot.command()
@commands.has_any_role("Commander")
async def major(ctx,Name:str,Time:str,Count:int):
    await UpdateTime(ctx,Name,Time,Count,"Major Update Time","Major")
#calls the UpdateTime function for major
@major.error
async def major_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('An Argument was missing from the command, Please consult the !help command.')
#checks error

@bot.command()
@commands.has_any_role("Commander")
async def minor(ctx,Name:str,Time:str,Count:int):
    await UpdateTime(ctx,Name,Time,Count,"Minor Update Time","Minor")
#Update time for minor
@minor.error
async def minor_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('An Argument was missing from the command, Please consult the !help command.')
#error

@bot.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def endocap(ctx):
    Req=urllib.request.urlopen("https://www.nationstates.net/cgi-bin/api.cgi?region=the_pacific&q=censusranks;scale=66;mode=score")
    Open=Req.read().decode("utf-8")
    Tree=ET.fromstring(Open)
    FullCap=[]
    CapWrite=[]
    #calculates top 20 endorsements
    data = dict()
    for item in invent.find({'EndoCap':{'$exists':True}}):
        data.update(item['EndoCap'])
    #calculates endocaps
    for Nation in Tree[0][0].findall("NATION"):
        CapNations=[]
        EndoName=Nation.find('NAME').text
        Endos=Nation.find('SCORE').text
        if int(Endos)>10:
            if str(EndoName) in data:
                if int(Endos)<=int(data.get(str(EndoName))):
                    pass
                #if greater than 10 endos and is not over cap pass, else V
                else:
                    try:
                        FullCap.append(EndoName)
                        Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?nation={}&q=endorsements'.format(EndoName))
                        Open=Req.read().decode("UTF-8")
                        EndoTree=ET.fromstring(Open)
                        Capped=EndoTree[0].text
                        CapList=Capped.split(",")
                        CapList2=[]
                        for nation in CapList:
                            CapList2.append("https://www.nationstates.net/nation={}".format(nation))
                            CapNations.append(nation)
                        CapWrite.append("{} {}".format(EndoName,",".join(CapNations)))
                        await ctx.send("-----\nhttps://www.nationstates.net/nation={0} has been endorsed over the endocap by: {1}".format(EndoName," , ".join(CapList2[int(data.get(str(EndoName)))-1:])))
                        #calculates the endorsers and outputs the most recent endorsers who pushed them overcap
                        time.sleep(1)
                    except AttributeError:
                        pass
            else:
            #if not in the dictionary default at 10
                try:
                    FullCap.append(EndoName)
                    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?nation={}&q=endorsements'.format(EndoName))
                    Open=Req.read().decode("UTF-8")
                    EndoTree=ET.fromstring(Open)
                    Capped=EndoTree[0].text
                    CapList=Capped.split(",")
                    CapList2=[]
                    for nation in CapList:
                        CapList2.append("https://www.nationstates.net/nation={}".format(nation))
                        CapNations.append(nation)
                    CapWrite.append("{} {}".format(EndoName,",".join(CapNations)))
                    await ctx.send("-----\nhttps://www.nationstates.net/nation={0} has been endorsed over the endocap by: {1}".format(EndoName," , ".join(CapList2[10:])))
                        
                    time.sleep(1)
                except AttributeError:
                    pass
        else:
            break

    CapFile=invent.find({'PrevCap':{'$exists':True}})
    for line in CapFile:
        k=str(line['PrevCap'])[1:-1].partition(':')
        i=k[0].replace("'",'')
        CapList2=k[2].replace("'",'').replace(' ','').split(',')
        if i not in FullCap:
            Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?nation={}&q=endorsements'.format(i))
            Open=Req.read().decode("utf-8")
            EndoTree=ET.fromstring(Open)

            Capped=EndoTree[0].text
            if Capped != None:
                CapList=Capped.split(',')

                CapList2=i[2].split(',')

                Unique_Nations=set(CapList2) - set(CapList)
                Uniqe_Nations = []
                for x in Unique_Nations:
                    Uniqe_Nations.append("https://www.nationstates.net/nation={}".format(x))
                await ctx.send('-----\nhttps://www.nationstates.net/nation={} is no longer over the endorsement cap after losing the endorsements of:\n{}'.format(i," , ".join(Uniqe_Nations)))
            else:
                await ctx.send('-----\nhttps://www.nationstates.net/nation={} has resigned from the WA or lost all endorsements'.format(i))
    #calculates people no longer of the cap
    invent.remove({'PrevCap':{'$exists':True}})
    for i in CapWrite:
        a=i.partition(' ')
        invent.insert({'PrevCap':{a[0]:a[2]}})
    #writes ppl over the cap right now

@bot.command()
@commands.has_any_role('Praetorian Guard','Senator','Emperor')
async def notendo(ctx):
    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=members')
    Open=Req.read().decode("utf-8")
    WATree=ET.fromstring(Open)
    WA=WATree[0].text.split(",")
    #wa members
    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?region=the_pacific&q=nations')
    Open=Req.read().decode("utf-8")
    EndoTree2=ET.fromstring(Open)
    Nations=EndoTree2[0].text.split(":")
    #pacific nations
    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?nation=east_durthang&q=endorsements')
    Open=Req.read().decode('utf-8')
    EndoTree2=ET.fromstring(Open)
    Endorsed=EndoTree2[0].text.split(",")
    #endorsers of the emperor
    WANations=set(Nations) & set(WA)
    NotEndorsed=list(set(WANations)-set(Endorsed))
    NotEndorsed.remove('east_durthang')
    #calculates all WA nations in the pacific not endorsing the emperor
    Epoch=calendar.timegm(gmtime())
    message=await ctx.send(":hourglass: :hourglass_flowing_sand: :hourglass: \n*gathering data*\nPlease wait this could take 2-4 minutes")
    Month=int(date.today().month)
    if Month != int(invent.find_one({'Month':{'$exists':True}})['Month']):
        invent.update({'Month':{'$exists':True}},{'Month':Month})
        invent.remove({'TotalEndos':{'$exists':True}})
        invent.insert({'TotalEndos':''})
    #if there's a new month, all the fils reset
    EndoFile=open('EndoFile.txt','w')
    for nation in NotEndorsed:
        if nation not in (invent.find_one({'TotalEndos':{'$exists':True}})['TotalEndos']).split(' '):
            Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?nation={}&q=foundedtime'.format(nation))
            Open=Req.read().decode("utf-8")
            EndoTree2=ET.fromstring(Open)
            NationTime=int(EndoTree2[0].text)
            time.sleep(1)
            await asyncio.sleep(0.01)
            if Epoch-NationTime>172800:
                CurMonth=invent.find_one({'TotalEndos':{'$exists':True}})['TotalEndos']+' '+nation
                invent.update({'TotalEndos':{'$exists':True}},{'TotalEndos':CurMonth})
                EndoFile.write("\nhttps://www.nationstates.net/nation={}".format(nation))
                #if more than 2 days old it is added to the files

    EndoFile.close()

    if os.stat("EndoFile.txt").st_size == 0:
        await ctx.send("No new nations which aren't endorsing east_durthang this month.")
        #if got nothing in it no nations sent
    else:
        await ctx.send("WA Nations not endorsing east_durthang are in this file:")
        await ctx.send(file=discord.File('EndoFile.txt'))
    os.remove('EndoFile.txt')


@bot.command()
@commands.has_any_role('Praetorian Guard','Senator','Emperor')
async def fullnotendo(ctx,name):
    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=members')
    Open=Req.read().decode("utf-8")
    WATree=ET.fromstring(Open)
    WA=WATree[0].text.split(",")
    #wa members
    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?region=the_pacific&q=nations')
    Open=Req.read().decode("utf-8")
    EndoTree2=ET.fromstring(Open)
    Nations=EndoTree2[0].text.split(":")
    #nations in the pacific
    Req=urllib.request.urlopen(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={name}&q=endorsements')
    Open=Req.read().decode('utf-8')
    EndoTree2=ET.fromstring(Open)
    Endorsed=EndoTree2[0].text.split(",")
    #endorsers
    WANations=set(Nations) & set(WA)
    NotEndorsed=list(set(WANations)-set(Endorsed))
    NotEndorsed.remove(name)
    #calculates wa nations not endosing the person in tp
    message=await ctx.send(":hourglass: :hourglass_flowing_sand: :hourglass: \n*gathering data*\nPlease wait this could take 2-4 minutes")
    Epoch=calendar.timegm(gmtime())

    EndoFile=open('EndoFile.txt','w')

    for nation in NotEndorsed:
        try:
            Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?nation={}&q=foundedtime'.format(nation))
            Open=Req.read().decode("utf-8")
            EndoTree2=ET.fromstring(Open)
            NationTime=int(EndoTree2[0].text)
            time.sleep(1)
            await asyncio.sleep(0.01)

            if Epoch-NationTime>172800:
                EndoFile.write("\nhttps://www.nationstates.net/nation={}".format(nation))
            #if nation older than2  days old is added
        except:
            pass
    EndoFile.close()

    if os.stat("EndoFile.txt").st_size == 0:
        await ctx.send(f"No new nations which aren't endorsing {name} this month.")
    else:
        await ctx.send(f"WA Nations not endorsing {name} are in this file:")
        await ctx.send(file=discord.File('EndoFile.txt'))
    os.remove('EndoFile.txt')
    #files sent


@bot.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def topendo(ctx):
    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?region=the_pacific&q=censusranks;scale=66;mode=score')
    Open=Req.read().decode("utf-8")
    WATree=ET.fromstring(Open)
    NameList=[]
    #top 20
    for region in WATree[0][0].findall('NATION'):
        NameList.append("\n https://www.nationstates.net/nation={} {} endorsements".format(region.find("NAME").text.replace(" ","_"),region.find("SCORE").text))
    await ctx.send("Top 40 Endorsed Nations in The Pacific:{}".format("".join(NameList)))
    #calculates each nations endorsements
    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?region=the_pacific&q=censusranks;scale=66;mode=score&start=21')
    Open=Req.read().decode("utf-8")
    WATree=ET.fromstring(Open)
    NameList=[]

    for region in WATree[0][0].findall('NATION'):
        NameList.append("\n https://www.nationstates.net/nation={} {} endorsements".format(region.find("NAME").text.replace(" ","_"),region.find("SCORE").text))
    await ctx.send("\n{}".format("".join(NameList)))
    #same for next 20, then sends it



@bot.command()
@commands.has_any_role("Commander","Senator","Emperor")
async def tags(ctx,*,arg):
    ExecList=invent.find_one({'ExecList':{'$exists':True}})['ExecList'].split(',')
    arguments=arg.split(" ")
    for i in arguments:
        Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?q=regionsbytag;tags=-miniscule,-medium,-large,-password,{}'.format(i))
        Open=Req.read().decode("utf-8")
        EndoTree=ET.fromstring(Open)
        time.sleep(1)
        #checks by tag
        File=open('ListForU.txt','w')
        Lis=EndoTree[0].text.split(",")

        for i in Lis:
            if i in ExecList:
                File.write(f"https://www.nationstates.net/region={i}\n")

        File.close()
        await ctx.send(file=discord.File('ListForU.txt'))
        #sends file with list in
        os.remove('ListForU.txt')


#commands removed. for starting and ending radio silence
'''
@bot.command()
@commands.has_any_role("Commander","Senator","Emperor")
async def startradio(ctx):
    global Operator
    Guild=ctx.guild
    Operator=Guild.roles
    for i in Operator:
        if i.name=="Operator":
            Operator=i
            break
    Operato=Operator.permissions.send_messages=False
    await Operator.edit(permissions=Operator.permissions)


@bot.command()
@commands.has_any_role("Commander","Senator","Emperor")
async def endradio(ctx):
    global Operator
    Guild=ctx.guild
    Operator=Guild.roles
    for i in Operator:
        if i.name=="Operator":
            Operator=i
            break
    Operato=Operator.permissions.send_messages=True
    await Operator.edit(permissions=Operator.permissions)
'''

@bot.command()
@commands.has_any_role("Emperor")
async def notendorsing(ctx,name):
    await ctx.send(":hourglass: :hourglass_flowing_sand: :hourglass: \n*gathering data*\nPlease wait this could take 2-15 minutes")
    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=members')
    Open=Req.read().decode("utf-8")
    WATree=ET.fromstring(Open)
    WA=WATree[0].text.split(",")
    #wa members
    Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?region=the_pacific&q=nations')
    Open=Req.read().decode("utf-8")
    EndoTree2=ET.fromstring(Open)
    Nations=EndoTree2[0].text.split(":")
    #nations in TP
    WANations=list(set(Nations) & set(WA))
    File=open('ENDOTART!.txt','w')
    File.close()
    File=open('ENDOTART!.txt','a')
    Not=[]
    async with aiohttp.ClientSession(headers={'User-Agent':'Cavedweller or cookieveenpo@gmail.com'}) as session:
        for nation in WANations:
            async with session.get(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=endorsements') as resp:
                Endorsements=await resp.text()
                EndoTree=ET.fromstring(Endorsements)
                if EndoTree[0].text!=None:
                    Endoers=EndoTree[0].text.split(',')
                    if name in Endoers:
                        pass
                    else:
                        Not.append(nation)
                time.sleep(1)
        await session.close()
    for i in Not:
       File.write(f'https://www.nationstates.net/nation={i}\n')
    File.close()
    await ctx.send(file=discord.File('ENDOTART!.txt'))
    os.remove('ENDOTART!.txt')
    
@bot.command()
async def region(ctx, *, arg):
    Req1 = urllib.request.Request("https://www.nationstates.net/cgi-bin/api.cgi?region=" + arg.replace(" ", "_"))
    try:
        Open1 = urllib.request.urlopen(Req1)
        Open2 = Open1.read().decode("utf-8")    
    except HTTPError as e:
        if hasattr(e, 'code'):
            await ctx.send("Region not found.")
            #checks if region exists
    else:
        tree = ET.fromstring(Open2)
        regname = tree.find('NAME')
        numnations = tree.find('NUMNATIONS')
        founder = tree.find('FOUNDER')
        founder2 = founder.text
        if founder.text == "0":
            founder2 = "None"
        else:
            founder = tree.find('FOUNDER')
            founder2 = founder.text
            foundauth = tree.find('FOUNDERAUTH')
        power = tree.find('POWER')
        rflag = tree.find('FLAG')
        delegate = tree.find('DELEGATE')
        delegate2 = delegate.text
        if delegate.text == "0":
            delegate2 = "None"
            delvotes2 = "0"
            delauth = tree.find('DELEGATEAUTH')
            delauth2 = delauth.text
            llogin = "N/A"
            lastact = "N/A"
        else:
            delegate = tree.find('DELEGATE')
            delegate2 = delegate.text
            delvotes = tree.find('DELEGATEVOTES')
            delvotes2 = str(int(delvotes.text) - 1)
            delauth = tree.find('DELEGATEAUTH')
            delauth2 = delauth.text
            Req2 = urllib.request.Request("https://www.nationstates.net/cgi-bin/api.cgi?nation=" + delegate2)
            Open3 = urllib.request.urlopen(Req2)
            Open4 = Open3.read().decode("utf-8")
            tree = ET.fromstring(Open4)
            lastlogin = tree.find('LASTLOGIN')
            llogin = lastlogin.text
            lastactivity = tree.find('LASTACTIVITY')
            lastact = lastactivity.text
        if delauth2.startswith('X'):
            delauth3 = "Executive"
        else:
            delauth3 = "Non-Executive"
        #checks all options callibrates
       
        await ctx.send("**Region: " + regname.text + " | Population: **" + str(numnations.text) + "\n"
                       "**Link: **https://www.nationstates.net/region=" + arg.replace(" ", "_") + "\n"
                       "**Flag:** " + rflag.text + "\n"
                       "**Founder: **" + str(founder2).replace("_", " ").title() + "\n"
                       "**Delegate** (" + delauth3 + "): " + str(delegate2).replace("_", " ").title() + " (Last Active: " + lastact + ") ** | Endorsements: **" + delvotes2)
         #sends the region

@bot.command()
async def nation(ctx, *, arg):
    Req1 = urllib.request.Request("https://www.nationstates.net/cgi-bin/api.cgi?nation=" + arg.replace(" ", "_"))
    try:
        Open1 = urllib.request.urlopen(Req1)
        Open2 = Open1.read().decode("utf-8")
    except HTTPError as e:
        if hasattr(e, 'code'):
            await ctx.send("Nation not found.")
            #checks if nation exsits
    else:
        tree = ET.fromstring(Open2)
        fullname = tree.find('FULLNAME')
        unstatus = tree.find('UNSTATUS')
        endos1 = tree.find('ENDORSEMENTS')
        region = tree.find('REGION')
        natflag = tree.find('FLAG')
        motto = tree.find('MOTTO')
        animal = tree.find('ANIMAL')
        currency = tree.find('CURRENCY')
        religion = tree.find('RELIGION')
        demonym = tree.find('DEMONYM')    
        demonym2 = tree.find('DEMONYM2')
        demonym2p = tree.find('DEMONYM2PLURAL')
        lastactive = tree.find('LASTACTIVITY')
        founded = tree.find('FOUNDED')
        if unstatus.text == "Non-member" :
            if founded.text == "0":
                founded.text = "Antiquity"
                await ctx.send("**" + fullname.text + "** (Last active: " + lastactive.text + ")\n"
                               "**Founded: **" + founded.text + "\n"
                               "https://www.nationstates.net/nation=" + arg.replace(" ", "_") + "\n"
                               "**WA Status: **" + unstatus.text + "\n"
                               "**Region:** " + region.text + "\n"
                               "**Flag:** " + natflag.text + "\n"
                               "**Motto:** " + motto.text + "\n"
                               "**Animal:** " + animal.text + "\n"
                               "**Currency:** " + currency.text + "\n"
                               "**Religion:** " + religion.text + "\n"
                               "**Demonyms:** " + demonym.text + ", " + demonym2.text + ", " + demonym2p.text)
 
            else:
                await ctx.send("**" + fullname.text + "** (Last active: " + lastactive.text + ")\n"
                               "**Founded: **" + founded.text + "\n"
                               "https://www.nationstates.net/nation=" + arg.replace(" ", "_") + "\n"
                               "**WA Status: **" + unstatus.text + "\n"
                               "**Region:** " + region.text + "\n"
                               "**Flag:** " + natflag.text + "\n"
                               "**Motto:** " + motto.text + "\n"
                               "**Animal:** " + animal.text + "\n"
                               "**Currency:** " + currency.text + "\n"
                               "**Religion:** " + religion.text + "\n"
                               "**Demonyms:** " + demonym.text + ", " + demonym2.text + ", " + demonym2p.text)
        else:
            endos2 = str((endos1.text).count(",") + 1)
            #if got wa do the following
                     
            if founded.text == "0":
                await ctx.send("**" + fullname.text + "**(Last active: " + lastactive.text + ")\n"
                               "**Founded: ** Antiquity" + "\n"
                               "**WA Status: **" + unstatus.text + "** | Endorsements:** " + endos2 + "\n"
                               "**Region:** " + region.text + "\n"
                               "**Flag:** " + natflag.text + "\n"
                               "**Motto:** " + motto.text + "\n"
                               "**Animal:** " + animal.text + "\n"
                               "**Currency:** " + currency.text + "\n"
                               "**Demonyms:** " + demonym.text + ", " + demonym2.text + ", " + demonym2p.text)
               
            else:
                await ctx.send("**" + fullname.text + "**" + "\n"
                               "**Founded: **" + founded.text + "\n"
                               "https://www.nationstates.net/nation=" + arg + "\n"
                               "**WA Status: **" + unstatus.text + "** | Endorsements:** " + endos2 + "\n"
                               "**Region:** " + region.text + "\n"
                               "**Flag:** " + natflag.text + "\n"
                               "**Motto:** " + motto.text + "\n"
                               "**Animal:** " + animal.text + "\n"
                               "**Currency:** " + currency.text + "\n"
                               "**Religion:** " + religion.text + "\n"
                               "**Demonyms:** " + demonym.text + ", " + demonym2.text + ", " + demonym2p.text)
       
@bot.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def check(ctx,arg):
    await checkbase(ctx,arg,';limit={};sinceid='.format(arg),False)
    await ctx.send("End of requested checks.")
 
@bot.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def checksince(ctx,arg):
    #same as above but since a certain time
    await ctx.send("Last ID: "+ (await checkbase(ctx,arg,';sinceid={}'.format(arg),False)))
    await ctx.send("End of requested checks.")
 
@bot.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def mcheck(ctx,arg):
    #remove moves from check
    await checkbase(ctx,arg,'+-move;limit={};sinceid='.format(arg),True)
    await ctx.send("End of requested checks.")
 
@bot.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def mchecksince(ctx, arg):
    #same as above but since a certain ID
    await ctx.send("Last ID: " + (await checkbase(ctx,arg,'+-move;sinceid={}'.format(arg),True)))
    await ctx.send("End of requested checks.")
 
 
@bot.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def mchecks(ctx):
    #checks since last id
    lid=invent.find_one({'lastid2':{'$exists':True}})['lastid2']
    lasteventid=await checkbase(ctx,lid,'+-move;sinceid={}'.format(lid),True)
    await ctx.send("Last ID: " + str(lasteventid))
    await ctx.send("End of requested checks.")
    invent.update({'lastid2':{'$exists':True}},{'lastid2':lasteventid})
       
 
@bot.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def checks(ctx):
    #checks since last id
    lid=invent.find_one({'lastid':{'$exists':True}})['lastid']
    lasteventid=await checkbase(ctx,lid,';sinceid={}'.format(lid),False)
    await ctx.send("Last ID: " + str(lasteventid))
    await ctx.send("End of requested checks.")
    invent.update({'lastid':{'$exists':True}},{'lastid':lasteventid})

@bot.command()
@commands.has_any_role('Emperor','Senator','Praetorian Guard')
async def EndoCTE(ctx,days,nation):
    await ctx.send(":hourglass: :hourglass_flowing_sand: :hourglass: \n*gathering data*\nPlease wait this could take 2-4 minutes")
    Likely=''
    EndoLink=urllib.request.urlopen(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=endorsements').read().decode('utf-8')
    EndoTree=ET.fromstring(EndoLink)
    Endoers=EndoTree[0].text.split(',')
    #counts endorsements on nations
    for endo in Endoers:
        time.sleep(1)
        await asyncio.sleep(0.01)
        Activity=urllib.request.urlopen(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={endo}&q=lastactivity').read().decode('utf-8')
        ActivityTree=ET.fromstring(Activity)
        LastList=(ActivityTree[0].text).split(' ')
        number=LastList[0]
        denom=LastList[1]
        if denom=='days':
            if int(number)>= int(days):
                Likely+=f' {endo},'
                #if they haven't been on for long enough they are added to the list
    await ctx.send(f'Inactive nations endorsing {nation} are: {Likely}')

@bot.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def WAS(ctx, *region):
        Req=urllib.request.urlopen('https://www.nationstates.net/cgi-bin/api.cgi?wa=1&q=members')
        Open=Req.read().decode("utf-8")
        WATree=ET.fromstring(Open)
        WA=WATree[0].text.split(",")
        #calculates list of WA nations
        if region:
            region='_'.join(region)
        else:
            region='the_pacific'
        Req=urllib.request.urlopen(f'https://www.nationstates.net/cgi-bin/api.cgi?region={region}&q=nations')
        Open=Req.read().decode("utf-8")
        EndoTree2=ET.fromstring(Open)
        Nations=EndoTree2[0].text.split(":")
        #calculates nations in TP
        WANations=set(Nations) & set(WA)

        await ctx.send(len(WANations))


@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send("Incorrect Mask Use !help for a list of commands")
        #if no permissions
        
scheduler.start()
#starts chron schedule
bot.loop.create_task(WA())
bot.loop.create_task(Endorsing())
bot.loop.create_task(checksinc())
bot.loop.create_task(WAMovement())
#starts hourly tasks
bot.run('NDk3Nzk3OTMzNjAxOTE0ODgw.Dpkerg.MB2c0XZxIJG_-SeGofhhomU7cyU')
#run bot
