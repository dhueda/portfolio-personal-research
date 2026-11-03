import pandas as pd
import matplotlib.pyplot as plt

corpus = pd.read_csv("corpus_filtre.csv", parse_dates=["date"])
corpus["titre"] = corpus["titre"].str.rsplit(" - ", n=1).str[0]
corpus["trimestre"] = corpus["date"].dt.to_period("Q")
corpus = corpus[corpus["trimestre"] < "2026Q4"]  # trimestre incomplet retiré

menace = r"supprim|dispara|remplac|menace|destruction|chômage|licenci"
plans = (r"plan social|plans sociaux|\bPSE\b|suppressions? de postes|suppressions? d'emplois"
         r"|postes? supprimés?|emplois? supprimés?|supprime \d|supprimer \d|supprimera \d"
         r"|réduction d'effectifs|réduire ses effectifs|restructuration|plan de départs|plan de licenciement")

corpus["menace"] = corpus["titre"].str.contains(menace, case=False, regex=True)
corpus["plans"] = corpus["titre"].str.contains(plans, case=False, regex=True)
corpus["menace_hors_plans"] = corpus["menace"] & ~corpus["plans"]

par_t = corpus.groupby("trimestre")[["menace", "menace_hors_plans", "plans"]].mean() * 100
print(par_t.round(1))
print("\nPart des titres menace qui citent un plan (%) :",
      round(corpus[corpus["menace"]]["plans"].mean() * 100, 1))

fig, ax = plt.subplots(figsize=(10, 5))
par_t["menace"].plot(ax=ax, marker="o", label="menace emploi")
par_t["menace_hors_plans"].plot(ax=ax, marker="o", linestyle="--", label="menace hors plans de suppression")
par_t["plans"].plot(ax=ax, marker="o", label="plans de suppression d'emplois")
ax.set_title("Menace pour l'emploi et plans de suppression d'emplois (% des titres)")
ax.set_ylabel("% des titres")
ax.legend()
plt.tight_layout()
plt.savefig("hypotheses.png", dpi=150)

print("\n--- plans ---")
sel = corpus[corpus["plans"]]
print(len(sel), "titres")
for t in sel["titre"].sample(min(10, len(sel)), random_state=1):
    print("•", t)