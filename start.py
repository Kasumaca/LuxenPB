import sys

from tools.dataIO import fileIO

#TRY TO IMPORT DISCORD.PY
try:
    from discord.ext import commands, tasks
    import discord
except ImportError:
    print("Discord.py is not installed!")
    sys.exit(5)

config_location = fileIO("config/config.json", "load") #LOAD JSON FILE
infomation = fileIO("config/infomation.json", "load") #LOAD JSON FILE
emojiReplace = fileIO("config/emoji_id.json", "load") #LOAD JSON FILE
Shards = config_location["Shards"] #GET SHARD/VER FROM JSON FILE
Prefix = config_location["Prefix"] #GET PREFIX FROM JSON FILE


#INIT UR BOT
intents = discord.Intents.default()
intents.message_content = True
bot = commands.AutoShardedBot(intents=intents, shard_count = Shards, command_prefix=Prefix, activity = discord.Game(name="Luxenhelp for help OwO"))

#DON'T WORRY ABOUT THIS
bot.remove_command('help')

@bot.event
async def on_ready():
    #THIS RUN WHEN BOT START UP
    print("Login info:\nUser: {}\nUser ID: {}\nPrefix: {}".format(bot.user.name, bot.user.id, Prefix))

@bot.event
async def on_message(message):
    if message.author == bot.author:
        return

@bot.event
async def on_command(command):
    #THIS RUN WHEN ANY COMMAND IS USED 
    info = fileIO("config/config.json", "load")
    info["Commands_used"] = info["Commands_used"] + 1
    fileIO("config/config.json", "save", info)

#THIS IS OUR COMMAND PROTOTYPE
#FUNCTION name which mean thats ur command prefix+functionName like '!database'

def replaceEmoji(text):
    for key in emojiReplace.keys():
        text = text.replace(key, emojiReplace[key])
    return text

class SecondEventDropdown(discord.ui.Select):
    def __init__(self, infoType):
        self.info = infoType
        optionss = []
        for key in infomation["event"][infoType.lower()]:
            optionss.append(discord.SelectOption(label=key.title(), value=key.lower()))
        super().__init__(placeholder="Choose Kind Of Info You Want To See", options=optionss)
    async def callback(self, interaction: discord.Interaction):
        data = infomation["event"][(self.info).lower()][self.values[0].lower()]
        messageDescripton =  replaceEmoji(data['message'])
        em = discord.Embed(title=f"**{self.values[0].title()}**",description=messageDescripton, color=discord.Color.blue())
        em.set_author(name="Phoenix Bloodline")
        if len(data['footer'])>0: 
            footermsg = (self.info).title()+"\n"+data['footer']
            em.set_footer(text=f"{footermsg}")
        if len(data['image'])>0: em.set_image(url=data['image'])
        em.set_thumbnail(url="https://cdn.discordapp.com/icons/875310053257777152/2f50786dd6d1665a01fe12f60e412de1.webp?size=96") 
        await interaction.response.edit_message(embed=em)

class FirstEventDropdown(discord.ui.Select):
    def __init__(self, infoType):
        self.info = infoType
        optionss = []
        for key in infomation[infoType].keys():
            optionss.append(discord.SelectOption(label=key.title(), value=key.lower()))
        super().__init__(placeholder=f"Choose {infoType.title()} You Want To See", options=optionss)
    async def callback(self, interaction: discord.Interaction):
        self.view.add_item(SecondEventDropdown(self.values[0]))
        if len(self.view.children) == 3:
            self.view.remove_item(self.view.children[1])
        await interaction.response.edit_message(embed=None,view=self.view)
class EventView(discord.ui.View):
    def __init__(self, infotype):
        super().__init__()
        self.add_item(FirstEventDropdown(infotype))


@bot.command()
async def test(ctx):
    await ctx.send("<:06_Knuckles:624593349034246152>") 

@bot.command()
async def help(ctx):
    message = f"""**1. {Prefix}info [event, lvling, foodbuff, guide, arrow-list, shield-list, mats, bosses]
2. idk .m.
    **"""
    em = discord.Embed(title=f"**Commands List**",description=message, color=discord.Color.blue())
    await ctx.send(embed=em) 
    
@bot.command(pass_context=True)
async def info(ctx, infotype=None):
    if infotype==None: 
        await ctx.send(f"<@{ctx.message.author.id}> Please use command with info you need \n`{Prefix}info [event, lvling, foodbuff, guide, arrow-list, shield-list, mats, bosses]`")
        return
    for i in ["event", "lvling", "foodbuff", "guide", "arrow-list", "shield-list", "mats", "bosses"]:
        if infotype in i: 
            infotype = i
            break
        await ctx.send(f"<@{ctx.message.author.id}> Please use command with info you need \n`{Prefix}info [event, lvling, foodbuff, guide, arrow-list, shield-list, mats, bosses]`")
        return
        
    view = EventView(infotype)
    await ctx.send(f"<@{ctx.message.author.id}> {infotype.title()}s Info",view=view)
  
bot.run(config_location["Token"]) #RUN BOT