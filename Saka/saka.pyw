import cv2
import numpy as np
from pynput import mouse
import threading
import tkinter as tk
from tkinter import messagebox
import pygame
import ctypes 
import time
import random


try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# --- AYARLAR ---
CAT_WIDTH, CAT_HEIGHT = 220, 160
LOWER_GREEN = np.array([35, 40, 40])
UPPER_GREEN = np.array([85, 255, 255])

# Ses sistemini başlat
pygame.mixer.init()
pygame.mixer.set_num_channels(64)

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

HUH_SOUND = load_sound("huh.wav")
DING_SOUND = load_sound("ding.wav")


frames = {"huh": None, "maxwell": None}

def video_worker(name, path):
    global frames
    cap = cv2.VideoCapture(path)
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        frame = cv2.resize(frame, (CAT_WIDTH, CAT_HEIGHT))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
        frame[mask != 0] = [0, 0, 0]
        frames[name] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        time.sleep(0.03)

# Videoları arka planda başlat
threading.Thread(target=video_worker, args=("huh", "huh_cat.mp4"), daemon=True).start()
threading.Thread(target=video_worker, args=("maxwell", "maxwell.mp4"), daemon=True).start()

# --- POPUP DÖNGÜSÜ ---
def popup_loop():
    while True:
        time.sleep(10)
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        messagebox.showinfo("Kedi Konseyi", random.choice([
            "Meow Meow Meow!!!",
            "Bilgisayarınız öKMEK Üzere!!!",
            "Mouse'un sağ tarafı Maxwell'e aittir!",
            "Bilgisayarınız öKMEK Üzere!!!"
        ]))
        root.destroy()

threading.Thread(target=popup_loop, daemon=True).start()

class CatOverlay:
    def __init__(self, x, y, type="huh"):
        self.x, self.y = int(x - (CAT_WIDTH / 2)), int(y - (CAT_HEIGHT / 2))
        self.type = type
        
        # Doğru sesi çal
        sound = HUH_SOUND if type == "huh" else DING_SOUND
        if sound: sound.play()
            
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes("-transparentcolor", "black")
        self.root.geometry(f"{CAT_WIDTH}x{CAT_HEIGHT}+{self.x}+{self.y}")

        self.label = tk.Label(self.root, bg='black')
        self.label.pack(fill=tk.BOTH, expand=tk.YES)

        self.start_time = time.time()
        self.update()
        self.root.mainloop()

    def update(self):
        # Kediler 1.5 saniye ekranda kalsın
        if time.time() - self.start_time > 1.5:
            self.root.destroy()
            return

        current_f = frames[self.type]
        if current_f is not None:
            img = tk.PhotoImage(data=cv2.imencode('.png', current_f)[1].tobytes())
            self.label.config(image=img)
            self.label.image = img
            
        self.root.after(30, self.update)

def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            threading.Thread(target=CatOverlay, args=(x, y, "huh"), daemon=True).start()
        elif button == mouse.Button.right:
            threading.Thread(target=CatOverlay, args=(x, y, "maxwell"), daemon=True).start()

if __name__ == "__main__":
    print("--- 😼 HUH & MAXWELL KEDİ ORDUSU BAŞLATILDI ---")
    print("Sol tık: Huh Cat | Sağ tık: Maxwell Cat")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()