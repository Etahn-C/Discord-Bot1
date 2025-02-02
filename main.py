import discord
import os
import GachaGame
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
DATA = os.getenv("DATA_FILE")


class MyClient(discord.Client):
    def start_game(self):
        self.game = GachaGame(DATA)
        self.game.load()

    async def on_ready(self):
        print("Logged on as", self.user)
        for guild in client.guilds:
            if guild.name == GUILD:
                break

        print(
            f"{client.user} is connected to the following guild:\n"
            f"{guild.name} (id: {guild.id})\n"
        )

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        # For testing purposes, if this don't work, bot died
        if message.content.upper() == "$PING":
            await message.channel.send("pong")

        # Game Functions
        if message.content.upper() == "$ADD PLAYER":
            await message.channel.send((self.game.add_player(str(message.author))))
            self.game.save()

        if message.content.upper() == "$REMOVE PLAYER":
            await message.channel.send((self.game.remove_player(str(message.author))))
            self.game.save()

        if message.content.upper() == "$RESET PLAYER":
            await message.channel.send((self.game.reset_player(str(message.author))))
            self.game.save()

        if message.content.upper() == "$ROLL GACHA":
            await message.channel.send((self.game.roll_gacha(str(message.author))))
            self.game.save()

        if message.content.upper() == "$INVENTORY":
            await message.channel.send((self.game.inventory(str(message.author))))
            self.game.save()


# Discord API stuffs, not gonna mess with it.
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.start_game()
client.run(TOKEN)
