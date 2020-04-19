from credentials import token, fromChannel, pokeTime, rollTime, claimTime, dailyTime, reactTime, operatingServer, \
    waifuChannel, pokeChannel, maintenanceServer, maintenanceChannel, userMention
import discord
import asyncio


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()


class Client(discord.Client):

    def __init__(self, *, loop=None, **options):
        super().__init__(loop=None, **options)
        self.pokeTimeLeft = pokeTime
        self.rollTimeLeft = rollTime
        self.claimTimeLeft = claimTime
        self.dailyTimeLeft = dailyTime
        self.reactTimeLeft = reactTime
        self.pokeTimer = Timer(self.pokeTimeLeft * 60, self.do_poke)
        #self.pokeTimer = Timer(5, self.do_poke)

    async def do_poke(self):
        await self.send_message(maintenanceChannel, "{} Pokemon roll time!".format(userMention))
        self.pokeTimer = Timer(self.pokeTimeLeft * 60, self.do_poke)
        print("Set pokeTimer to trigger in {} seconds!".format(self.pokeTimeLeft * 60))

    def tweak_time(self, timer, newTime):
        if timer == "poke":
            self.pokeTimeLeft = newTime
            self.pokeTimer.cancel()
            self.pokeTimer = Timer(self.pokeTimeLeft, self.do_poke)
        elif timer == "roll":
            self.rollTimeLeft = newTime
        elif timer == "claim":
            self.claimTimeLeft = newTime
        elif timer == "daily":
            self.dailyTimeLeft = newTime
        elif timer == "react":
            self.reactTimeLeft = newTime
        else:
            return "Invalid timer " + timer
        return "Set {} timer to {}!".format(timer, newTime)

    async def send_message(self, channel_id, message):
        channel = self.get_channel(channel_id)
        print("Sending " + message + " to " + channel.name + " in " + channel.guild.name)
        await channel.send(message)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.send_message(maintenanceChannel, "Logged on!")

    async def on_message(self, message):
        if not message.author.bot:
            if message.guild.id == maintenanceServer:
                if message.channel.id == maintenanceChannel:
                    parts = message.content.split(" ")
                    if len(parts) == 3 and parts[0] == "tweakTime":
                        tweakMessage = self.tweak_time(parts[1], int(parts[2]))
                        await self.send_message(maintenanceChannel, tweakMessage)
                #    keys = toChannels.keys()
                #    for key in keys:
                #        if parts[0] == key:
                #            await self.send_messages(key, ":".join(parts[1:]))
                #            return
                #    await self.send_messages("general", message.content)


client = Client()
print("logging in...")
client.run(token)
