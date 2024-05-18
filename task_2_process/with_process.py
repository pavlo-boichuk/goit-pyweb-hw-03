import datetime
from multiprocessing import cpu_count, Pool


def factorize(*number):
    for num in number:
        return [n for n in range(1, num+1) if num%n==0]


def callback(result):
    print(result)


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    with Pool(processes=cpu_count()) as pool:
        pool.map_async(factorize, [128, 255, 99999, 10651060], callback=callback)
        pool.close()
        pool.join()

    end_time = datetime.datetime.now()
    print(f'result time for processes: {end_time - start_time}')