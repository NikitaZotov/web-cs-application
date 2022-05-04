from pathlib import Path

from modules.params import models_dir_path

external_modules_dir_path = Path(__file__).resolve().parent.parent
models_dir_path = external_modules_dir_path / models_dir_path
Path(models_dir_path).mkdir(parents=True, exist_ok=True)
