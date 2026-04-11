from engines.lsb_engine import LSBEngine
from engines.hybrid_engine import HybridEngine


class EngineManager:
    def __init__(self):
        self.lsb = LSBEngine()

    def get_engine(self):
        return HybridEngine(self.lsb)