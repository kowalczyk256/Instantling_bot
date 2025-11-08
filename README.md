<p align="center">
  <img src="./logo.png" alt="Logo Projektu" width="150">
</p>

<h1 align="center">Instantling Bot</h1>

<p align="center">
  <strong><a href="#-english">English</a></strong> | <strong><a href="#-polski">Polski</a></strong>
</p>

---

<a name="-english"></a>

### 💡 About The Project

A server-based version of **Instantling**, created by [@Szami993](https://github.com/Szami993) and [@kowalczyk256](https://github.com/kowalczyk256).  
This edition runs as a **Discord bot** that automates the process of completing Instaling sessions for registered users — both manually and automatically for premium users.

The goal was to create a reliable automation tool that can run continuously on a server (e.g., Debian or Ubuntu), managing both regular and premium users' daily learning sessions.
This version originates from the <a href ="https://github.com/kowalczyk256/Instantling_desktop">desktop</a> edition — it was developed in 2024.

### ⚙️ Files Overview

| File | Description |
|------|--------------|
| `.env` | Enter your Discord bot token here. |
| `startPremiumPython.py` | Launches the automatic session process every day at 18:00. |
| `botPremium.py` | Starts automatic sessions for users listed in the premium database. |
| `instantling.py` | Core logic of the automation script — handles interaction with Instaling. |
| `main.py` | Main Discord bot script — handles commands and manual sessions. |
| `register.py` | Script for registering new bot users. |
| `registerPremium.py` | Script for adding users to automatic (premium) recurring sessions. |

### 🚀 Installation & Setup

#### 1. Requirements

Make sure you have the following installed:

- Python 3.x  
- Required libraries: `discord.py`, `requests`, `sqlite3`, `datetime`, `os`, `threading`, `selenium`  
- A server environment (Debian recommended)  

#### 2. Installation

Clone the repository:

```bash
git clone https://github.com/kowalczyk256/instantling_bot.git
cd instantling_bot
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and insert your Discord bot token:

```env
DISCORD_TOKEN=your_discord_token_here
```

#### 3. Running the Bot

Start the main bot manually:

```bash
python main.py
```

To start automatic sessions (premium users) at 18:00 every day, you can either use `cron` or run:

```bash
python startPremiumPython.py
```

You can also manually trigger automatic sessions:

```bash
python botPremium.py
```
### 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create.  
Any contributions you make are greatly appreciated!

1. Fork the Project  
2. Create your Feature Branch  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your Changes  
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the Branch  
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request  

---

<a name="-polski"></a>

### 💡 O Projekcie

Serwerowa wersja **Instantling**, stworzona przez [@Szami993](https://github.com/Szami993) i [@kowalczyk256](https://github.com/kowalczyk256).  
Ta wersja działa jako **bot Discord**, który automatyzuje proces wykonywania sesji Instaling dla zarejestrowanych użytkowników — zarówno ręcznie, jak i automatycznie (dla użytkowników premium).

Celem było stworzenie stabilnego narzędzia działającego 24/7 na serwerze (np. Debian lub Ubuntu), które samo wykonuje sesje w określonym czasie.
Ta wersja wywodzi się z wersji <a href ="https://github.com/kowalczyk256/Instantling_desktop">desktopowej</a> - powstała w 2024.

### ⚙️ Opis Plików

| Plik | Opis |
|------|------|
| `.env` | Wpisz tu swój token Discord. |
| `startPremiumPython.py` | Uruchamia proces automatycznych sesji codziennie o 18:00. |
| `botPremium.py` | Rozpoczyna sesje automatyczne dla użytkowników wpisanych do bazy premium. |
| `instantling.py` | Logika skryptu automatyzacji — komunikacja z Instaling. |
| `main.py` | Główny plik bota Discord, obsługuje komendy i uruchamianie sesji ręcznych. |
| `register.py` | Skrypt dodający użytkowników bota. |
| `registerPremium.py` | Skrypt dodający użytkowników do sesji cyklicznych (automatycznych). |

### 🚀 Instalacja i Uruchomienie

#### 1. Wymagania

Upewnij się, że masz zainstalowane:

- Python 3.x  
- Biblioteki: `discord.py`, `requests`, `sqlite3`, `datetime`, `os`, `threading`, `selenium` 
- System serwerowy (np. Debian)  

#### 2. Instalacja

Sklonuj repozytorium:

```bash
git clone https://github.com/kowalczyk256/instantling_bot.git
cd instantling_bot
```

Zainstaluj wymagane biblioteki:

```bash
pip install -r requirements.txt
```

Utwórz plik `.env` i wpisz swój token Discorda:

```env
DISCORD_TOKEN=twój_token_tutaj
```

#### 3. Uruchomienie

Aby uruchomić głównego bota:

```bash
python main.py
```

Aby uruchomić sesje automatyczne o 18:00:

```bash
python startPremiumPython.py
```

Aby ręcznie rozpocząć sesje premium:

```bash
python botPremium.py
```

### 🤝 Wkład (Contributing)

Wkład w rozwój projektu jest mile widziany! Jeśli masz pomysł na ulepszenie:

1. Zrób Fork projektu  
2. Stwórz nową gałąź  
   ```bash
   git checkout -b funkcja/niesamowita-funkcja
   ```
3. Zatwierdź zmiany  
   ```bash
   git commit -m 'Dodaj niesamowitą funkcję'
   ```
4. Wypchnij zmiany  
   ```bash
   git push origin funkcja/niesamowita-funkcja
   ```
5. Otwórz Pull Request  

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Szami993">@Szami993</a> & <a href="https://github.com/kowalczyk256">@kowalczyk256</a>
</p>
