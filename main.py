import requests
import time
from playsound import playsound

def get_alert_data():
    url = "https://ubilling.net.ua/aerialalerts/"
    response = requests.get(url)
    data = response.json()
    return data

def check_alert_status():
    data = get_alert_data()
    status = data['states']['Дніпропетровська область']
    return status

def play_alert_sound():
    playsound("alert.mp3", block=False)

def play_clear_sound():
    playsound("alert_clear.mp3", block=False)  # Воспроизведение файла при отмене тревоги

def main():
    alert_triggered = False
    while True:
        try:
            status = check_alert_status()
            if status['alertnow']:
                if not alert_triggered:
                    print(f"( {status['changed']} ) -  Тревога активна! Воспроизвожу звук...")
                    play_alert_sound()
                    alert_triggered = True
                else:
                    print(f"( {status['changed']} ) -  Тревога активна, звук уже воспроизведен.")
            else:
                if alert_triggered:
                    print(f"( {status['changed']} ) - 🟢 Тревога отменена! Воспроизвожу звук отмены...")
                    play_clear_sound()  # Воспроизведение звука отмены
                    alert_triggered = False
                else:
                    print(f"( {status['changed']} ) - 🟢 Тревоги нет.")
        except KeyError:
            print("Ошибка: данных по 'Дніпропетровська область' нет в ответе сервера.")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        time.sleep(5)

if __name__ == "__main__":
    main()