# test_exceptions.py

import timeit
from memory_profiler import memory_usage

# Import the Python versions of the exceptions
from qbraid.transpiler.exceptions import (
    CircuitConversionError as CircuitConversionError_py,
    NodeNotFoundError as NodeNotFoundError_py,
    ConversionPathNotFoundError as ConversionPathNotFoundError_py,
)

# Import the Cython versions of the exceptions
from qbraid.transpiler_c.exceptions import (
    CircuitConversionError as CircuitConversionError_cy,
    NodeNotFoundError as NodeNotFoundError_cy,
    ConversionPathNotFoundError as ConversionPathNotFoundError_cy,
)


def test_circuit_conversion_error():
    try:
        raise CircuitConversionError_py()
    except CircuitConversionError_py:
        pass

    try:
        raise CircuitConversionError_cy()
    except CircuitConversionError_cy:
        pass


def test_node_not_found_error():
    try:
        raise NodeNotFoundError_py("graph_type", "package", ["node1", "node2"])
    except NodeNotFoundError_py as e:
        assert (
            str(e)
            == "graph_type conversion graph does not contain node 'package'. Supported nodes are: ['node1', 'node2']"
        )

    try:
        raise NodeNotFoundError_cy("graph_type", "package", ["node1", "node2"])
    except NodeNotFoundError_cy as e:
        assert (
            str(e)
            == "graph_type conversion graph does not contain node 'package'. Supported nodes are: ['node1', 'node2']"
        )


def test_conversion_path_not_found_error():
    try:
        raise ConversionPathNotFoundError_py("source", "target", max_depth=5)
    except ConversionPathNotFoundError_py as e:
        assert str(e) == "No conversion path found from 'source' to 'target' with depth <= 5"

    try:
        raise ConversionPathNotFoundError_cy("source", "target", max_depth=5)
    except ConversionPathNotFoundError_cy as e:
        assert str(e) == "No conversion path found from 'source' to 'target' with depth <= 5"


if __name__ == "__main__":
    test_circuit_conversion_error()
    test_node_not_found_error()
    test_conversion_path_not_found_error()
