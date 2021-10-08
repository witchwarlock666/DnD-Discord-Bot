import os
import discord
import asyncio
import random
from mysql.connector import connection, cursor
import youtube_dl
import time
from discord.ext import commands, tasks
from pydub import AudioSegment
from pydub.playback import play


TOKEN = open("token.txt","r").read()

GUILD = open("guild.txt","r").read()

client = discord.Client()

bot = commands.Bot(
    command_prefix="#",
    help_command=None 
)

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


@bot.event
async def on_ready():

    guild = discord.utils.get(client.guilds, name=GUILD)

    print(f"{bot.user.name} has connected to Discord")
    print(discord.__version__)

@bot.command(name="help")
async def help(ctx):
    help_text = "m: Nome da Arma / Força + proficiência / mod de ataque / Posicionamento. Separados por espaço (Digite #help_m para mais informações)\n\n\
roll: '#roll 1d20+1d6+-3' = 1d20 + 1d6 - 3\n\n\
musica: abre lista de comandos de música\n\n\
arma: '#arma espadalonga 3' nome da arma / modificador\n\n\
lista_armas: mosta a lista de armas\n\n\
drive: abre o link para o drive compartilhado\n\n\
ficha: '#ficha gabigol' = abre ficha gabigol (Digite #nomes para lista de fichas)\n\n\
tools: abre o link para 5etools\n\n\
help: abre essa lista"
    help_format = 'Comandos\n\n>>> {}'.format(help_text)
    await ctx.send(help_format)

@bot.command(name="nomes")
async def nomes(ctx):
    nomes_text = "fabricio\n\
gabigol\n\
davi"
    nomes_format = "Nomes\n>>> {}".format(nomes_text)
    await ctx.send(nomes_format)

@bot.command(name="musicas")
async def musicas(ctx):
    lista_musicas = "batalha\n\
ambiente\n\
suspense\n\
taverna\n\
epico\n\
triste\n\
boss"
    lista_format = "Musicas\n>>> {}".format(lista_musicas)
    await ctx.send(lista_format)

@bot.command(name="lista_armas")
async def lista_armas(ctx):
    lista_text = "adaga\n\
azagaia\n\
bordão\n\
clavagrande\n\
foicecurta\n\
lança\n\
maça\n\
machadinha\n\
marteloleve\n\
porrete\n\
arcocurto\n\
bestaleve\n\
dardo\n\
funda\n\
alabarda\n\
cimitarra\n\
chicote\n\
espadacurta\n\
espadagrande\n\
espadalonga\n\
glaive\n\
lançademontaria\n\
lançalonga\n\
maçaestrela\n\
machadogrande\n\
machadodebatalha\n\
malho\n\
mangual\n\
martelodeguerra\n\
picaretadeguerra\n\
rapieira\n\
tridente\n\
arcolongo\n\
bestademão\n\
bestapesada\n\
espadatornado\n\
gema\n\
mosquetelesser\n\
blunderbuss\n\
mosquete"
    lista_format = "Armas\n>>> {}".format(lista_text)
    await ctx.send(lista_format)

@bot.command(name="musica")
async def musica(ctx):
    musica_text = "connect: conecta o bot no seu canal de voz\n\n\
play: toca musica por url ou por tema (#temas para ver os temas disponiveis)\n\n\
pause: pausa a música\n\n\
resume: volta a musica do ponto de pausa\n\n\
stop: para a musica\n\n\
disconnect: desconecta o bot do seu canal de voz"
    musica_format = "Comandos Música\n>>> {}".format(musica_text)
    await ctx.send(musica_format)

@bot.command(name="temas")
async def temas(ctx):
    temas_text = "batalha\n\
suspense\n\
taverna\n\
epico\n\
triste\n\
boss\n\
ambiente"
    temas_format = "Temas\n>>> {}".format(temas_text)
    await ctx.send(temas_format)

@bot.command(name="help_m")
async def help_m(ctx):
    m_text = "Exemplo de sintaxe: #m federov 3 5 1\n\n\
Armas:\nfederov: 4 balas; em pé: médio difícil; deitado: médio fácil\n\
madsen: 7 balas; em pé: médio difícil; deitado: médio fácil"
    m_format = "Ajuda Metralhadoras\n>>> {}".format(m_text)
    await ctx.send(m_format)

@bot.command(name="drive")
async def drive(ctx):
    await ctx.send(
        embed=discord.Embed(
            title="Link do drive",
            description="https://drive.google.com/drive/folders/1AX6ES0e2Hs7Smz-PiXIMV7ZqdRiZFPwA?usp=sharing"
        )
    )

@bot.command(name="ficha")
async def ficha(ctx, pessoa: str):
    if pessoa == "fabricio":
        await ctx.send(
            embed=discord.Embed(
                title="Fichas Fabricio",
                description="Ercastoteles:\nhttps://drive.google.com/file/d/13jLEyM-DX2SpqgWIjqOUOEVuo97NXCI0/view?usp=sharing\n\
Mai:\nhttps://drive.google.com/file/d/1cJCgKK6L6fuBGbDwyRSL6pbFBLz07aoH/view?usp=sharing"
            )
        )
    if pessoa == "gabigol":
        await ctx.send(
            embed=discord.Embed(
                title="Fichas Gabigol",
                description="Votty:\nhttps://drive.google.com/file/d/1CwH30rV4gpzOs9f4MZuwQbEtfOelop0L/view?usp=sharing\n\
Kenud:\nhttps://drive.google.com/file/d/1aB3H5j2Uto7qFgLqsZ5oLI8o5HnBAN65/view?usp=sharing\n\
Dreepy:\nhttps://drive.google.com/file/d/1Ha8YQC3kfV6r9bDNVo4BP6JIKwl-8OQF/view?usp=sharing"
            )
        )
    if pessoa == "davi":
        await ctx.send(
            embed=discord.Embed(
                title="Fichas Davi",
                description="https://drive.google.com/file/d/1NwViaCv9Fv_qKaPTbGC9c-RDABcitBSD/view?usp=sharing"
            )
        )
    if pessoa == "augusto":
        await ctx.send(
            embed=discord.Embed(
                title="Fichas Augusto",
                description="https://drive.google.com/file/d/1tde30gu_8iiJkghWy41IjFbuCZO-Q1j9/view?usp=sharing"
            )
        )
    if pessoa == "henrique":
        await ctx.send(
            embed=discord.Embed(
                title="Fichas Henrique",
                description="https://drive.google.com/file/d/1vX0BQQ12jhop5zcloDFVZbuDER-iJDR8/view?usp=sharing"
            )
        )

async def formula_arma(ctx, balas: int, recuo: int, forca: int, mod: int, dado_dano: str):
    hit = 0
    mod = str(mod+1)
    for x in range(balas):
        acerto = 100 - (recuo * x) + (forca * 4)
        acertou = random.randrange(100)
        #if it hits, add 1 to hit counter
        if acertou <= acerto:
            hit = hit + 1
    await ctx.send("{} acertos".format(hit))
    ataque = "1d20+" + mod
    await roll(ctx, ataque)
    dano = str(hit) + "d" + dado_dano + "+" + mod
    await roll(ctx, dano) 

@bot.command(name="m")
async def metralhadora(ctx, nome_m: str, forca: int, mod: int, pos: int):

    #federov gun
    if nome_m == "federov":
        balas = 4
        if pos == 1:
            recuo = 20
        elif pos == 2:
            recuo = 10
        dado_dano = "10"

        await formula_arma(ctx, balas, recuo, forca, mod, dado_dano)
    
    #madsen gun
    if nome_m == "madsen":
        balas = 7
        if pos == 1:
            recuo = 20
        elif pos == 2:
            recuo = 10
        dado_dano = "8"

        await formula_arma(ctx, balas, recuo, forca, mod, dado_dano)

@bot.command(name="roll")
async def roll(ctx, dices: str):
    l_dices = dices.split("+")
    values = []
    total = 0
    valueString = ""

    for x in l_dices:
        if "d" in x:
            number = int(x.split("d")[0])
            sides = int(x.split("d")[1])
            for i in range(number):
                dice_result = random.randrange(1, sides + 1)
                values.append(dice_result)
                
                if valueString == '':
                    valueString += str(dice_result)
                else:
                    valueString += ', ' + str(dice_result)
        else:
            total += int(x)
    total += sum(values)
    await ctx.send(
        embed=discord.Embed(
            title=dices,
            description=ctx.message.author.mention + "\n:VALORES:\n" + valueString + "\n:RESULTADO:\n" + str(total)
        )
        
    )

@bot.command(name="vant")
async def vant(ctx, dados: int, mod: int):
    values = []
    total = 0
    valueString = ""
    maior = 0

    for x in range(dados):
        dice_result = random.randrange(1, 20 + 1)
        values.append(dice_result)
        
        if valueString == '':
            valueString += str(dice_result)
        else:
            valueString += ', ' + str(dice_result)
        if dice_result > maior:
            maior = dice_result
    total = maior + mod
    await ctx.send(
        embed=discord.Embed(
            title=str(dados) + "d20+" + str(mod),
            description=ctx.message.author.mention + "\n:VALORES:\n" + valueString + "\n:RESULTADO:\n" + str(total)
        )
        
    )

@bot.command(name="des")
async def des(ctx, dados: int, mod: int):
    values = []
    total = 0
    valueString = ""
    menor = 21

    for x in range(dados):
        dice_result = random.randrange(1, 20 + 1)
        values.append(dice_result)
        
        if valueString == '':
            valueString += str(dice_result)
        else:
            valueString += ', ' + str(dice_result)
        if dice_result < menor:
            menor = dice_result
    total = menor + mod
    await ctx.send(
        embed=discord.Embed(
            title=str(dados) + "d20+" + str(mod),
            description=ctx.message.author.mention + "\n:VALORES:\n" + valueString + "\n:RESULTADO:\n" + str(total)
        )
        
    )
@bot.command(name="crit")
async def crit(ctx, dices: str):
    l_dices = dices.split("+")
    values = []
    total = 0
    valueString = ""

    for x in l_dices:
        if "d" in x:
            number = int(x.split("d")[0])
            sides = int(x.split("d")[1])
            for i in range(number):
                dice_result = random.randrange(1, sides + 1)
                values.append(dice_result)
                
                if valueString == '':
                    valueString += str(dice_result)
                else:
                    valueString += ', ' + str(dice_result)
        else:
            total += int(x)
    total += sum(values)
    total *= 2
    await ctx.send(
        embed=discord.Embed(
            title=dices,
            description=ctx.message.author.mention + "\n:VALORES:\n" + valueString + "\n:RESULTADO:\n" + str(total)
        )
        
    )

@bot.command(name="arma")
async def arma(ctx, armas: str, modifier: str):
    if armas == "adaga":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d4+" + modifier
        await roll(ctx, dano)
    elif armas == "azagaia":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+" + modifier
        await roll(ctx, dano)
    elif armas == "bordão":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "clavagrande":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "foicecurta":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d4+" + modifier
        await roll(ctx, dano)
    elif armas == "lança":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "maça":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+" + modifier
        await roll(ctx, dano)
    elif armas == "machadinha":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+" + modifier
        await roll(ctx, dano)
    elif armas == "marteloleve":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d4+" + modifier
        await roll(ctx, dano)
    elif armas == "porrete":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d4+" + modifier
        await roll(ctx, dano)
    elif armas == "arcocurto":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+" + modifier
        await roll(ctx, dano)
    elif armas == "bestaleve":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "dardo":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d4+" + modifier
        await roll(ctx, dano)
    elif armas == "funda":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d4+" + modifier
        await roll(ctx, dano)
    elif armas == "alabarda":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d10+" + modifier
        await roll(ctx, dano)
    elif armas == "cimitarra":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+" + modifier
        await roll(ctx, dano)
    elif armas == "chicote":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d4+" + modifier
        await roll(ctx, dano)
    elif armas == "espadacurta":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+" + modifier
        await roll(ctx, dano)
    elif armas == "espadagrande":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "2d6+" + modifier
        await roll(ctx, dano)
    elif armas == "espadalonga":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+1d10+" + modifier
        await roll(ctx, dano)
    elif armas == "glavia":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d10+" + modifier
        await roll(ctx, dano)
    elif armas == "lançademontaria":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d12+" + modifier
        await roll(ctx, dano)
    elif armas == "lançalonga":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d10+" + modifier
        await roll(ctx, dano)
    elif armas == "maçaestrela":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "machadogrande":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d12+" + modifier
        await roll(ctx, dano)
    elif armas == "machadodebatalha":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+1d10+" + modifier
        await roll(ctx, dano)
    elif armas == "malho":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "2d6+" + modifier
        await roll(ctx, dano)
    elif armas == "mangual":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "martelodeguerra":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+1d10+" + modifier
        await roll(ctx, dano)
    elif armas == "picaretadeguerra":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "rapieira":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "tridente":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "arcolongo":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "bestademão":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d6+" + modifier
        await roll(ctx, dano)
    elif armas == "bestapesada":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d10+" + modifier
        await roll(ctx, dano)
    elif armas == "espadatornado":
        ataque = "1d20+1+" + modifier
        await roll(ctx, ataque)
        dano = "2d6+1+" + modifier
        await roll(ctx, dano)
    elif armas == "gema":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "2d6"
        await roll(ctx, dano)
    elif armas == "mosquetelesser":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d10+" + modifier
        await roll(ctx, dano)
    elif armas == "mosquete":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d12+" + modifier
        await roll(ctx, dano)
    elif armas == "blunderbuss":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "2d6+" + modifier
        await roll(ctx, dano)
    elif armas == "obraz":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "monge":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d4+" + modifier
        await roll(ctx, dano)
    elif armas == "martelomosquete":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+1d10+" + modifier
        await roll(ctx, dano)
    elif armas == "palm":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "1d8+" + modifier
        await roll(ctx, dano)
    elif armas == "caracam":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "2d6+2d4+" + modifier
        await roll(ctx, dano)
    elif armas == "infernu":
        ataque = "1d20+1+" + modifier
        await roll(ctx, ataque)
        dano = "2d4+1d6+1d8+1+" + modifier
        await roll(ctx, dano)
    elif armas == "jorge":
        ataque = "1d20+1+" + modifier
        await roll(ctx, ataque)
        dano = "2d4+1d6+1+" + modifier
        await roll(ctx, dano)
    elif armas == "garfo":
        ataque = "1d20+" + modifier
        await roll(ctx, ataque)
        dano = "3d6+" + modifier
        await roll(ctx, dano)
        dano = "3d8+" + modifier
        await roll(ctx, dano)
    else:
        await ctx.send(
        embed=discord.Embed(
            title="Aprende a escrever"
        )
    )

@bot.command(name="tools")
async def tools(ctx):
    await ctx.send(
        embed=discord.Embed(
            title="5etools",
            description="https://5e.tools/5etools.html"
        )
    )

@bot.command(name="connect")
async def connect(ctx):
    user = ctx.message.author
    voiceChannel = user.voice.channel
    server = ctx.message.guild.voice_client
    if server == None:
        await voiceChannel.connect()
    else:
        await server.disconnect()
        await voiceChannel.connect()

batalha = ["https://www.youtube.com/watch?v=fJYlX2ISa-Y", "https://www.youtube.com/watch?v=tWl1ekjk2aQ",
"https://www.youtube.com/watch?v=JDleHc_LPeI", "https://www.youtube.com/watch?v=_f_BnneFanM", 
"https://www.youtube.com/watch?v=5goV2L51MUg", "https://www.youtube.com/watch?v=l_UEPrnHz6k",
"https://www.youtube.com/watch?v=NtqRjGP3uoY", "https://www.youtube.com/watch?v=xti_6Bzpa8A",
"https://www.youtube.com/watch?v=atuFSv2bLa8"
]

suspense = ["https://www.youtube.com/watch?v=avzbyt_fU-M", "https://www.youtube.com/watch?v=vKlgRqCi0Pc",
"https://www.youtube.com/watch?v=uhj18kaTxyA", "https://www.youtube.com/watch?v=HJun8DUZbkU",
"https://www.youtube.com/watch?v=5lE0f0Y3cMY", "https://www.youtube.com/watch?v=5lE0f0Y3cMY",
"https://www.youtube.com/watch?v=yiXkastXOcU", "https://www.youtube.com/watch?v=ovjd22Rkhlk",
"https://www.youtube.com/watch?v=bsvzP8EO65w"
]

taverna = ["https://www.youtube.com/watch?v=fIuO3RpMvHg", "https://www.youtube.com/watch?v=M0pOMVCUY50",
"https://www.youtube.com/watch?v=QVnT1Dl3eyk", "https://www.youtube.com/watch?v=4r_5A6K7gu0",
"https://www.youtube.com/watch?v=Oeo2VCCtUZQ&t=170s", "https://www.youtube.com/watch?v=8OxQeiS_Qjw"
]

epico = ["https://www.youtube.com/watch?v=lsHCzboWK0U", "https://www.youtube.com/watch?v=l_UEPrnHz6k",
"https://www.youtube.com/watch?v=B7xPeh7SQ8A", "https://www.youtube.com/watch?v=iceS6BvhuQ8",
"https://www.youtube.com/watch?v=1PO2AVXWBhk", "https://www.youtube.com/watch?v=07nRu4xjUTw&t=258s",
"https://www.youtube.com/watch?v=aW443RDnens", "https://www.youtube.com/watch?v=y9hh91-2iaA",
"https://www.youtube.com/watch?v=SVhHhtG4DPM"
]

triste = ["https://www.youtube.com/watch?v=I4Rharvcxzo", "https://www.youtube.com/watch?v=VagES3pxttQ",
"https://www.youtube.com/watch?v=z-SlA2NI9kc"
]

boss = ["https://www.youtube.com/watch?v=Owq_6b7q-eg&t=163s", "https://www.youtube.com/watch?v=NHIkUzmNmc0",
"https://www.patreon.com/posts/new-anthem-grim-50076297", "https://www.youtube.com/watch?v=T12ygsp9Mvg",
"https://www.youtube.com/watch?v=6U8K6SPPNLA", "https://www.youtube.com/watch?v=Z9dNrmGD7mU",
"https://www.youtube.com/watch?v=nxXcuDAv7Ss", "https://www.youtube.com/watch?v=JYFU_RiefKk&t=86s",
"https://www.youtube.com/watch?v=sW90d3qU2dQ", "https://www.youtube.com/watch?v=1zN7J64IeBo"
]

ambiente = ["https://www.youtube.com/watch?v=LUO5qhpD2pA", "https://www.youtube.com/watch?v=nRe3xFeyhVY",
"https://www.youtube.com/watch?v=-Eu28EjeLu0",
"https://www.patreon.com/posts/new-community-in-49470501"
]


@bot.command(name="play")
async def play(ctx, url: str):
    
    if url == "batalha":
        url = random.choice(batalha)
    if url == "suspense":
        url = random.choice(suspense)
    if url == "suspence":
        url = random.choice(suspense)
    if url == "taverna":
        url = random.choice(taverna)
    if url == "epico":
        url = random.choice(epico)
    if url == "triste":
        url = random.choice(triste)
    if url == "boss":
        url = random.choice(boss)
    if url == "ambiente":
        url = random.choice(ambiente)
    if url == "anbiente":
        url = random.choice(ambiente)
    if url == "critical":
        url = "https://www.youtube.com/watch?v=LhFETREAvhc"
    
    await connect(ctx)

    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop=bot.loop) 
        await ctx.send('**Now playing:** {}'.format(filename))
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))

@bot.command(name="disconnect")
async def disconnect(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()

@bot.command(name="pause")
async def pause(ctx):
    server = ctx.message.guild.voice_client
    if server.is_playing():
        server.pause()

@bot.command(name="resume")
async def resume(ctx):
    server = ctx.message.guild.voice_client
    if server.is_paused():
        server.resume()

@bot.command(name="stop")
async def stop(ctx):
    server = ctx.message.guild.voice_client
    if server.is_playing():
        server.stop()

bot.run(TOKEN)