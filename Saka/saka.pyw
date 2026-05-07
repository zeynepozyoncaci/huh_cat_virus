import cv2
import numpy as np
from pynput import mouse
import threading
import tkinter as tk
import pygame
import ctypes 
import time

# Ölçeklendirme düzeltmesi
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# --- AYARLAR ---
VIDEO_PATH = "huh_cat.mp4"
SOUND_PATH = "huh.wav"
CAT_WIDTH = 220
CAT_HEIGHT = 160
LOWER_GREEN = np.array([35, 40, 40])
UPPER_GREEN = np.array([85, 255, 255])

# Ses sistemini başlat
pygame.mixer.init()
pygame.mixer.set_num_channels(64) # Daha fazla kanal!
try:
    huh_sound = pygame.mixer.Sound(SOUND_PATH)
except:
    huh_sound = None

# --- KÜRESEL VİDEO YÖNETİCİSİ ---
# Videoyu sürekli okuyan bir mekanizma kuruyoruz
current_frame = None

def video_stream_worker():
    global current_frame
    cap = cv2.VideoCapture(VIDEO_PATH)
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Video biterse başa sar
            continue
        
        # Kareyi önceden hazırla (Boyutlandır ve Yeşil ekranı temizle)
        frame = cv2.resize(frame, (CAT_WIDTH, CAT_HEIGHT))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
        frame[mask != 0] = [0, 0, 0]
        current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        time.sleep(0.03) # Yaklaşık 30 FPS

# Videoyu arka planda başlat
threading.Thread(target=video_stream_worker, daemon=True).start()

class CatOverlay:
    def __init__(self, x, y):
        self.x = int(x - (CAT_WIDTH / 2))
        self.y = int(y - (CAT_HEIGHT / 2))
        
        if huh_sound:
            huh_sound.play()
            
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
        # Eğer 1.5 saniye geçtiyse (videonun süresi kadar) kediyi yok et
        if time.time() - self.start_time > 1.5:
            self.root.destroy()
            return

        if current_frame is not None:
            img = tk.PhotoImage(data=cv2.imencode('.png', current_frame)[1].tobytes())
            self.label.config(image=img)
            self.label.image = img
            
        self.root.after(30, self.update)

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        # Her tıklamada bağımsız kedi pencereleri aç
        threading.Thread(target=CatOverlay, args=(x, y), daemon=True).start()

if __name__ == "__main__":
    print("--- 😼 HUH CAT: SERİ VE SENKRONİZE SÜRÜM ---")
    print("Masaüstüne tıkla, kediler seri şekilde aksın!")
    
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()