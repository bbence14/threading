from multiprocessing import Process, Queue # More core results more calculation power
import time


def check_value_in_list(x, i, num_of_processes, queue):
    """
    Distributing values through multiple CPU-s
    :param x: value list that need to find
    :param i: current process number
    :param num_of_processes: all process number
    :param queue: result store
    :return:
    """
    max_number_to_check_to = 10**8
    lower = int(i * max_number_to_check_to / num_of_processes)
    upper = int((i +1) * max_number_to_check_to / num_of_processes)
    number_of_hits = 0
    for i in range(lower, upper):
        if i in x:
            number_of_hits += 1

    queue.put((lower, upper, number_of_hits))


if __name__ == '__main__':
    num_processes = 4
    comparison_list = [1, 2, 3]
    queue = Queue()
    processes = []
    start_time = time.time()
    for i in range(num_processes):
        t = Process(target=check_value_in_list, args=(comparison_list, i, num_processes, queue))
        processes.append(t)

    for t in processes:
        t.start()

    for t in processes:
        t.join()

    queue.put('DONE')
    while True:
        v = queue.get()
        if v == 'DONE':
            break
        lower, upper, number_of_hits = v
        print('Between', lower, 'and', upper, 'found', number_of_hits)
    print('Everything took: ', time.time() - start_time, 'seconds')
