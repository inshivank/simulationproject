# hospital.py

import simpy
import random
from .patient import Patient

class Hospital:
    def __init__(self, env, ui_callback, num_beds=5, num_doctors=3):
        self.env = env
        self.ui = ui_callback
        self.beds = simpy.Resource(env, capacity=num_beds)
        self.doctors = simpy.Resource(env, capacity=num_doctors)  # Removed preemptive for simplicity
        self.patient_counter = 0
        self.max_patients = 10
        self.referred_patients = 0  # To track how many patients are referred
        self.max_referred = random.choice([2, 3])  # Randomly select whether 2 or 3 patients will be referred
        env.process(self._generate_patients())

    def _generate_patients(self):
        for _ in range(self.max_patients):
            yield self.env.timeout(2)  # 2 seconds between new patient arrivals
            cond = random.choices(["Stable", "Serious", "Critical"], weights=[0.4, 0.4, 0.2])[0]
            p = Patient(self.patient_counter, cond)
            self.patient_counter += 1
            self.env.process(self._handle_patient(p))

    def _handle_patient(self, patient):
        self.ui("waiting_bed", patient)
        yield self.env.timeout(2)  # simulate 2s delay between transitions

        with self.beds.request() as bed_req:
            yield bed_req
            self.ui("waiting_doctor", patient)
            yield self.env.timeout(2)

            with self.doctors.request() as doc_req:
                yield doc_req
                self.ui("in_treatment", patient)
                yield self.env.timeout(2)

                # Referral Logic: If patient is Critical or Serious, and we've not exceeded the max referrals
                if patient.condition in ["Critical", "Serious"] and self.referred_patients < self.max_referred:
                    self.referred_patients += 1
                    self.ui("referred", patient)  # Mark the patient as referred
                    return  # Patient is referred, no further treatment here (they will not be discharged)

                # Proceed with the normal treatment if not referred
                yield self.env.timeout(patient.treatment_time)
                self.ui("discharged", patient)
