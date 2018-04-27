# -*- coding: utf-8 -*-
import discord,asyncio,time,csv,random,datetime,os,dropbox
from discord.ext import commands
from discord.ext.commands import Bot

xpban=[[""] * 2 for i in range(1)]

sectList = ["Autarch Flipping [ELON]","Explosion [Exp]","Blank [Blank]"]              #ADD NEW SECTS HERE
sectTags = ["「 ELON 」","Explosion","『　　』"]                  #ADD NEW TAGS HERE
sectOwner = ["Perpetual Phoenix", "Megumin_Explosion", "Storm"]

sectXP = list() #create empty xp list                                       When creating a new sect, make sure to add ", 0" to the end of level.csv. Same with sectLevels
trueSectLevel = list() #create empty level list                               This will allow it to start tracking xp for that sect without errors
requiredXP = [ 5000,7000,8000,10000,15000,20000,25000,30000,35000,400000,45000,50000,55000]

def download_file(file_to,file_from):
    dbx = dropbox.Dropbox(os.environ['DROPBOX_TOKEN'])
    f = open(file_to,"w")                    
    metadata,res = dbx.files_download(file_from)
    f.write(str(res.content)[2:-1])
    f.close()
    
def upload_file(file_from, file_to):
    dbx = dropbox.Dropbox(os.environ['DROPBOX_TOKEN']) #DROXBOX_TOKEN
    f = open(file_from, 'rb')
    dbx.files_upload(f.read(), file_to,mode=dropbox.files.WriteMode.overwrite)
    f.close()

    
download_file("levels.csv","/levels.csv")
download_file("sectLevels.csv","/sectLevels.csv")



with open("levels.csv", "r+") as sectLevels:        #Grab all XP levels from levels.csv due to startup/restart
    reader = csv.reader(sectLevels)
    for row in reader:
        for i in range(len(row)):
            sectXP.append(int(row[i]))
    sectLevels.close()

with open("sectLevels.csv", "r+") as trueLevel:        #Grab all true levels from sectLevels.csv due to startup/restart
    reader = csv.reader(trueLevel)
    for row in reader:
        for i in range(len(row)):
            trueSectLevel.append(int(row[i]))
    trueLevel.close()

async def second_timer(): ##will be our xp timer
    secondChecker = 0
    while True:
        global a
        a = datetime.datetime.now()
        
        for timeCheck in xpban:
            if a.second in timeCheck:
                del xpban[0]

        if a.second == 0:
            secondChecker +=1
            print(secondChecker,"/1")
            if secondChecker == 1:
                secondChecker = 0
                upload_file("levels.csv","/levels.csv")
                upload_file("sectLevels.csv","/sectLevels.csv")
                
        await asyncio.sleep(1)
 
bot = commands.Bot(command_prefix=".!") #bot prefix

@bot.event  
async def on_ready():   #when bot is ready will print on a new line, and change bot playing status
    
    print("_____________________\nSect XP Tracking On")
    await bot.change_presence(game=discord.Game(name="Tracking Sect XP"))
    bot.loop.create_task(second_timer())

@bot.command(pass_context=True)
async def sects(ctx, arg):
    
    argCh = "na"
    if arg.lower() == "elon":argCh=0
    elif arg.lower() == "exp":argCh=1
    elif arg.lower() == "blank":argCh=2
    elif arg.lower() == "help":argCh="h"
    elif arg.lower() == "lb":argCh="l"

    if argCh != "na" and argCh != "h" and argCh != "l":
        embed=discord.Embed(color=0xabcdef)
        embed.set_author(name=str(sectList[argCh]))
        embed.add_field(name="Leader", value=str(sectOwner[argCh]))
        embed.add_field(name="XP until Next level", value= str(requiredXP[trueSectLevel[argCh]] - sectXP[argCh])+"xp ("+str(requiredXP[trueSectLevel[argCh]])+")")
        embed.add_field(name="Level", value=str(trueSectLevel[argCh]+1))
        
        await bot.say(embed=embed,delete_after=10)

    elif argCh == "h" or arg == "h":
        embed=discord.Embed(description="```Usage:\n.!sect <searchtag>\n\nSearchtags Available:\nElon\nExp\nBlank\n\nAlternatively, you can use 'a' to display all of them```",color=0x31c7ce)
        await bot.say(embed=embed, delete_after=10)

        
    elif arg == "a":
            embed=discord.Embed(color=0xabcdef)
            embed.set_author(name="Sects")
            for printOut in range(len(sectList)):
                    
                    embed.add_field(name=str(sectList[printOut]), value="Lead by "+ sectOwner[printOut],inline=False)
                    embed.add_field(name="Level", value=str(trueSectLevel[printOut]+1))
                    embed.add_field(name="XP until Next level", value= str(requiredXP[trueSectLevel[printOut]] - sectXP[printOut])+"xp ("+str(requiredXP[trueSectLevel[printOut]])+")")

                    if printOut != len(sectList)-1:
                        embed.add_field(name="\u200b", value="\u200b",inline=False)

            await bot.say(embed=embed,delete_after=25)
    elif argCh == "l":
            tempName = list(sectList) 
            tempXP = list(sectXP)
            for xptotal in range(len(sectXP)):
                for getxp in range(trueSectLevel[xptotal]):
                    tempXP[xptotal] += requiredXP[getxp]

            for i in range(len(tempXP)-1):
               if tempXP[i]<tempXP[i+1]:
                        temp = tempXP[i]
                        temp2 = tempName[i]
                        tempXP[i] = tempXP[i+1]
                        tempName[i] = tempName[i+1]
                        tempXP[i+1] = temp
                        tempName[i+1] = temp2

            embed=discord.Embed(color=0xabcdef)
            embed.set_author(name="Leaderboard")

            for i in range(len(tempName)):
                if i != len(tempName):
                    embed.add_field(name="#"+str(i+1)+" "+tempName[i], value=str(tempXP[i]), inline=False)
            await bot.say(embed=embed,delete_after=20)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(description="```Invalid argument!\nTry using .!sects help```",color=0x31c7ce)

        msg = await bot.send_message(ctx.message.channel, embed=embed)
        await asyncio.sleep(20)
        await bot.delete_message(msg) 

@bot.command(pass_context=True)
async def about(ctx):
    await bot.say("This bot was made by `Weiqing#2360` and had help from `Perpetual Phoenix#0363`.\nAny questions or want to suggest something? Feel free to dm us",delete_after=30)
    
@bot.event
async def on_message(message):
    try:
        global xpban,a
        located = False

        search = message.author.id
        for idCheck in xpban:
            if search in idCheck:
                located = True
        if message.author.nick is None or located == True:
            pass
        
        else:    
            xpban +=[[""] * 2 for i in range(1)]
            xpban[len(xpban)-2][0] = (message.author.id)
            xpban[len(xpban)-2][1] = (a.second)

            
            for findTag in range(len(sectTags)):
                if sectTags[findTag].upper() in message.author.nick.upper() :                    
                            sectXP[findTag] += random.randint(2,5)    #set xp
                            print(str(sectList[findTag])+" = "+str(sectXP[findTag])+"xp")
                            
            for xpCheck in range(len(sectList)):
                if sectXP[xpCheck] >= requiredXP[trueSectLevel[xpCheck]]:
                    sectXP[xpCheck] = 0
                    trueSectLevel[xpCheck] +=1
                    await bot.send_message(message.channel,"***"+str(sectList[xpCheck])+" Sect has leveled up!*** :cake: :cake: :cake:")
                    await bot.send_message(message.channel,"***"+str(sectList[xpCheck])+" Sect has leveled up!*** :cake: :cake: :cake:")
                    
            lev = open('sectLevels.csv', 'w')
            xplev = open('levels.csv', 'w')
            for allSects in range(len(sectList)):
                lev.write(str(trueSectLevel[allSects]))
                xplev.write(str(sectXP[allSects]))
                if allSects != len(sectList)-1:
                    lev.write(",")
                    xplev.write(",")
            lev.close()
            xplev.close()

        await bot.process_commands(message)
    except:
        pass


bot.run(os.environ['BOT_TOKEN'])
  #Made by Weiqing#2360 & Perpetual Phoenix#0363
