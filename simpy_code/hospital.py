import simpy
import random
from .patient import Patient

class Hospital:
    def __init__(self, env, ui_callback, num_beds=5, num_doctors=5):
        self.env = env
        self.ui = ui_callback
        self.beds = simpy.Resource(env, capacity=num_beds)  # 5 beds
        self.doctors = simpy.PriorityResource(env, capacity=num_doctors)  # Use PriorityResource here
        self.patient_counter = 0
        self.max_patients = 10  # maximum patients
        self.patients = []  # List to store all patients
        env.process(self._generate_patients())

    def _generate_patients(self):
        # Generate 10 patients with random arrival times
        while len(self.patients) < self.max_patients:
            yield self.env.timeout(random.randint(1, 5))  # random arrival time between 1 to 5 seconds
            cond = random.choices(["Stable", "Serious", "Critical"], weights=[0.4, 0.4, 0.2])[0]
            p = Patient(self.patient_counter, cond)
            self.patient_counter += 1
            self.patients.append(p)  # Add patient to the list
            self.env.process(self._handle_patient(p))

    def _handle_patient(self, patient):
        self.ui("waiting_bed", patient)
        yield self.env.timeout(2)  # simulate 2s delay between transitions

        with self.beds.request() as bed_req:
            yield bed_req
            self.ui("waiting_doctor", patient)
            yield self.env.timeout(2)

            # Now using PriorityResource
            with self.doctors.request(priority=patient.urgency) as doc_req:
                yield doc_req
                self.ui("in_treatment", patient)
                yield self.env.timeout(2)

                yield self.env.timeout(patient.treatment_time)
                self.ui("discharged", patient)

        # Check if all patients have been treated and discharged
        if len([p for p in self.patients if not p.discharged]) == 0:
            self.env.exit()  # End the simulation once all patients are discharged
