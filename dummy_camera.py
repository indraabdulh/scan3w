import cv2
import numpy as np
import random
import os

class DummyCamera:
    """Simulasi webcam dengan gambar dummy"""
    def __init__(self, dummy_dir="assets/dummy_images"):
        self.dummy_dir = dummy_dir
        self.images = {}
        self.load_dummy_images()
        
    def load_dummy_images(self):
        """Load dummy image untuk masing-masing level"""
        levels = ["full", "medium", "low", "empty"]
        for level in levels:
            path = f"{self.dummy_dir}/polybox_{level}.jpg"
            if os.path.exists(path):
                img = cv2.imread(path)
                # Resize ke 640x480
                self.images[level] = cv2.resize(img, (640, 480))
            else:
                # Buat dummy image jika tidak ada file
                self.images[level] = self.create_dummy_image(level)
    
    def create_dummy_image(self, level):
        """Buat gambar sintetis polybox biru dengan isi baut simulasi"""
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        # Warna dasar polybox biru
        img[:, :] = (255, 100, 0)  # BGR blue
        
        # Simulasi baut (titik-titik gelap)
        fill_ratios = {
            "full": 0.9,
            "medium": 0.6,
            "low": 0.35,
            "empty": 0.05
        }
        
        ratio = fill_ratios[level]
        h, w = img.shape[:2]
        num_bolts = int(ratio * 1000)
        
        for _ in range(num_bolts):
            x = random.randint(50, w-50)
            y = random.randint(50, h-50)
            cv2.circle(img, (x, y), 5, (50, 50, 50), -1)
        
        return img
    
    def read(self):
        """Random pilih level untuk simulasi"""
        level = random.choice(["full", "medium", "low", "empty"])
        frame = self.images[level].copy()
        return True, frame