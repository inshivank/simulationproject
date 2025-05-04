import tkinter as tk
import simpy, threading
import time
from simpy_code.hospital import Hospital
from tkinter_ui.ui import HospitalUI

def main():
    root = tk.Tk()
    num_beds = 5  # 5 beds
    num_docs = 5  # 5 doctors
    ui = HospitalUI(root,
        start_cb=lambda: start(ui, num_beds, num_docs),
        num_beds=num_beds, num_docs=num_docs
    )
    root.mainloop()

def start(ui, beds, docs):
    ui.set_status("Running")
    def run():
        env = simpy.rt.RealtimeEnvironment(factor=1, strict=True)
        hosp = Hospital(env, ui.log_state, num_beds=beds, num_doctors=docs)
        env.run()  # Run the simulation
        ui.set_status("Finished")
    threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    main()
