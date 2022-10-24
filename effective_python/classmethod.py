import os
from pathlib import Path
from tempfile import TemporaryDirectory


class InputData:
    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


class Worker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


def execute(workers):
    for worker in workers:
        worker.map()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)


def write_test_files(tmpdir):
    for i in range(10):
        path = Path(tmpdir, f"example-{i}.txt")
        with open(path, mode="w") as f:
            for j in range(20):
                f.write(f"This text is written in python {j}\n")


if __name__ == '__main__':
    print('start')
    with TemporaryDirectory() as tmpdir:
        write_test_files(tmpdir)
        result = mapreduce(tmpdir)
    print(f'There are {result} lines')
