
import discord
from discord.ext import commands

import json

import asyncio

color = 0xdbdbdb

class main_commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        with open('cogs/cogsbase/cbservers.json', 'r') as file:
            self.cbservers = json.load(file)

        self.cbservers[guild.id] = {}
        self.cbservers[guild.id]['servers-settings'] = {}
        self.cbservers[guild.id]['servers-settings']['users-id'] = None
        self.cbservers[guild.id]['servers-settings']['users-mute-id'] = None

        with open('cogs/cogsbase/cbservers.json', 'w') as file:
            json.dump(self.cbservers, file, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        with open('cogs/cogsbase/cbservers.json', 'r') as file:
            self.cbservers = json.load(file)

        self.cbservers.pop(str(guild.id))

        with open('cogs/cogsbase/cbservers.json', 'w') as file:
            json.dump(self.cbservers, file, indent=4)

    # bans
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = ' '):

        try:

            if member.guild_permissions.administrator:

                embed = discord.Embed(title='',
                                      description=f'**ㅤ Пользователь {member.mention} не может быть заблокирован пока обладает правами администратора.**',
                                      color = color)
                await ctx.reply(embed=embed)

            else:

                try:

                    embed_member = discord.Embed(title='',
                                              description=f'**ㅤ Вы были заблокированы на сервере {ctx.guild.name} по причине: {reason}.**',
                                              color = color)
                    await member.send(embed=embed_member)

                except:
                    pass

                await member.ban(reason=reason)

                embed = discord.Embed(title='',
                                      description=f'**ㅤ Пользователь {member.mention} был заблокирован по причине: {reason}.**',
                                      color = color)
                await ctx.reply(embed=embed)

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, time, *, reason: str = ' '):

        try:

            if member.guild_permissions.administrator:

                embed = discord.Embed(title='',
                                      description=f'**ㅤ Пользователь {member.mention} не может быть заблокирован пока обладает правами администратора.**',
                                      color = color)
                await ctx.reply(embed=embed)

            else:

                try:

                    embed_member = discord.Embed(title='',
                                              description=f'**ㅤ Вы были временно заблокированы на сервере {ctx.guild.name} по причине: {reason}. Время: {time} секунд.**',
                                              color = color)
                    await member.send(embed=embed_member)

                except:
                    pass

                await member.ban(reason=reason)

                embed = discord.Embed(title='',
                                      description=f'**ㅤ Пользователь {member.mention} был временно заблокирован по причине: {reason}. Время: {time} секунд.**',
                                      color = color)
                await ctx.reply(embed=embed)

                await asyncio.sleep(int(time))

                await member.unban()

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, member_id):

        try:

            member = discord.Object(id = member_id)

            await ctx.guild.unban(member)

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Пользователь с айди {member_id} был разблокирован.**',
                                  color = color)
            await ctx.reply(embed=embed)

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    #mutes
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = ' '):

        try:

            with open('cogs/cogsbase/cbservers.json', 'r') as file:
                self.cbservers = json.load(file)

            role = discord.utils.get(ctx.guild.roles, id = self.cbservers[str(ctx.guild.id)]['servers-settings']['users-mute-id'])

            if self.cbservers[str(ctx.guild.id)]['servers-settings']['users-mute-id'] == None or not role:

                embed_create_mute = discord.Embed(title='',
                                      description=f'**ㅤ Роль для мьюта не обнаружена, идёт создание новой.**',
                                      color = color)
                message = await ctx.reply(embed=embed_create_mute)

                role = await ctx.guild.create_role(name='muted')

                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, send_messages = False)

                self.cbservers[str(ctx.guild.id)]['servers-settings']['users-mute-id'] = role.id

                embed_create_role = discord.Embed(title='',
                                                  description=f'**ㅤ Роль для мьюта была создана: {role.mention}**',
                                                  color = color)
                await message.edit(embed=embed_create_role, delete_after = 3)

            await member.add_roles(role, reason=reason)

            with open('cogs/cogsbase/cbservers.json', 'w') as file:
                json.dump(self.cbservers, file, indent=4)

            try:

                embed_member = discord.Embed(title='',
                                          description=f'**ㅤ Вы были замьючены на сервере {ctx.guild.name} по причине: {reason}.**',
                                          color = color)
                await member.send(embed=embed_member)

            except:
                pass

            embed = discord.Embed(title='',
                                         description=f'**ㅤ Пользователь {member.mention} был замьючен по причине: {reason}.**',
                                         color = color)
            await ctx.reply(embed=embed)

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def tempmute(self, ctx, member: discord.Member, time, *, reason: str = ' '):

        try:

            with open('cogs/cogsbase/cbservers.json', 'r') as file:
                self.cbservers = json.load(file)

            role = discord.utils.get(ctx.guild.roles, id = self.cbservers[str(ctx.guild.id)]['servers-settings']['users-mute-id'])

            if self.cbservers[str(ctx.guild.id)]['servers-settings']['users-mute-id'] == None or not role:

                embed_create_mute = discord.Embed(title='',
                                      description=f'**ㅤ Роль для мьюта не обноружена, идёт создание новой.**',
                                      color = color)
                message = await ctx.reply(embed=embed_create_mute)

                role = await ctx.guild.create_role(name='muted')

                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, send_messages = False)

                self.cbservers[str(ctx.guild.id)]['servers-settings']['users-mute-id'] = role.id

                embed_create_role = discord.Embed(title='',
                                                  description=f'**ㅤ Роль для мьюта была создана: {role.mention}**',
                                                  color = color)
                await message.edit(embed=embed_create_role, delete_after = 3)

            await member.add_roles(role, reason=reason)

            with open('cogs/cogsbase/cbservers.json', 'w') as file:
                json.dump(self.cbservers, file, indent=4)

            try:

                embed_member = discord.Embed(title='',
                                          description=f'**ㅤ Вы были временно замьючены на сервере {ctx.guild.name} по причине: {reason}. Время: {time} секунд.**',
                                          color = color)
                await member.send(embed=embed_member)

            except:
                pass

            embed = discord.Embed(title='',
                                         description=f'**ㅤ Пользователь {member.mention} был временно замьючен по причине: {reason}. Время: {time} секунд.**',
                                         color = color)
            await ctx.reply(embed=embed)

            await asyncio.sleep(int(time))

            if role in member.roles:

                await member.remove_roles(role)

                try:

                    embed_three = discord.Embed(title='',
                                                description=f'**ㅤ Вы были размьючены на сервере {ctx.guild.name} .**',
                                                color = color)
                    await member.send(embed=embed_three)

                except:
                    pass

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):

        try:

            with open('cogs/cogsbase/cbservers.json', 'r') as file:
                self.cbservers = json.load(file)

            role = discord.utils.get(ctx.guild.roles, id = self.cbservers[str(ctx.guild.id)]['servers-settings']['users-mute-id'])

            if role in member.roles:

                await member.remove_roles(role)

                try:

                    embed_member = discord.Embed(title='',
                                              description=f'**ㅤ Вы были размьючены на сервере {ctx.guild.name} .**',
                                              color = color)
                    await member.send(embed=embed_member)

                except:
                    pass

                embed = discord.Embed(title='',
                                             description=f'**ㅤ Пользователь {member.mention} был размьючен.**',
                                             color = color)
                await ctx.reply(embed=embed)

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    #auto role
    @commands.Cog.listener()
    async def on_member_join(self, member):

        with open('cogs/cogsbase/cbservers.json', 'r') as file:
            self.cbservers = json.load(file)

        role = discord.utils.get(member.guild.roles, id = self.cbservers[str(member.guild.id)]['servers-settings']['users-id'])

        await member.add_roles(role)

    @commands.hybrid_group(name = 'auto', description = 'auto role')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def auto(self, ctx) -> None:
        
        if ctx.invoked_subcommand is None:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    @auto.command(name = 'setup', description = 'auto setup role')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def auto_setup(self, ctx, role: discord.Role) -> None:

        try:

            with open('cogs/cogsbase/cbservers.json', 'r') as file:
                self.cbservers = json.load(file)

            self.cbservers[str(ctx.guild.id)]['servers-settings']['users-id'] = role.id

            with open('cogs/cogsbase/cbservers.json', 'w') as file:
                json.dump(self.cbservers, file, indent=4)

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Была присвоена роль для автовыдачи: {role.mention}**',
                                  color = color)
            await ctx.reply(embed=embed)

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    @auto.command(name = 'remove', description = 'auto remove')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def auto_remove(self, ctx):

        try:

            with open('cogs/cogsbase/cbservers.json', 'r') as file:
                self.cbservers = json.load(file)

            self.cbservers[str(ctx.guild.id)]['servers-settings']['users-id'] = None

            with open('cogs/cogsbase/cbservers.json', 'w') as file:
                json.dump(self.cbservers, file, indent=4)

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Была отсвоена роль для автовыдачи.**',
                                  color = color)
            await ctx.reply(embed=embed)

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    @auto.command(name = 'role', description = 'auto role')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def auto_role(self, ctx):

        try:

            with open('cogs/cogsbase/cbservers.json', 'r') as file:
                self.cbservers = json.load(file)

            role = discord.utils.get(ctx.guild.roles, id = self.cbservers[str(ctx.guild.id)]['servers-settings']['users-id'])

            if self.cbservers[str(ctx.guild.id)]['servers-settings']['users-id'] == None or not role:

                embed = discord.Embed(title='',
                                      description=f'**ㅤ Роль для автовыдачи не присвоена.**',
                                      color = color)
                await ctx.reply(embed=embed)

            else:

                embed = discord.Embed(title='',
                                      description=f'**ㅤ Роль для авдовыдачи: {role.mention}**',
                                      color = color)
                await ctx.reply(embed=embed)

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.reply(embed=embed)

    #other
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 0):

        try:

            if amount != 0:

                amount_messages = await ctx.channel.purge(limit = amount + 1)

                embed = discord.Embed(title='',
                                      description=f'**ㅤ Было очищено {len(amount_messages) - 1} сообщений.**',
                                      color = color)
                await ctx.send(embed=embed, delete_after = 3)

            else:

                embed = discord.Embed(title='',
                                      description='**ㅤ Произошла какая-то ошибка: вы не указали кол-во сообщений.**',
                                      color = color)
                await ctx.reply(embed=embed)

        except:

            embed = discord.Embed(title='',
                                  description=f'**ㅤ Произошла какая-то ошибка.**',
                                  color = color)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(main_commands(client))