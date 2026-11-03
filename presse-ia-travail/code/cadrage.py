import re
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

corpus = pd.read_csv("corpus_filtre.csv", parse_dates=["date"])
corpus["titre"] = corpus["titre"].str.rsplit(" - ", n=1).str[0]
corpus["trimestre"] = corpus["date"].dt.to_period("Q")

# 1. Mots les plus fréquents dans les titres
vide = ["les","des","une","pour","dans","sur","par","avec","qui","que","est","pas",
        "plus","aux","ses","son","vos","votre","comment","entre","vers","sans","ou",
        "et","en","du","de","la","le","un","au","ce","se","ne","il","elle","nous",
        "ia","intelligence","artificielle","artificielles","l'ia","d'ia"]
vec = CountVectorizer(stop_words=vide, token_pattern=r"(?u)\b[a-zA-Zéèêàâîôûç]{4,}\b")
X = vec.fit_transform(corpus["titre"].str.lower())
freq = pd.Series(X.sum(axis=0).A1, index=vec.get_feature_names_out())
print(freq.sort_values(ascending=False).head(30))

# 2. Cadrages par dictionnaire
cadrages = {
    "menace emploi": r"supprim|dispara|remplac|menace|destruction|chômage|licenci",    "opportunité": r"opportunit|productivit|efficacit|innovation|booste|accélér|gain",
    "régulation": r"régul|\bloi\b|AI Act|règlement|encadr|CNIL|juridique",
    "dialogue social": r"syndic|dialogue social|négocia|CFDT|CGT|accord|partenaires sociaux",
    "compétences": r"formation|compétence|former|apprend",
}
for nom, motif in cadrages.items():
    corpus[nom] = corpus["titre"].str.contains(motif, case=False, regex=True)

part = corpus.groupby("trimestre")[list(cadrages)].mean() * 100
print(part.round(1))
print("\nPart totale du corpus (%) :")
print((corpus[list(cadrages)].mean() * 100).round(1))

part.plot(marker="o", figsize=(10, 5))
plt.title("Part des titres par cadrage (%), par trimestre")
plt.ylabel("% des titres")
plt.tight_layout()
plt.savefig("cadrages.png", dpi=150)
plt.show()