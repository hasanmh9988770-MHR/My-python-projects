# core/pipeline.py

import os
from PIL import Image


class Pipeline:
    def __init__(self, engine, key_manager, crypto_class):
        self.engine = engine
        self.key_manager = key_manager
        self.crypto_class = crypto_class

    # ================= ENCODE =================
    def encode(self, message, password, image_path):
        if not message:
            raise ValueError("Message cannot be empty")

        if not password:
            raise ValueError("Password required")

        if not os.path.exists(image_path):
            raise FileNotFoundError("Image not found")

        try:
            # 🔐 derive key
            key = self.key_manager.derive_key(password)
            crypto = self.crypto_class(key)

            # 🔒 encrypt message
            encrypted = crypto.encrypt(message)

            # 🖼️ LOAD IMAGE (ANY FORMAT)
            img = Image.open(image_path)

            # 💥 FORCE SAFE MODE (IMPORTANT)
            img = img.convert("RGB")

            # 🧠 encode using engine (LSB recommended)
            encoded_img = self.engine.encode(img, encrypted)

            # 📁 SAFE OUTPUT (ALWAYS PNG)
            base = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(
                os.path.dirname(image_path),
                base + "_encoded.png"
            )

            encoded_img.save(output_path, "PNG")

            print("✅ ENCODE SUCCESS:", output_path)

            return output_path

        except Exception as e:
            print("❌ ENCODE ERROR:", e)
            raise e

    # ================= DECODE =================
    def decode(self, image_path, password):
        if not os.path.exists(image_path):
            raise FileNotFoundError("Image not found")

        if not password:
            raise ValueError("Password required")

        try:
            # 🔐 derive key
            key = self.key_manager.derive_key(password)
            crypto = self.crypto_class(key)

            # 🖼️ LOAD IMAGE
            img = Image.open(image_path).convert("RGB")

            # 🧠 extract hidden data
            extracted = self.engine.decode(img)

            if not extracted:
                print("❌ No hidden data found")
                return None

            try:
                # 🔓 decrypt
                message = crypto.decrypt(extracted)
                print("✅ DECODE SUCCESS")
                return message

            except Exception as e:
                print("❌ Wrong password or corrupted data")
                return None

        except Exception as e:
            print("❌ DECODE ERROR:", e)
            raise e