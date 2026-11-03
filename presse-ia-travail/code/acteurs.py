import pandas as pd
import matplotlib.pyplot as plt

corpus = pd.read_csv("corpus_filtre.csv", parse_dates=["date"])
corpus["titre"] = corpus["titre"].str.rsplit(" - ", n=1).str[0]
corpus["annee"] = corpus["date"].dt.year
corpus["trimestre"] = corpus["date"].dt.to_period("Q")
corpus = corpus[corpus["trimestre"] < "2026Q4"]

acteurs = {
    "syndicats": r"syndic|CGT|CFDT|CFE-CGC|CFTC|Solidaires|UNSA|Force ouvrière",
    "entreprises": r"entreprise|patron|dirigeant|PDG|\bDRH\b|employeur|Amazon|Microsoft|Google|OpenAI|IBM|Oracle|Allianz|HSBC|BNP|Société Générale|Orange|Samsung|banque|assureur",
    "pouvoirs publics": r"gouvernement|ministre|Macron|Assemblée|Sénat|Commission européenne|Bruxelles|Union européenne|pouvoirs publics|députés?|sénateurs?|DREETS|France Travail",
    "experts et études": r"étude|rapport|économiste|chercheur|expert|FMI|OCDE|\bOIT\b|Insee|McKinsey|Goldman|Dares|France Stratégie|Banque de France|sondage|baromètre",
}
for nom, motif in acteurs.items():
    corpus[nom] = corpus["titre"].str.contains(motif, case=False, regex=True)

menace = r"supprim|dispara|remplac|menace|destruction|chômage|licenci"
dialogue = r"dialogue social|négocia|accord|partenaires sociaux"
corpus["menace"] = corpus["titre"].str.contains(menace, case=False, regex=True)
corpus["dialogue"] = corpus["titre"].str.contains(dialogue, case=False, regex=True)

# 1. Place de chaque acteur, par année (% des titres)
part = corpus.groupby("annee")[list(acteurs)].mean() * 100
print("% des titres mentionnant chaque acteur (2026 : janvier à septembre)")
print(part.round(1))
print("\nNombre de titres par acteur :")
print(corpus[list(acteurs)].sum())

# 2. À quoi chaque acteur est associé
rows = []
for nom in acteurs:
    sel = corpus[corpus[nom]]
    rows.append({"acteur": nom, "n": len(sel),
                 "% menace emploi": round(sel["menace"].mean() * 100, 1),
                 "% dialogue social": round(sel["dialogue"].mean() * 100, 1)})
print("\n", pd.DataFrame(rows).set_index("acteur"))
print("\nRéférence, corpus entier : menace", round(corpus["menace"].mean() * 100, 1),
      "| dialogue", round(corpus["dialogue"].mean() * 100, 1))

# 3. Les syndicats : contestation ou négociation ?
contest = r"grève|mobilis|manifest|dénonc|alert|colère|conteste|réclam|exig|s'oppos|inquiét|craign|refus"
negoc = r"accord|négocia|dialogue|signent|signé|concertation|charte|protocole|encadr"
synd = corpus[corpus["syndicats"]].copy()
synd["contestation"] = synd["titre"].str.contains(contest, case=False, regex=True)
synd["négociation"] = synd["titre"].str.contains(negoc, case=False, regex=True)
print("\nTitres avec syndicats :", len(synd))
print((synd.groupby("annee")[["contestation", "négociation"]].mean() * 100).round(1))
print(synd.groupby("annee").size().rename("n par année"))

print("\n--- 10 titres avec syndicats ---")
for t in synd["titre"].sample(min(10, len(synd)), random_state=1):
    print("•", t)

part.plot(kind="bar", figsize=(10, 5))
plt.title("Acteurs mentionnés dans les titres (%), par année")
plt.ylabel("% des titres")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("acteurs.png", dpi=150)

dialogue_complet = r"syndic|dialogue social|négocia|CFDT|CGT|accord|partenaires sociaux"
d = corpus["titre"].str.contains(dialogue_complet, case=False, regex=True)
print("\nTitres dialogue social :", d.sum(),
      "dont avec syndicats :", (d & corpus["syndicats"]).sum())