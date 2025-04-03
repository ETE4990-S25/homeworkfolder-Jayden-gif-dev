import time
import asyncio
import math
import sys

# Python 3.11+ restricts converting very large integers to strings
# Found the fix on Stack Overflow and applied it here
sys.set_int_max_str_digits(1000000)

# Basic prime checker using trial division
def _is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Shared largest prime value and a lock to protect access
largest_prime = 0
lock = asyncio.Lock()

# Prime search task (each coroutine checks numbers starting at a different offset)
async def check_primes(start, step, end_time):
    global largest_prime
    n = start
    while time.time() < end_time:
        if _is_prime(n):
            async with lock:
                if n > largest_prime:
                    largest_prime = n
        n += step
        await asyncio.sleep(0)  # Yield control

# Capped Fibonacci calculation to keep runtime reasonable
async def compute_fibonacci(n):
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
        await asyncio.sleep(0)
    print(f"[Fibonacci] Done. Fib({n}) has {len(str(a))} digits.")

# Factorial with a cap to avoid memory explosion
async def compute_factorial(n):
    MAX_FACT = 100000
    if n > MAX_FACT:
        print(f"[Factorial] Prime too large, capping n from {n} to {MAX_FACT}")
        n = MAX_FACT

    print(f"[Factorial] Calculating {n}!...")
    result = math.factorial(n)
    print(f"[Factorial] Done. {n}! has {len(str(result))} digits.")

# Main async logic: run prime search for 3 minutes, then compute Fib + Factorial
async def main():
    global largest_prime
    NUM_TASKS = 10
    SEARCH_DURATION = 3 * 60
    end_time = time.time() + SEARCH_DURATION

    prime_tasks = [
        asyncio.create_task(check_primes(i, NUM_TASKS, end_time))
        for i in range(NUM_TASKS)
    ]
    await asyncio.gather(*prime_tasks)

    print(f"\nLargest prime found in 3 minutes: {largest_prime}\n")

    fib_task = asyncio.create_task(compute_fibonacci(largest_prime))
    fact_task = asyncio.create_task(compute_factorial(largest_prime))
    await asyncio.gather(fib_task, fact_task)

    print("\nAll tasks completed.")

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"\nTotal runtime: {time.time() - start:.2f} seconds")
