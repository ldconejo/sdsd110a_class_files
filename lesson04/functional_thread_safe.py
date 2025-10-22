import threading
# This is naturally thread-safe 
def calculate_interest(principal, rate, time): 
    return principal * (1 + rate) ** time 

# Multiple threads can call this simultaneously - no locks needed!

def worker(principal, rate, time):
    interest = calculate_interest(principal, rate, time)
    print(f"Calculated interest: {interest}")

if __name__ == "__main__":
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(1000, 0.05, i+1))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

