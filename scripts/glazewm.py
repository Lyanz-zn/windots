from __future__ import annotations

import subprocess as sp
import sys
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

CONFIG_PATH = Path.home() / ".glzr" / "glazewm" / "config.yaml"
MATUGEN_PATH = (
    Path.home() / ".config" / "windots" / "matugen" / "generated" / "glazewm.yaml"
)


def eprint(*args: Any, **kwargs: Any) -> None:
    """Cetak pesan error ke stderr."""
    print(*args, file=sys.stderr, **kwargs)


def get_yaml_instance() -> YAML:
    """Membuat konfigurasi ruamel.yaml."""
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml


def load_yaml_file(file_path: Path, yaml: YAML) -> dict[str, Any] | None:
    """Membaca file YAML menggunakan Pathlib."""
    if not file_path.exists():
        eprint(f"[ERROR] File tidak ditemukan: {file_path}")
        return None
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = yaml.load(f)
            return data if data is not None else {}
    except YAMLError as e:
        eprint(f"[ERROR] Gagal memparsing YAML pada {file_path}:\n{e}")
        return None
    except OSError as e:
        eprint(f"[ERROR] Tidak dapat membaca file {file_path}: {e}")
        return None


def save_yaml_file(file_path: Path, data: dict[str, Any], yaml: YAML) -> bool:
    """Menyimpan data kembali ke file YAML dengan aman."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as f:
            yaml.dump(data, f)
        return True
    except OSError as e:
        eprint(f"[ERROR] Gagal menyimpan ke {file_path}: {e}")
        return False


def get_nested_value(data: dict[str, Any], keys: list[str]) -> Any | None:
    """Mengambil nilai dari dictionary."""
    curr: Any = data
    for key in keys:
        if isinstance(curr, dict) and key in curr:
            curr = curr[key]
        else:
            return None
    return curr


def set_nested_value(data: dict[str, Any], keys: list[str], value: Any) -> bool:
    """Update nilai bertingkat pada dictionary, membuat key jika belum ada."""
    curr = data
    for key in keys[:-1]:
        if key not in curr or not isinstance(curr[key], dict):
            curr[key] = {}
        curr = curr[key]
    curr[keys[-1]] = value
    return True


def update_window_colors(
    config_data: dict[str, Any], matugen_data: dict[str, Any]
) -> bool:
    """
    Mengambil warna dari matugen_data dan memperbarui config_data
    tanpa merusak key lain (seperti `enabled: true`).
    """
    targets = [
        ("focused_window", ["window_effects", "focused_window", "border", "color"]),
        ("other_window", ["window_effects", "other_window", "border", "color"]),
    ]
    is_updated = False
    for name, path_keys in targets:
        # Ambil warna dari matugen
        new_color = get_nested_value(matugen_data, path_keys)
        if new_color is not None:
            set_nested_value(config_data, path_keys, new_color)
            is_updated = True
        else:
            eprint(
                f"[ERROR] Warna '{name}' tidak ditemukan di matugen.yaml (Dilewati)."
            )
    return is_updated


def main() -> None:
    yaml = get_yaml_instance()
    config_data = load_yaml_file(CONFIG_PATH, yaml)
    matugen_data = load_yaml_file(MATUGEN_PATH, yaml)
    if config_data is None or matugen_data is None:
        eprint("[ABORT] Proses dibatalkan karena ada kegagalan load file.")
        return
    updated = update_window_colors(config_data, matugen_data)
    if updated:
        if save_yaml_file(CONFIG_PATH, config_data, yaml):
            try:
                sp.run(
                    ["glazewm", "command", "wm-reload-config"],
                    check=True,
                    stdin=sp.DEVNULL,
                    stdout=sp.DEVNULL,
                )
            except (sp.CalledProcessError, FileNotFoundError) as e:
                eprint(f"[ERROR] Gagal menjalankan glazewm reload: {e}")
        else:
            eprint("[FAIL] Gagal menyimpan perubahan pada konfigurasi.")


if __name__ == "__main__":
    main()
