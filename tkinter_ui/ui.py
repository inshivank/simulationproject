import tkinter as tk

class HospitalUI:
    def __init__(self, root, start_cb, num_beds, num_docs):
        self.root = root
        self.root.title("Hospital Simulation")

        # Status label to show current status
        self.status_var = tk.StringVar(value="Not started")
        
        self._create_top_frame(start_cb, num_beds, num_docs)
        self._create_patient_status_columns()

    def _create_top_frame(self, start_cb, num_beds, num_docs):
        """
        Creates the top frame with start button and hospital status information
        """
        top = tk.Frame(self.root)
        top.pack(pady=5)

        # Display number of beds and doctors
        tk.Label(top, text=f"Beds: {num_beds}  Doctors: {num_docs}").pack(side="left", padx=5)

        # Start button to begin simulation
        tk.Button(top, text="▶ Start", bg="green", fg="white", command=start_cb).pack(side="left", padx=5)

        # Display status of the simulation
        tk.Label(top, textvariable=self.status_var).pack(side="left", padx=10)

    def _create_patient_status_columns(self):
        """
        Creates the four columns to display the patient's status in various stages
        """
        self.columns = {
            "waiting_bed": self._create_column("Waiting for Bed"),
            "waiting_doctor": self._create_column("Waiting for Doctor"),
            "in_treatment": self._create_column("In Treatment"),
            "discharged": self._create_column("Discharged"),
        }

    def _create_column(self, title):
        """
        Creates a column for patient status with a label and listbox
        """
        frame = tk.LabelFrame(self.root, text=title, padx=10, pady=10)
        frame.pack(side="left", padx=5, pady=10, fill="y")

        listbox = tk.Listbox(frame, width=30, height=15)
        listbox.pack(padx=5, pady=5)

        return listbox

    def set_status(self, text):
        """
        Update the simulation status displayed on the UI
        """
        self.status_var.set(f"Status: {text}")

    def log_state(self, state, patient):
        """
        Logs the patient's current state in the corresponding column
        Also updates the background color based on the patient's condition
        """
        # Remove the patient from the old state column
        for lst in self.columns.values():
            items = list(lst.get(0, "end"))
            display = str(patient)
            if display in items:
                lst.delete(items.index(display))

        # Determine background color based on patient's condition
        color = "white"  # Default color
        if patient.condition == "Critical":
            color = "red"
        elif patient.condition == "Serious":
            color = "yellow"
        elif patient.condition == "Stable":
            color = "lightblue"
        elif state == "discharged":
            color = "green"

        # Add the patient to the new state column with the appropriate background color
        if state in self.columns:
            self.columns[state].insert("end", str(patient))
            # Set the background color for the patient row
            index = self.columns[state].size() - 1
            self.columns[state].itemconfig(index, {'bg': color})
