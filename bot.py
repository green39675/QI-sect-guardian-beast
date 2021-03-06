# -*- coding: utf-8 -*-
import discord,asyncio,time,csv,random,datetime,os,dropbox
from discord.ext import commands
from discord.ext.commands import Bot
import math

xpban=[[""] * 2 for i in range(1)]

sectList = ["Autarch Flipping", "Explosion","Blank","Thousand and One Petals","Debauchery Tea Party","Sort Post A Massege", "Rising Peak","NOT A GAE","The Church","Constellation"] #Name of Sect
sectCall = ["ELON","Exp","Blank","PETALS","TeaParty","spam","Lord","gae","church","stellar"] #call for .!sect <name>
sectTags = ["「 ELON 」","Explosion","『　　』","《 PETALS 》","[TeaParty]","[spam]","Lord","【GAE】","✞ CHURCH ✞","〈Stellar〉"] #Tag required for xp   
sectOwner = ["Perpetual Phoenix", "Megumin_Explosion", "Weiqing","Ziyun","ZaChan","VANSTORM","Modsan","WitheringLeaf","Oer_","VeeVee"] #Owner of Sect
sectDescription = ["Listen, ye mortal of the finite realms, for We are the Autarchs that were present at the beginning, and shall be present at the end! We are the Holy Inheritors of Elon, transcendent of all other races! We have seen generations trickle by, in the river of history, yet remain unfettered by time! Those who proclaim themselves as people of power are nothing to Us, for there is no apex past Us! A force that rivals the Heavens! A force that has become the Heavens! Who dares claim to be our equal‽ ",  #Elon
                    "EXPlOSION that's all\nFounded by megumin", #Explosion
                    "I  am **thou**, thou art I... \nThou hast acquired a **new** vow.\n\nIt shall **become** the wings of rebellion that **breaketh** thy chains of captivity.\n\nWith the birth of the *BLANK* Persona, \nI have obtained the winds of **blessing** that shall lead to freedom and **new** power...\n\nAllowing knowledge to flow freely to one another, while not pondering over futile matters laying in conflict with the state of mind.\nBlank is the way your soul has to feel for proper understanding and mental fortitude.", #Blank
                    "NA", #Petals
                    "Debauchery Tea Party is a relaxed sect that uses Alchemy Server as its base. We enjoy having various discussions on many topics, including Tea, Food, and poetry - encouraging members to enjoy life. We only ask that members respect each other and behave appropriately. Join us, we have cookies! :cookie:", #Tea Party
                    "=============================\n---------------------------------------------\nAll Hail [spam] Sect.\n\nWith level up. We gain power.\nWith power. We gain freedom.\nWith freedom. We gain boredom.\nWith boredom. We gain [spam].\n\nMember can come and can go\nBut [spam] sect is always there. \n can still there and can change.\nBut [spam] sect is alwasy exist.\nSect master can me or anyone.\nBut [spam] sect always our. \n\n----------------------------------------------\n==============================", #Spam
		    "NA", #Lords
		    "NA", #GAE 
		    "Quos deus vult perdere dementat prius", #Church
		    "NA" #Stellar
                   ]

usableRoles = [
               "Literary Snobs", "Polygamist Reader", "Habitual Book Clubber",
               "Stockpiler", "Re-Reader", "Physical Book Loyalist", "Spoiler Lover",
               "Nonfiction Lover", "Fiction Fanatics", "Emotional Reader", "Book Juggler",
               "Die-Hard Reader", "Weekend Warrior Reader", "Obsessive Bibliophile",
               "Tentative Reader", "Shy Reader", "Librocubicularist", "Grumpy Reader",
               "Book Eater", "Seasonal Reader", "Trend Reader", "Moody Reader",
               "Practical Reader", "Slow Reader"
                       ]
sectXP = list() #create empty xp list
sectLvl = list() #create empty level list 

requiredXP = [ 5000,7000,8000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55000,60000] #xp required for next level

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

def openFile(fileName, openIn,listAdd):
        with open(fileName, openIn) as fData:
            reader = csv.reader(fData)
            for row in reader:
                for i in range(len(row)):
                    listAdd.append(int(row[i]))
        fData.close()
        
def writeFile(fileName, openIn,listWrite):
        fData = open(fileName, openIn)
        for allSects in range(len(sectCall)):
            fData.write(str(listWrite[allSects]))
            if allSects != len(sectCall)-1:
                fData.write(",")
        fData.close()
        
download_file("levels.csv","/levels.csv")
download_file("sectLevels.csv","/sectLevels.csv")
        
openFile("levels.csv", "r+",sectXP)
openFile("sectLevels.csv", "r+",sectLvl)

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


bot = commands.Bot(command_prefix=".") #bot prefix
	

@bot.event  
async def on_ready():   #when bot is ready will print on a new line, and change bot playing status
    
    print("_____________________\nSect XP Tracking On")    
    await bot.change_presence(game=discord.Game(name="the Chat :shy:",type=3))
    bot.loop.create_task(second_timer())

@bot.command(pass_context=True)
async def millie(ctx):
        image = "https://i.imgur.com/rB2Kg6X.png"
        embed = discord.Embed()
        embed.set_image(url=image)
        await bot.say(embed=embed)
	
@bot.command(pass_context=True)
async def invite(ctx, user: discord.User):
	
    inviteMsg = f"Hey {user.mention}! {ctx.message.author.mention} has invited you to join their sect. \n\n**Status: Pending**"
    msg = await bot.send_message(ctx.message.channel,
                                 inviteMsg)

    reactions = ['✅', '❌']
    for reaction in reactions:
        await bot.add_reaction(msg, reaction)

    try:
        reaction, reactor = await bot.wait_for_reaction(['✅', '❌'], user=user, timeout=600, message=msg)
    
        if reaction.emoji == "✅":
            reply = "Accepted"
            for i in range(len(sectTags)):
                if sectTags[i] in ctx.message.author.display_name:
                    try:
                        if sectTags[i] == "Lord" or sectTags[i] == "⧹Cult⧸" :await bot.change_nickname(user, sectTags[i]+" "+user.name)
                        else:await bot.change_nickname(user, user.name+" "+sectTags[i])
                        break
                    except Exception:           
                        await bot.send_message(ctx.message.channel, f"{user}, your nickname is too long for the tag to be added. Please contact a mod to have it changed.")
                        
        elif reaction.emoji == "❌":
            reply = "Rejected"
            
    except TypeError:
        reply = "Timed Out"
        
    await bot.edit_message(msg, new_content=inviteMsg.replace("Pending", reply))
    await bot.send_message(ctx.message.author, f"{user} has {reply.lower()} your sect invite.")
    await bot.send_message(bot.get_channel("477777298431672321"), f"{ctx.message.author} has invited {user} to their sect. | {reply}")
    await bot.clear_reactions(msg)
	
	
@bot.command(pass_context = True, aliases=["iam"])
async def addrole(ctx,*roleToAdd):
    roleToAdd = " ".join(roleToAdd)
    if roleToAdd.title() in usableRoles or roleToAdd.lower() == "none":
        currentRoles = [x.name for x in ctx.message.author.roles]
        if any(x in currentRoles for x in usableRoles):
            for i in range(len(usableRoles)-1):
                if usableRoles[i] in currentRoles and usableRoles[i] != "Interested in Events":
                    role = discord.utils.get(ctx.message.server.roles, name=usableRoles[i])
                    await bot.remove_roles(ctx.message.server.get_member(ctx.message.author.id),role)
        if roleToAdd.lower() == "none":
            
            await bot.say("Your coloured role has been removed.")
            pass
        else:
            await bot.say("Adding '" + str(roleToAdd) +"' to " + str(ctx.message.author.name))
            if roleToAdd.lower() == "interested in events":
                role = discord.utils.get(ctx.message.server.roles, name="Interested in Events")
            else:
                role = discord.utils.get(ctx.message.server.roles, name=roleToAdd.title())
            
            await bot.add_roles(ctx.message.server.get_member(ctx.message.author.id), role)
    else:
        await bot.say("That role is not available!")
	

@bot.command(pass_context=True)
async def roles(ctx):
    allRoles = ["Literary Snobs", "Polygamist Reader", "Habitual Book Clubber", "Stockpiler", "Re-Reader", "Physical Book Loyalist", "Spoiler Lover", "Nonfiction Lover", "Fiction Fanatics", "Emotional Reader", "Book Juggler", "Die-Hard Reader", "Weekend Warrior Reader", "Obsessive Bibliophile", "Tentative Reader", "Shy Reader", "Librocubicularist", "Grumpy Reader", "Book Eater", "Seasonal Reader", "Trend Reader", "Moody Reader", "Practical Reader", "Slow Reader"]
    embed = discord.Embed(title=f"**There are {len(allRoles)} self-assignable roles.**", color=16711680)
    pages = {}

    for x in range(math.ceil(len(allRoles)/15)):
        try:
            pages[f"page{x}"] = " \n".join(allRoles[0:15])
            del allRoles[0:14]
        except Exception:
            pages[f"page{x}"] = " \n".join(allRoles[:len(allRoles)-1])
            del allRoles[:len(allRoles)]

    embed.add_field(name="**⟪Cultivation Methods⟫**", value=pages["page0"])
    current = 0
    embed.set_footer(text=f"{current+1}/{len(pages)}")
    msg = await bot.send_message(ctx.message.channel, embed=embed)

    nav = ["⬅","➡"]
    for emote in nav:
        await bot.add_reaction(msg, emote)

    for x in range(5):

        try:
            reaction, reactor = await bot.wait_for_reaction(nav, user=ctx.message.author, timeout=10, message=msg)
            if reaction.emoji == "➡" and current == 0:
                current += 1
            elif reaction.emoji == "⬅" and current == 1:
                current -= 1

            embed.remove_field(0)
            embed.set_footer(text=f"{current+1}/{len(pages)}")
            embed.add_field(name="**⟪Cultivation Methods⟫**", value=pages[f"page{current}"])
            await bot.edit_message(msg, embed=embed)

        except TypeError:
            await bot.clear_reactions(msg)


    await bot.clear_reactions(msg)	
	
	
@bot.command(pass_context=True)
async def sects(ctx, arg="lb"):
    
    if arg.lower() not in ["l","lb","h","help","a","hof"]:
        for sects in sectCall: #check if arg in sects
                if arg.lower() == sects.lower(): #make sure both compared are lowercase
                        argCh = sectCall.index(sects) #set argCh to the index
                        embed=discord.Embed(color=0x71cecb)
                        embed.set_author(name=str(sectList[argCh]))
                        embed.add_field(name="Leader", value=str(sectOwner[argCh]))
                        embed.add_field(name="XP until Next level", value= str(requiredXP[sectLvl[argCh]] - sectXP[argCh])+"xp ("+str(requiredXP[sectLvl[argCh]])+")")
                        embed.add_field(name="Level", value=str(sectLvl[argCh]+1))
                        embed.add_field(name="Description", value=str(sectDescription[argCh]))
                        
                        
                        await bot.say(embed=embed,delete_after=25)
                        break

    if arg.lower() in ["h","help"]:
        embed=discord.Embed(color=3447003)
        embed.set_author(name="Usage")
        embed.add_field(name="<.sects a>", value="Redundant")
        embed.add_field(name="<.sects lb>", value="Display the sect leaderboard",inline=False)
        embed.add_field(name="<.sects hof>", value="Display the hall of fame",inline=False)
        embed.add_field(name="<.sects [search tag] >", value="Display tagged sects\n\u200b",inline=False)
        embed.add_field(name="Search Tags",value=sectCall,inline=False)
        

        await bot.say(embed=embed, delete_after=20)

        
    elif arg == "a":
            embed=discord.Embed(color=0xabcdef)
            embed.set_author(name="Sects Info!")
            embed.add_field(name="This command is no longer in use! Instead use <.!sects lb> or just <.!sects now!>", value="This change has been due to the fact as sects have grown, the command takes up the entire screen in #bot_commands. This is too much!",inline=False)
            await bot.say(embed=embed,delete_after=25)

            
    elif arg in ["l","lb"]:
            tempName = list(sectList) 
            tempTag = list(sectCall)
            tempXPC = list(sectXP)
            tempXP = list(sectXP)
            tempLvl = list(sectLvl)
            tempDesc = list(sectDescription)

            for xptotal in range(len(sectXP)):
                for getxp in range(sectLvl[xptotal]):
                    tempXP[xptotal] += requiredXP[getxp]

            tempXP, tempName, tempXPC, tempLvl,tempTag,tempDesc = zip(*sorted(zip(tempXP,tempName,tempXPC,tempLvl,tempTag,tempDesc),reverse=True))
            

            embed=discord.Embed(color=0x896fc4)
            embed.set_author(name="Leaderboard")

            for i in range(len(tempName)):
                    embed.add_field(name="#"+str(i+1)+" "+tempName[i]+" ["+tempTag[i]+"]", value=str(tempXPC[i])+" / "+str(requiredXP[tempLvl[i]])+" ("+str(tempXP[i])+")",inline=False)

            await bot.say(embed=embed,delete_after=20)

    elif arg in ["hof"]: #TBD
            pass

@bot.event
async def on_message(message):
    if message.channel.id == "326959934187110402":
        pass
    else:
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
    
                
                for findTag in range(len(sectCall)):
                    if sectTags[findTag].upper() in message.author.nick.upper() :                    
                                sectXP[findTag] += random.randint(2,5)    #set xp
                                print(str(sectList[findTag])+" = "+str(sectXP[findTag])+"xp") 
                                writeFile("levels.csv", "w", sectXP)

                                        
                for xpCheck in range(len(sectCall)):
                    if sectXP[xpCheck] >= requiredXP[sectLvl[xpCheck]]:
                        sectXP[xpCheck] = 0
                        sectLvl[xpCheck] +=1
                        writeFile("sectLevels.csv", "w", sectLvl)

                        for i in range(2):
                            await bot.send_message(message.channel,"***"+str(sectList[xpCheck])+" Sect has leveled up!*** :cake: :cake: :cake:")
                
        except:
            pass
    await bot.process_commands(message)
bot.run(os.environ['BOT_TOKEN'])
  #Made by Weiqing#2360 & Perpetual Phoenix#0363
