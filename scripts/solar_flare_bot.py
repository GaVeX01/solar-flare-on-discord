import requests

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
LAST_FLARE_TIME_FILE = 'scripts/last_flare_time.txt'

# Funkcja do odczytu ostatniego czasu rozbłysku
def read_last_flare_time():
    try:
        with open(LAST_FLARE_TIME_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# Funkcja do zapisywania ostatniego czasu rozbłysku
def save_last_flare_time(flare_time):
    with open(LAST_FLARE_TIME_FILE, 'w') as f:
        f.write(flare_time)

# Sprawdź ostatni czas rozbłysku
last_flare_time = read_last_flare_time()

flare = check_solar_flare()
if flare:
    flare_time = flare['time_tag']
    max_class = flare['max_class']

    # Warunek, aby nie wysyłać wiadomości, jeśli klasa to C
    if 'C' not in max_class:
        if last_flare_time != flare_time:
            last_flare_time = flare_time
            # Wyodrębnij dane rozbłysku
            begin_time = flare['begin_time']
            max_time = flare['max_time']
            end_time = flare['end_time']
            begin_class = flare['begin_class']
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
            save_last_flare_time(flare_time)  # Zapisz ostatni czas rozbłysku
    else:
        print(f"ostatni rozbłysk jakiś mierny to nie wysyłam")
        message = (
                f"# ten ostatni rozblysk to lipa jakas to nie wysylam (test)\n"
                
            )
            send_to_discord(message)
