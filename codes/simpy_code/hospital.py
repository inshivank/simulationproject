import simpy
import random

class Hospital:
    def __init__(self, env):
        self.env = env
        self.doctors = simpy.PreemptiveResource(env, capacity=2)
        self.beds = simpy.Resource(env, capacity=5)
        self.medicine_stock = simpy.Container(env, init=50, capacity=100)
        self.critical_monitor = env.process(self.monitor_medicine())

    def monitor_medicine(self):
        while True:
            if self.medicine_stock.level < 20:
                yield self.env.timeout(5)
                yield self.medicine_stock.put(50)

    def treat_patient(self, patient):
        with self.doctors.request(priority=patient.priority) as req:
            yield req
            with self.beds.request() as bed_req:
                yield bed_req
                yield self.medicine_stock.get(patient.medicine_needed)
                yield self.env.timeout(patient.treatment_time)
    