"""Compile .po translation files to .mo using polib (no gettext required)."""
import polib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

for po_path in BASE_DIR.glob("locale/*/LC_MESSAGES/django.po"):
    mo_path = po_path.with_suffix(".mo")
    po = polib.pofile(str(po_path))
    po.save_as_mofile(str(mo_path))
    print(f"Compiled: {po_path} → {mo_path}")

print("Done.")
