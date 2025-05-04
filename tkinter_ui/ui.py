import tkinter as tk

class HospitalUI:
    def __init__(self, root, start_cb, num_beds, num_docs):
        self.root = root
        self.root.title("Hospital Simulation")
        self.status_var = tk.StringVar(value="Not started")

        top = tk.Frame(root)
        top.pack(pady=5)
        tk.Label(top, text=f"Beds: {num_beds}  Doctors: {num_docs}").pack(side="left", padx=5)
        tk.Button(top, text="▶ Start", bg="green", fg="white", command=start_cb).pack(side="left")
        tk.Label(top, textvariable=self.status_var).pack(side="left", padx=10)

        self.columns = {
            "waiting_bed": self._create_column("Waiting for Bed"),
            "waiting_doctor": self._create_column("Waiting for Doctor"),
            "in_treatment": self._create_column("In Treatment"),
            "discharged": self._create_column("Discharged"),
        }

    def _create_column(self, title):
        frame = tk.LabelFrame(self.root, text=title)
        frame.pack(side="left", padx=5, pady=10, fill="y")
        listbox = tk.Listbox(frame, width=25, height=20)
        listbox.pack(padx=5, pady=5)
        return listbox

    def set_status(self, text):
        self.status_var.set(f"Status: {text}")

    def log_state(self, state, patient):
        for lst in self.columns.values():
            items = list(lst.get(0, "end"))
            display = str(patient)
            if display in items:
                lst.delete(items.index(display))

        if state in self.columns:
            self.columns[state].insert("end", str(patient))
