class HybridEngine:
    def __init__(self, lsb):
        self.lsb = lsb

    def encode(self, image, data):
        return self.lsb.encode(image, data)

    def decode(self, image):
        return self.lsb.decode(image)