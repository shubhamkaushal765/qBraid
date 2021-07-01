from ...gate import Gate
from typing import Optional

class Swap(Gate):

    def __init__(self, global_phase: Optional[float]=0.0):
        super().__init__(
            "Swap", 
            num_qubits=2, 
            params=[], 
            global_phase=global_phase)