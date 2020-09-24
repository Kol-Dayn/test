import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
from random import randint
import json
from discord.ext import commands
import datetime
import time
import os

import sqlite3
from io import BytesIO

client = commands.Bot( command_prefix = '!' )
client.remove_command('help')

# Say
@client.command(aliases=['Say', 'SAY'])
@commands.has_permissions( manage_messages = True)
async def say(ctx, *, text=None):
    if text is None:
      emb = discord.Embed(title='Использование', description = '!say <Текст>', color=0xff8c00)
      await ctx.send(embed=emb, delete_after = 10)
    else: 
      await ctx.channel.purge(limit = 1)
      await ctx.send(embed = discord.Embed(description = text, color = 0x7FFFD4))

# Clear 
@client.command(aliases=['Clear', 'CLEAR'])
@commands.has_permissions( manage_messages = True )
async def clear(ctx,amount=10):
  deleted = await ctx.message.channel.purge(limit=amount + 1)
  emb = discord.Embed(description=f'Удалено {amount} сообщений', color=0x7FFFD4)
  await ctx.send(embed = emb, delete_after=5)

# Help
@client.command(aliases=['Help', 'HELP'])
async def help( ctx ):
    emb = discord.Embed(title='Помощь по коммандам', description='Чтобы посмотреть команды раздела, напишите: `!help <раздел>`', color=0x7FFFD4)
    emb.add_field(name='• Модерация', value = 'Команды помогут админам и модераторам! В этой категории есть такие команды как `!mute` `!kick` `!ban` `!warn`')
    emb.add_field(name='• Информация', value = 'Команды для просмотра информации о `сервере` и `пользователях`')
    emb.add_field(name='• Утилы', value = '`Полезные` команды для сервера')
    emb.add_field(name='• Игры', value = 'Команды для разных `мини-игр`',)
    emb.add_field(name='• Полезности', value = 'Разные команды, как `погода`, `напомнить` и другие')
    emb.add_field(name='• Весёлости', value = '`Шутки` и `анекдоты` которые поднимут вам настроения.')
    emb.set_footer(text="Cлэйм  © 2020 Все права защищены! || ALPHA - VERSION", icon_url='https://cdn.discordapp.com/avatars/624491783522484225/938958ed5c63fe23cf5d5a98c7af0bc1.png?size=512')
    await ctx.send(embed=emb)

# Avatar
@client.command(aliases=['AVATAR', 'Avatar', 'Ava', 'ava', 'AVA'])
async def avatar(ctx, *,  avamember : discord.Member=None):
    if avamember is None:
        avamember = ctx.author
    userAvatarUrl = avamember.avatar_url
    emb=discord.Embed(title=f'Аватар пользователя {avamember.name}:', description=f'[Скачать]({avamember.avatar_url})', color=0x7FFFD4)
    emb.set_image(url=f'{userAvatarUrl}')
    await ctx.send(embed=emb)

# Info
@client.command(aliases=['Info', 'INFO'])
async def info(ctx,member:discord.Member = None):
    if not member:
        member = ctx.author
    emb = discord.Embed(title='Информация о пользователе',color=0x7FFFD4)
    emb.add_field(name='Когда присоеденился:',value=member.joined_at,inline=False)
    emb.add_field(name='Настоящее имя:',value=member.name,inline=False)
    emb.add_field(name='Изменённое имя:',value=member.display_name,inline=False)
    emb.add_field(name='Айди:',value=member.id)
    emb.add_field(name='Аккаунт был создан:',value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p utc'),inline=False)
    emb.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed = emb)

# 8Ball
@client.command(aliases=['8ball', '8BALL', '8Ball'])
async def _8ball(ctx, *, question=None):
    if question is None:
      emb = discord.Embed(title='Использование', description = '!8ball <Вопрос>', color=0xff8c00)
      await ctx.send(embed=emb, delete_after = 10)
    else:
      responses = ['Это точно.',
                 'Без сомнений.',
                 'Загадочный ответ.',
                 'Определённо - Да.',
                 'Вы можете положиться на него.',
                 'Знаки указывают на да.',
                 'Прогноз хороший.',
                 'Наверняка.',
                 'Да.',
                 'Ответ туманный, попробуй ещё раз.',
                 'Спроси позже.',
                 'Очень сомнительно.',
                 'Лучше не говорить тебе сейчас.',
                 'Не могу сейчас предсказать.',
                 'Сконцентрируйся и спроси снова.',
                 'Не рассчитывай на это.',
                 'Мой ответ нет.',
                 'Мои источники говорят нет.',
                 'Прогноз не очень хороший.']

    emb = discord.Embed(title='🎱 Шар',color=0x7FFFD4)
    emb.add_field(name='🧩 | Вопрос:', value=question, inline=False)
    emb.add_field(name='🎲 | Предсказание:',value=random.choice(responses))
    await ctx.channel.send(embed=emb)

# Poll
@client.command(aliases=['Poll', 'POLL'])
@commands.has_permissions( manage_messages = True )
async def poll(ctx, *, message):
    emb=discord.Embed(title='📢 Голосование', color=0x7FFFD4, description=f':bar_chart: {message}')
    msg=await ctx.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

# Pig
pig= [
    "https://cdn.iz.ru/sites/default/files/styles/640x360/public/news-2018-02/200910224_gaf_u46_4944.jpg?itok=v0eul4qO",
    "https://o-prirode.ru/wp-content/uploads/2018/10/1600x1000-03.jpg",
    "https://cdn.fishki.net/upload/post/2018/02/13/2511394/tn/svinya-porosnok-zagorod-kopyta-krupnyy-plan-lico-78678-1920x1200.jpg",
    "https://simple-fauna.ru/wp-content/uploads/2015/10/morskaya-svinka-1.jpg",
    "https://svinki.ru/media/original_images/27072811-416-640x585_pMBrO4C.jpg",
    "https://zooclub.ru/attach/34000/34411.jpg",
    "https://opt-1031816.ssl.1c-bitrix-cdn.ru/upload/resize_cache/iblock/a0a/750_400_1/texel_svinka.jpg?1528195922120417",
    "https://lemurrr.ru/medias/sys_master/images/hca/h91/8904033435678.jpg",
    "https://faunistics.com/wp-content/uploads/2019/08/6-7.jpg",
    "https://3.bp.blogspot.com/-sZsfIdK_ELA/V1WS4yvg-lI/AAAAAAAAJyg/USz8nT7L2wc9b_taQTZ-VWHvryhRuefBgCLcB/s1600/bg3-1024x708.jpg",
    "https://3.bp.blogspot.com/-sZsfIdK_ELA/V1WS4yvg-lI/AAAAAAAAJyg/USz8nT7L2wc9b_taQTZ-VWHvryhRuefBgCLcB/s1600/bg3-1024x708.jpg",
    "https://wildfrontier.ru/wp-content/uploads/2018/12/1-1-700x461.jpg",
    "https://msvinkam.ru/wp-content/uploads/2018/12/1-17.jpg",
    "https://vplate.ru/images/article/thumb/480-0/2019/03/spisok-imen-dlya-morskih-svinok.jpg",
    "https://i.simpalsmedia.com/point.md/news/thumbnails/large/be77fc0f5dd94388b7e8d3fb952fda52.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Two_adult_Guinea_Pigs_%28Cavia_porcellus%29.jpg/275px-Two_adult_Guinea_Pigs_%28Cavia_porcellus%29.jpg",
    "https://ptichka.net/wp-content/uploads/kormlenie-morskix-svinok-300x225.jpg",
    "https://homkin.ru/wp-content/uploads/2018/06/pig21-651x381.jpg",
    "https://svinki.ru/media/original_images/03_mrD4Tj1.jpg",
    "https://zoozov.com/wp-content/uploads/attachpost/1988/post-1988-0.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcR862u0cIxAgGeLwqG9lT68WqEsI4Q_vpfvEg&usqp=CAU",
    "https://s1.1zoom.ru/prev2/391/390089.jpg",
    "https://vplate.ru/images/article/thumb/480-0/2019/03/porody-morskih-svinok-6.jpg",
    "https://svinki.ru/media/original_images/self.jpg",
    "https://www.zoospravka.ru/Rabbit/images/guinea_pig.jpg",
    "https://msvinkam.ru/wp-content/uploads/2018/01/1-2.jpg",
    "https://svinki.ru/media/original_images/04_8bl3PFw.jpg",
    "https://homkin.ru/wp-content/uploads/2018/07/70.2-678x381.jpg"
]
@client.command(aliases=['pig','Pig', 'PIG'])
async def _pig(ctx):
    emb=discord.Embed(title=f'Свинка по вашему запросу:', color = 0x7FFFD4)
    emb.set_image(url=f'{random.choice(pig)}')
    await ctx.channel.send(embed=emb)

# Battle
@client.command(aliases=['Battle', 'BATTLE'])
async def battle( ctx, member: discord.Member = None ):
    if member is None:
        emb = discord.Embed( title = f'Использование', description='!battle <пользователь>', color = 0x7FFFD4)
        await ctx.send( embed = emb )
    elif member.id == ctx.author.id:
            emb = discord.Embed( description = f"Вы не можете сразится с собой!", color = 0xff8c00)
            await ctx.send( embed = emb )
    else:
        a = random.randint(1,2)
        if a == 1:
            emb = discord.Embed( title = f"Победитель - {ctx.author}", color = 0x00FF7F )
            await ctx.send( embed = emb )

            emb = discord.Embed( title = f"Проигравший - {member}", color = 0xFA8072    )
            await ctx.send( embed = emb )
        else:
            emb = discord.Embed( title = f"Победитель - {member}", color = 0x00FF7F)
            await ctx.send( embed = emb )

            emb = discord.Embed( title = f"Проигравший - {ctx.author}", color = 0xFA8072    )
            await ctx.send( embed = emb )

# All - Server
@client.command(aliases=['Totla', 'TOTAL'])
async def total(ctx):
    total = 0
    for guild in client.guilds:
        if ctx.author in guild.members:
            total += 1
    emb = discord.Embed(title=f'Общих серверов: {total}', color=0x7FFFD4)
    await ctx.send(embed=emb)

# Kick
@client.command(aliases=['KICK', 'Kick'])
@commands.has_permissions( kick_members = True )
async def kick(ctx, member: discord.Member = None, *, reason = 'Причина не указанна!'):
    if member == None:
        emb = discord.Embed(title='Использование команды !kick', description = 'Выгнать пользователя, с возможностью возврата', color=0xff8c00)
        emb.add_field(name='Пример 1', value='`!kick <@пользователь>`\n ╰ Кикнет пользователя без причины')
        emb.add_field(name='Пример 2', value='`!kick <@пользователь> <причина>`\n ╰ Кикнет пользователя с указанной причиной', inline=False)
        await ctx.send(embed=emb, delete_after = 10)
    elif member.id == ctx.author.id:
            emb = discord.Embed( title = f"Вы не можете кикнуть себя!", color = 0xff8c00)
            await ctx.send( embed = emb ) 
    else:
        emb = discord.Embed(title='Кик',color=0xFA8072)
        emb.add_field(name='Модератор:',value=ctx.message.author.mention,inline=False)
        emb.add_field(name='Нарушитель:',value=member.mention,inline=False)
        emb.add_field(name='Причина:',value=reason,inline=False)
        await member.kick(reason = reason)
        await ctx.send(embed = emb)
        emb = discord.Embed(title=':alarm_clock: Информация',color=0x7FFFD4)
        emb.add_field(name='Вы были кикнуты модератором:',value=ctx.message.author.mention, inline=False)
        emb.add_field(name='Причина:',value=reason, inline=False)
        emb.add_field(name='Сервер:',value=ctx.guild.name, inline=False)
        await member.send(embed = emb)

# Ban
@client.command(aliases=['BAN', 'Ban'])
@commands.has_permissions( ban_members = True )
async def ban(ctx, member: discord.Member = None, *, reason = 'Причина не указнанна!'):
    if member == None:
        emb = discord.Embed(title='Использование команды !ban', description = 'Выгнать пользователя, без возможности возврата', color=0xff8c00)
        emb.add_field(name='Пример 1', value='`!ban <@пользователь>`\n ╰ Забанит пользователя без причины')
        emb.add_field(name='Пример 2', value='`!ban <@пользователь> <причина>`\n ╰ Забанит пользователя с указанной причиной', inline=False)
        await ctx.send(embed = emb, delete_after = 10)
    elif member.id == ctx.author.id:
            emb = discord.Embed( title = f"Вы не можете забанить себя!", color = 0xff8c00)
            await ctx.send( embed = emb )
    else:
        emb = discord.Embed(title='Бан',color=0xFA8072)
        emb.add_field(name='Модератор:',value=ctx.message.author.mention,inline=False)
        emb.add_field(name='Нарушитель:',value=member.mention,inline=False)
        emb.add_field(name='Причина:',value=reason,inline=False)
        await member.ban(reason = reason)
        await ctx.send(embed = emb)
        emb = discord.Embed(title='⏰ Информация',color=0x7FFFD4)
        emb.add_field(name='Вы были забанены модератором:',value=ctx.message.author.mention, inline=False)
        emb.add_field(name='Причина:',value=reason, inline=False)
        emb.add_field(name='Сервер:',value=ctx.guild.name, inline=False)
        await member.send(embed = emb)

#UnBan
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unban')
            return

# Errors
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        emb=discord.Embed(title =f'Недостаточно прав для удаления сообщений!', color=0xFA8072)
        emb.add_field(name='Нужные права:', value='\n Управления сообщениями')
        await ctx.send(embed=emb, delete_after = 10)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        emb=discord.Embed(title =f'Недостаточно прав для кика пльзователя!', color=0xFA8072)
        emb.add_field(name='Нужные права:', value='\n Выгонять участников')
        await ctx.send(embed=emb, delete_after = 10)

@poll.error
async def poll(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.purge(limit = 1)
        emb=discord.Embed(title='Использование', description='!poll <Текст>', color=0xff8c00)
        await ctx.send(embed=emb, delete_after=10)
    if isinstance(error,commands.MissingPermissions):
        emb=discord.Embed(description =f'Недостаточно прав для удаления сообщений!', color=0xFA8072)
        emb.add_field(name='Нужные права:', value='\n Управления сообщениями')
        await ctx.send(embed=emb, delete_after=10) 

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        emb=discord.Embed(title =f'Недостаточно прав для бана пльзователя!', color=0xFA8072)
        emb.add_field(name='Нужные права:', value='\n Банить участников')
        await ctx.send(embed=emb, delete_after = 10)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        emb=discord.Embed(title =f'Недостаточно прав для отправки сообщений от имени бота!', color=0xFA8072)
        emb.add_field(name='Нужные права:', value='\n Управлять сообщениями')
        await ctx.send(embed=emb, delete_after = 10)

# Anti - Ls
@client.event
async def on_message(message):
    try:
        try:
            if isinstance(message.channel, discord.DMChannel):
                return
        except AttributeError:
            return
        await client.process_commands(message)
    except TypeError:
        return

# Connect
@client.event 
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help"))
    print('Login!')

token = os.eniron.get('BOT_TOKEN')