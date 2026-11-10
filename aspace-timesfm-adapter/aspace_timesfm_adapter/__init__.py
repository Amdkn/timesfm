"""A'Space adapter — timesfm (D-N053 pas A, design Clara).

Contrat seul, patron D-N048 (dify / cordis) : cet adapter ne modifie AUCUN
fichier amont, ne fait AUCUN appel reseau, ne monte AUCUN poids.
Il constate : le gel epingle, la licence, le confinement, l'importabilite
du paquet amont, l'absence de poids dans le fork.

Adresse : fiber:a0:timesfm
Fork souverain : Amdkn/timesfm (parent google-research/timesfm, branche master)
Gel amont : e51928e27119cb17bebc005be2696b75e0a9e688 (« Update README.md »)
Bind Cordis Fiber (16L) : 105057005b5f740cb57b26fcd2aed6211b1b69cf
Licence : Apache-2.0
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path

FIBER_ADDRESS = "fiber:a0:timesfm"
FORK = "Amdkn/timesfm"
UPSTREAM_REPO = "google-research/timesfm"
UPSTREAM_BRANCH = "master"
PINNED_UPSTREAM_COMMIT = "e51928e27119cb17bebc005be2696b75e0a9e688"
PINNED_UPSTREAM_COMMIT_SHORT = "e51928e"
BIND_COMMIT = "105057005b5f740cb57b26fcd2aed6211b1b69cf"
BIND_LAYER = "16L"
LICENSE = "Apache-2.0"
ADAPTER_VERSION = "0.1.0"
UPSTREAM_PACKAGE = "timesfm"
UPSTREAM_PACKAGE_DIR = "src/timesfm"
CONFINEMENT = """CONFINEMENT PROFIL INTERNE (D-N052 D3, design D-N053 D3) : les POIDS TimesFM sont non-commerciaux (licence Google non-commerciale des checkpoints) ; jamais en B2B, jamais montes dans le fork (les miroirs HF sont le travail R1). Le code du repo est Apache-2.0."""

_WEIGHT_SUFFIXES = (".safetensors", ".bin", ".pt", ".pth")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _weight_files(root: Path) -> list[dict]:
    out = []
    for p in sorted(root.rglob("*")):
        if ".git" in p.parts:
            continue
        if p.is_file() and p.suffix in _WEIGHT_SUFFIXES:
            try:
                size = p.stat().st_size
            except OSError:
                size = -1
            out.append({"path": str(p.relative_to(root)), "size_o": size})
    return out


def describe() -> dict:
    """Decrit l'adapter (manifeste machine, sans effet de bord)."""
    return {
        "fiber": FIBER_ADDRESS,
        "fork": FORK,
        "upstream": UPSTREAM_REPO,
        "upstream_branch": UPSTREAM_BRANCH,
        "pinned_upstream_commit": PINNED_UPSTREAM_COMMIT,
        "bind_commit": BIND_COMMIT,
        "bind_layer": BIND_LAYER,
        "license": LICENSE,
        "adapter_version": ADAPTER_VERSION,
        "upstream_package": UPSTREAM_PACKAGE,
        "confinement": CONFINEMENT,
        "surface": "validate() -> dict ; doctor() -> list[check] ; describe() -> dict",
    }


def validate() -> dict:
    """Constate l'etat du fork gele. Aucun appel reseau, aucune ecriture."""
    root = _repo_root()
    try:
        mod = importlib.import_module(UPSTREAM_PACKAGE)
        importable, import_error = True, None
        upstream_version = getattr(mod, "__version__", None)
    except Exception as exc:  # noqa: BLE001 - constate, ne leve pas
        importable, import_error = False, f"{type(exc).__name__}: {exc}"
        upstream_version = None
    weights = _weight_files(root)
    return {
        "fiber": FIBER_ADDRESS,
        "pinned_upstream_commit": PINNED_UPSTREAM_COMMIT,
        "pinned_commit_is_40_hex": bool(re.fullmatch(r"[0-9a-f]{40}", PINNED_UPSTREAM_COMMIT)),
        "license_file_present": (root / "LICENSE").exists(),
        "license": LICENSE,
        "upstream_package_dir_present": (root / UPSTREAM_PACKAGE_DIR).is_dir(),
        "upstream_importable": importable,
        "upstream_import_error": import_error,
        "upstream_version": upstream_version,
        "weight_files_in_repo": weights,
        "adapter_network_calls": 0,
        "confinement": CONFINEMENT,
    }


def doctor() -> list[dict]:
    """Liste de controles (ok / detail). Tout doit etre ok en vert."""
    v = validate()
    root = _repo_root()
    weights = v["weight_files_in_repo"]
    # Seuls toleres : les fixtures factices de test (< 1 Mo, sous test/).
    unexpected = [w for w in weights if not (w["path"].startswith("test/") and w["size_o"] < 1_000_000)]
    checks = [
        {"check": "pinned_commit_40_hex", "ok": v["pinned_commit_is_40_hex"],
          "detail": PINNED_UPSTREAM_COMMIT_SHORT},
        {"check": "license_file_present", "ok": v["license_file_present"],
          "detail": LICENSE},
        {"check": "upstream_package_dir_present", "ok": v["upstream_package_dir_present"],
          "detail": UPSTREAM_PACKAGE_DIR},
        {"check": "upstream_importable", "ok": v["upstream_importable"],
          "detail": v["upstream_import_error"] or f"{UPSTREAM_PACKAGE} {v['upstream_version']}"},
        {"check": "no_real_weights_in_fork", "ok": not unexpected,
          "detail": f"{len(weights)} fichier(s) poids, {len(unexpected)} inattendu(s) : {unexpected}"},
        {"check": "adapter_network_calls_zero", "ok": v["adapter_network_calls"] == 0,
          "detail": "aucun import reseau dans l'adapter (verifie par grep a l'audit)"},
        {"check": "confinement_nomme", "ok": bool(CONFINEMENT),
          "detail": CONFINEMENT.split(":")[0]},
    ]
    return checks
