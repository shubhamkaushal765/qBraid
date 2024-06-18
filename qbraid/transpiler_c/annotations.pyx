# Copyright (C) 2024 qBraid
#
# This file is part of the qBraid-SDK
#
# The qBraid-SDK is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid-SDK, as per Section 15 of the GPL v3.

"""
Module defining function annotations (e.g. decorators) used in the transpiler.

"""

from cpython.object cimport PyObject_HasAttrString
from cpython.list cimport PyList_Append, PyList_New

def requires_extras(str dependency):
    """
    Decorator factory to mark conversion functions that require additional dependencies
    beyond their "{source}_to_{target}" naming convention. It adds a specified dependency
    as an attribute to the function.

    Args:
        dependency (str): The name of the required additional dependency.

    Returns:
        Callable: A decorator that marks a function with the required dependency.
    """

    def decorator(func):
        if PyObject_HasAttrString(func, "requires_extras"):
            PyList_Append(func.requires_extras, dependency)
        else:
            func.requires_extras = PyList_New(0)
            PyList_Append(func.requires_extras, dependency)
        return func

    return decorator


def weight(float value):
    """
    Decorator factory to mark conversion functions with a weight attribute.
    This weight attribute is used to prioritize conversion paths in a conversion graph.

    Args:
        value (float): The weight of the conversion function. Must be between 0 and 1 inclusive.

    Returns:
        Callable: A decorator that assigns the specified weight to a function.
    """
    if not 0 <= value <= 1:
        raise ValueError("Weight value must be between 0 and 1.")

    def decorator(func):
        func.weight = value
        return func

    return decorator
