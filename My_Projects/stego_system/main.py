import sys
from PySide6.QtWidgets import QApplication

from core.pipeline import Pipeline
from core.engine_manager import EngineManager
from security.key_manager import KeyManager
from security.crypto_aes import CryptoAES
from interface.gui import StegoApp


if __name__ == "__main__":
    app = QApplication(sys.argv)

    engine = EngineManager().get_engine()
    pipeline = Pipeline(engine, KeyManager(), CryptoAES)

    window = StegoApp(pipeline)
    window.show()

    sys.exit(app.exec())