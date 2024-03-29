import os
from pathlib import Path
from tempfile import TemporaryDirectory


class GenericInputData:
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData(GenericInputData):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def execute(workers):
    for worker in workers:
        worker.map()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
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
        config = {'data_dir': tmpdir}
        result = mapreduce(LineCountWorker, PathInputData, config)
    print(f'There are {result} lines')
