import pandas as pd

corpus = pd.read_csv("corpus_filtre.csv")
corpus["titre"] = corpus["titre"].str.rsplit(" - ", n=1).str[0]
ech = corpus.sample(200, random_state=42)[["titre", "source"]].reset_index(drop=True)
for col in ["menace_emploi", "dialogue_social", "plans_suppression", "menace_niee"]:
    ech[col] = ""
ech.to_csv("echantillon_a_coder.csv", sep=";", index=False, encoding="utf-8-sig")