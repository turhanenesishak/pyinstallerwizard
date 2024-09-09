import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import subprocess

# Ana pencereyi oluştur
root = tk.Tk()
root.title("PyInstaller Wizard")
root.geometry("500x400")

# Global değişkenler
selected_folder = ""
py_files = []
current_step = 1

# Adımların gösterildiği kısım
step_frame = tk.Frame(root)
step_frame.pack(pady=20)

# Adım başlığı
step_label = tk.Label(step_frame, text="Step 1: Select the project folder", font=("Arial", 14))
step_label.pack()

# Klasör ve dosya seçimi için alanlar
folder_label = tk.Label(step_frame, text="No folder selected", wraplength=400)
folder_label.pack(pady=10)

file_combobox = ttk.Combobox(step_frame, state="disabled")

# Butonlar çerçevesi (Back, Next, Cancel)
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=20)

# Adım değiştirme fonksiyonu
def update_step(step):
    global current_step
    current_step = step
    
    if current_step == 1:
        step_label.config(text="Step 1: Select the project folder")
        file_combobox.pack_forget()  # ComboBox gizlenir
        folder_label.pack(pady=10)   # Klasör label'ı tekrar görünür
        next_button.config(text="Next")
        back_button.config(state="disabled")  # İlk adımda Back butonu devre dışı
    elif current_step == 2:
        step_label.config(text="Step 2: Select a .py file")
        folder_label.pack_forget()    # Klasör label'ı gizlenir
        file_combobox.pack(pady=10)   # ComboBox görünür olur
        next_button.config(text="Create EXE")
        back_button.config(state="normal")
    else:
        pass

# Klasör seçme fonksiyonu
def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    
    if selected_folder:
        folder_label.config(text=f"Selected Folder: {selected_folder}")
        load_py_files(selected_folder)

# Klasördeki .py dosyalarını ComboBox'a yükle
def load_py_files(folder):
    global py_files
    py_files = [f for f in os.listdir(folder) if f.endswith(".py")]
    
    if py_files:
        file_combobox['values'] = py_files
        file_combobox.current(0)
        file_combobox.config(state="readonly")
        next_button.config(state="normal")
    else:
        messagebox.showwarning("Warning", "No .py files found in the selected folder.")
        next_button.config(state="disabled")

# PyInstaller'ı çalıştıran fonksiyon
def create_exe():
    if not selected_folder or not py_files:
        messagebox.showerror("Error", "Please select a valid folder and .py file.")
        return
    
    selected_py_file = file_combobox.get()
    py_file_path = os.path.join(selected_folder, selected_py_file)
    
    if not os.path.isfile(py_file_path):
        messagebox.showerror("Error", f"{selected_py_file} is not a valid file.")
        return

    # PyInstaller komutu
    try:
        result = subprocess.run(
            ["pyinstaller", "--onefile", py_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.returncode == 0:
            messagebox.showinfo("Success", f"{selected_py_file} has been converted to an executable.")
        else:
            messagebox.showerror("Error", f"Failed to create executable:\n{result.stderr.decode()}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Next butonuna tıklandığında
def next_step():
    if current_step == 1:
        if not selected_folder:
            messagebox.showwarning("Warning", "Please select a folder first.")
        else:
            update_step(2)
    elif current_step == 2:
        create_exe()

# Back butonuna tıklandığında
def back_step():
    if current_step == 2:
        update_step(1)

# Cancel butonuna tıklandığında
def cancel_wizard():
    root.quit()

# Arayüz elemanları
folder_button = tk.Button(step_frame, text="Select Folder", command=select_folder)
folder_button.pack(pady=10)

# Butonlar
back_button = tk.Button(button_frame, text="Back", command=back_step, state="disabled")
back_button.pack(side=tk.LEFT, padx=10)

next_button = tk.Button(button_frame, text="Next", command=next_step)
next_button.pack(side=tk.LEFT, padx=10)

cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_wizard)
cancel_button.pack(side=tk.LEFT, padx=10)

# Tkinter döngüsü
root.mainloop()

#Created by @turhanenesishak, this program is protected by the ApacheLicense2.0 License. 