import json
import re

def parse_json_column(cell):
    if not isinstance(cell, str):
        return []

    try:
        # Fix single quotes to double quotes
        fixed = re.sub(r"'", '"', cell)

        # Ensure property names are quoted
        fixed = re.sub(r'([{,])\s*([a-zA-Z_]+)\s*:', r'\\1 "\\2":', fixed)

        return json.loads(fixed)
    except Exception as e:
        print(f"[!] Erreur JSON: {e}")
        return []


def pretty_print_kv_list(data):
    if not isinstance(data, list):
        print("⚠️ Donnée non reconnue.")
        return
    for entry in data:
        print(" -", entry)

def calculate_growth_rate(json_list):
    try:
        values = [entry["value"] for entry in json_list if isinstance(entry, dict) and entry["value"] not in [None, 0]]
        if len(values) < 2:
            return 0
        return (values[-1] - values[0]) / values[0]
    except:
        return 0
