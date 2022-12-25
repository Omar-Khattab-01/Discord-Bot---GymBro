# My first bot

import os
import urllib
import json
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import has_permissions
from discord.ext.tasks import loop
from win10toast_click import ToastNotifier
import random
import urllib.request
from datetime import datetime
from win10toast_click import ToastNotifier
import tkinter as tk
from tkinter import *
from decimal import Decimal
import webbrowser

noti = ToastNotifier()

top = 0
label = 0
canvas = 0
img = ""

def makeWindow():
    global top, label, canvas, img
    top = tk.Tk()
    top.geometry('50x50')
    top.title('shop')
    canvas = Canvas(top, bg="blue", height=250, width=300)
    img = PhotoImage(file="sched.png")
    label = Label(top, image=img)
    label.place(x=0, y=0, relwidth=1, relheight=1)
    label.place(x=0, y=0)


def notify():
    global noti, top
    noti.show_toast('Random', 'Hello World', threaded=True, callback_on_click=open_link)
    top.destroy()


class AppURLopener(urllib.request.URLopener):
    version = "Mozilla/5.0"


opener = AppURLopener()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
dic = {}
gymDic = {}
output = ["Calories", "Fats", "Carbs", "Protein"]
commands_names = ["cal", "addm", "meal"]
keyWords = {}
meals = {}
fileName = "links.txt"
gym = "gym.txt"
meals_file = "meals.txt"
link = ""


def open_link():
    global link
    webbrowser.open(link)


@tasks.loop(seconds=60.0)
async def printer():
    global link, noti
    now = datetime.now()
    current_time = str(datetime.today().weekday()) + now.strftime("%H:%M")
    # print(current_time)
    if current_time in keyWords:
        link = dic[keyWords[current_time].lower()]
        makeWindow()
        noti = ToastNotifier()
        btn = Button(top, text="Enter", command=notify)
        btn.pack()

        top.mainloop()


def aquire_loop_status(fileName):
    links = open(fileName).read().split()
    if links[0] == "***True":
        printer.start()


aquire_loop_status(fileName)


def aquire_Json(url):
    response = opener.open(url)
    data = json.loads(response.read())
    return data


def populate():
    x = 0
    links = open(fileName).read().split("\n")
    for line in links:
        line = line.split()
        if len(line) != 1 and len(line) != 0:
            # print(line)
            dic.update({line[0]: line[1]})
            keyWords.update({line[2]: line[0]})

def populateGym():
    x = 0
    days = open(gym).read().split("\n")
    #print(len(days))
    for day in days:
        if(len(day))!=0:

            day = day.split()

            #print(day)
            try:
                if len(gymDic[day[0]]) != 0:
                    current = gymDic[day[0]]
                    current.append({day[1]:[day[2],day[3],day[4],day[5]]})
            except:
                gymDic[day[0]] = []
                current = gymDic[day[0]]
                current.append({day[1]: [day[2], day[3], day[4], day[5]]})

def populateMeals():
    file = open(meals_file).read().split("\n")
    for line in file:
        line = line.split()
        if(len(line) == 5):
            meals[line[0]] = [line[1],line[2],line[3],line[4]]


def add(key, link, time):
    dic.update({key.lower(): link})
    keyWords.update({time: key.lower()})
    file = open(fileName).read().split("\n")
    write = open(fileName, "w")
    write.write("\n"+key + " " + link + " " + time + "\n")

def addCal(day,id, cal, fat, carbs, pro):
    global gymDic
    #print(gymDic)
    done = False
    calories = 0
    fats = 0
    carb = 0
    protein = 0
    #print(gymDic["002/14/22"])
    #print(gymDic["002/14/22"]["414782368319275008"][0])
    #print(day)
    #print(id)
    index = -1
    if day in gymDic:
        for ids in gymDic[day]:
            if str(id) in ids:
                #print(ids)
                index +=1
                calories = Decimal(ids[str(id)][0])
                fats = Decimal(ids[str(id)][1])
                carb = Decimal(ids[str(id)][2])
                protein = Decimal(ids[str(id)][3])
                gymDic[day].pop(index)

    if index == -1:
        gymDic[day] = []
    

    current = gymDic[day]
    new_calories = str(Decimal(cal)+calories)
    new_fats = str(Decimal(fat)+fats)
    new_carbs = str(Decimal(carbs)+carb)
    new_proteins = str(Decimal(pro)+protein)
    current.append({str(id):[new_calories,new_fats,new_carbs,new_proteins]})
    lines = open(gym, "r+")
    db = lines.read().split("\n")
    lines.seek(0)
    line = ""
    word = day + " " + str(id) + " " + new_calories + " " + new_fats+" "+new_carbs+" "+new_proteins
   ##lines = open(gym).read().split("\n")
    for row in db:
        row = row.split()
        if(len(row) !=0):
            if(row[0] == day and row[1] == str(id)):
                done = True
                lines.writelines(word+"\n")
            else:
                row = " ".join(row)
                #print(row)
                #print(2)
                lines.writelines(row+"\n")
    if done == False:
        lines.writelines(word+"\n")

    lines.truncate()


def addMeal(meal):
    #lines = open(meals_file, "r+")
    line = meal+" "+" ".join(meals[meal])
    #lines.writelines(line)

    with open(meals_file, "a") as file:
        # Append 'hello' at the end of file
        file.write("\n"+line)



@client.event
async def on_ready():
    loop = 0
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    Channel = client.get_channel(roles)
    Text= "YOUR_MESSAGE_HERE"
    Moji = await Channel.send(text)
    await Moji.add_reaction('🏃')

@client.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel(YOUR_CHANNEL_ID)
    if reaction.message.channel.id != Channel.id:
        return
    if reaction.emoji == "🏃":
      Role = discord.utils.get(user.server.roles, name="YOUR_ROLE_NAME_HERE")
      await user.add_roles(Role)


client.counter = 1
client.flag = True

bot = commands.Bot(command_prefix='?')
bot.remove_command("help")

@bot.group(invoke_without_command = True)
async def help(ctx):
    em = discord.Embed(title="help", description="use ?help <command> for more info")
    em.add_field(name="Commands", value="\n".join(commands_names))
    await ctx.send(embed=em)


@bot.command(name="id")
async def id_(ctx):
    await ctx.send(ctx.author.id)

@bot.command(name="addm")
async def id_(ctx, meal, cal=0.0, fat=0.0, carb=0.0, pro=0.0):
    meals[meal] = [str(cal), str(fat), str(carb), str(pro)]
    addMeal(meal)

@help.command()
async def addm(ctx):
    em = discord.Embed(title="addm", description="adds a new meal nutrition")
    em.add_field(name="Syntax", value="?addm [meal] [calories] [fats] [carbs] [protein]")
    await ctx.send(embed=em)

@bot.command(name="meal")
async def id_(ctx, meal):
    global output
    try:
        current_meal = meals[meal]
        word = " "*5 + meal + "\n"
        for i in range(len(output)):
            word = word + output[i]+" "+str(current_meal[i])+"\n"
    except:
        word = meal+" does not exist, use command ?addm to add it"

    await ctx.send(word)

@help.command()
async def meal(ctx):
    em = discord.Embed(title="meal", description="prints out nutrition facts")
    em.add_field(name="Syntax", value="?meal [meal]")
    await ctx.send(embed=em)

@bot.command(name='cal', help='adds to gym.txt')
async def cal_calories(ctx, calories = "0", fats = "0", carbs = "0", pro = "0"):
    now = datetime.now()
    id = ctx.author.id
    date = str(datetime.today().weekday()) + now.strftime("%D")
    #print("done")
    exist = True
    try:
        int(calories)
        addCal(date,id, calories,fats,carbs,pro)
    except:
        meal = calories
        if meal in meals:
            addCal(date, id, meals[meal][0], meals[meal][1], meals[meal][2], meals[meal][3])
        else:
            exist = False
    if exist:
        out = ""
        index = len(gymDic[date])-1
        for i in range(len(gymDic[date][index][str(id)])):
            #print(gymDic[date])
            #print(gymDic[date][index])
            x = gymDic[date][index][str(id)][i]
            number_2dec = float("{0:.2f}".format(float(x)))
            out = out+output[i]+" "+str(number_2dec)+"\n"
    else:
        out = calories+" does not exist, use command ?addm to add it"
    await ctx.send(out)

@help.command()
async def cal(ctx):
    em = discord.Embed(title="cal", description="adds to your daily intake")
    em.add_field(name="Syntax", value="?cal [calories] [fats] [carbs] [protein]")
    em.add_field(name="Syntax", value="?cal [meal] → meal needs to be added first")
    em.add_field(name="Syntax", value="?cal → shows your intake")
    await ctx.send(embed=em)

@bot.command(name='add', help='adds link to the dic')
async def addLink(ctx, key, time, link):
    if key in dic:
        await ctx.send("keyword: (" + key + ") was used before. Please use a different keyword.")
    else:
        add(key, link, time)


@bot.command(name='?', help='opens lectures zoom link')
async def show(ctx, t):
    try:
        # print(dic)
        webbrowser.open(dic[t.lower()])

    except:
        await ctx.send(t + " not found")


@bot.command(name='!', help='lists all keywords and links saved in database')
async def list(ctx):
    file = open(fileName).read()
    file2 = "keywords -> link\n\n" + file
    await ctx.send(file2)


@bot.command(name="clr")
async def clear(ctx):
    file = open(fileName, "w")
    file.write("")


@bot.command(name="enableAuto")
async def enable(ctx):
    printer.start()
    with open('links.txt', 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace('**False', '**True')

    # Write the file out again
    with open('links.txt', 'w') as file:
        file.write(filedata)
    print("Auto on")


@bot.command(name="disableAuto")
async def disable(ctx):
    printer.cancel()
    with open('links.txt', 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace('**True', '**False')

    # Write the file out again
    with open('links.txt', 'w') as file:
        file.write(filedata)
    printer.stop()
    print("Auto off")

def populateAll():
    populate()
    populateGym()
    populateMeals()


populateAll()
bot.run(TOKEN)
on_ready()
