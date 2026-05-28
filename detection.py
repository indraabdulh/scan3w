import cv2
import numpy as np
import config

class FastenerDetector:
    def __init__(self):
        self.blue_lower = np.array(config.BLUE_LOWER)
        self.blue_upper = np.array(config.BLUE_UPPER)
    
    def detect_polybox(self, frame):
        """Deteksi polybox biru dan return mask serta contour"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_blue = cv2.inRange(hsv, self.blue_lower, self.blue_upper)
        
        # Noise removal
        kernel = np.ones((5,5), np.uint8)
        mask_clean = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)
        mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Ambil contour terbesar (polybox utama)
            polybox_contour = max(contours, key=cv2.contourArea)
            return mask_clean, polybox_contour
        return None, None
    
    def calculate_fill_ratio(self, frame, polybox_mask):
        """Hitung persentase area yang terisi baut dalam polybox"""
        if polybox_mask is None:
            return 0.0
        
        # ROI area polybox
        masked_frame = cv2.bitwise_and(frame, frame, mask=polybox_mask)
        gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
        
        # Threshold untuk deteksi baut (area gelap)
        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        
        # Hitung area baut
        bolt_area = cv2.countNonZero(thresh)
        total_area = cv2.countNonZero(polybox_mask)
        
        if total_area == 0:
            return 0.0
        
        fill_ratio = (bolt_area / total_area) * 100
        # Clip ke 0-100
        return min(max(fill_ratio, 0.0), 100.0)
    
    def classify_level(self, fill_ratio):
        """Klasifikasi level berdasarkan fill ratio"""
        for level, config_level in config.LEVEL_CONFIG.items():
            if config_level["min"] <= fill_ratio <= config_level["max"]:
                return level
        return "EMPTY"
    
    def process_frame(self, frame):
        """Pipeline utama deteksi"""
        # Deteksi polybox
        polybox_mask, contour = self.detect_polybox(frame)
        
        if polybox_mask is None:
            return 0.0, "EMPTY", None, None
        
        # Hitung fill ratio
        fill_ratio = self.calculate_fill_ratio(frame, polybox_mask)
        level = self.classify_level(fill_ratio)
        
        # Visualisasi
        vis_frame = frame.copy()
        cv2.drawContours(vis_frame, [contour], -1, (0, 255, 0), 2)
        
        # Tampilkan persentase
        h, w, _ = vis_frame.shape
        cv2.putText(vis_frame, f"Fill: {fill_ratio:.1f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return fill_ratio, level, vis_frame, polybox_mask