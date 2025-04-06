import pandas as pd
from score_utils import parse_json_column, pretty_print_kv_list, calculate_growth_rate

def display_company_score():
    df = pd.read_excel("data/mockup_agriculture_messy_keyvalue.xlsx")

    print("\nEntreprises disponibles :")
    for name in df["Nom PME"]:
        print("-", name)

    company_name = input("\nNom de la PME à évaluer ? ")
    row = df[df["Nom PME"] == company_name]

    if row.empty:
        print("⛔ PME non trouvée.")
        return

    row = row.squeeze()

    # Parse JSON fields
    ca_list = parse_json_column(row["Chiffres_Affaires"])
    ch_list = parse_json_column(row["Charges"])
    pp_list = parse_json_column(row["Prix_Produits"])
    pm_list = parse_json_column(row["Prix_Marche"])

    # === ECO1: Chiffres d'affaires + Charges ===
    ca_growth = calculate_growth_rate(ca_list)
    charge_growth = calculate_growth_rate(ch_list)

    score_eco1 = 0
    if ca_growth > 1.5:
        score_eco1 += 15
    elif ca_growth > 0.75:
        score_eco1 += 10
    elif ca_growth > 0.25:
        score_eco1 += 5
    elif ca_growth > 0:
        score_eco1 += 3
    else:
        score_eco1 += 0

    if charge_growth < -0.10:
        score_eco1 += 5
    elif charge_growth < -0.05:
        score_eco1 += 2

    # === ECO2: Valorisation (Produit vs Marché) ===
    score_eco2 = 0
    try:
        scores = []
        for prod, market in zip(pp_list, pm_list):
            if not isinstance(prod, dict) or not isinstance(market, dict): continue
            if market["price"] is None or market["price"] == 0: continue
            diff = (prod["price"] - market["price"]) / market["price"]
            if diff > 0.10:
                scores.append(7)
            elif diff > 0.05:
                scores.append(4)
            elif diff >= 0:
                scores.append(1)
            else:
                scores.append(0)
        score_eco2 = max(scores) if scores else 0
    except:
        score_eco2 = 0

    # === ECO3: Diversification ===
    score_eco3 = 0
    n_div = 0
    try:
        if int(row["Nb_produits"]) > 1: n_div += 1
        if int(row["Nb_sources"]) > 1: n_div += 1
        if int(row["Nb_circuits"]) > 1: n_div += 1
    except:
        pass

    if n_div == 0:
        score_eco3 = 0
    elif n_div == 1:
        score_eco3 = 2
    elif n_div == 2:
        score_eco3 = 4
    elif n_div == 3:
        score_eco3 = 7

    # === ECO4: Sécurisation ===
        
    score_eco4 = 0
    try:
        dep_score = 0
        assur_score = 0

        dep = float(row["Ratio_dependance"])
        if dep < 1.0:  # Any gain
            dep_score += 4
        if dep < 0.7:  # Significant gain
            dep_score += 3

        assur = float(row["Ratio_assurance"])
        if assur > 0.3:
            assur_score = 4
        elif assur > 0:
            assur_score = 2

        score_eco4 = min(dep_score + assur_score, 6)
    except:
        score_eco4 = 0


    total_score = score_eco1 + score_eco2 + score_eco3 + score_eco4

    print("\n💡 Résultats par critère :")
    print(f"🔹 ECO1 (CA & charges): {score_eco1}/20")
    print(f"🔹 ECO2 (Valorisation): {score_eco2}/7")
    print(f"🔹 ECO3 (Diversification): {score_eco3}/7")
    print(f"🔹 ECO4 (Sécurisation): {score_eco4}/6")
    print(f"\n✅ Score total: {total_score} / 40")
    
import matplotlib.pyplot as plt

def compare_all_scores():
    df = pd.read_excel("data/mockup_agriculture_messy_keyvalue.xlsx")
    results = []

    for _, row in df.iterrows():
        try:
            name = row["Nom PME"]
            ca = parse_json_column(row["Chiffres_Affaires"])
            ch = parse_json_column(row["Charges"])
            pp = parse_json_column(row["Prix_Produits"])
            pm = parse_json_column(row["Prix_Marche"])

            # === ECO1
            ca_growth = calculate_growth_rate(ca)
            ch_growth = calculate_growth_rate(ch)

            s1 = 0
            if ca_growth > 1.5: s1 += 15
            elif ca_growth > 0.75: s1 += 10
            elif ca_growth > 0.25: s1 += 5
            elif ca_growth > 0: s1 += 3
            if ch_growth < -0.10: s1 += 5
            elif ch_growth < -0.05: s1 += 2

            # === ECO2
            s2 = 0
            try:
                scores = []
                for prod, market in zip(pp, pm):
                    if not isinstance(prod, dict) or not isinstance(market, dict): continue
                    if market["price"] is None or market["price"] == 0: continue
                    diff = (prod["price"] - market["price"]) / market["price"]
                    if diff > 0.10: scores.append(7)
                    elif diff > 0.05: scores.append(4)
                    elif diff >= 0: scores.append(1)
                    else: scores.append(0)
                s2 = max(scores) if scores else 0
            except:
                s2 = 0

            # === ECO3
            n_div = 0
            try:
                if int(row["Nb_produits"]) > 1: n_div += 1
                if int(row["Nb_sources"]) > 1: n_div += 1
                if int(row["Nb_circuits"]) > 1: n_div += 1
            except: pass

            if n_div == 0: s3 = 0
            elif n_div == 1: s3 = 2
            elif n_div == 2: s3 = 4
            elif n_div == 3: s3 = 7

            # === ECO4
            try:
                dep_score = 0
                assur_score = 0
                dep = float(row["Ratio_dependance"])
                if dep < 1.0: dep_score += 4
                if dep < 0.7: dep_score += 3
                assur = float(row["Ratio_assurance"])
                if assur > 0.3: assur_score = 4
                elif assur > 0: assur_score = 2
                s4 = min(dep_score + assur_score, 6)
            except:
                s4 = 0

            total = s1 + s2 + s3 + s4
            results.append((name, total))
        except:
            continue

    # === PLOT ===
    results.sort(key=lambda x: x[1], reverse=True)
    names = [r[0] for r in results]
    scores = [r[1] for r in results]

    plt.figure(figsize=(12, 6))
    bars = plt.barh(names, scores, color="seagreen")
    plt.xlabel("Score / 40")
    plt.title("Comparaison des scores des entreprises")
    plt.gca().invert_yaxis()

    # Add labels
    for bar, score in zip(bars, scores):
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{score}", va='center')

    plt.tight_layout()
    plt.show()
