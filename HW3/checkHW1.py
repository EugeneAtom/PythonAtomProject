from HW1 import Task, Roadmap
from yaml import load, YAMLError

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


if __name__ == '__main__':
    dataset = list(get_dataset())
    for data in dataset:
        print(data)

    tasks = []
    for data in dataset:
        task = Task(data[0], data[2], data[1])
        tasks.append(task)

    road = Roadmap(tasks)
    print(road.filter('ready'))
