from datetime import date, timedelta


class Task:
    def __init__(self, _title, _estimate, _state='in_progress'):
        self.title = _title
        assert isinstance(_estimate, type(date.today())), "Incorrect type of estimate"
        self.estimate = _estimate
        self.state = _state

    @property
    def remaining(self):
        if self.state == "in_progress":
            return self.estimate - date.today()
        else:
            return timedelta(days=0)

    @property
    def is_failed(self):
        return self.state == "in_progress" and self.estimate < date.today()

    def ready(self):
        if self.state == 'in_progress': self.state = 'ready'


class Roadmap:
    def __init__(self, _tasks):
        self.tasks = _tasks

    @property
    def today(self):
        return [task.title for task in self.tasks if task.estimate == date.today]

    def filter(self, state):
        return [task.title for task in self.tasks if state == task.state]
