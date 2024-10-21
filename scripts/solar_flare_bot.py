import requests
import time

# URL do webhooka Discord
WEBHOOK_URL = 'https://discord.com/api/webhooks/1297959006446293055/K_9MdkpBJ0j2Yaw_FwkG-5l2dW4Qg50-92zfjZvfpGtWYS04rnQydkQ2IjkNExwRr40J'  # Wstaw tutaj URL webhooka Discord

# URL pliku JSON z danymi o rozbłyskach
url = 'https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json'

# Funkcja pobierająca najnowsze dane o rozbłyskach
def check_solar_flare():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            latest_flare = data[0]  # Zakładamy, że najnowszy rozbłysk jest na pierwszym miejscu
            return latest_flare
    return None

# Funkcja wysyłająca wiadomość do Discord przez webhook
def send_to_discord(message):
    data = {
        "content": message
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Wiadomość wysłana pomyślnie!")
    else:
        print(f"Błąd przy wysyłaniu wiadomości: {response.status_code}")

# Główna pętla sprawdzająca dane co pewien czas
last_flare_time = None

while True:
    flare = check_solar_flare()
    if flare:
        flare_time = flare['time_tag']
        
        if last_flare_time != flare_time:
            last_flare_time = flare_time
            # Wyodrębnij dane rozbłysku
            begin_time = flare['begin_time']
            max_time = flare['max_time']
            end_time = flare['end_time']
            begin_class = flare['begin_class']
            max_class = flare['max_class']
            end_class = flare['end_class']
            current_class = flare['current_class']
            
            # Wiadomość do wysłania na Discord
            message = (
                f"# Nowy rozbłysk słoneczny!\n"
                f"- Czas rozpoczęcia: {begin_time}\n"
                f"- Maksymalna moc: {max_class} o {max_time}\n"
                f"- Czas zakończenia: {end_time}\n"
                f"- Klasa na zakończenie: {end_class}\n"
                f"- Aktualna moc: {current_class}"
            )
            send_to_discord(message)
    
    # Sprawdzanie co godzinę
    time.sleep(60)
