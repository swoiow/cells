#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem

q = Queue()
WORKER = 10
def TASKS():
    pass

Producer.main(queue=q, tasks=TASKS)
Consumer.main(queue=q, worker_func=ft, task_number=WORKER)
"""

import threading

from six.moves.queue import Queue


class Producer(threading.Thread):

    def __init__(self, t_name, queue: Queue, tasks: (list, iter, tuple)):
        self.queue = queue
        self._tasks = tasks

        threading.Thread.__init__(self, name=t_name)

    def run(self):
        for t in self._tasks:
            self.queue.put(t)

    @staticmethod
    def main(queue: Queue, tasks: (list, iter, tuple)):
        producer = Producer("producer", queue, tasks=tasks)
        producer.start()
        producer.join()

        print("Producer is under running!")


class Consumer(threading.Thread):

    def __init__(self, t_name, queue: Queue, func_handle_task: callable):
        self.queue = queue
        self._func_handle_task = func_handle_task
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        self._func_handle_task(self.queue)

    @staticmethod
    def main(worker_func: callable, queue: Queue, task_number: int, daemon=False):
        for num in range(task_number):
            consumer = Consumer("consumer", queue, func_handle_task=worker_func)
            if daemon:
                consumer.setDaemon(True)

            consumer.start()
            print("Consumer-{} is running!".format(num))

        consumer.join()
