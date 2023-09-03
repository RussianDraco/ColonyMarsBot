import discord
from discord.ext.commands import BucketType
from discord.ext.commands import Bot
from discord.ext.commands import cooldown
from discord.ext.commands import command
from discord.ext.commands import BadArgument
from discord.ext import commands
import os
import time
import datetime
from datetime import datetime as dt
import random
from keep_alive import keep_alive
import asyncio
import json
import math

TOKEN = os.getenv('TOKEN')


PREFIX = 'co'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = PREFIX, intents=intents)

starterarray = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


#ADD EMOJI ID OF BUILDING
emj_id_array = ["845799123361595445","817080316102705222", "817204375843504158", "817487344282239017", "817893543166869565", "817175786590568469", "818267279384772618", "818297175028400138", "818514590501175367", "818576048488841218", "818994995494518816", "845364914909609984", "929531775770832936", "929850517683855480", "1056767501813424158", "1058600418273402950", "1059211098840113323"]
#ADD THE LETTER OF THE BUILDING AT THE SAME NUMBER AS THE EMOJI ID
emj_name_array = ["^", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]

acsslt_id = 812325097317728256
m_coin = 812336933006999613


def add_log(user_change, change_action, change_text):
	with open("changeslog.txt", 'a') as changelog:
		changelog.write('\n' + change_action + ' - ' + user_change + ': ' + change_text)

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()
    clean_lines(file_name)

def clean_lines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    with open(filename, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(line for line in lines if line.strip())
        f.truncate()

def is_equal(a, b, c, overdrive):
    if overdrive == True:
        return c
    if a == b:
        return ''
    if a > b:
        return ''
    if a < b:
        return c

def dict_access():
    json_file = open('alluserdata.json', 'r')
    data = json.loads(json_file.read())
    json_file.close()
    return data

def refresh_dict(data): #at some point make a back-up system!!
    with open('alluserdata.json', "w") as json_file:
        json.dump(data, json_file, indent=2)
    json_file.close()

def quest_check(commandName, user):
    json_file = open('quests.json', 'r')
    quest_data = json.loads(json_file.read())
    json_file.close()

    dict_ = dict_access()
    try:
        user_access = dict_[str(user)]
    except KeyError:
        return [False]


    if dict_[str(user)]["currentquest"][0]:
        qKey = dict_[str(user)]["currentquest"][1]
        qId = dict_[str(user)]["currentquest"][2] #currentquest: [false, "basicguide", 1, false] #onQuest, quest_key, quest_number, finishedQuest

        if dict_[str(user)]["currentquest"][3]:
            return [False]

        quest = quest_data.get(qKey)[str(qId)]
        if quest["info"]["type"] == "command" and commandName == quest["info"]["name"]:
            hasReturn = False
                
            try:
                if not quest["info"]["return"] == None:
                    hasReturn = True
            except KeyError:
                hasReturn = False

            if not hasReturn:
                return [True, False] #[check, sendreturn]
            else:
                return [True, True]
        else:
            return [False]
    else:
        return [False] #check

def quest_notify(user, return_ = None):
    dict_ = dict_access()

    json_file = open('quests.json', 'r')
    quest_data = json.loads(json_file.read())
    json_file.close()

    if return_ == None:
        dict_[str(user)]["currentquest"][3] = True
        refresh_dict(dict_)
        #dict_ = dict_access()
        return
    else:
        cquestData = quest_data.get(dict_[str(user)]["currentquest"][1])[str(dict_[str(user)]["currentquest"][2])]
        if return_ == cquestData["info"]["return"]:
            dict_[str(user)]["currentquest"][3] = True
            refresh_dict(dict_)

def person_exists(user, dict__):
    user_names = []
    for p in dict__: 
        user_names.append(dict__.get(p)["id"])
  
    if int(user) in user_names:
        return True
    else:
        return False

@bot.event
async def on_ready():
    print(bot.user.name + ' is active')
    await bot.change_presence(activity=discord.Game(name=PREFIX + "commands"))

#@bot.command(name = 'version')
#async def bot_version(ctx):
#    await ctx.send("ColonyMarsBot is in 1.5 Alpha")


@bot.command(name = 'invite')
async def invite(ctx):
    await ctx.send("You can invite ColonyMarsBot into your own server using this link:") 
    await ctx.send("__***https://discord.com/api/oauth2/authorize?client_id=807622074234699838&permissions=8&scope=bot***__")


@bot.command(name = 'server')
async def server(ctx):
    await ctx.send("You can join the official ColonyMarsBot using this link: https://discord.gg/zTSyJpJFdA")

@bot.remove_command("help")
@bot.command(name = 'help')
async def help_(ctx):
    await ctx.send("Welcome to 🥳 ColonyMarsBot 🥳, the one and only discord bot built to colonize Mars ")
    time.sleep(0.5)
    await ctx.send("If you are just starting, type `costartcolony` to start playing")
    time.sleep(0.5)
    await ctx.send("A list of commands is found in `cocommands`")


@bot.command(name = 'base')
async def base(ctx, person : discord.Member = None):
    if person == None:
        other_person = False
    else:
        other_person = True

    dict_ = dict_access()

    user_names = []
    for p in dict_:
        user_names.append(str(dict_.get(p)["id"]))

    if other_person == True:
        if not str(person.id) in user_names:
            await ctx.send(f"{str(person).split('#')[0]} dosen't have a colony")
            return
    else:
        if not str(ctx.author.id) in user_names:
            await ctx.send('You arent signed up to Colony Mars')
            await ctx.send(f'Type {PREFIX}startcolony to start your own colony!')
            return

    user_datas = []
    for p in dict_:
        user_datas.append(dict_.get(p)["data"])

    if other_person == False:
        user_index = user_names.index(str(ctx.author.id))
    else:
        user_index = user_names.index(str(person.id))

    user_list = list(user_datas[user_index])

    await ctx.send(f"{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[0])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[1])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[2])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[3])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[4])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[5])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[6])]))}")
			  
    await ctx.send(f"{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[7])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[8])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[9])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[10])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[11])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[12])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[13])]))}")
			  
    await ctx.send(f"{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[14])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[15])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[16])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[17])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[18])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[19])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[20])]))}")
			  
    await ctx.send(f"{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[21])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[22])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[23])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[24])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[25])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[26])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[27])]))}")
			  
    await ctx.send(f"{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[28])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[28])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[30])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[31])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[32])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[33])]))}{bot.get_emoji(int(emj_id_array[emj_name_array.index(user_list[34])]))}")
			  
    if other_person == True:
        await ctx.send(f"{str(person).split('#')[0]}'s base has been generated!")
    else:
        await ctx.send("Your base has been generated!")


@bot.command(name = 'startcolony')
async def startcolony(ctx):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        await ctx.send("You already have a colony")
    else:
        dict_[str(ctx.author.id)] = {
            "id": ctx.author.id,
            "money": 1750,
            "data": starterarray,
            "crafts": {
                "circuitboard": 0,
                "electromagnets": 0,
                "diamondtooltip": 0,
                "navkey": 0
            },
            "other_items": {
            },
            "ores": {
                "rock": 0,
                "iron": 0,
                "copper": 0,
                "gold": 0,
                "diamond": 0
            },
            "people": 0,
            "specialists": {
                "soldier": 0,
                "spy": 0,
                "scientist": 0,
                "engineer": 0,
                "artisan": 0,
                "miner": 0
            },
            "status": 0,
            "research": {
                "navkey": False,
                "basicmilitary": False
            },
            "currentquest": [False],
            "finishedquests": []
        }

        refresh_dict(dict_)

        add_log(str(ctx.author), "Mars Colony Sign Up", " ")

        await ctx.send(str(ctx.author).split('#')[0] + ', you started your own colony on mars!')
        time.sleep(1)
        await ctx.send("Your colony bank account has also been setup!")
        time.sleep(0.5)
        await ctx.send("Use coquests to find the basic starting guide")

@bot.command(name = 'shop')
async def shop(ctx):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        user_n = str(ctx.author).split('#')

        await ctx.send("Accessing database...")
        time.sleep(2)
        await ctx.send("Welcome back, " + user_n[0])

        json_file = open("buildstore.json", "r")
        json_builds = json.loads(json_file.read())
        json_file.close()

        json_file = open('research.json', 'r')
        json_data = json.loads(json_file.read())
        json_file.close()

        researches_ = []
        for re in json_data:
            researches_.append(re)

        embed_desc = " "
			
        first_build = 0
			
        for builds in json_builds:
            builds = json_builds.get(builds)

            if builds["research"][0]:
                try:
                    spec_key = None
                    for re in researches_:
                        if json_data.get(re)["id"] == builds["research"][1]:
                            spec_key = json_data.get(re)["key"]
                            break

                    haveResearch = False
                    try:
                        haveResearch = dict_[str(ctx.author.id)]["research"][spec_key]
                    except KeyError:
                        pass

                    if haveResearch == False:
                        continue
                except (IndexError, NameError):
                    pass

            bname = builds["name"]
            bid = builds["id"]
            bcost = builds["price"]
            bdesc = builds["description"]
				
            matreq = False
            try:
                matreq = len(builds["materials"]) > 0 #"key": {"name": _, "id": _, "quantity": _, "type": _}
            except KeyError:
                matreq = False

            mats = ""
            if matreq:
                mats = "\nMaterials:"

                json_file = open('workshop.json', 'r')
                recipe_data = json.loads(json_file.read())
                json_file.close()

                recipe_data2 = []
                for re in recipe_data:
                    recipe_data2.append(recipe_data.get(re))

                ore_file = open('ores.json', 'r')
                ore_data = json.loads(ore_file.read())
                ore_file.close()

                ore_names = []
                for o_d in ore_data:
                    ore_names.append(ore_data.get(o_d)["name"])

                comma_add = " "

                for ma in builds["materials"]:
                    ma = builds["materials"].get(ma)
                    if ma["type"] == "ore":
                        mats += comma_add + str(ma["quantity"]) + " " + ore_names[ma["id"]]
                    elif ma["type"] == "craft":
                        mats += comma_add + str(ma["quantity"]) + " " + recipe_data2[ma["id"]]["name"]
                    
                    if comma_add == " ":
                        comma_add = ", "

            if first_build == 0:
                embed_desc = embed_desc + '\n' + '**' + bname + '**' + '\n' + 'Id: ' + str(bid) + '\n' + '*' + str(bcost) + ' ' + f" {bot.get_emoji(m_coin)}" + '*' + mats + '\n' + bdesc
            else:
                embed_desc = embed_desc + '\n' + '\n' + '**' + bname + '**' + '\n' + 'Id: ' + str(bid) + '\n' + '*' + str(bcost) + ' ' + f" {bot.get_emoji(m_coin)}" + '*' + mats + '\n' + bdesc
					
            first_build = 1
        
        embed=discord.Embed(title="Colony Mars Build Shop", description = embed_desc, color=0xc8701e)
        await ctx.send(embed=embed)
    else:  
			  await ctx.send("What are you doing, you dont have a mars colony")


@bot.command(name = 'remove')
async def remove(ctx, *, askremove_array : str = None):
    if askremove_array == None:
        await ctx.send("You have to send: `coremove [tile_number]`")
        return

    if askremove_array.isnumeric() and int(askremove_array) < 36:
        dict_ = dict_access()

        if person_exists(ctx.author.id, dict_):
            user_data = list(dict_[str(ctx.author.id)]["data"])

            #remove_location_1 = list(askremove_array)[0]
            #remove_location_2 = list(askremove_array)[1]

            remove_location = int(askremove_array) - 1

            if user_data[remove_location] == "^":
                await ctx.send("You can't remove an occupied launch pad")
                return

            if user_data[remove_location] == "a":
                await ctx.send("There isn't anything there to break...")
            else:
                json_file = open("buildstore.json", "r")
                json_builds = json.loads(json_file.read())
                json_file.close()

                build_array_ = []
                for j_d in json_builds:
                    build_array_.append(j_d)

                removing_build = json_builds.get(build_array_[emj_name_array.index(user_data[remove_location]) - 2])

                user_data[remove_location] = "a"

                dict_[str(ctx.author.id)]["data"] = ''.join(user_data)

                time.sleep(2)

                new_user_money = dict_[str(ctx.author.id)]["money"] + round(removing_build["price"]/2)

                dict_[str(ctx.author.id)]["money"] = new_user_money

                refresh_dict(dict_)

                removed_price = str(round(removing_build["price"]/2))

                await ctx.send("Ok... we broke the " + str(removing_build["name"]) + " and cleaned up the scraps worth " + removed_price + f"{bot.get_emoji(m_coin)}")

        else:
            await ctx.send("What are you going to remove? You dont even have anything")


@bot.command(name = 'build')
async def build(ctx, *, askbuild_arrayraw : str = None):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        if askbuild_arrayraw == None:
            await ctx.send("You have to send `cobuild [object id] [tile number]`, look at options in coshop")
            return

        json_file = open("buildstore.json", "r")
        json_builds = json.loads(json_file.read())
        json_file.close()

        user_list = list(dict_[str(ctx.author.id)]["data"])

        try:
            askbuild_arrayraw = askbuild_arrayraw.split(' ')

            try:
                askbuild_arrayraw1 = askbuild_arrayraw[1]
            except IndexError:
                askbuild_arrayraw1 = None

            buildings_ = []
            for j_d in json_builds:
                buildings_.append(j_d)

            ask_name = ""

            double_name = False

            if not str(askbuild_arrayraw[0]).isnumeric() and not askbuild_arrayraw[0] == None and str(askbuild_arrayraw1).isnumeric() or askbuild_arrayraw1 == None:
                ask_name = askbuild_arrayraw[0]
            elif not str(askbuild_arrayraw[0]).isnumeric() and not str(askbuild_arrayraw1).isnumeric() and not askbuild_arrayraw1 == None:
                ask_name = " ".join([askbuild_arrayraw[0], askbuild_arrayraw1])
                double_name = True

            if ask_name.lower().replace(" ", "") in buildings_:
                askbuild_arrayraw[0] = str(json_builds.get(ask_name.lower().replace(" ", ""))["id"])
                if double_name:
                    askbuild_arrayraw1 = None

            if askbuild_arrayraw1 == None:
                n = 1
                for bd in user_list:
                    if bd == "a":
                        askbuild_arrayraw.append(str(n))
                    n+=1

        except ValueError:
            await ctx.send("No no no, you have to send:" + " `cobuild [object id] [tile number]`")
            await ctx.send("For example: " + "`cobuild 1 24`" + "Which is constructing the building with id 1 on the 24th tile")
            await ctx.send("Options are found in coshop")
            return

        if askbuild_arrayraw[0].isnumeric() and askbuild_arrayraw[1].isnumeric():
            build_id = int(askbuild_arrayraw[0])

            build_array_ = []
            for j_d in json_builds:
                build_array_.append(j_d)

            try:
                req_build = json_builds.get(build_array_[build_id])
            except IndexError:
                await ctx.send("No no no, you have to send:" + " `cobuild [object id] [tile number]`")
                await ctx.send("For example: " + "`cobuild 1 24`" + "Which is constructing the building with id 1 on the 24th tile")
                await ctx.send("Options are found in coshop")
                return

            user_cash = dict_[str(ctx.author.id)]["money"]

            matreq = False
            try:
                matreq = len(req_build["materials"]) > 0 #"key": {"name": _, "id": _, "quantity": _, "type": _}
            except KeyError:
                matreq = False

            if int(askbuild_arrayraw[1]) > 34:
                await ctx.send("Number is over 35, you dont have that much territory")
                return

            build_location = int(askbuild_arrayraw[1]) - 1

            if req_build["l_id"] == "h":
                if "h" in user_list or "^" in user_list:
                    await ctx.send("You already have a launch pad!")
                    return

            if not user_list[build_location] == "a":
                await ctx.send("That place is taken... gotta remove the building first!")
                return

            json_file = open('research.json', 'r')
            json_data = json.loads(json_file.read())
            json_file.close()

            researches_ = []
            for re in json_data:
                researches_.append(re)

            if req_build["research"][0]:
                try:
                    spec_key = None
                    for re in researches_:
                        if json_data.get(re)["id"] == req_build["research"][1]:
                            spec_key = json_data.get(re)["key"]
                            break

                    haveResearch = False
                    try:
                        haveResearch = dict_[str(ctx.author.id)]["research"][spec_key]
                    except KeyError:
                        pass

                    if haveResearch == False:
                        await ctx.send("You cannot build this")
                        return
                except IndexError:
                    pass

            if matreq:
                for m_ in req_build["materials"]:
                    m = req_build["materials"].get(m_)
                    if dict_[str(ctx.author.id)][m["type"] + "s"][m_] >= m["quantity"]:
                        dict_[str(ctx.author.id)][m["type"] + "s"][m_] = dict_[str(ctx.author.id)][m["type"] + "s"][m_] - m["quantity"]
                    else:
                        await ctx.send("You do not have enough " + m["name"] + "s")
                        return

            if int(user_cash) >= int(req_build["price"]):
                await ctx.send("Building...")
                time.sleep(2)

                user_cash_now = int(user_cash) - int(req_build["price"])

                dict_[str(ctx.author.id)]["money"] = user_cash_now

                user_list[build_location] = req_build["l_id"]

                dict_[str(ctx.author.id)]["data"] = ''.join(user_list)

                refresh_dict(dict_)

                await ctx.send("Phew, we finished building the " + req_build["name"])
            else:
                await ctx.send("Not enough money")
        else:
            await ctx.send("No no no, you have to send:" + " `cobuild [object id] [tile number]`")
            await ctx.send("For example: " + "`cobuild 1 24`" + "Which is constructing the building with id 1 on the 24th tile")
            await ctx.send("Options are found in coshop")

    else:
        await ctx.send("You cannot build into inexistence, you dont have a mars colony, type costartcolony")


@bot.command(name = 'bank')
async def bank(ctx, person: discord.Member = None):
    dict_ = dict_access()
    user_names = []
    for p in dict_:
        user_names.append(str(dict_.get(p)["id"]))

    if not person == None:
        other_person = True
    else:
        other_person = False

    if other_person == True and not person == None:
        if not str(person.id) in user_names:
            await ctx.send(f"{str(person).split('#')[0]} dosen't have a colony")
            return
    else:
        if not str(ctx.author.id) in user_names:
            await ctx.send("You do not have a colony, type costartcolony")
            return

    if other_person == False:
        user_id_ = str(ctx.author.id)
        user_n = str(ctx.author).split('#')
    else:
        user_id_ = str(person.id)
        user_n = str(person).split('#')

    user_moneycount = dict_[user_id_]["money"]

    bankembed = discord.Embed(title = user_n[0] + "'s Colony Bank", description = "Colony Bank: " + str(user_moneycount) + ' ' + f"{bot.get_emoji(m_coin)}", color = 0x4e4e79)

    await ctx.send(embed = bankembed)


@bot.command(name = 'daily', pass_context = True)
@commands.cooldown(1, 60*60*24, commands.BucketType.user)
async def daily(ctx):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        questNotify = quest_check("codaily", ctx.author.id)[0]
        random_income = random.randint(150, 500)

        usercash_now = dict_[str(ctx.author.id)]["money"] + random_income

        dict_[str(ctx.author.id)]["money"] = usercash_now

        refresh_dict(dict_)

        await ctx.send(f"You got {str(random_income)} {bot.get_emoji(m_coin)}")

        if questNotify:
            quest_notify(ctx.author.id)
    else:
        await ctx.send("You dont have a colony, type costartcolony")
        daily.reset_cooldown(ctx)

@daily.error
async def daily_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
        msg = 'Wait for codaily to recharge in ' + remaining_time
        await ctx.send(msg)
    else:
        raise error

@bot.command(name = 'commands')
async def command_list(ctx, specific : str = None):
    json_file = open("commandslist.json", "r")
    json_commands = json.loads(json_file.read())
    json_file.close()

    questNotify = quest_check("cocommands", ctx.author.id)[0]

    page = 0

    if not specific == None:
        if not specific.isnumeric() and not specific == "all":
            await ctx.send('The command is: `cocommands [page number OR "all"]`')
            return
        elif specific.isnumeric():
            page = int(specific)

    maxpage = 0
    for com in json_commands:
        com = json_commands.get(com)
        if com["page"] > maxpage:
            maxpage = com["page"]

    if not specific == "all":
        if page > maxpage:
            await ctx.send("The page is out of range")
            return

    embed_desc = " "

    first_c = False

    for command_n in json_commands:
        command_ = json_commands.get(command_n)
        cname = str(command_n)
        cdesc = command_["description"]

        if specific == "all" or command_["page"] == page:
            if first_c == False:
                embed_desc = embed_desc + '\n **' + cname + '** \n' + cdesc
            else:
                embed_desc = embed_desc + '\n \n **' + cname + '** \n' + cdesc
                        
            first_c = True

    helpembed=discord.Embed(title="Colony Mars Command List", description = embed_desc, color=0xffffff)
    if specific == "all":
        helpembed.set_footer(text = "all pages")
    else:
        if specific == None:
            helpembed.set_footer(text = str(page) + "/" + str(maxpage) + " page   -   ( cocommands [page number OR all] )")
        else:
            helpembed.set_footer(text = str(page) + "/" + str(maxpage) + " page")

    if questNotify:
        quest_notify(ctx.author.id)

    await ctx.send(embed=helpembed)


@bot.command(name = 'error')
async def report_error(ctx, *, error_msg : str = None):
    if error_msg == None or error_msg == " ":
        await ctx.send("Invalid error message")
        return

    add_log(str(ctx.author), "ERROR", error_msg)

    await ctx.send("Thanks, your error was submitted :)")


@bot.command(name = 'feedback')
async def submit_feedback(ctx, *, feedback : str = None):
    if feedback == None or feedback == " ":
        await ctx.send("Empty feedback")
        return

    add_log(str(ctx.author), "Feedback", feedback)

    await ctx.send("Thank you for giving us feedback about the bot :)")


@bot.command(name = 'mine')
@commands.cooldown(1, 60 * 60 * 3, commands.BucketType.user)
async def mine_ores(ctx):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        user_data = list(dict_[str(ctx.author.id)]["data"])

        num_ofminers = dict_[str(ctx.author.id)]["specialists"]["miner"]
        num_ofmines = 0
        for x in user_data:
            if x == "e":
                num_ofmines += 1

        if "e" in user_data:
            questNotify = quest_check("comine", ctx.author.id)[0]
            await ctx.send("Yes commander, starting the miners...")
            time.sleep(5)
            found_rocks = random.randint(0 + int(num_ofminers), round((15 + int(num_ofminers) * (num_ofmines * 0.75 + 0.25))))

            if found_rocks == 0:
                await ctx.send("Sorry, didnt get anything")
                return
            else:
                if found_rocks > 1:
                    rock_plural = "rocks"
                else:
                    rock_plural = "rock"

                if "j" in user_data:
                    user_rock = dict_[str(ctx.author.id)]["ores"]["rock"]

                    new_user_rock = user_rock + found_rocks

                    dict_[str(ctx.author.id)]["ores"]["rock"] = new_user_rock

                    if questNotify:
                        quest_notify(ctx.author.id)

                    refresh_dict(dict_)

                    await ctx.send(f"Ok we have got {str(found_rocks)} {rock_plural} and stored them in the storage facility")
                    if not dict_[str(ctx.author.id)]["other_items"].get("radio_relic") == 1 and not dict_[str(ctx.author.id)]["other_items"].get("radio_relic") == "^" and random.randint(0,100) < 34 and dict_[str(ctx.author.id)]["current_quest"][0]:
                        if dict_[str(ctx.author.id)]["current_quest"][1] == "talkwithstrangers":
                            time.sleep(1.5)
                            await ctx.send("WAIT A SECOND")
                            time.sleep(0.15)
                            await ctx.send("We just dug up something verry interesting")
                            time.sleep(0.15)
                            await ctx.send("It looks like some sort of an ancient relic?!")
                            await ctx.send("Our scientists believe it can be implemented to send some sort of radio signals...")
                            await ctx.send("If only there was a way to implement it to our technology...")
                            dict_[str(ctx.author.id)]["other_items"]["radio_relic"] = 1
                            if questNotify:
                                quest_notify(ctx.author.id)
                            refresh_dict(dict_)
                        
                else:
                    await ctx.send(f"Well... we found {str(found_rocks)} {rock_plural} but you dont have a storage so...")
        else:
            await ctx.send("You don't have an Earth Mine, Mars rocks are hard, not gonna mine with your hands")
    else:
        await ctx.send("You don't even have a colony, type costartcolony")

@mine_ores.error
async def mine_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
        msg = 'The mines will recieve the next load in ' + remaining_time
        await ctx.send(msg)
    else:
        raise error


@bot.command(name = 'inventory')
async def storage_inventory(ctx, person : discord.Member = None):
    dict_ = dict_access()
    if person == None:
        other_person = False
    else:
        other_person = True
    
    user_names = []
    for p in dict_:
        user_names.append(str(dict_.get(p)["id"]))

    if other_person == False:
        user_id_ = str(ctx.author.id)
    else:
        user_id_ = str(person.id)

    user_data = list(dict_[user_id_]["data"])

    if other_person == False:
        user_name = str(ctx.author).split('#')[0]
    else:
        user_name = str(person).split('#')[0]

    if other_person == True:
        if not str(person.id) in user_names:
            await ctx.send(f"{str(person).split('#')[0]} dosen't have a colony")
            return
    else:
        if not str(ctx.author.id) in user_names:
            await ctx.send('YOU DONT HAVE A COLONY, use costartcolony to get one')
            return

    questNotify = False
    if other_person == False:
        questNotify = quest_check("coinventory", ctx.author.id)[0]

    if "j" in user_data:
        await ctx.send("Opening facility...")
        time.sleep(2)

        embed_desc = "**Rocks**: " + str(dict_[user_id_]["ores"]["rock"]) + "\n\n**Iron**: " + str(dict_[user_id_]["ores"]["iron"]) + "\n\n**Copper**: " + str(dict_[user_id_]["ores"]["copper"]) + "\n\n**Gold**: " + str(dict_[user_id_]["ores"]["gold"]) + "\n\n**Diamonds**: " + str(dict_[user_id_]["ores"]["diamond"])

        embed=discord.Embed(title=user_name+"'s Storage Facility", description = embed_desc, color=0xffffff)

        await ctx.send(embed = embed)

        if questNotify:
            quest_notify(ctx.author.id)
    else:
        if other_person == True:
            await ctx.send(f"{user_name} dosent have a storage facility so...")
        else:
            await ctx.send("You dont have a storage facility so...")


@bot.command(name = 'refine')
@commands.cooldown(1, 60 * 30, commands.BucketType.user)
async def refine_ores(ctx, rocks : str = None):
    dict_ = dict_access()
    if rocks == None:
        await ctx.send("The command is `corefine [number_of_rocks OR max]`")
        refine_ores.reset_cooldown(ctx)
        return

    user_data = list(dict_[str(ctx.author.id)]["data"])

    if person_exists(ctx.author.id, dict_):
        questNotify = quest_check("corefine", ctx.author.id)[0]

        num_of_refiners = 0
        for x in user_data:
            if x == "b":
                num_of_refiners += 1

        if rocks.lower() == "max":
            if dict_[str(ctx.author.id)]["ores"]["rock"] == 0:
                await ctx.send("You dont have any rocks")
                refine_ores.reset_cooldown(ctx)
                return

            if dict_[str(ctx.author.id)]["ores"]["rock"] > num_of_refiners * 10:
                rocks = str(num_of_refiners * 10)
            else:
                rocks = dict_[str(ctx.author.id)]["ores"]["rock"]

        if int(rocks) == 0:
            await ctx.send("You cant refine 0 rocks")
            refine_ores.reset_cooldown(ctx)
            return

        if not rocks.isnumeric():
            await ctx.send("Nah, you have to send ```corefine number_of_rocks```")
            refine_ores.reset_cooldown(ctx)
            return

        if int(rocks) > dict_[str(ctx.author.id)]["ores"]["rock"]:
            await ctx.send("You are trying to refine more rocks then you have")
            refine_ores.reset_cooldown(ctx)
            return

        if int(rocks) > num_of_refiners * 10:
            await ctx.send("Thats too much rocks, the limit is 10 per refiner, so " + str(num_of_refiners * 10) + " for you")
            refine_ores.reset_cooldown(ctx)
            return

        if "b" in user_data:
            await ctx.send("Getting the refiner ready!")
            time.sleep(1)
            await ctx.send("Refining...")
            time.sleep(4)

            userore_0 = dict_[str(ctx.author.id)]["ores"]["rock"] - int(rocks)

            refine_while_int = int(rocks)

            userore_1 = 0
            userore_2 = 0
            userore_3 = 0
            userore_4 = 0

            for x in range(refine_while_int):
                rock_percentage = random.randint(0,100)

                if rock_percentage < 51:
                    userore_1 += round(random.randint(100, 140 + num_of_refiners * 35)/100)

                if rock_percentage > 57 and rock_percentage < 87:
                    userore_2 += round(random.randint(100, 140 + num_of_refiners * 27)/100)

                if rock_percentage > 87 and rock_percentage < 96:
                    userore_3 += round(random.randint(100, 140 + num_of_refiners * 20)/100)

                if rock_percentage > 96:
                    userore_4 += round(random.randint(100, 140 + num_of_refiners * 10)/100)

            dict_[str(ctx.author.id)]["ores"]["rock"] = userore_0
            dict_[str(ctx.author.id)]["ores"]["iron"] = dict_[str(ctx.author.id)]["ores"]["iron"] + userore_1
            dict_[str(ctx.author.id)]["ores"]["copper"] = dict_[str(ctx.author.id)]["ores"]["copper"] + userore_2
            dict_[str(ctx.author.id)]["ores"]["gold"] = dict_[str(ctx.author.id)]["ores"]["gold"] + userore_3
            dict_[str(ctx.author.id)]["ores"]["diamond"] = dict_[str(ctx.author.id)]["ores"]["diamond"] + userore_4

            if questNotify:
                quest_notify(ctx.author.id)

            refresh_dict(dict_)

            await ctx.send("We have found " + str(int(userore_1)) + " iron, " + str(int(userore_2)) + " copper, " + str(int(userore_3)) + " gold and " + str(userore_4) + " diamonds and also lost " + str(abs(int(int(rocks)) - int(userore_1) - int(userore_2) - int(userore_3) - int(userore_4))) + " rocks during refining")

        else:
            await ctx.send("First create a refiner!")
            refine_ores.reset_cooldown(ctx)
    else:
        await ctx.send("You cannot refine without a colony")
        refine_ores.reset_cooldown(ctx)

@refine_ores.error
async def refine_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
        msg = 'The refiners will recharge in ' + remaining_time
        await ctx.send(msg)
    else:
        raise error


@bot.command(name = 'work')
@commands.cooldown(1, 60 * 60, commands.BucketType.user)
async def work(ctx):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        questNotify = quest_check("cowork", ctx.author.id)[0]

        random_income = random.randint(50, 250)

        usercash_now = dict_[str(ctx.author.id)]["money"] + random_income

        dict_[str(ctx.author.id)]["money"] = usercash_now

        refresh_dict(dict_)

        phrase_list = [f"After picking up and selling a few rocks you recieve {str(random_income)} {bot.get_emoji(m_coin)}", 
        f"You delivered some packages on a rover you got {str(random_income)} {bot.get_emoji(m_coin)}", 
        f"Genetic modification got you {str(random_income)} {bot.get_emoji(m_coin)}", 
        f"You slapped a wanted criminal and got {str(random_income)} {bot.get_emoji(m_coin)}", 
        f"Fixed a rover, {str(random_income)} {bot.get_emoji(m_coin)} recieved", 
        f"You took out the trash and you got {str(random_income)} {bot.get_emoji(m_coin)}"]

        work_phrase = phrase_list[random.randint(0, 5)]

        await ctx.send(work_phrase)

        if questNotify:
            quest_notify(ctx.author.id)
    else:
        await ctx.send("You dont have a colony, type costartcolony")
        work.reset_cooldown(ctx)

@work.error
async def work_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
        msg = 'Wait for cowork to recharge in ' + remaining_time
        await ctx.send(msg)
    else:
        raise error

@bot.command(name = 'workshop')
async def workshop_list(ctx):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        user_data = list(dict_[str(ctx.author.id)]["data"])

        json_file = open('workshop.json', 'r')
        recipe_data = json.loads(json_file.read())
        json_file.close()

        json_file = open('research.json', 'r')
        json_data = json.loads(json_file.read())
        json_file.close()

        researches_ = []
        for re in json_data:
            researches_.append(re)

        embed_desc = " "

        first_recipe = 0
			
        if "k" in user_data:
            for builds__ in recipe_data:
                builds = recipe_data.get(builds__)

                if builds["research"][0]:
                    try:
                        spec_key = None
                        for re in researches_:
                            if json_data.get(re)["id"] == builds["research"][1]:
                                spec_key = json_data.get(re)["key"]
                                break

                        haveResearch = False
                        try:
                            haveResearch = dict_[str(ctx.author.id)]["research"][spec_key]
                        except KeyError:
                            pass

                        if haveResearch == False:
                            continue
                    except IndexError:
                        pass

                rname = builds["name"]
                rid = builds["id"]
                rsellprice = builds["price"]
                rdesc = builds["description"]

                numOfOwned = 0

                try:
                    numOfOwned = dict_[str(ctx.author.id)]["crafts"][builds__]
                except KeyError:
                    dict_[str(ctx.author.id)]["crafts"][builds__] = 0
                    refresh_dict(dict_)
                    numOfOwned = 0

                rname = rname + f" *(Owned: {str(numOfOwned)})*"

                rmaterials = builds["materials"]

                mats = "**Materials:** "

                recipe_data2 = []
                for re in recipe_data:
                    recipe_data2.append(recipe_data.get(re))

                ore_file = open('ores.json', 'r')
                ore_data = json.loads(ore_file.read())
                ore_file.close()

                ore_names = []
                for o_d in ore_data:
                    ore_names.append(ore_data.get(o_d)["name"])

                for ma in rmaterials:
                    ma = rmaterials.get(ma)
                    if ma["type"] == "ore":
                        mats += "\n  -" + str(ma["quantity"]) + " " + ore_names[ma["id"]]
                    elif ma["type"] == "craft":
                        mats += "\n  -" + str(ma["quantity"]) + " " + recipe_data2[ma["id"]]["name"]

                n = 0

                start_n = 0

                if first_recipe == 0:
                    embed_desc = embed_desc + '\n' + '**' + rname + '**' + '\n' + 'Id: ' + str(rid) + '\n' + 'Selling Price: ' + str(rsellprice) + '\n*' + rdesc + '*' + '\n' + mats
                else:
                    embed_desc = embed_desc + '\n\n' + '**' + rname + '**' + '\n' + 'Id: ' + str(rid) + '\n' + 'Selling Price: ' + str(rsellprice) + '\n*' + rdesc + '*' + '\n' + mats
					
                first_recipe = 1

            embed=discord.Embed(title="WorkShop Recipes", description = embed_desc, color=878787)
            await ctx.send(embed=embed)


        else:
            await ctx.send("You do not have a workshop")
    else:
        await ctx.send("No colony, no crafting, type costartcolony")


@bot.command(name = 'colonize')
@commands.cooldown(1, 60 * 60 * 12, commands.BucketType.user)
async def colonize(ctx):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        user_data = list(dict_[str(ctx.author.id)]["data"])

        if "^" in user_data:
            await ctx.send("You can't accept more ships now!")
            return

        if not "d" in user_data:
            await ctx.send("You don't have an Oxygenerator, what are they going to breath?")
            return

        if not "f" in user_data:
            await ctx.send("You don't have a Biodome, Umm... human eat food...")
            return

        if not "g" in user_data:
            await ctx.send("Where is you're Accomodation Pod?")
            return

        if not "h" in user_data:
            await ctx.send("Wait what, where's your Launch Pad? Wait.. NO DON'T CRASH INTO THE-")
            return

        if not "i" in user_data:
            await ctx.send("People don't drink rocks, build a water mine")
            return

        try:
            if dict_[str(ctx.author.id)]["crafts"]["navkey"] >= 1:
                await ctx.send("Using **Space Navigational Key** to land rocket...")
                dict_[str(ctx.author.id)]["crafts"]["navkey"] = dict_[str(ctx.author.id)]["crafts"]["navkey"] - 1
            else:
                await ctx.send("You are prepared to import a colonier ship, research and craft a **Space Navigational Key** to land it")
                colonize.reset_cooldown(ctx)
                return
        except KeyError:
            dict_[str(ctx.author.id)]["crafts"]["navkey"] = 0
            refresh_dict(dict_)
            await ctx.send("You are prepared to import a colonier ship, research and craft a **Space Navigational Key** to land it")
            colonize.reset_cooldown(ctx)
            return
        
        time.sleep(random.randint(2,5))
        random_people = random.randint(5,25)

        user_people = dict_[str(ctx.author.id)]["people"]

        old_user_specialist = dict_[str(ctx.author.id)]["specialists"]

        #Soldier|Spy|Scientist|Engineer|Artisan|Miner

        if dict_[str(ctx.author.id)]["specialists"]["soldier"] < 1:
            dict_[str(ctx.author.id)]["specialists"]["soldier"] = 1
            random_people -= 1

        for ppl in range(random_people): #Specialist generation
            if random.randint(1,20) == 1:
                dict_[str(ctx.author.id)]["specialists"]["soldier"] = dict_[str(ctx.author.id)]["specialists"]["soldier"] + 1
                random_people -= 1
                continue
            if random.randint(1,30) == 1:
                dict_[str(ctx.author.id)]["specialists"]["spy"] = dict_[str(ctx.author.id)]["specialists"]["spy"] + 1
                random_people -= 1
                continue
            if random.randint(1,50) == 1:
                dict_[str(ctx.author.id)]["specialists"]["scientist"] = dict_[str(ctx.author.id)]["specialists"]["scientist"] + 1
                random_people -= 1
                continue
            if random.randint(1,80) == 1:
                dict_[str(ctx.author.id)]["specialists"]["engineer"] = dict_[str(ctx.author.id)]["specialists"]["engineer"] + 1
                random_people -= 1
                continue
            if random.randint(1,65) == 1:
                dict_[str(ctx.author.id)]["specialists"]["artisan"] = dict_[str(ctx.author.id)]["specialists"]["artisan"] + 1
                random_people -= 1
                continue
            if random.randint(1,15) == 1:
                dict_[str(ctx.author.id)]["specialists"]["miner"] = dict_[str(ctx.author.id)]["specialists"]["miner"] + 1
                random_people -= 1
                continue

        new_user_people = user_people + random_people

        dict_[str(ctx.author.id)]["people"] = new_user_people

        launch_pad = user_data.index("h")

        new_user_data = user_data

        new_user_data[launch_pad] = "^"

        dict_[str(ctx.author.id)]["data"] = ''.join(new_user_data)
        refresh_dict(dict_)

        if new_user_people == user_people:
            await ctx.send("All arrived people are specialists")
        else:
            await ctx.send("Congrats! The ship got you " + str(random_people) + " people, make sure to send it back in launchpad later!")
        
        spec_names = ["Soldier", "Spy", "Scientist", "Engineer", "Artisan", "Miner"]

        n = 0

        if not old_user_specialist == dict_[str(ctx.author.id)]["specialists"]:
            msg = "Also you got"
            spec_differences = [str(dict_[str(ctx.author.id)]["specialists"]["soldier"]-old_user_specialist["soldier"]), str(dict_[str(ctx.author.id)]["specialists"]["spy"]-old_user_specialist["spy"]), str(dict_[str(ctx.author.id)]["specialists"]["scientist"]-old_user_specialist["scientist"]), str(dict_[str(ctx.author.id)]["specialists"]["engineer"]-old_user_specialist["engineer"]), str(dict_[str(ctx.author.id)]["specialists"]["artisan"]-old_user_specialist["artisan"]), str(dict_[str(ctx.author.id)]["specialists"]["miner"]-old_user_specialist["miner"])]
            for dif in spec_differences[n]:
                if int(spec_differences[n]) == 0:
                    msg += str(spec_differences[n]) + spec_names[n]
                    n += 1

            await ctx.send(msg)
    else:
        await ctx.send("You do not have a colony, use costartcolony to make one")
        colonize.reset_cooldown(ctx)

@colonize.error
async def colonize_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
        msg = "Wait for the next ship in " + remaining_time
        await ctx.send(msg)
    else:
        raise error


@bot.command(name = 'trade_terminal')
async def trade_terminal(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        questNotify = quest_check("cotrade_terminal", ctx.author.id)[0]
        try:
            needReturn = quest_check("cotrade_terminal", ctx.author.id)[1]
        except IndexError:
            needReturn = False

        user_data = list(dict_[str(ctx.author.id)]["data"])

        if "c" in user_data:
            msg_ = await ctx.send("Accessing intergalactic market...")

            content_change = "Accessing intergalactic market..."

            for x in range(6):
                if content_change == "Accessing intergalactic market...":
                    content_change = "Accessing intergalactic market."
                elif content_change == "Accessing intergalactic market.":
                    content_change = "Accessing intergalactic market.."
                elif content_change == "Accessing intergalactic market..":
                    content_change = "Accessing intergalactic market..."

                await msg_.edit(content = content_change)
                time.sleep(0.33)

            json_file = open('workshop.json', 'r')
            recipe_data = json.loads(json_file.read())
            json_file.close()

            ore_file = open('ores.json', 'r')
            ore_data = json.loads(ore_file.read())
            ore_file.close()

            trade_embed_desc = ""

            first_ore_ = False

            for ore_ in ore_data:
                ore_ = ore_data.get(ore_)
                if first_ore_:
                    trade_embed_desc += "**" + ore_["name"] + "**\nId: " + str(ore_["id"]) + "\nSelling price: " + str(ore_["price"])
                else:
                    trade_embed_desc += "\n\n**" + ore_["name"] + "**\nId: " + str(ore_["id"]) + "\nSelling price: " + str(ore_["price"])

            for item in recipe_data:
                item = recipe_data.get(item)
                rname = item["name"]
                rid = item["id"]
                rsellprice = str(item["price"])

                trade_embed_desc = trade_embed_desc + '\n\n**' + rname + '**\nId: ' + str(int(rid) + 5) + '\nSelling price: ' + rsellprice
            
            embed=discord.Embed(title="Intergalactical Market", description = trade_embed_desc, color=2899536)
            await ctx.send(embed=embed)
            time.sleep(3)
            await ctx.send('What would you like to do at the trade terminal today?(sell, no)') #add buy later
            try:
                action = await bot.wait_for('message', check=check, timeout = 15.0)
            except asyncio.TimeoutError:
                await ctx.send("Disconnecting from terminal")
                return
            action = action.content

            try:
                if action == None:
                    await ctx.send("Disconnecting from terminal")
                    return
            except UnboundLocalError:
                try:
                    action = await bot.wait_for('message', check=check, timeout = 15.0)
                except asyncio.TimeoutError:
                    await ctx.send("Disconnecting from terminal")
                    return
                action = action.content

            if action.lower() == 'sell':
                try:
                    await ctx.send('Select what your selling and the quantity')
                    action = await bot.wait_for('message', check=check, timeout = 15.0)
                    sell_array = action.content.split(' ')
                    if sell_array[0].isnumeric() and sell_array[1].isnumeric():
                        if int(sell_array[0]) < 5:
                            selling_ore = int(list(dict_[str(ctx.author.id)]["ores"].values())[int(sell_array[0])])

                            if selling_ore >= int(sell_array[1]):
                                sell_ores = []
                                for ore_ in ore_data:
                                    sell_ores.append(str(ore_))

                                sell_ore_names = []
                                for ore_ in ore_data:
                                    sell_ore_names.append(ore_data.get(ore_)["name"])

                                selling_ore_name = sell_ores[int(sell_array[0])]

                                dict_[str(ctx.author.id)]["ores"][selling_ore_name] = selling_ore - int(sell_array[1])

                                user_money = dict_[str(ctx.author.id)]["money"]

                                ore_prices = []
                                for ore_ in ore_data:
                                    ore_prices.append(ore_data.get(ore_)["price"])

                                user_money += int(sell_array[1]) * ore_prices[int(sell_array[0])]

                                dict_[str(ctx.author.id)]["money"] = user_money

                                refresh_dict(dict_)

                                if questNotify and needReturn:
                                    quest_notify(ctx.author.id, return_ = "sell:any:any") #sell/buy:type of ore:quantity of ore

                                await ctx.send(f"You sold {str(sell_array[1])} {sell_ore_names[int(sell_array[0])]} and earned {str(int(sell_array[1]) * ore_prices[int(sell_array[0])])} {bot.get_emoji(m_coin)}")
                            else:
                                await ctx.send("Not enough selling product")
                        else:
                            json_file = open('workshop.json', 'r')
                            recipe_data = json.loads(json_file.read())
                            json_file.close()

                            all_crafts = []
                            for rec in recipe_data:
                                rec = recipe_data.get(rec)
                                all_crafts.append(rec)

                            if int(sell_array[0]) <= len(recipe_data) - 1 + 5:
                                sell_crft = list(dict_[str(ctx.author.id)]["crafts"].values())[int(sell_array[0]) - 5]

                                if sell_crft >= int(sell_array[1]):
                                    craft_ar = []
                                    for rcp in recipe_data:
                                        craft_ar.append(str(rcp))

                                    craft_name = craft_ar[int(sell_array[0]) - 5]

                                    dict_[str(ctx.author.id)]["crafts"][craft_name] = sell_crft - int(sell_array[1])

                                    user_money = dict_[str(ctx.author.id)]["money"]

                                    craft_price = all_crafts[int(sell_array[0]) - 5][2]

                                    user_money += int(craft_price) * int(sell_array[1])

                                    dict_[str(ctx.author.id)]["money"] = user_money

                                    craft_name = all_crafts[int(sell_array[0]) - 5][0]

                                    refresh_dict(dict_)

                                    await ctx.send(f"You sold {str(sell_array[1])} {craft_name} and earned {str(craft_price * int(sell_array[1]))} {bot.get_emoji(m_coin)}")


                                else:
                                      await ctx.send("Not enough selling product")

                            else:
                                      await ctx.send("Invalid selling id")
                            

                    else:
                        await ctx.send('Message is ``[selling id] [quantity to sell]``')
                except asyncio.TimeoutError:
                    await ctx.send("Disconnecting from terminal")
                    return
            else:
                await ctx.send("Goodbye, beep!")
            #Maybe also add buying or something with an elif statement in the middle of the if and else
        else:
            await ctx.send("You don't own an intergalactic trade terminal")
    else:
        await ctx.send("You do NOT have a colony, type costartcolony")


@bot.command(name = 'craft')
async def craft(ctx, id : str = None):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        user_data = list(dict_[str(ctx.author.id)]["data"])

        if id == None:
            await ctx.send("Send `cocraft [object_id]`, look at options in coworkshop")
            return

        if "k" in user_data:
            json_file = open('workshop.json', 'r')
            recipe_data = json.loads(json_file.read())
            json_file.close()

            recipe_keys = []
            for rec in recipe_data:
                recipe_keys.append(rec)

            if not id.isnumeric():
                if id.lower().replace(" ", "") in recipe_keys:
                    id = str(recipe_keys.index(id.lower().replace(" ", "")))
                else:
                    await ctx.send("Send `cocraft [object_id]`, look at options in coworkshop")
                    return

            json_file = open('research.json', 'r')
            json_data = json.loads(json_file.read())
            json_file.close()

            researches_ = []
            for re in json_data:
                researches_.append(re)

            id_array = []
                        
            #num_ofartis = dict_[str(ctx.author.id)]["specialists"]["artisan"] #Add some bonus from artisans

            for obj in recipe_data:
                obj = recipe_data.get(obj)
                id_array.append(int(obj["id"]))

            if int(id) in id_array:
                id = int(id)

                craft_obj = None

                for r_d in recipe_data:
                    if recipe_data.get(r_d)["id"] == id:
                        craft_obj = recipe_data.get(r_d)

                if craft_obj["research"][0]:
                    try:
                        spec_key = None
                        for re in researches_:
                            if json_data.get(re)["id"] == craft_obj["research"][1]:
                                spec_key = json_data.get(re)["key"]
                                break

                        haveResearch = False
                        try:
                            haveResearch = dict_[str(ctx.author.id)]["research"][spec_key]
                        except KeyError:
                            pass

                        if haveResearch == False:
                            await ctx.send("You cannot craft this")
                            return
                    except IndexError:
                        pass

                for itm_ in craft_obj["materials"]:
                    itm = craft_obj["materials"].get(itm_)
                        
                    if not dict_[str(ctx.author.id)][itm["type"] + "s"][itm_] >= itm["quantity"]:
                        await ctx.send("You do not have enough " + itm_ + "s")
                        return
                    else:
                        dict_[str(ctx.author.id)][itm["type"] + "s"][itm_] = dict_[str(ctx.author.id)][itm["type"] + "s"][itm_] - itm["quantity"]

                craft_ar = []
                for wrk in recipe_data:
                    craft_ar.append(str(wrk))

                craft_name = craft_ar[id]

                dict_[str(ctx.author.id)]["crafts"][craft_name] = dict_[str(ctx.author.id)]["crafts"][craft_name] + 1

                refresh_dict(dict_)

                craft_name_name = recipe_data[craft_name]["name"]
                  
                await ctx.send(f"You succesfully crafted the {craft_name_name}")
            else:
                await ctx.send("Invalid craft id")


@bot.command(name = 'spy') #Need to draw and add espionage embassy
@commands.cooldown(1, 60 * 60 * 6, commands.BucketType.user)
async def spy(ctx, person : discord.Member = None):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me

    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        user_data = dict_[str(ctx.author.id)]["data"]

        if "l" in user_data:
            if not dict_[str(ctx.author.id)]["specialists"]["spy"] > 0:
                await ctx.send("You dont even own a spy!")
                spy.reset_cooldown(ctx)
                return

            if person == None:
                await ctx.send("Please select person to perform espionage on, if the mission isnt on anyone, select yourself")
                spy.reset_cooldown(ctx)
                return

            if person_exists(person.id, dict_):
                enem_id = str(person.id)
            else:
                await ctx.send(f"{str(person)} does not have a colony")
                spy.reset_cooldown(ctx)
                return

            await ctx.send("Accessing espionage embassy databases...")
            time.sleep(1)
            await ctx.send("Select spy mission(rob, counter-spy)")
            try:
                action = await bot.wait_for('message', check=check, timeout = 15.0)
            except asyncio.TimeoutError:
                await ctx.send("Timeout, you left the embassy")
                spy.reset_cooldown(ctx)
                return
            action = action.content

            if action == 'rob':
                if ctx.author.id == person.id:
                    await ctx.send("Are you stupid? You cannot rob yourself")
                    spy.reset_cooldown(ctx)
                    return

                await ctx.send(f"Preparing to rob {str(person)}...")

                enem_stat = dict_[enem_id]["status"]

                if int(enem_stat) == 0:
                    robbing_pro = 0
                else:
                    robbing_pro = 1

                chance_torob = random.randint(0,100)

                expon_array = [90, 10]

                if chance_torob < expon_array[robbing_pro]:
                    time.sleep(3)

                    user_money = dict_[str(ctx.author.id)]["money"]

                    enem_money = dict_[enem_id]["money"]

                    robin_quan = random.randint(round(int(enem_money)/10), round(int(enem_money)/3))

                    enem_money = int(enem_money) - robin_quan
                    user_money = int(user_money) + robin_quan

                    dict_[str(ctx.author.id)]["money"] = user_money
                    dict_[enem_id]["money"] = enem_money

                    if int(robbing_pro) == 1:
                        dict_[enem_id]["status"] = 0

                    refresh_dict(dict_)

                    await ctx.send(f"You have stolen {str(robin_quan)} {bot.get_emoji(m_coin)} from {str(person)}")
                    
                else:
                    time.sleep(3)

                    dict_[str(ctx.author.id)]["specialists"]["spy"] = dict_[str(ctx.author.id)]["specialists"]["spy"] - 1

                    if int(robbing_pro) == 1:
                        dict_[enem_id]["status"] = 0

                    refresh_dict(dict_)

                    await ctx.send("Robbing failed, one spy lost")

            elif action == 'counter-spy':
                user_status = dict_[str(ctx.author.id)]["status"]

                if int(user_status) == 0:
                    dict_[str(ctx.author.id)]["status"] = 1

                    dict_[str(ctx.author.id)]["specialists"]["spy"] = dict_[str(ctx.author.id)]["specialists"]["spy"] - 1

                    refresh_dict(dict_)

                    await ctx.send("A spy was appointed to counter spy protection")
                else:
                    await ctx.send("You are already counter spying")
                    spy.reset_cooldown(ctx)
            else:
                await ctx.send("Invalid mission")
                spy.reset_cooldown(ctx)
        else:
            await ctx.send("You dont own an espionage embassy")
            spy.reset_cooldown(ctx)
    else:
        await ctx.send("You dont even have a colony, type costartcolony")
        spy.reset_cooldown(ctx)
            
@spy.error
async def spy_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
        msg = 'All your spies are on missions, wait ' + remaining_time
        await ctx.send(msg)
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Hey, that's not a real person")
        spy.reset_cooldown(ctx)
    else:
        raise error


@bot.command(name = 'research_station')
async def research_station(ctx):
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        user_data = list(dict_[str(ctx.author.id)]["data"])
      
        research_facility = False
        if "n" in user_data:
            research_facility = True

        research_list = []

        json_file = open('research.json', 'r')
        json_data = json.loads(json_file.read())
        json_file.close()
        
        n = 0

        json_data_keys = [key for key, val in json_data.items()]

        for obj in json_data:
            if research_facility:
                research_list.append(json_data_keys[n])
            else:
                if json_data.get(obj)["researchstation"] == False:
                    research_list.append(json_data_keys[n])
            n+=1

        hr1 = []
        hr2 = []

        n = 0
        for obj in research_list:
            haveResearch = False
            try:
                haveResearch = dict_.get(str(ctx.author.id))["research"][obj]
            except KeyError:
                pass

            if haveResearch:
                hr2.append(obj)
            else:
                hr1.append(obj)
            n+=1

        research_list = hr1 + hr2

        first_build = True

        embed_desc = ""

        if research_facility:
            embed_desc = "*(Research Facility: present)*"
        else:
            embed_desc = "*(Research Facility: not present)*"

        for obj in research_list:
            object_data = json_data.get(obj)

            prereq_ = "**Prerequisites:** "
            if object_data["prereq"] == False:
                prereq_ += "None"
            else:
                if len(object_data["prerequisites"]["building"]) > 0: #stored as a single id per building as seen in buildstore
                    prereq_ += "\n  -Buildings: "

                    json_file = open("buildstore.json", "r")
                    json_builds = json.loads(json_file.read())
                    json_file.close()

                    build_array_ = []
                    for j_d in json_builds:
                        build_array_.append(j_d)

                    first_thing = True

                    for ob in object_data["prerequisites"]["building"]:
                        if first_thing:
                            prereq_ += json_builds.get(build_array_[ob])["name"]
                        else:
                            prereq_ += ", " + json_builds.get(build_array_[ob])["name"]

                if len(object_data["prerequisites"]["research"]) > 0: #stored as a single id per research as seen in research.json
                    prereq_ += "\n  -Researches: "

                    research_names = []

                    for res in json_data:
                        research_names.append(json_data.get(res)["name"])

                    first_thing = True

                    for ob in object_data["prerequisites"]["research"]:
                        if first_thing:
                            prereq_ += research_names[ob]
                        else:
                            prereq_ += ", " + research_names[ob]

            mats = "**Materials: **"
            if object_data["matreq"] == False:
                mats += "None"
            else:
                if len(object_data["materials"]["item"]) > 0: #stored as name and quantity "name" :{"id": id, "quantity": quantity, "type": (craft/ore)}   #the id is the id found in the correspondant file for the ore/craft
                    mats += "\n -Items:"

                    json_file = open('workshop.json', 'r')
                    recipe_data = json.loads(json_file.read())
                    json_file.close()

                    recipe_data2 = []
                    for re in recipe_data:
                        recipe_data2.append(recipe_data.get(re))

                    ore_file = open('ores.json', 'r')
                    ore_data = json.loads(ore_file.read())
                    ore_file.close()

                    ore_names = []
                    for o_d in ore_data:
                        ore_names.append(ore_data.get(o_d)["name"])

                    for ma in object_data["materials"]["item"]:
                        ma = object_data["materials"]["item"].get(ma)
                        if ma["type"] == "ore":
                            mats += "\n  --" + str(ma["quantity"]) + " " + ore_names[ma["id"]]
                        elif ma["type"] == "craft":
                            mats += "\n  --" + str(ma["quantity"]) + " " + recipe_data2[ma["id"]]["name"]

                if len(object_data["materials"]["specialist"]) > 0: #stored as name and quantity "name" :{"id": id, "quantity": quantity}
                    mats += "\n -Specialists:"

                    spec_file = open('specialists.json', 'r')
                    spec_data = json.loads(spec_file.read())
                    spec_file.close()

                    spec_names = []
                    for s_d in spec_data:
                        spec_names.append(spec_data.get(s_d)["name"])

                    for sp in object_data["materials"]["specialist"]:
                        sp = object_data["materials"]["specialist"].get(sp)
                        mats += "\n  --" + str(sp["quantity"]) + " " + spec_names[sp["id"]]

            isOwned = " "

            haveResearch = False
            try:
                haveResearch = dict_.get(str(ctx.author.id))["research"][obj]
            except KeyError:
                pass

            if haveResearch:
                isOwned = " *(Researched)*"

            if first_build:
                embed_desc = embed_desc + "\n**" + object_data["name"] + "**" + isOwned + "\nId: " + str(object_data["id"]) + "\n" + object_data["description"] + "\n" + prereq_ + "\n" + mats
                first_build = False
            else:
                embed_desc = embed_desc + "\n\n**" + object_data["name"] + "**" + isOwned + "\nId: " + str(object_data["id"]) + "\n" + object_data["description"] + "\n" + prereq_ + "\n" + mats


        embed=discord.Embed(title="Research Facility", description = embed_desc, color=0xa00bb7)
        await ctx.send(embed=embed)
    else:
        await ctx.send("You do not own a colony")
    

@bot.command(name = 'research')
@commands.cooldown(1, 60 * 60 * 3, commands.BucketType.user)
async def research(ctx, target_id : str = None):
    dict_ = dict_access()

    if target_id == None or not target_id.isnumeric():
        await ctx.send("The command is `coresearch [research_id]`, look at options in coresearch_station")
        research.reset_cooldown(ctx)
        return

    target_id = int(target_id)

    if person_exists(ctx.author.id, dict_):
        json_file = open('research.json', 'r')
        json_data = json.loads(json_file.read())
        json_file.close()

        target_key = None
        target_ = None

        for re in json_data:
            if json_data.get(re)["id"] == target_id:
                target_key = json_data.get(re)["key"]
                target_ = json_data.get(re)

        if target_key == None or target_ == None:
            await ctx.send("This is not a valid research id")
            research.reset_cooldown(ctx)
            return

        haveResearch = False
        try:
            haveResearch = dict_[str(ctx.author.id)]["research"][target_key]
        except KeyError:
            pass

        if haveResearch:
            await ctx.send("You already researched " + target_["name"])
            research.reset_cooldown(ctx)
            return

        user_data = list(dict_[str(ctx.author.id)]["data"])
      
        research_facility = False
        if "n" in user_data:
            research_facility = True

        research_list = []
        
        n = 0

        json_data_keys = [key for key, val in json_data.items()]

        for obj in json_data:
            if research_facility:
                research_list.append(json_data_keys[n])
            else:
                if json_data.get(obj)["researchstation"] == False:
                    research_list.append(json_data_keys[n])
            n+=1

        if not target_["key"] in research_list:
            await ctx.send("You can not research this")
            research.reset_cooldown(ctx)
            return

        if target_["prereq"] == True:
            if len(target_["prerequisites"]["building"]) > 0:
                json_file = open("buildstore.json", "r")
                json_builds = json.loads(json_file.read())
                json_file.close()

                build_array_ = []
                for j_d in json_builds:
                    build_array_.append(j_d)

                for build_ in target_["prerequisites"]["building"]:
                    build_l_id = json_builds.get(build_array_[build_])["l_id"]

                    if not build_l_id in user_data:
                        await ctx.send("You do not have the " + json_builds.get(build_array_[build_])["name"] + " which is a prerequisite")
                        research.reset_cooldown(ctx)
                        return

            if len(target_["prerequisites"]["research"]) > 0:
                researches_ = []
                for re in json_data:
                    researches_.append(json_data.get(re))

                for re in target_["prerequisites"]["research"]:
                    haveResearch = False
                    try:
                        haveResearch = dict_[str(ctx.author.id)]["research"][researches_[re]["key"]]
                    except KeyError:
                        pass

                    if haveResearch == False:
                        await ctx.send("You didn't unlock " + researches_[re]["name"] + " which is a prerequisite")
                        research.reset_cooldown(ctx)
                        return

        if target_["matreq"] == True:
            if len(target_["materials"]["item"]) > 0:
                for itm_ in target_["materials"]["item"]:
                    itm = target_["materials"]["item"].get(itm_)
                    
                    if not dict_[str(ctx.author.id)][itm["type"] + "s"][itm_] >= itm["quantity"]:
                        await ctx.send("You do not have enough " + itm_ + "s")
                        research.reset_cooldown(ctx)
                        return
                    else:
                        dict_[str(ctx.author.id)][itm["type"] + "s"][itm_] = dict_[str(ctx.author.id)][itm["type"] + "s"][itm_] - itm["quantity"]

            if len(target_["materials"]["specialist"]) > 0:
                for spec_ in target_["materials"]["specialist"]:
                    spec = target_["materials"]["specialist"].get(spec_)

                    if not dict_[str(ctx.author.id)]["specialists"][spec_] >= spec["quantity"]:
                        await ctx.send("You do not have enough " + spec_ + "s")
                        research.reset_cooldown(ctx)
                        return
                    else:
                        dict_[str(ctx.author.id)]["specialists"][spec_] = dict_[str(ctx.author.id)]["specialists"][spec_] - spec["quantity"]

        dict_[str(ctx.author.id)]["research"][target_key] = True

        refresh_dict(dict_)

        await ctx.send("Research complete, **" + target_["name"] + "** discovered")    

    else:
        await ctx.send("You do not have a colony, type costartcolony")
        research.reset_cooldown(ctx)

@research.error
async def daily_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
        msg = 'Researchers will be ready again in ' + remaining_time
        await ctx.send(msg)
    else:
        raise error


@bot.command(name = 'stats')
async def stats(ctx, person : discord.Member = None):
    member_data_ = None
    if person == None:
        other_person = False
        member_data_ = ctx.author
    else:
        other_person = True
        member_data_ = person

    dict_ = dict_access()

    if other_person == True:
        if not person_exists(person.id, dict_):
            await ctx.send(f"{str(person).split('#')[0]} dosen't have a colony")
            return
    else:
        if not person_exists(ctx.author.id, dict_):
            await ctx.send('You arent signed up to Colony Mars')
            await ctx.send(f'Type {PREFIX}startcolony to start your own colony!')
            return

    if other_person == False:
        user_info = dict_[str(ctx.author.id)]
    else:
        other_person_id = person.id
        user_info = dict_[str(other_person_id)]

    user_pfp = member_data_.avatar.url

    user_info_ = [str(user_info["people"]), [str(user_info["specialists"]["soldier"]), str(user_info["specialists"]["spy"]), str(user_info["specialists"]["scientist"]), str(user_info["specialists"]["engineer"]), str(user_info["specialists"]["artisan"]), str(user_info["specialists"]["miner"])]]


    embed_desc = f"Mars Colonist\nNumber Of People: {user_info_[0]}\nSpecialists: {user_info_[1][0]} soldiers, {user_info_[1][1]} spies, {user_info_[1][2]} scientists, {user_info_[1][3]} engineers, {user_info_[1][4]} artisans, {user_info_[1][5]} miners"

    embed=discord.Embed(title="User: " + str(member_data_).split('#')[0], description = embed_desc, color=0xf5f4f7)
    embed.set_thumbnail(url = user_pfp)
    await ctx.send(embed=embed)


@bot.command(name = 'launchpad')
async def launchpad(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me
    dict_ = dict_access()
    if person_exists(ctx.author.id, dict_):
        user_data = list(dict_[str(ctx.author.id)]["data"])
        if "h" in user_data:
            await ctx.send("You have one empty launchpad")
        elif "^" in user_data:
            await ctx.send("You have a ship currently on your launchpad")
            await ctx.send("Choose what to do with it next (send_back, nothing)")

            try:
                action = await bot.wait_for('message', check=check, timeout = 15.0)
            except asyncio.TimeoutError:
                await ctx.send("Timeout, you exited the launchpad")
                return
            action = (action.content).lower()

            if action == "send_back":
                await ctx.send("Preparing to send ship back...")
                time.sleep(2)

                dict_[str(ctx.author.id)]["data"] = "".join(user_data).replace("^", "h")

                refresh_dict(dict_)

                await ctx.send("Ship was sent back")
            else:
                await ctx.send("Exiting the launchpad")

        else:
            await ctx.send("You do not own a launchpad")

    else:
        await ctx.send("You do not have a colony, type costartcolony to start")


@bot.command(name = 'expeditions')
async def expeditions(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        user_data = list(dict_[str(ctx.author.id)]["data"])
        if "o" in user_data:
            isOnExpedition = None
            try:
                isOnExpedition = (len(dict_[str(ctx.author.id)]["expedition"]) > 0) #"expedition": {"type": _, "people": _, "failed": _, "gains": {}, "returntime": _} #for every element in gains --> "key": {"name": _,"id": _, "quantity": _, "type": _}
            except KeyError:
                dict_[str(ctx.author.id)]["expedition"] = {}
                refresh_dict(dict_)
                isOnExpedition = False

            if isOnExpedition:
                if dt.now() > dt.strptime(dict_[str(ctx.author.id)]["expedition"]["returntime"], r"%Y-%m-%d %H:%M:%S"):
                    if dict_[str(ctx.author.id)]["expedition"]["failed"] == False:
                        await ctx.send("Your **" + str(dict_[str(ctx.author.id)]["expedition"]["type"]) + "** expedition has returned")
                        
                        gain_string = "The expedition recieved "
                        first_gain = True
                        for g_ in dict_[str(ctx.author.id)]["expedition"]["gains"]:
                            g = dict_[str(ctx.author.id)]["expedition"]["gains"].get(g_)

                            if g["type"] == "ore":
                                dict_[str(ctx.author.id)]["ores"][g_] = dict_[str(ctx.author.id)]["ores"][g_] + g["quantity"]
                            elif g["type"] == "craft":
                                dict_[str(ctx.author.id)]["crafts"][g_] = dict_[str(ctx.author.id)]["crafts"][g_] + g["quantity"]

                            if first_gain:
                                gain_string += str(g["quantity"]) + " " + g["name"] + ["s", ""][[True, False].index(g["quantity"] > 1)]
                                first_gain = False
                            else:
                                gain_string += ", " + str(g["quantity"]) + " " + g["name"] + ["s", ""][[True, False].index(g["quantity"] > 1)]

                        await ctx.send(gain_string)

                        hasMod = False
                        try:
                            if not dict_[str(ctx.author.id)]["expedition"]["mod"] == None:
                                hasMod = True
                        except KeyError:
                            pass

                        #FOR MODIFICATIONS FROM EXPEDITIONS
                        if hasMod:
                            if dict_[str(ctx.author.id)]["expedition"]["mod"] == "alien_1_meet":
                                pass

                        dict_[str(ctx.author.id)]["people"] = dict_[str(ctx.author.id)]["people"] + dict_[str(ctx.author.id)]["expedition"]["people"]
                        dict_[str(ctx.author.id)]["expedition"] = {}
                        refresh_dict(dict_)
                        return

                    else:
                        await ctx.send("Your **" + str(dict_[str(ctx.author.id)]["expedition"]["type"]) + "** expedition has failed, all members dead, nothing found")
                        return
                else:
                    time_left = str(datetime.timedelta(seconds = (dt.strptime(dict_[str(ctx.author.id)]["expedition"]["returntime"], r"%Y-%m-%d %H:%M:%S") - dt.now()).total_seconds())).split('.')[0]
                    await ctx.send("Your **" + str(dict_[str(ctx.author.id)]["expedition"]["type"]) + "** expedition will arrive in " + time_left)
                    return
            else:
                expedition_embed = "**Basic**\nNumber of People: 5\nDuration: 3 hours\nFailure chance: 30%\nPossible returns: Rocks, Iron, Copper\n\n**Advanced**\nNumber of People: 15\nDuration: 6 hours\nFailure chance: 20%\nPossible returns: Rocks, Iron, Copper, Gold, Diamonds\n\n**Expert**\nNumber of People: 30\nDuration: 12 hours\nFailure chance: 15%\nPossible returns: Rocks, Iron, Copper, Gold, Diamonds, Electromagents, Circuit Boards, Space Navigational Key"
                embed=discord.Embed(title="Expeditions", description = expedition_embed, color=0xb27917)
                await ctx.send(embed=embed)

                await ctx.send("Select expedition (basic, advanced, expert, no)")

                try:
                    action = await bot.wait_for('message', check=check, timeout = 15.0)
                except asyncio.TimeoutError:
                    await ctx.send("Leaving the expedition hut")
                    return
                action = str(action.content).lower()

                if not action in ["basic", "advanced", "expert"]:
                    await ctx.send("Leaving the expedition hut")
                    return

                present = dt.now()

                if action == "basic":
                    if dict_[str(ctx.author.id)]["people"] < 5:
                        await ctx.send("You do not have enough people for a basic expedition")
                        return

                    return_time = str(present + datetime.timedelta(hours = 3)).split('.')[0]
                    dict_[str(ctx.author.id)]["expedition"]["returntime"] = return_time

                    dict_[str(ctx.author.id)]["expedition"]["type"] = "Basic"
                    dict_[str(ctx.author.id)]["expedition"]["people"] = 5

                    dict_[str(ctx.author.id)]["expedition"]["failed"] = (random.randint(1, 10) <= 3)

                    gains = {}

                    rock_gains = [random.randint(1, 8), 0][[True, False].index((random.randint(1, 3) < 3))]
                    iron_gains = [random.randint(1, 8), 0][[True, False].index((random.randint(1, 2) == 1))]
                    copper_gains = [random.randint(1, 6), 0][[True, False].index((random.randint(1, 2) == 1))]

                    if rock_gains > 0:
                        gains["rock"] = {"name": "Rock", "id": 0, "quantity": rock_gains, "type": "ore"}

                    if iron_gains > 0:
                        gains["iron"] = {"name": "Iron", "id": 1, "quantity": iron_gains, "type": "ore"}

                    if copper_gains > 0:
                        gains["copper"] = {"name": "Copper", "id": 2, "quantity": copper_gains, "type": "ore"}

                    dict_[str(ctx.author.id)]["expedition"]["gains"] = gains

                    dict_[str(ctx.author.id)]["people"] = dict_[str(ctx.author.id)]["people"] - 5

                    refresh_dict(dict_)

                    await ctx.send("**Basic** expedition sent out")
                    return

                elif action == "advanced":
                    if dict_[str(ctx.author.id)]["people"] < 15:
                        await ctx.send("You do not have enough people for an advanced expedition")
                        return

                    return_time = str(present + datetime.timedelta(hours = 6)).split('.')[0]
                    dict_[str(ctx.author.id)]["expedition"]["returntime"] = return_time

                    dict_[str(ctx.author.id)]["expedition"]["type"] = "Advanced"
                    dict_[str(ctx.author.id)]["expedition"]["people"] = 15

                    dict_[str(ctx.author.id)]["expedition"]["failed"] = (random.randint(1, 10) <= 2)

                    gains = {}

                    rock_gains = [random.randint(1, 12), 0][[True, False].index((random.randint(1, 4) < 4))]
                    iron_gains = [random.randint(1, 12), 0][[True, False].index((random.randint(1, 3) < 3))]
                    copper_gains = [random.randint(1, 12), 0][[True, False].index((random.randint(1, 3) < 3))]
                    gold_gains = [random.randint(1, 5), 0][[True, False].index((random.randint(1, 5) == 1))]
                    diamond_gains = [random.randint(1, 3), 0][[True, False].index((random.randint(1, 6) == 1))]

                    if rock_gains > 0:
                        gains["rock"] = {"name": "Rock", "id": 0, "quantity": rock_gains, "type": "ore"}

                    if iron_gains > 0:
                        gains["iron"] = {"name": "Iron", "id": 1, "quantity": iron_gains, "type": "ore"}

                    if copper_gains > 0:
                        gains["copper"] = {"name": "Copper", "id": 2, "quantity": copper_gains, "type": "ore"}

                    if gold_gains > 0:
                        gains["gold"] = {"name": "Gold", "id": 3, "quantity": gold_gains, "type": "ore"}

                    if diamond_gains > 0:
                        gains["diamond"] = {"name": "Diamond", "id": 4, "quantity": diamond_gains, "type": "ore"}

                    dict_[str(ctx.author.id)]["expedition"]["gains"] = gains

                    dict_[str(ctx.author.id)]["people"] = dict_[str(ctx.author.id)]["people"] - 15

                    refresh_dict(dict_)

                    await ctx.send("**Advanced** expedition sent out")
                    return

                elif action == "expert":
                    if dict_[str(ctx.author.id)]["people"] < 30:
                        await ctx.send("You do not have enough people for an expert expedition")
                        return

                    return_time = str(present + datetime.timedelta(hours = 12)).split('.')[0]
                    dict_[str(ctx.author.id)]["expedition"]["returntime"] = return_time

                    dict_[str(ctx.author.id)]["expedition"]["type"] = "Expert"
                    dict_[str(ctx.author.id)]["expedition"]["people"] = 30

                    dict_[str(ctx.author.id)]["expedition"]["failed"] = (random.randint(15, 100) <= 15)

                    gains = {}

                    rock_gains = random.randint(1, 17)
                    iron_gains = [random.randint(1, 15), 0][[True, False].index((random.randint(1, 5) < 5))]
                    copper_gains = [random.randint(1, 15), 0][[True, False].index((random.randint(1, 4) < 4))]
                    gold_gains = [random.randint(1, 7), 0][[True, False].index((random.randint(1, 2) == 1))]
                    diamond_gains = [random.randint(1, 5), 0][[True, False].index((random.randint(1, 2) == 1))]
                    electromagnet_gains = [random.randint(1, 2), 0][[True, False].index((random.randint(1, 3) == 1))]
                    circuitboard_gains = [random.randint(1, 2), 0][[True, False].index((random.randint(1, 2) == 1))]
                    navkey_gains = [1, 0][[True, False].index((random.randint(1, 100) == 1))]

                    gains["rock"] = {"name": "Rock", "id": 0, "quantity": rock_gains, "type": "ore"}

                    if iron_gains > 0:
                        gains["iron"] = {"name": "Iron", "id": 1, "quantity": iron_gains, "type": "ore"}

                    if copper_gains > 0:
                        gains["copper"] = {"name": "Copper", "id": 2, "quantity": copper_gains, "type": "ore"}

                    if gold_gains > 0:
                        gains["gold"] = {"name": "Gold", "id": 3, "quantity": gold_gains, "type": "ore"}

                    if diamond_gains > 0:
                        gains["diamond"] = {"name": "Diamond", "id": 4, "quantity": diamond_gains, "type": "ore"}

                    if electromagnet_gains > 0:
                        gains["electromagnets"] = {"name": "Electromagnet", "id": 1, "quantity": electromagnet_gains, "type": "craft"}

                    if circuitboard_gains > 0:
                        gains["circuitboard"] = {"name": "Circuit Board", "id": 0, "quantity": circuitboard_gains, "type": "craft"}

                    if navkey_gains > 0:
                        gains["navkey"] = {"name": "Space Navigational Key", "id": 3, "quantity": navkey_gains, "type": "craft"}


                    dict_[str(ctx.author.id)]["expedition"]["gains"] = gains

                    dict_[str(ctx.author.id)]["people"] = dict_[str(ctx.author.id)]["people"] - 30

                    refresh_dict(dict_)

                    await ctx.send("**Expert** expedition sent out")
                    return
        else:
            await ctx.send("You did not build an expedition hut")
    else:
        await ctx.send("You don't have a colony, type costartcolony to start one")


@bot.command(name = 'radio')
async def use_radio(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me
    dict_ = dict_access()
    user_data = list(dict_[str(ctx.author.id)]["data"])

    if person_exists(ctx.author.id, dict_):
        questNotify = quest_check("coradio", ctx.author.id)[0]

        if "p" in user_data:
            await ctx.send("You accessed the radio observatory")
            await ctx.send("You have not recieved any new messages") #change this later with msgs n stuff
            
            action_list = []
            if dict_[str(ctx.author.id)]["other_items"].get("radio_relic") == 1: action_list.append("Use Radio Relic(respond with 'a')")

            if len(action_list) == 0: return

            await ctx.send("Select your action: " + ", ".join(action_list))
            try:
                action = await bot.wait_for('message', check=check, timeout = 15.0)
            except asyncio.TimeoutError:
                await ctx.send("Timeout, you left the observatory")
                return
            action = action.content

            if action == "a":
                dict_[str(ctx.author.id)]["other_items"]["radio_relic"] = "^"
                if questNotify:
                    quest_notify(ctx.author.id)
                refresh_dict(dict_)

                await ctx.send("Activating the radio observatory...")
                time.sleep(0.3)
                await ctx.send("Implementing the radio relic...")
                time.sleep(0.4)
                await ctx.send("Propogating relic radio waves...")
                time.sleep(0.3)
                await ctx.send("Recieving trace signals...!")
                
                encoded_trace_msg = "00101110 00101110 00101110 01100011 01001111 01110010 01100100 01001001 01101110 01100001 01010100 01000101 01110011 00111010 00101110 00101110 00101110".split(" ")

                msg_ = await ctx.send(encoded_trace_msg[0]) 

                n = 1
                msglen = len(encoded_trace_msg)

                for x in range(msglen) - 1:
                    time.sleep(0.1)
                    await msg_.edit(content = encoded_trace_msg[n])
                    n+=1

                time.sleep(0.3)

                await ctx.send("---__MESSAGE CONTENTS UNKNOWN__---")
                time.sleep(0.5)
                await ctx.send("---__COORDINATES RETRIEVED__---")
                time.sleep(0.1)
                await ctx.send("Whew, the radio tower almost overheated from that, anyways, we will need to check the expedition hut to organize an expedition to those coordinates")
                await ctx.send("Leaving the radio observatory")
                return

            else:
                await ctx.send("Leaving the radio observatory")
                return

        else:
            await ctx.send("You need to build a radio observatory")
            return
    else:
        await ctx.send("You cannot use the radio without a colony")
        return


@bot.command(name = 'quests')
async def quests(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me
    dict_ = dict_access()

    if person_exists(ctx.author.id, dict_):
        json_file = open('quests.json', 'r')
        quest_data = json.loads(json_file.read())
        json_file.close()

        currentQuest = dict_[str(ctx.author.id)]["currentquest"] #currentquest: [false, "basicguide", 1, false] #onQuest, quest_key, quest_number, finishedQuest
        finishedQuestLines = dict_[str(ctx.author.id)]["finishedquests"] #a list of quest line keys the player finished

        if currentQuest[0]:
            currentQuestData = quest_data.get(dict_[str(ctx.author.id)]["currentquest"][1])[str(dict_[str(ctx.author.id)]["currentquest"][2])]
            qType = currentQuestData["info"]["type"]

            json_file = open("buildstore.json", "r")
            json_builds = json.loads(json_file.read())
            json_file.close()

            if qType == "building":
                id_override = False
                try:
                    id_override = currentQuestData["info"]["id_override"]
                except KeyError:
                    pass

                user_data = list(dict_[str(ctx.author.id)]["data"])

                if id_override:
                    if currentQuestData["info"]["name"] in user_data:
                        dict_[str(ctx.author.id)]["currentquest"][3] = True
                else:
                    reqBuild = json_builds.get(currentQuestData["info"]["name"])

                    if reqBuild["l_id"] in user_data:
                        dict_[str(ctx.author.id)]["currentquest"][3] = True

            elif qType == "money":
                if dict_[str(ctx.author.id)]["money"] >= currentQuestData["info"]["quantity"]:
                    dict_[str(ctx.author.id)]["currentquest"][3] = True

            elif qType == "ore":
                if not "!" in list(currentQuestData["info"]["name"]):
                    if dict_[str(ctx.author.id)]["ores"][currentQuestData["info"]["name"]] >= currentQuestData["info"]["quantity"]:
                        dict_[str(ctx.author.id)]["currentquest"][3] = True
                else:
                    #! in the name with "any" in front of it indicates any of the things thats not the thing after the !
                    ore_file = open('ores.json', 'r')
                    ore_data = json.loads(ore_file.read())
                    ore_file.close()

                    list_of_names = []
                    for or_ in ore_data:
                        if not or_ == currentQuestData["info"]["name"].split('!')[1]:
                            list_of_names.append(or_)

                    for or_ in list_of_names:
                        if dict_[str(ctx.author.id)]["ores"][or_] >= currentQuestData["info"]["quantity"]:
                            dict_[str(ctx.author.id)]["currentquest"][3] = True
                            break

            elif qType == "craft":
                if dict_[str(ctx.author.id)]["crafts"][currentQuestData["info"]["name"]] >= currentQuestData["info"]["quantity"]:
                    dict_[str(ctx.author.id)]["currentquest"][3] = True

            elif qType == "other_items":
                if dict_[str(ctx.author.id)]["other_items"].get(currentQuestData["info"]["name"]) != None:
                    if dict_[str(ctx.author.id)]["other_items"].get(currentQuestData["info"]["name"]) >= currentQuestData["info"]["quantity"]:
                        dict_[str(ctx.author.id)]["currentquest"][3] = True

            elif qType == "research":
                try:
                    haveResearch = False
                    try:
                        haveResearch = dict_[str(ctx.author.id)]["research"][currentQuestData["info"]["name"]]
                    except KeyError:
                        pass

                    if haveResearch:
                        dict_[str(ctx.author.id)]["currentquest"][3] = True
                except KeyError:
                    pass

            elif qType == "expedition":
                if dict_[str(ctx.author.id)]["expedition"]["type"] in currentQuestData["info"]["name"]:
                    dict_[str(ctx.author.id)]["currentquest"][3] = True

            if currentQuest[3]:
                await ctx.send("You completed the quest: **" + currentQuestData["name"] + "**")

                hasReward = False
                try:
                    if not currentQuestData["reward"] == None:
                        hasReward = True
                except KeyError:
                    pass

                if hasReward:
                    rwrd_type = currentQuestData["reward"]["type"]
                    
                    if rwrd_type == "money":
                        dict_[str(ctx.author.id)]["money"] = dict_[str(ctx.author.id)]["money"] + currentQuestData["reward"]["quantity"]
                        await ctx.send("As a reward, you have recieved " + str(currentQuestData["reward"]["quantity"]) + " " + f"{bot.get_emoji(m_coin)}")
                        refresh_dict(dict_)

                    elif rwrd_type == "people":
                        dict_[str(ctx.author.id)]["people"] = dict_[str(ctx.author.id)]["people"] + currentQuestData["reward"]["quantity"]
                        await ctx.send("As a reward, you have recieved " + str(currentQuestData["reward"]["quantity"]) + " people")
                        refresh_dict(dict_)
                    #elif for other rewards of quests like people/specialists/items

                hasMod = False
                try:
                    if not currentQuestData["mod"] == None:
                        hasMod = True
                except KeyError:
                    pass

                if hasMod:
                    mod_type = currentQuestData["mod"]["type"]

                    if mod_type == "expedition":
                        if currentQuestData["mod"]["name"] == "alien_1_meet":
                            dict_[str(ctx.author.id)]["expedition"]["mod"] = "alien_1_meet"

                last_quest_n = 0
                for q_ in quest_data.get(currentQuest[1]):
                    if q_.isnumeric():
                        if int(q_) > last_quest_n:
                            last_quest_n = int(q_)

                if currentQuest[2] == last_quest_n:
                    await ctx.send("You completed the quest line: **"  + quest_data.get(currentQuest[1])["name"] + "**!")
                    await ctx.send("Do coquests to start another quest line")
                    dict_[str(ctx.author.id)]["currentquest"] = [False]
                    dict_[str(ctx.author.id)]["finishedquests"].append(currentQuest[1])
                    refresh_dict(dict_)
                else:
                    await ctx.send("Do coquests for the next quest")
                    dict_[str(ctx.author.id)]["currentquest"][2] = dict_[str(ctx.author.id)]["currentquest"][2] + 1
                    dict_[str(ctx.author.id)]["currentquest"][3] = False
                    refresh_dict(dict_)
                return
            else:
                last_quest_n = 0
                for q_ in quest_data.get(currentQuest[1]):
                    if q_.isnumeric():
                        if int(q_) > last_quest_n:
                            last_quest_n = int(q_)

                embed_desc = "*" + currentQuestData["description"] + "*"

                hasReward = False
                try:
                    if not currentQuestData["reward"] == None:
                        hasReward = True
                except KeyError:
                    pass

                if hasReward:
                    reward_str = ""
                    rwrd_type = currentQuestData["reward"]["type"]

                    if rwrd_type == "money":
                        reward_str = str(currentQuestData["reward"]["quantity"]) + f" {bot.get_emoji(m_coin)}"
                    
                        embed_desc += "\n**" + "Reward:** " + reward_str

                    elif rwrd_type == "people":
                        reward_str = str(currentQuestData["reward"]["quantity"]) + " people"
                    
                        embed_desc += "\n**" + "Reward:** " + reward_str
                    #elif for different reward types

                embed=discord.Embed(title = currentQuestData["name"], description = embed_desc, color=0x1e1e1e)
                embed.set_footer(text = quest_data.get(currentQuest[1])["name"] + " quests: " + str(currentQuest[2]) + "/" + str(last_quest_n))
                await ctx.send(embed=embed)
        else:
            #if not on quest (quest options)
            quest_lines = []
            for q_ in quest_data:
                if not q_ in finishedQuestLines:
                    quest_lines.append(q_)

            if len(quest_lines) == 0:
                await ctx.send("You don't have any available quests right now!")
                return

            n = 0
            for q_ in quest_lines:
                if quest_data.get(q_)["type"] == "main":
                    break
                n+=1

            quest_lines = quest_lines[:n+1]

            if n > 0:
                quest_lines[0], quest_lines[len(quest_lines) - 1] = quest_lines[len(quest_lines) - 1], quest_lines[0]

            embed_desc = ""

            qId_array = []

            for q_ in quest_lines:
                q = quest_data.get(q_)
                embed_desc += "**" + q["name"] + "**\nId: " + str(q["id"]) + "\n" + q["description"] + "\n\n"
                qId_array.append(q["id"])

            embed=discord.Embed(title = "Quests", description = embed_desc, color=0x000000)
            await ctx.send(embed=embed)

            await ctx.send("**Send the quest line *id* to start or *no* to leave**")

            action = None
            try:
                action = await bot.wait_for('message', check=check, timeout = 15.0)
            except asyncio.TimeoutError:
                await ctx.send("Leaving quests")
                return
            action = action.content

            if action.isnumeric():
                if int(action) in qId_array:
                    questlineData = quest_data.get(quest_lines[qId_array.index(int(action))])
                    await ctx.send("Starting quest line: **" + questlineData["name"] + "**")
                    dict_[str(ctx.author.id)]["currentquest"] = [True, quest_lines[qId_array.index(int(action))], 1, False]
                    refresh_dict(dict_)
                    await ctx.send("Do coquests to see first quest")

    else:
        await ctx.send("You do not have a colony, type costartcolony to start")

    


keep_alive()
bot.run(TOKEN)