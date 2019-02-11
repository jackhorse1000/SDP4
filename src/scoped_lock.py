class ScopedLock:
    def __init__ (self, mutex):
        self.mutex = mutex
        mutex.acquire()

    def __del__ (self):
        self.mutex.release ()