# Adiciona o diretório atual ao Python path
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))