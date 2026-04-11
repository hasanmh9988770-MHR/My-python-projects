# engines/dct_engine.py

import cv2
import numpy as np
from PIL import Image


class DCTEngine:
    DELIMITER = "#####"

    # ================= ENCODE =================
    def encode(self, image, data):
        img = np.array(image)
        img = np.float32(img)

        data += self.DELIMITER
        binary = ''.join(format(ord(c), '08b') for c in data)

        idx = 0

        for i in range(0, img.shape[0] - 8, 8):
            for j in range(0, img.shape[1] - 8, 8):
                if idx >= len(binary):
                    break

                block = img[i:i + 8, j:j + 8, 0]

                dct_block = cv2.dct(block)

                # embed bit
                if binary[idx] == '1':
                    dct_block[3, 3] = abs(dct_block[3, 3]) + 5
                else:
                    dct_block[3, 3] = -abs(dct_block[3, 3]) - 5

                img[i:i + 8, j:j + 8, 0] = cv2.idct(dct_block)

                idx += 1

        img = np.clip(img, 0, 255).astype(np.uint8)

        return Image.fromarray(img)

    # ================= DECODE =================
    def decode(self, image):
        img = np.array(image)
        img = np.float32(img)

        binary = ""

        for i in range(0, img.shape[0] - 8, 8):
            for j in range(0, img.shape[1] - 8, 8):
                block = img[i:i + 8, j:j + 8, 0]

                dct_block = cv2.dct(block)

                if dct_block[3, 3] > 0:
                    binary += "1"
                else:
                    binary += "0"

        # binary → text
        chars = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i + 8]
            if len(byte) < 8:
                break

            try:
                char = chr(int(byte, 2))
                chars += char

                if self.DELIMITER in chars:
                    return chars.replace(self.DELIMITER, "")
            except:
                break

        return None