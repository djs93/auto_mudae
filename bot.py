from credentials import token, fromChannel, pokeTime, rollTime, claimTime, dailyTime, reactTime, operatingServer, \
    waifuChannel, pokeChannel, maintenanceServer
import discord


class Client(discord.Client):
    pokeTimeLeft = pokeTime
    rollTimeLeft = rollTime
    claimTimeLeft = claimTime
    dailyTimeLeft = dailyTime
    reactTimeLeft = reactTime

    def tweak_time(self, timer, newTime):
        if timer == "poke":
            self.pokeTimeLeft = newTime
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

    async def on_message(self, message):
        if message.guild.id == maintenanceServer:
            if message.channel.id == fromChannel:
                parts = message.content.split(" ")
                if len(parts) == 3 and parts[0] == "tweakTime":
                    tweakMessage = self.tweak_time(parts[1], parts[2])
                    await self.send_message(fromChannel, tweakMessage)
            #    keys = toChannels.keys()
            #    for key in keys:
            #        if parts[0] == key:
            #            await self.send_messages(key, ":".join(parts[1:]))
            #            return
            #    await self.send_messages("general", message.content)


client = Client()
client.run(token, bot=False)
