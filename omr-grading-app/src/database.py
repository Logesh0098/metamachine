
class OMRDatabase:
    def __init__(self):
        # Initialize with empty exam list
        self.exams = []

    def save_result(self, result):
        """Save grading result to database (mock implementation)."""
        self.exams.append(result)

    def get_all_exams(self):
        """Return all saved exams (mock implementation)."""
        return self.exams
