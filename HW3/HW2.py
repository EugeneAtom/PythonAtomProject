from datetime import date

possible_states = ('in_progress', 'ready')


class Task:
    def __init__(self, _title, _estimate, _state='in_progress'):
        assert isinstance(_title, type("")), "Incorrect type of title"
        self.title = _title
        assert isinstance(_estimate, type(date.today())), "Incorrect type of estimate"
        self.estimate = _estimate
        assert _state in possible_states, "Impossible state"
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


from yaml import load, YAMLError
from datetime import timedelta

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def get_dataset():
    try:
        with open("dataset", 'rt', encoding='utf-8') as input:
            try:
                package = load(input, Loader=Loader)
                dataset = package.get('dataset')
                if not isinstance(dataset, list):
                    raise ValueError('wrong format')
                yield from dataset
            except YAMLError:
                raise YAMLError
    except OSError:
        raise OSError


dataset = list(get_dataset())


class WSGIApplication(object):
    default_headers = [
        ('Content-Type', 'text/plain'),
        ('Server', 'WSGIExample/1.0'),
    ]

    def __init__(self, environment, start_response):
        self.environment = environment
        self.start = start_response

    def __iter__(self):
        self.start('200 OK', self.default_headers)

        message = ''
        for data in dataset:
            task = Task(data[0], data[2], data[1])
            if task.remaining < timedelta(days=3) and task.state == 'in_progress':
                message = message + task.title + '\n'

        yield message.encode('utf-8')


from wsgiref.simple_server import make_server

if __name__ == '__main__':
    http_server = make_server('127.0.0.1', 1997, WSGIApplication)
    http_server.handle_request()
