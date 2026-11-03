import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

ech = pd.read_csv("echantillon_a_coder.csv", sep=";", encoding="utf-8-sig")

dico = {
    "menace_emploi": r"supprim|dispara|remplac|menace|destruction|chômage|licenci",
    "dialogue_social": r"syndic|dialogue social|négocia|CFDT|CGT|accord|partenaires sociaux",
    "plans_suppression": (r"plan social|plans sociaux|\bPSE\b|suppressions? de postes|suppressions? d'emplois"
        r"|postes? supprimés?|emplois? supprimés?|supprime \d|supprimer \d|supprimera \d"
        r"|réduction d'effectifs|réduire ses effectifs|restructuration|plan de départs|plan de licenciement"),
}

for var, motif in dico.items():
    manuel = pd.to_numeric(ech[var], errors="coerce").fillna(0).astype(int)
    auto = ech["titre"].str.contains(motif, case=False, regex=True).astype(int)
    print(f"\n=== {var} ===")
    print("codés 1 à la main :", manuel.sum(), "| trouvés par le dictionnaire :", auto.sum())
    print("précision :", round(precision_score(manuel, auto, zero_division=0), 2))
    print("rappel    :", round(recall_score(manuel, auto, zero_division=0), 2))
    print("F1        :", round(f1_score(manuel, auto, zero_division=0), 2))
    print("Faux positifs (dictionnaire oui, toi non) :")
    for t in ech[(auto == 1) & (manuel == 0)]["titre"].head(8):
        print("  •", t)
    print("Faux négatifs (toi oui, dictionnaire non) :")
    for t in ech[(auto == 0) & (manuel == 1)]["titre"].head(8):
        print("  •", t)

m = pd.to_numeric(ech["menace_emploi"], errors="coerce").fillna(0).astype(int) == 1
niee = pd.to_numeric(ech.loc[m, "menace_niee"], errors="coerce").fillna(0)
print(f"\nParmi {m.sum()} titres de menace codés à la main, {int(niee.sum())} nient la menace ({niee.mean()*100:.0f} %).")