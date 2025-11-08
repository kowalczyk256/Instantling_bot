import sqlite3
import os

db_path = 'register.db'

def create_db():
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                         username TEXT PRIMARY KEY,
                         login TEXT NOT NULL,
                         password TEXT NOT NULL
                       )''')
        conn.commit()
        conn.close()
        print(f"Baza danych '{db_path}' została utworzona.")
    else:
        print(f"Baza danych '{db_path}' już istnieje.")

def register_user(username, login, password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        c.execute('INSERT INTO users (username, login, password) VALUES (?, ?, ?)', 
                  (username, login, password))
        conn.commit()
        print(f"Użytkownik {username} zarejestrowany pomyślnie!")
    except sqlite3.IntegrityError:
        print(f"Użytkownik {username} już istnieje.")
    finally:
        conn.close()

def delete_user(username):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    if user:
        c.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        print(f"Użytkownik {username} został usunięty z bazy danych.")
    else:
        print(f"Użytkownik {username} nie istnieje w bazie danych.")

    conn.close()

def get_user_data():
    username = input("Podaj nazwę użytkownika: ")
    login = input("Podaj login do Instatling: ")
    password = input("Podaj hasło do Instatling: ")
    return username, login, password

def main():
    create_db()
    
    while True:
        print("\nMenu:")
        print("1. Dodaj nowego użytkownika")
        print("2. Usuń użytkownika")
        print("3. Wyjdź")
        
        choice = input("Wybierz opcję (1/2/3): ")
        
        if choice == '1':
            username, login, password = get_user_data()
            register_user(username, login, password)
        
        elif choice == '2':
            username = input("Podaj nazwę użytkownika do usunięcia: ")
            delete_user(username)
        
        elif choice == '3':
            print("Zamykanie programu.")
            break
        
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main()