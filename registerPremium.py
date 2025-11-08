import sqlite3
import os

db_path = 'premium.db'

def create_db():
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE users (
                         discord_username TEXT NOT NULL,
                         login TEXT NOT NULL,
                         password TEXT NOT NULL,
                         sessions INTEGER NOT NULL
                       )''')
        conn.commit()
        conn.close()
        print(f"Baza danych '{db_path}' została utworzona.")
    else:
        print(f"Baza danych '{db_path}' już istnieje.")

def add_user(discord_username, login, password, sessions):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("INSERT INTO users (discord_username, login, password, sessions) VALUES (?, ?, ?, ?)",
              (discord_username, login, password, sessions))
    
    conn.commit()
    conn.close()
    print(f"Użytkownik {discord_username} został dodany do bazy danych.")

def get_user_data():
    discord_username = input("Podaj nazwę użytkownika Discorda: ")
    login = input("Podaj login do Instaling: ")
    password = input("Podaj hasło do Instaling: ")
    
    while True:
        try:
            sessions = int(input("Podaj liczbę sesji (całkowita liczba): "))
            if sessions <= 0:
                print("Liczba sesji musi być większa od zera.")
            else:
                break
        except ValueError:
            print("Nieprawidłowa wartość. Podaj liczbę całkowitą.")

    return discord_username, login, password, sessions

def main():
    create_db()
    
    while True:
        print("\nMenu:")
        print("1. Dodaj nowego użytkownika")
        print("2. Wyjdź")
        
        choice = input("Wybierz opcję (1/2): ")
        
        if choice == '1':
            discord_username, login, password, sessions = get_user_data()
            add_user(discord_username, login, password, sessions)
        elif choice == '2':
            print("Zamykanie programu.")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main()