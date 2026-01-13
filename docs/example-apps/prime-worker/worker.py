"""
Worker thread: Pyodide with numpy doing the computation.
"""
import numpy as np


def sieve_numpy(limit):
    """
    Sieve of Eratosthenes using numpy arrays.
    """
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    primes = np.where(is_prime)[0]
    return [int(p) for p in primes]


def sieve_python(limit):
    """
    Sieve of Eratosthenes using pure Python.
    """
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]


def find_primes(limit, use_numpy=True):
    """
    Find all primes up to limit using Sieve of Eratosthenes.
    """
    if use_numpy:
        primes_list = sieve_numpy(limit)
    else:
        primes_list = sieve_python(limit)
    first_20 = [int(primes_list[i]) for i in range(min(20, len(primes_list)))]
    return {
        "count": len(primes_list),
        "first_20": first_20
    }


# Export functions to make them accessible from main thread.
__export__ = ["find_primes"]