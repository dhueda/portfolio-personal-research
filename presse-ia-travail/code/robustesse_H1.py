import pandas as pd

corpus = pd.read_csv("corpus_filtre.csv", parse_dates=["date"])
corpus["trimestre"] = corpus["date"].dt.to_period("Q")
corpus = corpus[corpus["trimestre"] < "2026Q4"]

print("Nombre de médias différents par trimestre :")
print(corpus.groupby("trimestre")["source"].nunique())

top = corpus["source"].value_counts().head(5).index
print("\nTitres par trimestre pour les 5 médias les plus présents :")
print(corpus[corpus["source"].isin(top)].groupby(["trimestre", "source"]).size().unstack(fill_value=0))