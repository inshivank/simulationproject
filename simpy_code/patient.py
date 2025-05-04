class Patient:
    def __init__(self, pid, condition):
        self.pid = pid
        self.condition = condition
        self.discharged = False  # Track whether the patient has been discharged
        if condition == "Critical":
            self.urgency = 0
            self.treatment_time = 10  # 10 seconds for critical
        elif condition == "Serious":
            self.urgency = 1
            self.treatment_time = 8  # 8 seconds for serious
        else:
            self.urgency = 2
            self.treatment_time = 5  # 5 seconds for stable

    def __str__(self):
        return f"P{self.pid} ({self.condition})"

    def mark_discharged(self):
        self.discharged = True  # Mark the patient as discharged
