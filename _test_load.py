from pathlib import Path
import importlib.util

APP = Path(__file__).parent / "app.py"
SPEC = importlib.util.spec_from_file_location("app_mod", str(APP))
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

DATA = Path(__file__).parent / "sample_data.json"
ducks = MOD.load_ducks_from_path(DATA)
print("Loaded", len(ducks), "ducks")
for d in ducks:
    print(d.id, d.height_cm, d.weight_g)
