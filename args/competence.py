class Competence:
    def __init__(self, subjects, languages, disabilities):
        self.subjects = set(subjects)
        self.languages = set(languages)
        self.disabilities = set(disabilities)

    def match_subjects(self, internship):
        intersection = len(self.subjects & internship.subjects)
        return intersection / len(internship.subjects)

    def match_language(self, internship):
        intersection = len(self.languages & internship.languages)
        return 1 if intersection > 0 else 0

    def match_disabilities(self, internship):
        return 0
