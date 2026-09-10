#!/usr/bin/env python3
"""Generate a source coverage audit for pension parameters."""

from __future__ import annotations

import datetime as dt
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PARAMETERS_DIR = ROOT / "openfisca_tunisia_pension" / "parameters" / "retraite"
VARIABLES_DIR = ROOT / "openfisca_tunisia_pension" / "variables"
JORTS_DIR = ROOT / "tmp" / "JORTs"
REPORT_PATH = ROOT / "reports" / "openfisca" / "pension_source_audit.md"
CANDIDATES_PATH = ROOT / "parameters_candidates" / "retraite_source_candidates.yml"
EXTERNAL_JORT_CACHE = ROOT.parent / "PDFs-legislation-tunisie" / "jort_cache.db"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LAW_RE = re.compile(r"(?:loi\s*)?(?:n[°º]\s*)?(\d{2,4})[-‑](\d+)", re.IGNORECASE)
PARAMETER_ACCESS_RE = re.compile(r"parameters\(period\)\.retraite\.([A-Za-z0-9_\.]+)")

KNOWN_TEXTS = {
    "1959-18": "Loi n° 59-18 du 5 février 1959, pensions civiles et militaires",
    "1960-33": "Loi n° 60-33 du 14 décembre 1960, invalidité/vieillesse/survie secteur non agricole",
    "1981-6": "Loi n° 81-6 du 12 février 1981, sécurité sociale secteur agricole",
    "1985-12": "Loi n° 85-12 du 5 mars 1985, pensions civiles et militaires secteur public",
    "2007-43": "Loi n° 2007-43 du 25 juin 2007, pensions public/privé/régimes spéciaux",
    "2019-37": "Loi n° 2019-37 du 30 avril 2019, relèvement âge retraite",
}

KNOWN_TEXT_TYPES = {
    "1959-18": "Loi",
    "1960-33": "Loi",
    "1981-6": "Loi",
    "1985-12": "Loi",
    "2007-43": "Loi",
    "2019-37": "Loi",
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream) or {}
    if not isinstance(data, dict):
        return {}
    return data


# Champs d'une référence structurée où un numéro de texte peut légitimement figurer.
# La `note` en est exclue : elle porte la localisation JORT, dont les plages de pages
# — « pp. 1312-1315 » — ont exactement la forme d'un numéro de loi et étaient comptées
# comme tel. Le rapport annonçait ainsi un « texte 1312-1315 » à résoudre.
CHAMPS_PORTEURS_DE_TEXTE = ("title", "href")


def flatten_reference(reference: Any) -> list[str]:
    if reference is None:
        return []
    if isinstance(reference, str):
        return [reference]
    if isinstance(reference, dict):
        refs: list[str] = []
        # Une référence structurée : on ne lit que les champs qui nomment un texte.
        if any(champ in reference for champ in CHAMPS_PORTEURS_DE_TEXTE):
            for champ in CHAMPS_PORTEURS_DE_TEXTE:
                if champ in reference:
                    refs.extend(flatten_reference(reference[champ]))
            return refs
        for value in reference.values():
            refs.extend(flatten_reference(value))
        return refs
    if isinstance(reference, list):
        refs = []
        for value in reference:
            refs.extend(flatten_reference(value))
        return refs
    return [str(reference)]


def collect_dates(value: Any) -> set[str]:
    dates: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key)
            if DATE_RE.match(key_text):
                dates.add(key_text)
            dates.update(collect_dates(nested))
    elif isinstance(value, list):
        for nested in value:
            dates.update(collect_dates(nested))
    return dates


def normalize_law_id(year_text: str, number_text: str) -> str:
    if len(year_text) == 2:
        year = int(year_text)
        full_year = 2000 + year if year < 30 else 1900 + year
    else:
        full_year = int(year_text)
    return f"{full_year}-{int(number_text)}"


def extract_laws(texts: list[str]) -> set[str]:
    laws: set[str] = set()
    for text in texts:
        for year, number in LAW_RE.findall(text):
            laws.add(normalize_law_id(year, number))
    return laws


def jort_numbers(law: str) -> tuple[str, str]:
    year, suffix = law.split("-", 1)
    short_number = f"{int(year) % 100}-{suffix}" if int(year) < 2000 else law
    return law, short_number


def describe_parameters() -> tuple[list[dict[str, Any]], Counter[str], Counter[str]]:
    rows: list[dict[str, Any]] = []
    regimes: Counter[str] = Counter()
    law_counts: Counter[str] = Counter()

    for path in sorted(PARAMETERS_DIR.rglob("*.yaml")):
        relative_path = path.relative_to(ROOT).as_posix()
        relative_parameter = path.relative_to(PARAMETERS_DIR).with_suffix("").as_posix()
        parts = relative_parameter.split("/")
        regime = parts[0] if parts else "retraite"
        data = load_yaml(path)
        metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
        references = flatten_reference(metadata.get("reference"))
        laws = sorted(extract_laws(references))
        for law in laws:
            law_counts[law] += 1

        has_scale_or_values = "values" in data or "brackets" in data
        if has_scale_or_values:
            regimes[regime] += 1

        rows.append(
            {
                "path": relative_path,
                "parameter": f"retraite.{relative_parameter.replace('/', '.')}",
                "regime": regime,
                "description": data.get("description", ""),
                "has_values": has_scale_or_values,
                "has_reference": bool(references),
                "references": references,
                "laws": laws,
                "dates": sorted(collect_dates(data)),
                "unit": metadata.get("unit") or metadata.get("rate_unit") or data.get("unit"),
            }
        )

    return rows, regimes, law_counts


def describe_variables() -> dict[str, list[str]]:
    accesses: dict[str, set[str]] = defaultdict(set)
    for path in sorted(VARIABLES_DIR.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for access in PARAMETER_ACCESS_RE.findall(text):
            accesses[path.name].add(f"retraite.{access}")
    return {key: sorted(value) for key, value in sorted(accesses.items())}


def describe_local_jorts() -> list[dict[str, Any]]:
    rows = []
    if not JORTS_DIR.exists():
        return rows
    for path in sorted(JORTS_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8", errors="replace")
        articles = re.findall(r"(?im)^\s*(?:Art\.|Article)\s+([^–\-\n]+)", text)
        primary_laws = sorted(extract_laws([path.name, "\n".join(text.splitlines()[:4])]))
        cited_laws = sorted(extract_laws([text[:2000]]))
        rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "line_count": text.count("\n") + 1,
                "primary_laws": primary_laws,
                "cited_laws": cited_laws,
                "articles": [article.strip() for article in articles],
            }
        )
    return rows


def query_external_jort_cache(laws: set[str]) -> dict[str, list[dict[str, Any]]]:
    matches: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if not EXTERNAL_JORT_CACHE.exists():
        return matches

    query = """
        SELECT type, numero, titre, date_signature, date_publication,
               jort_annee, jort_numero, pages, pdf_fr, pdf_ar
        FROM textes
        WHERE numero IN (?, ?)
        ORDER BY date_signature, recid
    """
    connection = sqlite3.connect(f"file:{EXTERNAL_JORT_CACHE}?mode=ro", uri=True)
    try:
        for law in sorted(laws):
            rows = connection.execute(query, jort_numbers(law)).fetchall()
            expected_type = KNOWN_TEXT_TYPES.get(law)
            if expected_type:
                rows = [row for row in rows if row[0] == expected_type] or rows
            for row in rows:
                matches[law].append(
                    {
                        "type": row[0],
                        "numero": row[1],
                        "titre": row[2],
                        "date_signature": row[3],
                        "date_publication": row[4],
                        "jort_annee": row[5],
                        "jort_numero": row[6],
                        "pages": row[7],
                        "pdf_fr": row[8],
                        "pdf_ar": row[9],
                    }
                )
    finally:
        connection.close()
    return matches


def best_jort_match(law: str, matches: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not matches:
        return None
    expected_type = KNOWN_TEXT_TYPES.get(law)
    if expected_type:
        for match in matches:
            if match["type"] == expected_type:
                return match
    return matches[0]


def make_markdown(
    parameter_rows: list[dict[str, Any]],
    regimes: Counter[str],
    law_counts: Counter[str],
    variable_accesses: dict[str, list[str]],
    local_jorts: list[dict[str, Any]],
    jort_matches: dict[str, list[dict[str, Any]]],
) -> str:
    value_rows = [row for row in parameter_rows if row["has_values"]]
    referenced_rows = [row for row in value_rows if row["has_reference"]]
    unreferenced_rows = [row for row in value_rows if not row["has_reference"]]
    multi_date_rows = [row for row in value_rows if len(row["dates"]) > 1]

    lines = [
        "# Audit sources retraite OpenFisca Tunisia Pension",
        "",
        f"Généré le {dt.date.today().isoformat()} par `scripts/generate_pension_source_audit.py`.",
        "",
        "## Synthèse",
        "",
        f"- Fichiers paramètres retraite: {len(parameter_rows)}",
        f"- Paramètres avec valeurs ou barèmes: {len(value_rows)}",
        f"- Paramètres avec référence: {len(referenced_rows)} / {len(value_rows)}",
        f"- Paramètres sans référence: {len(unreferenced_rows)} / {len(value_rows)}",
        f"- Paramètres multi-dates: {len(multi_date_rows)}",
        f"- Textes JORT locaux: {len(local_jorts)}",
        "",
        "## Couverture par régime",
        "",
        "| Régime | Paramètres avec valeurs |",
        "| --- | ---: |",
    ]

    for regime, count in sorted(regimes.items()):
        lines.append(f"| `{regime}` | {count} |")

    lines.extend(["", "## Textes cités dans les références", ""])
    if law_counts:
        lines.extend(["| Texte | Occurrences paramètres | Statut |", "| --- | ---: | --- |"])
        for law, count in sorted(law_counts.items()):
            title = KNOWN_TEXTS.get(law, "Texte cité par les paramètres")
            status_parts = []
            if any(law in row["primary_laws"] for row in local_jorts):
                status_parts.append("texte local")
            first_match = best_jort_match(law, jort_matches.get(law, []))
            if first_match:
                status_parts.append(f"JORT {first_match['jort_annee']}/{first_match['jort_numero']}")
            if law in KNOWN_TEXTS:
                status_parts.append("texte pivot")
            status = ", ".join(status_parts) or "à résoudre"
            lines.append(f"| `{law}` - {title} | {count} | {status} |")
    else:
        lines.append("Aucun numéro de loi détecté dans les métadonnées de référence.")

    lines.extend(["", "## Textes JORT locaux", ""])
    if local_jorts:
        lines.extend(["| Fichier | Lois détectées | Articles détectés |", "| --- | --- | --- |"])
        for row in local_jorts:
            primary = ", ".join(f"`{law}`" for law in row["primary_laws"]) or "-"
            cited = ", ".join(f"`{law}`" for law in row["cited_laws"] if law not in row["primary_laws"])
            laws = primary if not cited else f"{primary}; cite {cited}"
            articles = ", ".join(row["articles"][:12]) or "-"
            lines.append(f"| `{row['path']}` | {laws} | {articles} |")
    else:
        lines.append("Aucun texte JORT local trouvé dans `tmp/JORTs`.")

    lines.extend(["", "## Paramètres sans référence", ""])
    if unreferenced_rows:
        lines.extend(["| Paramètre | Description | Dates |", "| --- | --- | --- |"])
        for row in unreferenced_rows:
            dates = ", ".join(row["dates"]) or "-"
            lines.append(f"| `{row['parameter']}` | {row['description']} | {dates} |")
    else:
        lines.append("Tous les paramètres avec valeurs ont au moins une référence.")

    lines.extend(["", "## Paramètres multi-dates à relier finement", ""])
    if multi_date_rows:
        lines.extend(["| Paramètre | Dates | Lois citées |", "| --- | --- | --- |"])
        for row in multi_date_rows:
            dates = ", ".join(row["dates"])
            laws = ", ".join(f"`{law}`" for law in row["laws"]) or "-"
            lines.append(f"| `{row['parameter']}` | {dates} | {laws} |")
    else:
        lines.append("Aucun paramètre multi-dates détecté.")

    lines.extend(["", "## Accès aux paramètres depuis les variables", ""])
    if variable_accesses:
        lines.extend(["| Fichier | Paramètres retraite accédés |", "| --- | --- |"])
        for filename, accesses in variable_accesses.items():
            joined = ", ".join(f"`{access}`" for access in accesses)
            lines.append(f"| `{filename}` | {joined} |")
    else:
        lines.append("Aucun accès `parameters(period).retraite.*` détecté.")

    lines.extend(["", "## Recommandations", ""])
    lines.extend(
        [
            "- Ajouter des références aux paramètres RSA et aux accessoires/pensions minimales avant toute correction de valeur.",
            "- Promouvoir le texte `2007-43` depuis `tmp/JORTs` vers un emplacement de sources documenté si le dépôt doit conserver les textes pivots.",
            "- Résoudre prioritairement les textes `1959-18`, `1960-33`, `1981-6`, `1985-12` et `2019-37` dans le cache JORT ou dans le corpus législatif externe.",
            "- Traiter les paramètres multi-dates avec une référence par date d'effet, car les dates OpenFisca ne coïncident pas toujours avec la date de signature du texte.",
        ]
    )

    return "\n".join(lines) + "\n"


def make_candidates(
    parameter_rows: list[dict[str, Any]],
    local_jorts: list[dict[str, Any]],
    jort_matches: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    value_rows = [row for row in parameter_rows if row["has_values"]]
    laws = sorted({law for row in parameter_rows for law in row["laws"]})
    local_laws = sorted({law for row in local_jorts for law in row["primary_laws"]})
    return {
        "metadata": {
            "generated_by": "scripts/generate_pension_source_audit.py",
            "generated_at": dt.date.today().isoformat(),
            "needs_review": True,
            "scope": "openfisca_tunisia_pension.parameters.retraite",
        },
        "coverage": {
            "parameters_with_values": len(value_rows),
            "parameters_with_reference": sum(1 for row in value_rows if row["has_reference"]),
            "parameters_without_reference": [row["parameter"] for row in value_rows if not row["has_reference"]],
            "local_jort_laws": local_laws,
        },
        "law_candidates": {
            law: {
                "title": KNOWN_TEXTS.get(law),
                "local_texts": [row["path"] for row in local_jorts if law in row["primary_laws"]],
                "jort_cache_matches": jort_matches.get(law, []),
                "parameters": [row["parameter"] for row in parameter_rows if law in row["laws"]],
            }
            for law in laws
        },
        "parameter_candidates": [
            {
                "parameter": row["parameter"],
                "description": row["description"],
                "dates": row["dates"],
                "laws": row["laws"],
                "references": row["references"],
                "needs_review": True,
            }
            for row in value_rows
        ],
    }


def main() -> None:
    parameter_rows, regimes, law_counts = describe_parameters()
    variable_accesses = describe_variables()
    local_jorts = describe_local_jorts()
    all_laws = set(law_counts) | {law for row in local_jorts for law in row["primary_laws"]}
    jort_matches = query_external_jort_cache(all_laws)

    REPORT_PATH.write_text(
        make_markdown(
            parameter_rows,
            regimes,
            law_counts,
            variable_accesses,
            local_jorts,
            jort_matches,
        ),
        encoding="utf-8",
    )
    CANDIDATES_PATH.write_text(
        yaml.safe_dump(
            make_candidates(parameter_rows, local_jorts, jort_matches),
            allow_unicode=True,
            sort_keys=False,
            width=100,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
