class Patient:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition
        self.set_attributes()

    def set_attributes(self):
        if self.condition == 'Critical':
            self.priority = 0
            self.treatment_time = 10
            self.medicine_needed = 20
        elif self.condition == 'Emergency':
            self.priority = 1
            self.treatment_time = 7
            self.medicine_needed = 15
        else:
            self.priority = 2
            self.treatment_time = 5
            self.medicine_needed = 10
