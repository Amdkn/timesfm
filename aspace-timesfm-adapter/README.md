# A'Space adapter — timesfm

**Adresse :** `fiber:a0:timesfm` — D-N053 pas A (design Clara, dispatch D-N053).
**Fork souverain :** `Amdkn/timesfm` (parent `google-research/timesfm`, branche `master`).
**Gel amont :** `e51928e27119cb17bebc005be2696b75e0a9e688` (« Update README.md »).
**Bind Cordis Fiber (16L) :** `105057005b5f740cb57b26fcd2aed6211b1b69cf` — `aspace-plugin.json`, re-applique VERBATIM sur `main` au-dessus de l'adapter (F8 D2).
**Licence :** `Apache-2.0`.
**Version adapter :** 0.1.0 — contrat seul, patron D-N048 (dify / cordis).

## Ce que fait l'adapter

TimesFM : Time Series Foundation Model (Google Research), backends torch / flax / mlx. Poids non-commerciaux, confines au profil interne.

Surface : `validate()` (constate : gel, licence, importabilite amont, poids
presents dans le fork, zero appel reseau), `doctor()` (liste de controles),
`describe()` (manifeste machine). **Aucun fichier amont touche, aucun appel
reseau, aucun poids monte dans le fork.**

## Confinement

CONFINEMENT PROFIL INTERNE (D-N052 D3, design D-N053 D3) : les POIDS TimesFM sont non-commerciaux (licence Google non-commerciale des checkpoints) ; jamais en B2B, jamais montes dans le fork (les miroirs HF sont le travail R1). Le code du repo est Apache-2.0.

## Tests

```bash
python -m pytest aspace-timesfm-adapter/tests/test_smoke.py -v
```

Smoke : constantes (gel 40-hex, adresse fiber, licence), `validate()` vert,
`doctor()` tout ok, import amont, zero import reseau dans l'adapter.
La suite amont est celle du module au gel (voir la fiche d'adaptation :
`timesfm-ADAPTATION.md`, evidence D-N053/a/timesfm/).
