import pandas as pd
import matplotlib.pyplot as plt

corpus = pd.read_csv("corpus.csv")
corpus["date"] = pd.to_datetime(corpus["date"], utc=True, errors="coerce").dt.tz_localize(None)
corpus = corpus.dropna(subset=["date"])
print("avant filtre :", len(corpus))

# garder les titres qui parlent vraiment d'IA
motif = r"\bIA\b|[Ii]ntelligence artificielle|ChatGPT"
corpus = corpus[corpus["titre"].str.contains(motif, regex=True)]
corpus = corpus.drop_duplicates(subset=["titre", "source"])
print("après filtre :", len(corpus))

corpus.to_csv("corpus_filtre.csv", index=False)

# volume d'articles par mois
corpus["mois"] = corpus["date"].dt.to_period("M")
volume = corpus.groupby("mois").size()

volume.plot(kind="line", marker="o", figsize=(10, 5))
plt.title("Articles sur l'IA et le travail dans la presse francophone")
plt.xlabel("Mois")
plt.ylabel("Nombre d'articles")
plt.tight_layout()
plt.savefig("volume_mensuel.png", dpi=150)
plt.show()