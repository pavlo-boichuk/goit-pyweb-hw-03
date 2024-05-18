import datetime
from random import randint
from multiprocessing import Process, cpu_count
import sys


def factorize(*number):
    result = []
    for num in number:
        result.append([n for n in range(1, num+1) if num%n==0])

    print(result)
    sys.exit(0)


if __name__ == '__main__':

    if cpu_count() > 1:
        start_time = datetime.datetime.now()

        process = []
    
        pr1 = Process(target=factorize, args=(128, 255))
        pr1.start()
        process.append(pr1)

        pr2 = Process(target=factorize, args=(99999, 10651060))
        pr2.start()
        process.append(pr2)

        [pr.join() for pr in process]
        [print(pr.exitcode, end=' ') for pr in process]
        print('')

        end_time = datetime.datetime.now()
        print(f'result time for 2 process: {end_time - start_time}')

    # process_count = randint(1, cpu_count())
    # process = []
    # for i in range(process_count):
    #     pr = Process(target=factorize, args=(128, 255, 99999, 10651060))
    #     pr.start()
    #     process.append(pr)

    # [pr.join() for pr in process]
    # [print(pr.exitcode, end=' ')]
    # print('')