from multiprocessing import Pool, cpu_count
from functools import partial

import time


def square(y, x):
    return x ** y


if __name__ == '__main__':
    num_processes = 4
    comparison_list = [1, 2, 3]
    power_list = [4, 5, 6]

    processes = []
    start_time = time.time()
    power = 3
    num_cpus_available = max(1, cpu_count()-1)
    print('num cpu available: ', num_cpus_available)
    partial_function = partial(square, power)
    prepared_list = []
    for i in range(len(comparison_list)):
        prepared_list.append((comparison_list[i], power_list[i]))

    with Pool(num_cpus_available) as multiprocessing_pool:
        result = multiprocessing_pool.starmap(square, prepared_list)

    print(result)

    print('Everything took: ', time.time() - start_time, 'seconds')
