import random
import threading
import time

from Awaiting import awaiting


class BlockingQueue:
    def __init__(self):
        self.queue = []

    def push(self, item):
        self.queue.append(item)
        awaiting.notify()  # 自动获取当前函数名称，唤醒等待的线程

    def pop(self):
        awaiting.wait_for('push', lambda: len(self.queue) > 0)  # 等待队列不为空
        return self.queue.pop(0)

    def __str__(self):
        return str(self.queue)


# 使用示例
def producer(queue):
    for i in range(5):
        time.sleep(random.randint(0, 2))
        print('pushing')
        print(f"push: {i}", f"now: {queue}")
        queue.push(i)


def consumer(queue):
    for i in range(6):
        time.sleep(random.randint(1, 2))
        print('I want to pop')
        item = queue.pop()
        print(f"pop: {item}", f"now: {queue}")


if __name__ == "__main__":
    bq = BlockingQueue()
    t1 = threading.Thread(target=producer, args=(bq,))
    t2 = threading.Thread(target=consumer, args=(bq,))
    t1.start()
    t2.start()
    time.sleep(3)
    bq.push(5)

    t1.join()
    t2.join()
