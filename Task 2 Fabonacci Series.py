import timeit


def generate_fibonacci(lower_bound, upper_bound):

    # Parameter sanitization
    if lower_bound < 0:
        lower_bound = 0

    if upper_bound < 0:
        upper_bound = 0

    if lower_bound > upper_bound:
        return []

    fibonacci = []

    a = 0
    b = 1

    while a <= upper_bound:

        if a >= lower_bound:
            fibonacci.append(a)

        a, b = b, a + b

    return fibonacci


# Input bounds
lower = 0
upper = 100

# Generate Fibonacci sequence
result = generate_fibonacci(lower, upper)

print("Fibonacci Sequence:", result)


# Runtime benchmark
runtime = timeit.timeit(
    lambda: generate_fibonacci(lower, upper),
    number=1000
)

print("Execution Time:", runtime, "seconds")