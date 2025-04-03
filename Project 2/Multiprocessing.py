import time
from multiprocessing import Process, Value, Lock
import math
import sys

# Python 3.11+ won't let you convert huge integers to strings unless you raise the limit.
# I ran into this trying to print Fib(1000000), so thanks to Stack Overflow for the fix.
sys.set_int_max_str_digits(1000000)

# Basic prime checker using trial division.
# It's not fast for huge numbers, but it works — and I needed something reliable.
def _is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Each process runs this function to search for primes.
# I split the search space across multiple processes using different start points and steps.
# If a larger prime is found, I update the shared variable with a lock to avoid conflicts.
def search_primes(start, step, largest_prime, lock, end_time):
    n = start
    while time.time() < end_time:
        if _is_prime(n):
            with lock:
                if n > largest_prime.value:
                    largest_prime.value = n
        n += step

# Iterative Fibonacci function.
# I capped it because trying to compute something like Fib(50000000) made my machine beg for mercy.
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

# Factorial computation.
# I initially didn’t expect how massive factorials get — thank you Stack Overflow again.
def compute_factorial(n):
    MAX_FACT = 100000
    if n > MAX_FACT:
        print(f"[Factorial] Prime too large, capping n from {n} to {MAX_FACT}")
        n = MAX_FACT

    print(f"[Factorial] Calculating {n}!...")
    result = math.factorial(n)
    print(f"[Factorial] Done. {n}! has {len(str(result))} digits.")

# Main function to control the flow.
# I used multiple processes to search for primes in parallel over 3 minutes.
# Once a prime is found, I run Fibonacci and factorial calculations at the same time.
def main():
    NUM_PROCESSES = 7
    SEARCH_DURATION = 3 * 60  # 3 minutes

    largest_prime = Value('i', 0)
    lock = Lock()
    end_time = time.time() + SEARCH_DURATION

    processes = []
    for i in range(NUM_PROCESSES):
        p = Process(target=search_primes, args=(i, NUM_PROCESSES, largest_prime, lock, end_time))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    prime_found = largest_prime.value
    print(f"\nLargest prime found in 3 minutes: {prime_found}\n")

    # Run the two heavy computations in parallel (learned this trick from multiprocessing docs and forums)
    fib_proc = Process(target=compute_fibonacci, args=(prime_found,))
    fact_proc = Process(target=compute_factorial, args=(prime_found,))

    fib_proc.start()
    fact_proc.start()

    fib_proc.join()
    fact_proc.join()

    print("\nAll tasks completed.")

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"\nTotal runtime: {time.time() - start:.2f} seconds")
