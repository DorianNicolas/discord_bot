import random

import discord

from module import *
import utils.utils
import utils.constants as const
import utils.aws_utils as s3
import quiz

client = discord.Client()
quiz = quiz.Quiz(client)

# BOT COMMANDS

def get_commands(bot, logger):

    # @bot.command()
    # async def echo(*, message):
    #    await bot.say(message)

    @bot.command()
    async def tableflip():
        """Flips a table"""
        await bot.say("(╯°□°）╯︵ ┻━┻")

    @bot.command()
    async def add(left: int, right: int):
        """Adds two numbers together."""
        await bot.say(left + right)

    @bot.command()
    async def roll(dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception as error:
            logger.warning(error)
            await bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await bot.say(result)

    @bot.command(description='For when you wanna settle the score some other way')
    async def choose(*choices: str):
        """Chooses between multiple choices."""
        await bot.say(random.choice(choices))

    @bot.command()
    async def repeat(times: int, content='repeating...'):
        """Repeats a message multiple times."""
        for i in range(times):
            await bot.say(content)

    @bot.command()
    async def joined(member: discord.Member):
        """Says when a member joined."""
        await bot.say('{0.name} joined in {0.joined_at}'.format(member))

    @bot.group(pass_context=True)
    async def cool(ctx):
        """Says if a user is cool.

        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

    @cool.command(name='bot')
    async def _bot():
        """Is the bot cool?"""
        await bot.say('Yes, the bot is cool.')

    @bot.command()
    async def citation(*theme):
        """Affiche une citation"""
        if len(theme) > 0:
            random_citation = citations.get_citation_by_theme(theme[0])
        else:
            random_citation = citations.get_random_citation()
        logger.debug('Citation : %s', random_citation)
        await bot.say(random_citation)

    # @bot.command()
    # async def punir(member: discord.Member):
    #    await  bot.say('{0.name} est puni(e) !'.format(member))

    @bot.command(pass_context=True)
    async def count(ctx):
        id_server = ctx.message.server.id
        # FIXME move this try/catch
        try:
            s3.download_file(const.STATS_FILE_PATH)
        except Exception as e:
            logger.warning('Download error - %s', e)
            return

        if ctx.message.mentions:
            id_member = ctx.message.mentions[0].id
            emoji_count = utils.utils.count_emoji_by_server_and_nick(id_server, id_member, logger)
        else:
            emoji_count = utils.utils.count_emoji_by_server(id_server, logger)
        visible_emojis = bot.get_all_emojis()
        visible_emojis_count = []
        for emoji in visible_emojis:
            if emoji.id in emoji_count:
                visible_emojis_count.append([emoji, emoji_count[emoji.id]])

        visible_emojis_count = sorted(visible_emojis_count, key=lambda v: v[1], reverse=True)

        i = 0
        while i < 10 and i < len(visible_emojis_count):
            await bot.say(str(visible_emojis_count[i][0])+' a été utilisé '+str(visible_emojis_count[i][1])+' fois',)
            i += 1


    #Quiz part here, don't touch if you don't know what you are doing

    @bot.command()
    async def startquiz(number: int):
        await quiz.start(bot, number)

    @bot.command()
    async def statsquiz():
        await bot.say('Affichage des meilleurs joueurs du quiz.')

    @bot.command()
    async def stopquiz():
        await quiz.stop(bot)
