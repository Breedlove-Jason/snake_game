"""Build a static site with the exact same engine as the desktop app."""
from pathlib import Path
import shutil
root = Path(__file__).resolve().parent
out = root / 'dist'
out.mkdir(exist_ok=True)
for file in (root / 'web').iterdir():
    if file.is_file():
        shutil.copy2(file, out / file.name)
shutil.copy2(root / 'engine.py', out / 'engine.py')
print('Built static Snake site in dist/')
