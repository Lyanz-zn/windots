import json
import sys
from pathlib import Path
import commentjson
from ruamel.yaml import YAML


def merge_dicts(target, patch):
    """
    Melakukan deep merge dari patch ke target.
    Mengubah/menambah value tanpa merusak struktur dictionary target.
    """
    for key, value in patch.items():
        if isinstance(value, dict) and key in target and isinstance(target[key], dict):
            merge_dicts(target[key], value)
        else:
            target[key] = value


def update_json_file(target_path, patch_data):
    """Membaca file JSONC, memperbarui nilainya, lalu menyimpannya kembali."""
    with open(target_path, "r", encoding="utf-8") as f:
        data = commentjson.load(f)
    # Merge/override
    merge_dicts(data, patch_data)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def update_yaml_file(target_path, patch_data):
    """Membaca file YAML, memperbarui nilainya (mempertahankan komentar dan struktur), lalu menyimpannya."""
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(target_path, "r", encoding="utf-8") as f:
        data = yaml.load(f)
    # Lakukan merge/override
    merge_dicts(data, patch_data)
    with open(target_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f)


def main():
    if len(sys.argv) < 3:
        print("Penggunaan: python theme_injector.py <target_file> <patch_json>")
        sys.exit(1)
    target_file = Path(sys.argv[1])
    patch_file = Path(sys.argv[2])
    if not target_file.exists() or not patch_file.exists():
        print("Error: Berkas target atau patch tidak ditemukan.")
        sys.exit(1)
    # Baca patch dari output Matugen
    with open(patch_file, "r", encoding="utf-8") as f:
        patch_data = json.load(f)
    ext = target_file.suffix.lower()
    if ext in [".yaml", ".yml"]:
        update_yaml_file(target_file, patch_data)
    elif ext in [".json", ".jsonc"]:
        update_json_file(target_file, patch_data)
    else:
        print(f"Format {ext} tidak didukung.")


if __name__ == "__main__":
    main()
