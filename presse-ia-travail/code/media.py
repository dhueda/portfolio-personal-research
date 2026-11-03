import pandas as pd
import matplotlib.pyplot as plt

corpus = pd.read_csv("corpus_filtre.csv", parse_dates=["date"])

# retirer " - Nom du média" à la fin des titres
corpus["titre"] = corpus["titre"].str.rsplit(" - ", n=1).str[0]

cadrages = {
    "menace emploi": r"supprim|dispara|remplac|menace|destruction|chômage|licenci",
    "opportunité": r"opportunit|productivit|efficacit|innovation|booste|accélér|gain",
    "régulation": r"régul|\bloi\b|AI Act|règlement|encadr|CNIL|juridique",
    "dialogue social": r"syndic|dialogue social|négocia|CFDT|CGT|accord|partenaires sociaux",
    "compétences": r"formation|compétence|former|apprend",
}
for nom, motif in cadrages.items():
    corpus[nom] = corpus["titre"].str.contains(motif, case=False, regex=True)

# 1. Comparaison des médias les plus présents
top = corpus["source"].value_counts().head(6).index
par_media = corpus[corpus["source"].isin(top)].groupby("source")[list(cadrages)].mean() * 100
print(corpus[corpus["source"].isin(top)]["source"].value_counts())
print(par_media.round(1))

par_media.plot(kind="bar", figsize=(10, 5))
plt.title("Part des titres par cadrage et par média (%)")
plt.ylabel("% des titres")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("cadrages_medias.png", dpi=150)

# 2. Vérification du dictionnaire : 10 titres au hasard par cadrage
for nom in ["menace emploi", "dialogue social"]:
    print(f"\n--- {nom} ---")
    for t in corpus[corpus[nom]]["titre"].sample(10, random_state=1):
        print("•", t)

hors_france = ["La Presse", "Radio-Canada", "Le Devoir", "Le Temps", "RTS", "RTBF", "Le Soir", "La Libre"]
n = corpus["source"].isin(hors_france).sum()
print(f"\nTitres de médias hors de France : {n} sur {len(corpus)} ({n/len(corpus)*100:.1f} %)")