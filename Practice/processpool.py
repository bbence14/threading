from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import wait, as_completed
import multiprocessing


def square(x):
    return x * x


if __name__ == '__main__':
    inputs = [0, 1, 2, 3, 4]
    executor = ProcessPoolExecutor(max_workers=4)
    fut1 = executor.submit(square, 2)
    fut2 = executor.submit(square, 3)
    wait([fut1, fut2])

    results = as_completed([fut1, fut2])
    print(list(results))
