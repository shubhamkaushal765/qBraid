import timeit
from memory_profiler import memory_usage
from qbraid.transpiler.annotations import requires_extras as py_requires_extras, weight as py_weight
from qbraid.transpiler_c.annotations import (
    requires_extras as cy_requires_extras,
    weight as cy_weight,
)


def test_func():
    pass


def test_requires_extras():
    # Test Python version
    py_decorator = py_requires_extras("test_dependency")
    py_decorated_func = py_decorator(test_func)

    # Test Cython version
    cy_decorator = cy_requires_extras("test_dependency")
    cy_decorated_func = cy_decorator(test_func)

    # Verify the results are the same
    assert py_decorated_func.requires_extras == cy_decorated_func.requires_extras

    # Time the Python version
    py_time = timeit.timeit(lambda: py_decorator(test_func), number=100000)
    print(f"Python requires_extras time: {py_time:.4f} seconds")

    # Time the Cython version
    cy_time = timeit.timeit(lambda: cy_decorator(test_func), number=100000)
    print(f"Cython requires_extras time: {cy_time:.4f} seconds")

    # Measure memory usage for the Python version
    py_mem_usage = memory_usage((py_decorator, (test_func,)), max_usage=True)
    print(f"Python requires_extras memory usage: {py_mem_usage:.4f} MiB")

    # Measure memory usage for the Cython version
    cy_mem_usage = memory_usage((cy_decorator, (test_func,)), max_usage=True)
    print(f"Cython requires_extras memory usage: {cy_mem_usage:.4f} MiB")


def test_weight():
    # Test Python version
    py_decorator = py_weight(0.5)
    py_decorated_func = py_decorator(test_func)

    # Test Cython version
    cy_decorator = cy_weight(0.5)
    cy_decorated_func = cy_decorator(test_func)

    # Verify the results are the same
    assert py_decorated_func.weight == cy_decorated_func.weight

    # Time the Python version
    py_time = timeit.timeit(lambda: py_decorator(test_func), number=100000)
    print(f"Python weight time: {py_time:.4f} seconds")

    # Time the Cython version
    cy_time = timeit.timeit(lambda: cy_decorator(test_func), number=100000)
    print(f"Cython weight time: {cy_time:.4f} seconds")

    # Measure memory usage for the Python version
    py_mem_usage = memory_usage((py_decorator, (test_func,)), max_usage=True)
    print(f"Python weight memory usage: {py_mem_usage:.4f} MiB")

    # Measure memory usage for the Cython version
    cy_mem_usage = memory_usage((cy_decorator, (test_func,)), max_usage=True)
    print(f"Cython weight memory usage: {cy_mem_usage:.4f} MiB")


if __name__ == "__main__":
    test_requires_extras()
    test_weight()
