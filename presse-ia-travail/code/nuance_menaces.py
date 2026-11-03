import pandas as pd

corpus = pd.read_csv("corpus_filtre.csv", parse_dates=["date"])
corpus["titre"] = corpus["titre"].str.rsplit(" - ", n=1).str[0]
corpus["trimestre"] = corpus["date"].dt.to_period("Q")
corpus = corpus[corpus["trimestre"] < "2026Q4"]

menace = r"supprim|dispara|remplac|menace|destruction|chômage|licenci"
corpus["menace"] = corpus["titre"].str.contains(menace, case=False, regex=True)
m = corpus[corpus["menace"]].copy()

# titres sous forme de question
m["question"] = m["titre"].str.contains(r"\?", regex=True)

# démentis ou protections (liste volontairement simple)
dementi = (r"ne remplac|ne va pas|ne vont pas|ne supprim|ne détruir|pas remplac|pas supprim"
           r"|jamais|aucun licenci|sans licenci|sans suppression|protéger contre|contre les licenci"
           r"|plutôt qu'une|plutôt que de supprimer|pas de destruction|mythe|idée reçue|fantasme")
m["démenti"] = m["titre"].str.contains(dementi, case=False, regex=True)
m["affirmé"] = ~m["question"] & ~m["démenti"]

print("Titres de menace :", len(m))
print((m[["question", "démenti", "affirmé"]].mean() * 100).round(1))
print("\nPar trimestre (%) :")
print((m.groupby("trimestre")[["question", "démenti", "affirmé"]].mean() * 100).round(1))

for col in ["question", "démenti"]:
    print(f"\n--- {col} (10 titres) ---")
    sel = m[m[col]]
    for t in sel["titre"].sample(min(10, len(sel)), random_state=1):
        print("•", t)