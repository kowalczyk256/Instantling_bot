import os
import sqlite3
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Intents, Interaction, ButtonStyle
from discord.ui import Button, View
import asyncio
import logging

logging.basicConfig(
    filename='mainLog.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_message(message):
    print(message)
    logging.info(message)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def check_registration(username):
    try:
        db_path = 'register.db'
        if not os.path.exists(db_path):
            log_message(f"Plik bazy danych '{db_path}' nie istnieje.")
            return None
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        log_message(f"Sprawdzanie użytkownika: {username}")
        c.execute("SELECT login, password FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()
        
        if result:
            log_message(f"Znaleziono użytkownika w bazie danych: {result}")
        else:
            log_message(f"Nie znaleziono użytkownika {username} w bazie danych.")
        
        return result
    
    except sqlite3.Error as e:
        log_message(f"Błąd bazy danych: {e}")
        return None

class StartSessionButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Rozpocznij sesję bot", style=ButtonStyle.green)
    async def start_session_bot(self, interaction: Interaction, button: Button):
        await self.start_session(interaction, is_human=False)

    @discord.ui.button(label="Rozpocznij sesję człowiek", style=ButtonStyle.blurple)
    async def start_session_human(self, interaction: Interaction, button: Button):
        await self.start_session(interaction, is_human=True)

    async def start_session(self, interaction: Interaction, is_human: bool):
        username = interaction.user.name
        log_message(f"Sprawdzanie rejestracji dla użytkownika: {username}")
        result = check_registration(username)

        try:
            await interaction.response.send_message("Zerknij na wiadomości prywatne ode mnie :)", ephemeral=True)
        except discord.errors.InteractionResponded:
            log_message("Interakcja już została obsłużona.")

        if result:
            login, password = result
            user = interaction.user
            try:
                dm_channel = await user.create_dm()
                session_type = "człowiek" if is_human else "bot"
                await dm_channel.send(f"Wybrano tryb {session_type}. Podaj liczbę sesji, które chcesz uruchomić:")
                
                def check_dm(m):
                    return m.author == user and m.channel == dm_channel

                response = await bot.wait_for("message", check=check_dm)

                try:
                    number_of_sessions = int(response.content)

                    if number_of_sessions > 20:
                        await dm_channel.send("Możesz uruchomić maksymalnie 20 sesji na raz. Podaj mniejszą liczbę.")
                        return
                    
                    log_message(f"Liczba sesji od użytkownika {user}: {number_of_sessions}")

                    await dm_channel.send(f"Rozpoczynam w trybie {session_type}, liczba sesji: {number_of_sessions}.")
                    
                    await self.run_subprocess(user, login, password, number_of_sessions, '📲〉utworz-sesje', session_type)

                except ValueError:
                    await dm_channel.send("Podano nieprawidłową liczbę sesji. Upewnij się, że to liczba całkowita.")
            
            except discord.Forbidden:
                log_message(f"Nie można wysłać prywatnej wiadomości do {user}")
                await interaction.followup.send("Nie mogę wysłać Ci wiadomości prywatnej. Upewnij się, że masz włączone wiadomości prywatne.", ephemeral=True)
        
        else:
            log_message(f"Nie znaleziono użytkownika {username} w bazie danych.")
            try:
                await interaction.followup.send("Nie jesteś zarejestrowany w bazie danych!", ephemeral=True)
            except discord.errors.InteractionResponded:
                log_message("Interakcja już została obsłużona.")

    async def run_subprocess(self, user, login, password, number_of_sessions, report_channel_name, session_type):
        command = [
            'python3', 'instantling.py',
            login,
            password,
            str(number_of_sessions),
            report_channel_name,
            'human' if session_type == "człowiek" else 'bot'
        ]
        log_message(f"Uruchamianie subprocess: {' '.join(command)}")
        
        process = await asyncio.create_subprocess_exec(*command)
        
        await process.wait()
        
        dm_channel = await user.create_dm()
        await dm_channel.send(f"Sesje w trybie {session_type} zostały zakończone!")

@bot.event
async def on_ready():
    log_message(f'{bot.user} działa!')

    channel_name = '📲〉utworz-sesje'
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if channel:
            view = StartSessionButton()  
            await channel.send("Kliknij poniżej, aby rozpocząć sesję.", view=view)
            log_message(f"Wiadomość z przyciskami wysłana do kanału {channel_name} na serwerze {guild.name}.")
        else:
            log_message(f"Nie znaleziono kanału {channel_name} na serwerze {guild.name}.")

@bot.command(name="start")
async def start(ctx):
    if ctx.channel.name == '📲〉utworz-sesje':
        view = StartSessionButton()
        await ctx.send("Kliknij poniżej, aby rozpocząć sesję.", view=view)

def main():
    bot.run(TOKEN)

async def start_session_for_user(username, login, password, number_of_sessions, session_type):
    log_message(f"Rozpoczynanie sesji dla {username} w trybie {session_type} na {number_of_sessions} sesji.")
    
    command = [
        'python3', 'instantling.py',
        login,
        password,
        str(number_of_sessions),
        '📲〉utworz-sesje',
        session_type
    ]
    log_message(f"Uruchamianie subprocess: {' '.join(command)}")
    
    process = await asyncio.create_subprocess_exec(*command)
    
    await process.wait()
    
    log_message(f"Zakończono sesje dla {username}.")

if __name__ == '__main__':
    main()
