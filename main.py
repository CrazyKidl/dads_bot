import discord
from discord import utils
import config
import asyncio
import random


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        print(message)
        if message.content.startswith('.help'):
            await message.channel.send('Тебе нужна помощь {0.author.mention}?\n'
                                       'Тут вот ниже список комманд:\n'
                                       '.help - ну ты уже тута\n'
                                       '.littlegame - маленькая игрушка\n'
                                       '.bot - проверка есть ли я тута)\n'
                                       '.music - музычка)'.format(message))
        elif message.content.startswith('.bot'):
            await message.channel.send('Че надо а? {0.author.mention}'.format(message))
        elif message.content.startswith('.music'):
            await message.channel.send('Еще не сделоль((9('
                                       'Соре( {0.author.mention}'.format(message))
        elif message.content.startswith('.littlegame'):
            await message.channel.send('О, го поиграем))0) {0.author.mention}\n'
                                       'Угадай число от 1 до 10'.format(message))

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)
            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(
                    'Че такой долгий, быстрее отвечай, кста правильное число было: {}.'.format(answer))
            if int(guess.content) == answer:
                await message.channel.send('Ебать ты че шанс был 10% и ты угадал? Нихуя везучий!')
            else:
                await message.channel.send('Ха-ха, лох, правильное число было: {}.'.format(answer))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
            channel = self.get_channel(payload.channel_id)  # получаем объект канала
            message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
            member = utils.get(message.guild.members,
                               id=payload.user_id)  # получаем объект пользователя который поставил реакцию
            try:
                emoji = str(payload.emoji)  # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=config.ROLES[emoji])  # объект выбранной роли (если есть)
                if (len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))
            except KeyError:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)  # получаем объект канала
        message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
        member = utils.get(message.guild.members,
                           id=payload.user_id)  # получаем объект пользователя который поставил реакцию
        try:
            emoji = str(payload.emoji)  # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])  # объект выбранной роли (если есть)
            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
        except KeyError:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


client = MyClient()
client.run(config.TOKEN)
