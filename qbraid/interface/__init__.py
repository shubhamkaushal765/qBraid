"""
===============================================
Interface (:mod:`qbraid.interface`)
===============================================

.. currentmodule:: qbraid.interface

.. autosummary::
   :toctree: ../stubs/

   to_unitary
   convert_to_contiguous
   equal_unitaries
   bell

"""
from .calculate_unitary import equal_unitaries, to_unitary
from .convert_to_contiguous import convert_to_contiguous
from .bell_circuit import bell
