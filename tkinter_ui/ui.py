import tkinter as tk
from tkinter import font

class HospitalUI:
    def __init__(self, root, start_cb, num_beds, num_docs):
        self.root = root
        self.root.title("🏥 Hospital Simulation")
        self.root.geometry("1100x500")
        self.root.configure(bg="#f0f4f8")

        self.status_var = tk.StringVar(value="Not started")

        # Custom font
        self.title_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.patient_font = font.Font(family="Consolas", size=10)

        # Top panel
        top = tk.Frame(root, bg="#f0f4f8")
        top.pack(pady=10)

        tk.Label(top, text=f"🛏 Beds: {num_beds}    👨‍⚕️ Doctors: {num_docs}",
                 font=self.title_font, bg="#f0f4f8").pack(side="left", padx=10)

        tk.Button(top, text="▶ Start", bg="#28a745", fg="white",
                  font=self.title_font, command=start_cb).pack(side="left", padx=10)

        tk.Label(top, textvariable=self.status_var, font=self.title_font,
                 bg="#f0f4f8", fg="black").pack(side="left", padx=20)

        # Column layout
        self.columns = {
            "waiting_bed": self._create_column("🕐 Waiting for Bed", "#ffffff"),
            "waiting_doctor": self._create_column("🧑‍⚕️ Waiting for Doctor", "#e6f7ff"),
            "in_treatment": self._create_column("💉 In Treatment", "#fff7e6"),
            "discharged": self._create_column("✅ Discharged", "#e6ffe6"),
            "referred": self._create_column("🚑 Referred to Another Hospital", "#ffe6e6"),
        }

    def _create_column(self, title, bg_color):
        frame = tk.LabelFrame(self.root, text=title, bg="#f9f9f9", font=self.title_font,
                              fg="#333", labelanchor="n", padx=5, pady=5)
        frame.pack(side="left", padx=7, pady=10, fill="y")

        listbox = tk.Listbox(frame, width=25, height=20, font=self.patient_font,
                             bg=bg_color, borderwidth=2, relief="groove")
        listbox.pack(padx=5, pady=5)
        return listbox

    def set_status(self, text):
        self.status_var.set(f"Status: {text}")

    def log_state(self, state, patient):
        # Remove patient from all other lists
        for lst in self.columns.values():
            items = list(lst.get(0, "end"))
            display = str(patient)
            if display in items:
                lst.delete(items.index(display))

        # Add to relevant column
        if state in self.columns:
            self.columns[state].insert("end", str(patient))
