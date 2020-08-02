#Legio Bot
#Made By:CookiEvee
from apscheduler.schedulers.background import BackgroundScheduler
#Module for scheduling tasks on a specific time(used for updating data dumps)
from datetime import *
#handling datetime data types
from discord.ext import commands
#Discord module to interact with the discord api
from pymongo import *
#Module for accessing Mongo DataBase
from time import *
#used for time.sleep()
from urllib.error import URLError, HTTPError
#urllib error catches errors in urllib


import asyncio
#asyncio integrates with discord in allowing multiple commands to be run at once using asyncio.sleep()
import aiofiles
#handles files asyncroniously
import calendar
#allows showing the current date
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
import xml.etree.ElementTree as ET
#xml Etree is used to parse XML data
client=MongoClient()
db=client.admin
invent=db.inventory
coupregion = ['*the* Pacific', 'The South Pacific', 'The North Pacific', 'The East Pacific', 'The West Pacific', 'Osiris', 'Balder', 'The Rejected Realms', 'Lazarus']
sevlist=['The NPO severs fascist ties to the Pacifics.','Did you know that he came from several regions?',"Have you seen Sev lately? I feel like he hasn't been very expressev.",]
#lists for the sev trigger
time.sleep(20)
os.chdir('/home/ubuntu/Legionarius')
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
taglist =[]
tagindeex = 0
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(activity=discord.Game(name='!help | Practise makes Perfect'))
embed1=discord.Embed(title="Comrade Help", description="Help info box for Comrade commands", color=0x3498DB)
embed1.add_field(name='!join | Joins an OP', value='!join', inline=False)
embed1.add_field(name='!leave | Leaves an OP', value='!leave', inline=False)
embed1.add_field(name='!credit | Credits for the bot', value='!credit', inline=False)
embed1.add_field(name='!nation [name] | Sends data about the nation', value='!nation cavedweller', inline=False)
embed1.add_field(name='!region [name] | Sends data about the region', value='!region The_Pacific', inline=False)
embed1.add_field(name='!help [Commander/PG/Emperor] | Sends help information for relevant masks', value='!help PG', inline=False)
embed1.add_field(name='!PrevMinor | sends  Previous Minor information', value='!PrevMinor', inline=False)
embed1.add_field(name='!addrole [Major/Minor] | adds or removes major/minor updater', value = '!addrole', inline= False)
embed1.add_field(name='Easter Eggs', value='There are currently 30 Easter Eggs.', inline=False)
embed1.set_footer(text="Send any questions to CookiEvee#2267 or Sev#6435")

embed2=discord.Embed(title="Praetorian Guard Help", description="Help info box for Praetorian Guard commands", color=0x83449E)
embed2.add_field(name='!notendo | Sends a file with all nations not endorsing the Emperor*', value='!notendo', inline=False)
embed2.add_field(name='!fullnotendo [name] | Sends file with all nations not endorsing the target', value='!fullnotendo cavedweller', inline=False)
embed2.add_field(name='!(m)check [quantity] | Checks founding feed for [quantity] nations(omits moved nations) ', value='!check 20', inline=False)
embed2.add_field(name='!(m)checksince [EventID] | Checks founding feed since [EventID] (omits moved nations)', value='!mchecksince 1984320', inline=False)
embed2.add_field(name='!endocap | Sends all nations over the endocap', value='!endocap', inline=False)
embed2.add_field(name='!EndoCTE [days inactive] [nation] | Sends endorsers who have not logged in for [days inactive]', value='!EndoCTE 10 east_durthang', inline=False)
embed2.add_field(name='!WAS | Sends number of all WAs in The Pacific', value='!WAS', inline=False)
embed2.set_footer(text="Send any questions to CookiEvee#2267 or Sev#6435")

embed3=discord.Embed(title="Commander  Help", description="Help info box for Commander commands", color=0x008000)
embed3.add_field(name='!(minor/major) [Target] [Time:m/s] [Quantity] | Sends [Quantity] reccomended triggers for (major/minor) around [Time]', value='!major the_pacific 20s 5', inline=False)
embed3.add_field(name='!start | Starts an OP', value='!start', inline=False)
embed3.add_field(name='!archive | Sends file with all OPs since start of recording', value='!archive', inline=False)
embed3.add_field(name='!end | Ends current OP', value='!end', inline=False)
embed3.add_field(name='!abort| aborts current OP', value='!abort', inline=False)
embed3.add_field(name='!sc [@user] | switches commander to [@user]', value='!sc @CookiEvee', inline=False)
embed3.add_field(name='!topendo | Displays 40 most endorsed nations in TP', value='!topendo', inline=False)
embed3.add_field(name='!t | Sends next target',value = '!t',inline=False)
embed3.add_field(name='!tagrun | Input file for  tagrun with a txt file with regions seperated by lines',value = '!tagrun',inline=False)
embed3.add_field(name='!name [Search] | Searches for a region with their name in the name/WFE', value='!name Nazi', inline=False)
embed3.add_field(name='!tags [Search] | Sends file with all regions with the tags specified:,(No Space) between tags to find regions with both, a space to find regions with either and - for regions without the tag', value='!tags nazi,-defender fascist', inline=False)
embed3.set_footer(text="Commands with a * next to them reset monthly\nSend any questions to CookiEvee#2267 or Sev#6435")

embed4=discord.Embed(title="Emperor Help", description="Help info box for normal commands", color=0xF50F0F)
embed4.add_field(name='!notendorsing [name] | Sends nations than [name] has not endorsed', value='!notendorsing cavedweller', inline=False)
embed4.add_field(name='!addcap [name] [cap]| adds an endocap for [name]', value='!addcap cavdweller 10', inline=False)
embed4.add_field(name='!removecap | Removes a cap for [name]', value='!removecap Cavedweller', inline=False)
embed4.add_field(name='!endocaplist | Sends a list of all the endocaps', value='!endocaplist', inline=False)
embed4.add_field(name='!region [name] | Sends data about the region', value='!region The_Pacific', inline=False)
embed4.add_field(name='Easter Eggs', value='All Easter Eggs:spam,glealian,AA,aleisyr,xoriet,perg,jar,legio bot,samasbhi,coup,laws,banject,pacificat,kk,cooki,sev,commu,purge,userite,hug,hug(with sassoon),lod,praetorian guard,flan,cards,glitter,ele,pierconium,conflux', inline=False)
embed4.set_footer(text="Send any questions to CookiEvee#2267 or Sev#6435")

@bot.group()
async def help(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(embed=embed1)

@help.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor")
async def PG(ctx):
    await ctx.send(embed=embed2)

@help.command()
@commands.has_any_role("Praetorian Guard","Senator","Emperor","Commander")
async def Commander(ctx):
    await ctx.send(embed=embed3)

@help.command()
@commands.has_any_role("Emperor")
async def Emperor(ctx):
    await ctx.send(embed=embed4)

@bot.command()
async def credit(ctx):
    await ctx.send('''This bot was created for the use of the Legio Pacifica alone
Bot coded by: CookiEvee#2267 and Sev#6435 
Many Thanks to: Sassoon#1737 and all other testers!''')

@bot.command()
@commands.has_any_role("Commander","Senator","Emperor")
async def archive(ctx):
    with open('ArchiveOP.txt','w') as Arch:
        Arch.write(invent.find_one({'Archive':{'$exists':True}})['Archive'])
        Arch.close()
        await ctx.send(file=discord.File('ArchiveOP.txt'))
    os.remove('ArchiveOP.txt')
    #sends archive of OPs

@bot.command()
@commands.has_any_role("Commander","Senator","Emperor")
async def abort(ctx):
        OP=[]
        OPFile=[]
        await ctx.send('OP has been aborted.')
        #aborts the OP

@bot.command()
@commands.has_any_role("Commander","Senator","Emperor")
async def end(ctx):
    global OP,OPFile
    if OP==[]:
        await ctx.send("No Op scheduled.")
        #if empty no op is scheduled
    else:
        await ctx.send("Do you wish to archive this OP? Y/N")
        #checks if they want to archive the op
        try:
            def check(m):
                return m.author == ctx.message.author and m.channel == ctx.message.channel

            guess = await bot.wait_for('message',check=check,timeout=5.0)

            if guess.content == "Y":
                #if answer is yes
                await ctx.send("Please enter in the following order:[Link to target] [Major/Minor] [Hit/Miss]")
                FileInput=await bot.wait_for('message',timeout=15.0, check=check)
                CurrentArchive=(invent.find_one({'Archive':{'$exists':True}}))['Archive']
                SplitFile=FileInput.content.split(" ")
                ArchiveIn=("{} {} {} {} {}".format(date.today(),SplitFile[0],SplitFile[1],SplitFile[2],OPFile))                
                ArchInput=CurrentArchive+'\n'+ArchiveIn
                invent.update({'Archive':{'$exists':True}},{'Archive':ArchInput})
                #inputs data
            await ctx.send('Participants of this OP were: {}'.format("".join(OP)))
            OP=[]
            OPFile=[]
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you have timed out")

@bot.command()
@commands.has_any_role("Commander")
async def tagrun(ctx):
    global taglist, tagindex
    try:
        def FileCheck(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel and m.attachments !=[]

        await ctx.send('Please send a text file with lines of [region] [time], this will timeout in 50 seconds.')
        FileWait = await bot.wait_for('message', check=FileCheck, timeout = 50.0)

        File = await FileWait.attachments[0].read()
        FileRead = File.decode('UTF-8').replace('\r','').split('\n')

        taglist = list(filter(None, FileRead))
        tagindex = 0
        await ctx.send('Thank You')
    except asyncio.TimeoutError:
        await ctx.send('Sorry, you have timed out')

@bot.command()
@commands.has_any_role('Commander')
async def t(ctx):
    global tagindex
    if ctx.message.channel.id == 572376696150556693:
        try:
            await ctx.send('<@&572375899434123269> '+taglist[tagindex])
            tagindex+=1
        except IndexError:
            await ctx.send('List has finished, restarting List. Good Job everybody!')
            tagindex = 0

@bot.command()
async def addrole(ctx,*,RoleInput):
    RoleInput = RoleInput.lower()
    member = ctx.message.author
    role = ctx.message.channel.guild.roles
    if RoleInput == 'major':
        RoleInput = 'major updater'
    elif RoleInput == 'minor':
        RoleInput = 'minor updater'
    if RoleInput == 'major updater' or RoleInput == 'minor updater' or RoleInput == 'team one' or RoleInput == 'team two':
        for i in role:
            if i.name.lower() == RoleInput:
                member_role = i

        if member_role in member.roles:
            await member.remove_roles(member_role)
        else:
            await member.add_roles(member_role)


@bot.command()
async def OPList(ctx):
    await ctx.send(OP)

@bot.command()
@commands.has_any_role('Emperor')
async def addcap(ctx,name,cap):
    invent.insert_one({'EndoCap':{name:cap}})
    await ctx.send("Task Completed use !endocaplist to get the file.")

@bot.command()
@commands.has_any_role("Emperor")
async def removecap(ctx,name):
    invent.remove({"EndoCap."+name:{'$exists':True}})
    await ctx.send("Task Completed use !endocaplist to get the file.")

@bot.command()
async def PrevMinor(ctx):
    prev=invent.find_one({'PrevMinor':{'$exists':True}})['PrevMinor']
    await ctx.send(f'Previous Minors are: {prev}')

@bot.command()
async def PrevMajor(ctx):
    prev=invent.find_one({'PrevMajor':{'$exists':True}})['PrevMajor']
    await ctx.send(f'Previous Minors are: {prev}')

@bot.command()
@commands.has_any_role("Emperor")
async def endocaplist(ctx):
    Cursor=invent.find({'EndoCap':{'$exists':True}})
    Dict=''
    for i in Cursor:
        Split=(str(i).split(':'))[2:]
        Dict+='\n'+str(Split).replace("'","").replace("{","").replace("}","").replace('"','').replace(" ","").replace(",",":").replace("[","").replace("]","")
    await ctx.send(str(Dict))
#outputs the file showing the endocap

@bot.command()
@commands.has_any_role("Commander","Senator","Emperor")
async def start(ctx):
    global OP,OPFile
    OP=["<@{}>[Commander]".format(ctx.author.id)]
    OPFile=["{}[Commander]".format(ctx.author.name)]
    await ctx.send('Op has been scheduled,type !join to join the Op')
    #new op starts

@bot.command()
@commands.has_any_role('Praetorian Guard','Senator','Emperor')
async def totalnotendo(ctx):
    with open('TotalEndos.txt','w') as Tot:
        Tot.write(invent.find_one({'TotalEndo':{'$exists':True}})['TotalEndo'])
        Tot.close()
        await ctx.send(file=discord.File('TotalEndos.txt'))
    os.remove('TotalEndos.txt')
#outputs total nations not endorsed this month
    
@bot.command()
@commands.has_any_role("Commander","Senator","Emperor")
async def sc(ctx,arg:discord.Member):
    global OP,OPFile
    try:
        try:
            OP.remove(f'{arg.mention}')
            #removes current commander
        except ValueError:
            pass
        OP.insert(1,"{}[Commander]".format(arg.mention))
        OP.remove(OP[0])
        #inserts new commander and removes old one
        OPFile.insert(1,"{}[Commander]".format(arg.name))
        OPFile.remove(OPFile[0])
        #same but the file
        await ctx.send(f"Commander changed to {arg.mention}")
    except NameError:
        await ctx.send("There is currently no Op scheduled")
    except IndexError:
        await ctx.send("SYNTAX wrong:format of command is ```!sc [@name]```")

        
@bot.command()
@commands.has_any_role("Commander","Senator","Emperor")
async def name(ctx,*,arg):
    Argument=arg.split(" ")
    NameTree=ET.parse('region.xml')
    NameRoot=NameTree.getroot()
    #parses region xml
    File=open('ListForU.txt','w')
    File.close()
    File=open('ListForU.txt','a')
    Args=[]
    #resets file
    for i in Argument:
        Args.append(i.split(","))
    #splits arguments
    for region in NameRoot.findall("REGION"):
        Add=False
        for i in Args:
            for x in i:
                #for tags withij the tags
                if x in region[0].text:
                    Add=True
                    #if tag is in region add it
                elif region[1].text and x in region[1].text:
                    Add=True
                    #else if region is in text
                else:
                    Add=False
                    break

        if Add==True:
            File.write("\nhttps://www.nationstates.net/region={}".format(region[0].text))
        #if true add to file
    File.close()
    await ctx.send(file=discord.File('ListForU.txt'))
    os.remove('ListForU.txt')
    
@bot.command()
async def join(ctx):
    if OP !=[]:
        Joined=False
        for i in OP:
            if str(ctx.author.id) in i:
                Joined=True
        #joined op
        if Joined==True:    
            await ctx.send("You have already joined the op")
        #if joined say joined already
        else:
            #else join the op
            OP.append(",<@{}>".format(ctx.author.id))
            OPFile.append("{}".format(ctx.author.name))
            await ctx.send("You have been added to the OP")
    else:
        await ctx.send('There is currently no Op scheduled')


@bot.command()
async def leave(ctx):
    if OP !=[]:
        Potato=False
        counter=0
        for i in OP:
            counter+=1
            if str(ctx.author.id) in i:
                Potato=True
                break
        #finds index in list
        if Potato==True:
            if counter==1:
                await ctx.send("You are the Commander,you may switch commanders or abort the mission but the commander may not leave the current OP")
                #if commander doesn't allow
            else:
                OP.remove(i)
                await ctx.send(f"{ctx.author.mention} has left the OP")
                #leaves op
        else:
            await ctx.send("You have not joined the OP")

    else:
        await ctx.send("There is no Op scheduled")

@bot.event
async def on_message(message):
    #TRIGGERS: say a word in chat and the following will be sent
    global listcount
    channel=message.channel
    if message.author == bot.user:
        return
    if channel.id == 264874669314801667 or channel.id == 496364817863540742 or channel.id == 539932260493950989:
        if "GO GO GO" in message.content:
            for i in message.author.roles:
                if i.name == "Commander":
                    await channel.send(message.content)
                    await channel.send(message.content)
    if channel.id == 496074271454658564 or channel.id == 264874669314801667:
        pass
    else:
        if "lod" in message.content.lower() or "emperor" in message.content.lower():
            if listcount[0]>=7:
                listcount[0]=0
                await channel.send("**Hail the Emperor! o/**")
        if "hug" in message.content.lower():
            if "sass" in message.content.lower() or"<@273190234831978497>" in message.content or message.author.id==273190234831978497:
                if listcount[1]>=7:
                    listcount[1]=0
                    await channel.send("PergamemeToday at 10:37 PM")
                    await asyncio.sleep(0.5)
                    await channel.send("**HOW**")
                    await asyncio.sleep(0.5)
                    await channel.send("**ABOUT**")
                    await asyncio.sleep(0.5)
                    await channel.send("**NO**")
                    await asyncio.sleep(0.5)
                    await channel.send("**HUGS**")
                    await asyncio.sleep(0.5)
                    await channel.send("**AT**")
                    await asyncio.sleep(0.5)
                    await channel.send("**ALL**")
                    await asyncio.sleep(0.5)
                    await channel.send("**WHEN**")
                    await asyncio.sleep(0.5)
                    await channel.send("**WILL**")
                    await asyncio.sleep(0.5)
                    await channel.send("**YOUR**")
                    await asyncio.sleep(0.5)
                    await channel.send("**FISH**")
                    await asyncio.sleep(0.5)
                    await channel.send("**BRAIN**")
                    await asyncio.sleep(0.5)
                    await channel.send("**UNDERSTAND**")
                    await asyncio.sleep(0.5)
                    await channel.send("**THAT?**")
            else:
                if listcount[2]>=7:
                    listcount[2]=0
                    await channel.send("*pushes the Sregguhs into the dungeon*")
        if "sassoon" in message.content.lower():
            if listcount[4]>=7:
                listcount[4]=0
                await channel.send("Give the dolphin some fish! He deserves it!")
        if "perg" in message.content.lower():
            if listcount[5]>=7:
                listcount[5]=0
                await channel.send("Hail the great pergifier! o/")
        if "o/" in message.content:
            if listcount[6]>=7:
                listcount[6]=0
                await channel.send("o/")
        if "xoriet" in message.content.lower() or "xor" in message.content.lower():
            if listcount[7]>=7:
                listcount[7]=0
                await channel.send("Hail the Ocelempress!")
        if "purge" in message.content.lower():
            if listcount[8]>=7:
                listcount[8]=0
                await channel.send("*Cleans my Banhammer and Bantrident*")
        if "jar" in message.content.lower():
            if listcount[9]>=7:
                listcount[9]=0
                await channel.send(file=discord.File("102374191_jarjar.png"))
        if "samasbhi" in message.content.lower():
            if listcount[10]>=7:
                listcount[10]=0
                await channel.send("*It's Samasbhi!*")
        if "legio bot" in message.content.lower():
            if listcount[11]>=7:
                listcount[11]=0
                await channel.send('Here to serve! o/')
        if "laws" in message.content.lower() or "LaB" in message.content:
            if listcount[12]>=7:
                listcount[12]=0
                await channel.send('*summons laws and bylaws with his flame thrower*')
        if "banject" in message.content.lower():
            if listcount[13]>=7:
                listcount[13]=0
                await channel.send('fascist re-education zone: https://www.nationstates.net/region=the_rejected_realms')
        if "pacificat" in message.content.lower():
            if listcount[14]>=7:
                listcount[14]=0
                await channel.send('Meow!')
        if "kk" in message.content.lower():
            if listcount[15]>=7:
                listcount[15]=0
                await channel.send('*watches as the snail slowly slithers into view.*')
        if "cooki" in message.content.lower():
            if listcount[16]>=7:
                listcount[16]=0
                await channel.send('The holy creator! Blessed be his name!')
        if "sev" in message.content.lower():
            if listcount[17]>=7:
                listcount[17]=0
                await channel.send(random.choice(sevlist))
        if "commu" in message.content.lower():
            if listcount[18]>=7:
                listcount[18]=0
                await channel.send('*watches community cheat on heli. AGAIN*')
        if "ale" in message.content.lower():
            if listcount[19]>=7:
                listcount[19]=0
                await channel.send('**RAWR!** Here comes the Emperah-emeritus-saur!')
        if "pg" in message.content.lower():
            if listcount[20]>=7:
                listcount[20]=0
                await channel.send('*Here come the Praetorian Guard!*')
        if "aa" in message.content.lower() or "augustin" in message.content.lower():
            if listcount[21]>=7:
                listcount[21]=0
                await channel.send(file=discord.File('AA.png'))
        if "flan" in message.content.lower():
            if listcount[22]>=7:
                listcount[22]=0
                await channel.send(file=discord.File('Flan.jpg'))
        if "spam" in message.content.lower():
            if listcount[23]>=7:
                listcount[23]=0
                await channel.send('*looks to see if Limestone is about*')
        if "glealian" in message.content.lower():
            if listcount[24]>=7:
                listcount[24]=0
                await channel.send('Hail province Tannenberg!')
        if "cards" in message.content.lower():
            if listcount[25]>=7:
                listcount[25]=0
                await channel.send('*founds some more puppets to farm cards*')
        if "marmar" in message.content.lower() or 'marina' in message.content.lower():
            if listcount[26]>=7:
                listcount[26]=0
                await channel.send("quick!The praetor's here, act normal!")
        if "ele" in message.content.lower():
            if listcount[27]>=7:
                listcount[27]=0
                await channel.send('Somone give Consul Elegarth some strawberry ice cream!')
        if "glitter" in message.content.lower():
            if listcount[28]>=7:
                listcount[28]=0
                await channel.send('*Throws fistfuls of glitter into the air*')
        if "conflux" in message.content.lower():
            if listcount[29]>=7:
                listcount[29]=0
                await channel.send('*Looks for his long-lost bot-brother*')
        if "sak" in message.content.lower() or '<@168962459321892864>' in message.content:
            if listcount[30]>=7:
                listcount[30]=0
                await channel.send(file=discord.File('Hi_buddy.jpg'))
        if "chi" in message.content.lower():
            if listcount[31]>=7:
                listcount[31]=0
                await channel.send(':chitato: > :endertank:')
        if "ender" in message.content.lower():
            if listcount[32]>=7:
                listcount[32]=0
                await channel.send(file=discord.File('chiuahaha.gif'))


    listcount=list(map(lambda x:x+1,listcount))
    await bot.process_commands(message)
    #proceses commands
listcount=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]



bot.run('TOKEN')
