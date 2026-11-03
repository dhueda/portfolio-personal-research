import feedparser
import pandas as pd
from urllib.parse import quote

def recuperer(requete, debut, fin):
    q = f"{requete} after:{debut} before:{fin}"
    url = f"https://news.google.com/rss/search?q={quote(q)}&hl=fr&gl=FR&ceid=FR:fr"
    flux = feedparser.parse(url)
    lignes = []
    for e in flux.entries:
        lignes.append({
            "titre": e.title,
            "date": e.published,
            "source": e.source.title if "source" in e else None,
            "lien": e.link,
            "requete": requete,
        })
    return pd.DataFrame(lignes)

df = recuperer("intelligence artificielle emploi", "2025-01-01", "2025-02-01")
import time

requetes = [
    "intelligence artificielle emploi",
    "intelligence artificielle travail",
    "IA syndicats",
    "IA dialogue social",
    "IA salariés",
]

mois = pd.date_range("2024-01-01", "2026-11-01", freq="MS")
morceaux = []

for requete in requetes:
    for i in range(len(mois) - 1):
        debut = mois[i].strftime("%Y-%m-%d")
        fin = mois[i + 1].strftime("%Y-%m-%d")
        morceaux.append(recuperer(requete, debut, fin))
        time.sleep(1)  # pause pour ne pas surcharger le serveur
    print("terminé :", requete)

corpus = pd.concat(morceaux, ignore_index=True)
corpus["date"] = pd.to_datetime(corpus["date"], errors="coerce")
corpus = corpus.drop_duplicates(subset="lien")
corpus.to_csv("corpus.csv", index=False)
print(corpus.shape)
print(corpus["source"].value_counts().head(15))