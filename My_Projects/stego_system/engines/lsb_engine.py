import numpy as np
from PIL import Image


class LSBEngine:
    DELIMITER = "#####"

    def encode(self, image, data):
        img = np.array(image).copy()

        data += self.DELIMITER
        binary = ''.join(format(ord(c), '08b') for c in data)

        idx = 0
        h, w, c = img.shape

        for i in range(h):
            for j in range(w):
                for k in range(c):
                    if idx < len(binary):
                        val = int(img[i, j, k])
                        bit = int(binary[idx])

                        # SAFE BIT WRITE
                        val = (val & 254) | bit

                        img[i, j, k] = np.uint8(val)
                        idx += 1

        return Image.fromarray(img)

    def decode(self, image):
        img = np.array(image)

        binary = ""
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                for k in range(img.shape[2]):
                    binary += str(img[i, j, k] & 1)

        chars = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) < 8:
                break

            char = chr(int(byte, 2))
            chars += char

            if self.DELIMITER in chars:
                return chars.replace(self.DELIMITER, "")

        return None