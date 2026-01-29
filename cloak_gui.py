"""
Invisibility Cloak with GUI - Enhanced User Experience
Features: Multi-language, Transparency Control, Real-time Settings
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from PIL import Image, ImageTk

# Translations
TRANSLATIONS = {
    'en': {
        'title': 'Invisibility Cloak Control Panel',
        'start': 'Start Cloak',
        'stop': 'Stop Cloak',
        'capture_bg': 'Capture Background',
        'color': 'Cloak Color:',
        'transparency': 'Transparency:',
        'blur': 'Edge Blur:',
        'camera': 'Camera Index:',
        'language': 'Language:',
        'status': 'Status: Ready',
        'capturing': 'Status: Capturing background...',
        'running': 'Status: Cloak Active',
        'stopped': 'Status: Stopped',
        'instructions': 'Instructions:\n1. Select color and settings\n2. Click "Capture Background"\n3. Stay out of frame for 3 seconds\n4. Click "Start Cloak"',
    },
    'es': {
        'title': 'Panel de Control de Capa Invisible',
        'start': 'Iniciar Capa',
        'stop': 'Detener Capa',
        'capture_bg': 'Capturar Fondo',
        'color': 'Color de Capa:',
        'transparency': 'Transparencia:',
        'blur': 'Desenfoque de Bordes:',
        'camera': 'Índice de Cámara:',
        'language': 'Idioma:',
        'status': 'Estado: Listo',
        'capturing': 'Estado: Capturando fondo...',
        'running': 'Estado: Capa Activa',
        'stopped': 'Estado: Detenido',
        'instructions': 'Instrucciones:\n1. Seleccione color y configuración\n2. Haga clic en "Capturar Fondo"\n3. Salga del cuadro por 3 segundos\n4. Haga clic en "Iniciar Capa"',
    },
    'hi': {
        'title': 'अदृश्यता क्लोक नियंत्रण पैनल',
        'start': 'क्लोक शुरू करें',
        'stop': 'क्लोक बंद करें',
        'capture_bg': 'पृष्ठभूमि कैप्चर करें',
        'color': 'क्लोक रंग:',
        'transparency': 'पारदर्शिता:',
        'blur': 'किनारा धुंधला:',
        'camera': 'कैमरा इंडेक्स:',
        'language': 'भाषा:',
        'status': 'स्थिति: तैयार',
        'capturing': 'स्थिति: पृष्ठभूमि कैप्चर कर रहा है...',
        'running': 'स्थिति: क्लोक सक्रिय',
        'stopped': 'स्थिति: बंद',
        'instructions': 'निर्देश:\n1. रंग और सेटिंग्स चुनें\n2. "पृष्ठभूमि कैप्चर करें" क्लिक करें\n3. 3 सेकंड के लिए फ्रेम से बाहर रहें\n4. "क्लोक शुरू करें" क्लिक करें',
    },
    'fr': {
        'title': 'Panneau de Contrôle de Cape d\'Invisibilité',
        'start': 'Démarrer la Cape',
        'stop': 'Arrêter la Cape',
        'capture_bg': 'Capturer l\'Arrière-plan',
        'color': 'Couleur de la Cape:',
        'transparency': 'Transparence:',
        'blur': 'Flou des Bords:',
        'camera': 'Index de Caméra:',
        'language': 'Langue:',
        'status': 'Statut: Prêt',
        'capturing': 'Statut: Capture de l\'arrière-plan...',
        'running': 'Statut: Cape Active',
        'stopped': 'Statut: Arrêté',
        'instructions': 'Instructions:\n1. Sélectionnez la couleur et les paramètres\n2. Cliquez sur "Capturer l\'Arrière-plan"\n3. Sortez du cadre pendant 3 secondes\n4. Cliquez sur "Démarrer la Cape"',
    }
}

COLOR_RANGES = {
    'red': [(np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))],
    'blue': [(np.array([94, 80, 2]), np.array([126, 255, 255]))],
    'green': [(np.array([40, 40, 40]), np.array([80, 255, 255]))],
    'yellow': [(np.array([20, 100, 100]), np.array([30, 255, 255]))],
}

class InvisibilityCloakGUI:
    def __init__(self, root):
        self.root = root
        self.lang = 'en'
        self.root.title(TRANSLATIONS[self.lang]['title'])
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Variables
        self.cap = None
        self.background = None
        self.is_running = False
        self.selected_color = tk.StringVar(value='red')
        self.transparency = tk.DoubleVar(value=1.0)
        self.blur_amount = tk.IntVar(value=5)
        self.camera_index = tk.IntVar(value=0)
        self.language = tk.StringVar(value='en')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="⚙️ Settings", padding="10")
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S))
        
        # Language selector
        ttk.Label(control_frame, text=TRANSLATIONS[self.lang]['language']).grid(row=0, column=0, sticky=tk.W, pady=5)
        lang_combo = ttk.Combobox(control_frame, textvariable=self.language, 
                                  values=['en', 'es', 'hi', 'fr'], state='readonly', width=15)
        lang_combo.grid(row=0, column=1, pady=5)
        lang_combo.bind('<<ComboboxSelected>>', self.change_language)
        
        # Camera index
        ttk.Label(control_frame, text=TRANSLATIONS[self.lang]['camera']).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(control_frame, from_=0, to=5, textvariable=self.camera_index, width=15).grid(row=1, column=1, pady=5)
        
        # Color selection
        ttk.Label(control_frame, text=TRANSLATIONS[self.lang]['color']).grid(row=2, column=0, sticky=tk.W, pady=5)
        color_combo = ttk.Combobox(control_frame, textvariable=self.selected_color, 
                                   values=['red', 'blue', 'green', 'yellow'], state='readonly', width=15)
        color_combo.grid(row=2, column=1, pady=5)
        
        # Transparency slider
        ttk.Label(control_frame, text=TRANSLATIONS[self.lang]['transparency']).grid(row=3, column=0, sticky=tk.W, pady=5)
        transparency_scale = ttk.Scale(control_frame, from_=0.0, to=1.0, variable=self.transparency, 
                                       orient=tk.HORIZONTAL, length=150)
        transparency_scale.grid(row=3, column=1, pady=5)
        self.transparency_label = ttk.Label(control_frame, text="100%")
        self.transparency_label.grid(row=3, column=2, pady=5)
        transparency_scale.configure(command=self.update_transparency_label)
        
        # Blur slider
        ttk.Label(control_frame, text=TRANSLATIONS[self.lang]['blur']).grid(row=4, column=0, sticky=tk.W, pady=5)
        blur_scale = ttk.Scale(control_frame, from_=1, to=15, variable=self.blur_amount, 
                              orient=tk.HORIZONTAL, length=150)
        blur_scale.grid(row=4, column=1, pady=5)
        self.blur_label = ttk.Label(control_frame, text="5")
        self.blur_label.grid(row=4, column=2, pady=5)
        blur_scale.configure(command=self.update_blur_label)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        self.capture_btn = ttk.Button(button_frame, text=TRANSLATIONS[self.lang]['capture_bg'], 
                                      command=self.capture_background, width=20)
        self.capture_btn.grid(row=0, column=0, pady=5)
        
        self.start_btn = ttk.Button(button_frame, text=TRANSLATIONS[self.lang]['start'], 
                                    command=self.start_cloak, width=20)
        self.start_btn.grid(row=1, column=0, pady=5)
        
        self.stop_btn = ttk.Button(button_frame, text=TRANSLATIONS[self.lang]['stop'], 
                                   command=self.stop_cloak, width=20, state='disabled')
        self.stop_btn.grid(row=2, column=0, pady=5)
        
        # Instructions
        instr_frame = ttk.LabelFrame(control_frame, text="📖 Guide", padding="10")
        instr_frame.grid(row=6, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        self.instructions_text = tk.Text(instr_frame, height=8, width=35, wrap=tk.WORD, 
                                        bg='#f0f0f0', font=('Arial', 9))
        self.instructions_text.insert('1.0', TRANSLATIONS[self.lang]['instructions'])
        self.instructions_text.config(state='disabled')
        self.instructions_text.pack()
        
        # Right panel - Video preview
        video_frame = ttk.LabelFrame(main_frame, text="📹 Live Preview", padding="10")
        video_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        self.video_label = ttk.Label(video_frame)
        self.video_label.pack()
        
        # Status bar
        self.status_var = tk.StringVar(value=TRANSLATIONS[self.lang]['status'])
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
    def change_language(self, event=None):
        self.lang = self.language.get()
        self.root.title(TRANSLATIONS[self.lang]['title'])
        self.capture_btn.config(text=TRANSLATIONS[self.lang]['capture_bg'])
        self.start_btn.config(text=TRANSLATIONS[self.lang]['start'])
        self.stop_btn.config(text=TRANSLATIONS[self.lang]['stop'])
        self.status_var.set(TRANSLATIONS[self.lang]['status'])
        
        self.instructions_text.config(state='normal')
        self.instructions_text.delete('1.0', tk.END)
        self.instructions_text.insert('1.0', TRANSLATIONS[self.lang]['instructions'])
        self.instructions_text.config(state='disabled')
        
    def update_transparency_label(self, value):
        self.transparency_label.config(text=f"{int(float(value) * 100)}%")
        
    def update_blur_label(self, value):
        self.blur_label.config(text=str(int(float(value))))
        
    def capture_background(self):
        self.status_var.set(TRANSLATIONS[self.lang]['capturing'])
        threading.Thread(target=self._capture_background_thread, daemon=True).start()
        
    def _capture_background_thread(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(self.camera_index.get())
            
        time.sleep(1)
        for i in range(30):
            ret, self.background = self.cap.read()
        self.background = cv2.flip(self.background, 1)
        
        self.status_var.set(TRANSLATIONS[self.lang]['status'] + " - Background captured!")
        
    def start_cloak(self):
        if self.background is None:
            messagebox.showwarning("Warning", "Please capture background first!")
            return
            
        self.is_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_var.set(TRANSLATIONS[self.lang]['running'])
        threading.Thread(target=self._process_video, daemon=True).start()
        
    def stop_cloak(self):
        self.is_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_var.set(TRANSLATIONS[self.lang]['stopped'])
        
    def _process_video(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create mask
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            for lower, upper in COLOR_RANGES[self.selected_color.get()]:
                mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
            
            # Noise removal
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.dilate(mask, kernel, iterations=2)
            
            # Apply blur to edges
            blur_val = self.blur_amount.get()
            if blur_val > 1:
                mask = cv2.GaussianBlur(mask, (blur_val, blur_val), 0)
            
            mask_inv = cv2.bitwise_not(mask)
            
            # Cloak effect with transparency
            res1 = cv2.bitwise_and(self.background, self.background, mask=mask)
            res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
            
            alpha = self.transparency.get()
            final_output = cv2.addWeighted(res1, alpha, res2, 1, 0)
            
            # Convert for tkinter display
            cv2image = cv2.cvtColor(final_output, cv2.COLOR_BGR2RGB)
            cv2image = cv2.resize(cv2image, (480, 360))
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            
        if self.cap:
            self.cap.release()
            
    def on_closing(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvisibilityCloakGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
