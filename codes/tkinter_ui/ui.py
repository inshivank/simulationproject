import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

class HospitalERApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital ER System")
        self.center_window()
        self.setup_ui()

    def center_window(self):
        w, h = 400, 300
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def setup_ui(self):
        self.patient_label = tk.Label(self.root, text="Patient Details", font=("Arial", 16))
        self.patient_label.pack(pady=10)

        self.patient_name_label = tk.Label(self.root, text="Name:", font=("Arial", 12))
        self.patient_name_label.pack(pady=5)

        self.patient_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.patient_name_entry.pack(pady=5)

        self.patient_condition_label = tk.Label(self.root, text="Condition:", font=("Arial", 12))
        self.patient_condition_label.pack(pady=5)

        self.condition_var = tk.StringVar(value="Stable")
        self.condition_menu = tk.OptionMenu(self.root, self.condition_var, "Stable", "Critical", "Emergency")
        self.condition_menu.config(font=("Arial", 12))
        self.condition_menu.pack(pady=5)

        self.enter_button = tk.Button(self.root, text="Enter Patient", font=("Arial", 14), command=self.enter_patient)
        self.enter_button.pack(pady=20)

        self.patients_display = tk.Listbox(self.root, width=40, height=6, font=("Arial", 12))
        self.patients_display.pack(pady=5)

    def enter_patient(self):
        name = self.patient_name_entry.get()
        condition = self.condition_var.get()
        if not name:
            messagebox.showerror("Input Error", "Please enter a patient name.")
            return

        self.patient_name_entry.delete(0, tk.END)
        info = f"{name} - {condition}"
        self.patients_display.insert(tk.END, info)

        if condition == "Critical":
            self.change_ui_for_critical()
        else:
            self.reset_ui()

        threading.Thread(target=self.simulate_discharge, args=(name, condition)).start()

    def simulate_discharge(self, name, condition):
        time.sleep(random.randint(3, 5))
        self.patients_display.delete(0)
        self.patients_display.insert(tk.END, f"{name} - {condition} - Discharged")
        if condition == "Critical":
            self.reset_ui()

    def change_ui_for_critical(self):
        self.root.config(bg="red")
        self.enter_button.config(bg="yellow", fg="red")
        self.patients_display.config(bg="yellow", fg="red")
        self.patient_label.config(fg="white")

    def reset_ui(self):
        self.root.config(bg="white")
        self.enter_button.config(bg="blue", fg="white")
        self.patients_display.config(bg="white", fg="black")
        self.patient_label.config(fg="black")

def run_ui():
    root = tk.Tk()
    app = HospitalERApp(root)
    root.mainloop()
