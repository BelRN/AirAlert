import flet as ft
import requests
import time
import sounddevice as sd
import soundfile as sf
from threading import Thread

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
    data, samplerate = sf.read("alert.mp3")
    sd.play(data, samplerate)
    time.sleep(len(data) / samplerate)
    sd.stop()

def play_clear_sound():
    data, samplerate = sf.read("alert_clear.mp3")
    sd.play(data, samplerate)
    time.sleep(len(data) / samplerate)
    sd.stop()

def main(page: ft.Page):
    page.title = "Статус повітряної тривоги"
    status_text = ft.Text("Очікування даних...", size=20)
    page.add(status_text)

    alert_triggered = False

    def update_status():
        nonlocal alert_triggered
        try:
            status = check_alert_status()
            if status['alertnow']:
                if not alert_triggered:
                    status_text.value = f"( {status['changed']} ) - Тривога активна!"
                    status_text.Color = ft.Colors.RED
                    Thread(target=play_alert_sound).start()
                    alert_triggered = True
                else:
                    status_text.value = f"( {status['changed']} ) - Тривога активна, звук вже відтворено."
                    status_text.Color = ft.Colors.RED
            else:
                if alert_triggered:
                    status_text.value = f"( {status['changed']} ) - Тривога скасована!"
                    status_text.Color = ft.Colors.GREEN
                    Thread(target=play_clear_sound).start()
                    alert_triggered = False
                else:
                    status_text.value = f"( {status['changed']} ) - Тривоги немає."
                    status_text.Color = ft.Colors.GREEN
        except KeyError:
            status_text.value = "Ошибка: данных по 'Дніпропетровська область' нет в ответе сервера."
            status_text.Color = ft.Colors.ORANGE
        except requests.exceptions.RequestException as e:
            status_text.value = f"Ошибка запроса: {e}"
            status_text.Color = ft.Colors.ORANGE
        except Exception as e:
            status_text.value = f"Произошла ошибка: {e}"
            status_text.Color = ft.Colors.ORANGE
        page.update()

    def create_timer():
        page.timer = ft.Timer(5, update_status)
        page.timer.repeat = True  # repeat the timer.
        page.timer.start()

    create_timer()

ft.app(target=main)