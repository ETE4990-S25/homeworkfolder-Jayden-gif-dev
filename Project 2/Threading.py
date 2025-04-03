import time
import threading
import math
import sys

# Same Python 3.11 issue as before — need to increase the digit limit for giant integers
sys.set_int_max_str_digits(1000000)

# Basic prime check using trial division
# Again, not optimized for speed, but reliable enough for this kind of use
def _is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Global variables shared between threads
largest_prime = 0
lock = threading.Lock()

# Each thread runs this function to check numbers in a slice of the range
# I use a lock to make sure no two threads try to update largest_prime at the same time
def search_primes(start, step, end_time):
    global largest_prime
    n = start
    while time.time() < end_time:
        if _is_prime(n):
            with lock:
                if n > largest_prime:
                    largest_prime = n
        n += step

# Iterative Fibonacci — capped to avoid memory explosion
def compute_fibonacci(n):
    MAX_FIB = 1000000
    if n > MAX_FIB:
        print(f"[Fibonacci] Prime too large, capping n from {n} to {MAX_FIB}")
        n = MAX_FIB

    print(f"[Fibonacci] Calculating Fib({n})...")
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        if i % 200000 == 0:
            print(f"  Reached Fib({i})")
    print(f"[Fibonacci] Done. Fib({n}) has {len(str(a))} digits.")

# Built-in factorial with a cap — thanks again Stack Overflow for helping me understand how fast this grows
def compute_factorial(n):
    MAX_FACT = 100000
    if n > MAX_FACT:
        print(f"[Factorial] Prime too large, capping n from {n} to {MAX_FACT}")
        n = MAX_FACT

    print(f"[Factorial] Calculating {n}!...")
    result = math.factorial(n)
    print(f"[Factorial] Done. {n}! has {len(str(result))} digits.")

# Main threading logic
def main():
    NUM_THREADS = 10
    SEARCH_DURATION = 3 * 60  # 3 minutes

    end_time = time.time() + SEARCH_DURATION
    threads = []

    # Start each thread with a unique offset and shared step to divide the range
    for i in range(NUM_THREADS):
        t = threading.Thread(target=search_primes, args=(i, NUM_THREADS, end_time))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    prime_found = largest_prime
    print(f"\nLargest prime found in 3 minutes: {prime_found}\n")

    # Start Fibonacci and Factorial threads after the prime is found
    fib_thread = threading.Thread(target=compute_fibonacci, args=(prime_found,))
    fact_thread = threading.Thread(target=compute_factorial, args=(prime_found,))

    fib_thread.start()
    fact_thread.start()

    fib_thread.join()
    fact_thread.join()

    print("\nAll tasks completed.")

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"\nTotal runtime: {time.time() - start:.2f} seconds")
