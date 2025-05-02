import simpy
from simpy_code.hospital import Hospital
from simpy_code.patient import Patient
import threading
from tkinter_ui.ui import run_ui

def simulate(env, hospital):
    names = ["Ram", "Ali", "Sara", "Geeta", "Ravi"]
    conditions = ["Stable", "Emergency", "Critical"]
    for i in range(5):
        name = names[i % len(names)]
        cond = conditions[i % len(conditions)]
        p = Patient(name, cond)
        env.process(hospital.treat_patient(p))
        yield env.timeout(3)

def run_simpy():
    env = simpy.Environment()
    hospital = Hospital(env)
    env.process(simulate(env, hospital))
    env.run(until=30)

def main():
    sim_thread = threading.Thread(target=run_simpy)
    sim_thread.start()
    run_ui()

if __name__ == "__main__":
    main()
