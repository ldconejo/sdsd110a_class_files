from multiprocessing import Process, Semaphore
import time

def worker(sem, name):
    print(f"{name} waiting for access...")
    sem.acquire()
    print(f"{name} entered critical section")
    time.sleep(2)
    print(f"{name} leaving critical section")
    sem.release()

if __name__ == "__main__":
    sem = Semaphore(2)
    
    processes = [Process(target=worker, args=(sem, f"Process-{i}")) for i in range(5)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()