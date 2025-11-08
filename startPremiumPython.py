import subprocess
import time
from datetime import datetime

def wait_until_18():
    while True:
        now = datetime.now()
        if now.hour == 18 and now.minute == 0:
            break
        time.sleep(30)

def run_script():
    subprocess.run(['python3', 'botPremium.py'])

if __name__ == "__main__":
    while True:
        print("Czekam do godziny 18:00...")
        wait_until_18()
        print("Uruchamiam skrypt!")
        run_script()
        time.sleep(60)
