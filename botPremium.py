import os
import sqlite3
import asyncio
import logging
from main import start_session_for_user

logging.basicConfig(
    filename='auto_session_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_message(message):
    print(message) 
    logging.info(message)

def get_users_from_db():
    db_path = 'premium.db'
    if not os.path.exists(db_path):
        log_message(f"Plik bazy danych '{db_path}' nie istnieje.")
        return []

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT discord_username, login, password, sessions FROM users")
        users = c.fetchall()
        conn.close()
        return users
    except sqlite3.Error as e:
        log_message(f"Błąd bazy danych: {e}")
        return []

async def run_sessions_for_all_users():
    users = get_users_from_db()

    if not users:
        log_message("Brak użytkowników w bazie danych do uruchomienia sesji.")
        return

    for user in users:
        discord_username, login, password, sessions = user

        log_message(f"Rozpoczynanie sesji dla {discord_username}, sesji: {sessions}")

        await start_session_for_user(discord_username, login, password, sessions, "bot")

        log_message(f"Sesje dla {discord_username} zakończone.")

async def main():
    await run_sessions_for_all_users()

if __name__ == "__main__":
    asyncio.run(main())
