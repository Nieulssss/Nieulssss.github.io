"""
Optimisation de la production agroalimentaire par programmation linéaire.

Ce script maximise le bénéfice mensuel d'une usine en tenant compte des contraintes de matières premières, machines, personnel et demande du marché.
Utilise la bibliothèque PuLP pour la modélisation et la résolution.

Entrées utilisateur :
- Coefficients de marché
- Objectifs de production
- Prix de vente
- Coûts des matières premières
- Salaires et effectifs

Sorties :
- Quantités à produire
- Ressources nécessaires
- Pertes et coûts
- Bénéfice maximal

Dépendances : pulp, math
"""
from pulp import *
from math import *

class Produit:
    """
    Classe représentant un produit fini.
    Attributs:
        nom (str): Nom du produit.
        prix_vente (float): Prix de vente du produit.
        recettes (dict): Recettes nécessaires pour produire le produit.
        poids_final (float): Poids final du produit.
    """
    def __init__(self, nom, prix_vente, recettes, poids_final):
        self.nom = nom
        self.prix_vente = prix_vente
        self.recettes = recettes
        self.poids_final = poids_final

class Machine:
    """
    Classe représentant une machine de production.
    Attributs:
        nom (str): Nom de la machine.
        capacite (dict): Capacité de la machine pour chaque type de matière.
        cout_mensuel (float): Coût mensuel de la machine.
        nb_ouvriers (int): Nombre d'ouvriers nécessaires pour faire fonctionner la machine.
    """
    def __init__(self, nom, capacite, cout_mensuel, nb_ouvriers):
        self.nom = nom
        self.capacite = capacite
        self.cout_mensuel = cout_mensuel
        self.nb_ouvriers = nb_ouvriers

class Carcasse:
    """
    Classe représentant une carcasse d'animal.
    Attributs:
        nom (str): Nom de l'animal.
        poids (float): Poids de la carcasse.
        conversion (dict): Conversion de la carcasse en matières premières.
        cout_kg (float): Coût au kilogramme de la carcasse.
    """
    def __init__(self, nom, poids, conversion, cout_kg):
        self.nom = nom
        self.poids = poids
        self.conversion = conversion
        self.cout_kg = cout_kg

class Bobine:
    """
    Classe représentant une bobine de matière.
    Attributs:
        nom (str): Nom de la bobine.
        poids (float): Poids de la bobine.
        cout_kg (float): Coût au kilogramme de la bobine.
    """
    def __init__(self, nom, poids, cout_kg):
        self.nom = nom
        self.poids = poids
        self.cout_kg = cout_kg

def saisie_minmax(min: float, max: float) -> float:
    """
    Demande à l'utilisateur un nombre flottant entre min et max (inclus).
    Redemande tant que la valeur n'est pas valide.

    Args:
        min (float): Valeur minimale acceptée.
        max (float): Valeur maximale acceptée.

    Returns:
        float: Valeur saisie par l'utilisateur, comprise entre min et max.
    """
    result = float(input())
    while result < min or result > max:
        result = float(input(f"Entrez nombre entre {min} et {max}"))
    return result

# Entrée des coefficients des marchés
def saisir_coefficients():
    """
    Demande à l'utilisateur de saisir les coefficients de marché avec validation des entrées.
    
    - Les coefficients doivent être positifs et entre 0 et 2
    
    Returns:
        dict: Dictionnaire des coefficients validés
    """
    print("Entrer coefficients entre 0 et 2\n")
    coef = {}
    print("Coefficient cuisses de poulet\n")
    coef["Cuisses"] = saisie_minmax(0,2)
    print("Coefficient tranches de jambon\n")
    coef["Jambon"] = saisie_minmax(0,2)
    print("Coefficient pate de porc\n")
    coef["Pate"] = saisie_minmax(0,2)
    print("Coefficient terrines de volaille\n")
    coef["Terrines"] = saisie_minmax(0,2)
    print("Coefficient mousses de canard\n")
    coef["Mousses"] = saisie_minmax(0,2)
    return coef

def saisie_objectif_prod():
    """
    Demande à l'utilisateur de saisir l'objectif de production avec validation des entrées.
    
    - L'objectif doit être positif et entre 0 et 100
    
    Returns:
        float: Objectif de production validé
    """
    print("Entrer objectif de production en pourcentage entre 0 et 100\n")
    objectif = {}
    print("Objectif cuisses de poulet)\n")
    objectif["Cuisses"] = saisie_minmax(0,100) / 100
    print("Objectif tranches de jambon\n")
    objectif["Jambon"] = saisie_minmax(0,100) / 100
    print("Objectif pate de porc\n")
    objectif["Pate"] = saisie_minmax(0,100) / 100
    print("Objectif terrines de volaille\n")
    objectif["Terrines"] = saisie_minmax(0,100) / 100
    print("Objectif mousses de canard\n")
    objectif["Mousses"] = saisie_minmax(0,100) / 100
    return objectif

# === Données ===

# Demande maximale du marché
def calcul_demande():
    """
    Calcule la demande maximale du marché pour chaque produit en fonction des coefficients saisis par l'utilisateur.
    Returns:
        dict: Un dictionnaire contenant la demande maximale pour chaque produit, calculée en multipliant les coefficients par 
            les valeurs de base.
            Les produits incluent "Cuisses", "Jambon", "Pate", "Terrines", "Mousses".
    """
    coef = saisir_coefficients()  # Appel de la fonction pour saisir les coefficients
    demande_max = {
        "Cuisses": 250000 * coef["Cuisses"],
        "Jambon": 1250000 * coef["Jambon"],
        "Pate": 10000000 * coef["Pate"],
        "Terrines": 3750000 * coef["Terrines"],
        "Mousses": 900000 * coef["Mousses"]
    }
    return demande_max

# Prix de vente des produits finis
def saisie_prix_vente():
    """
    Demande à l'utilisateur de saisir les prix de vente des produits finis.
    Returns:
        dict: Un dictionnaire contenant les prix de vente pour chaque produit.
              Les produits incluent "Cuisses", "Jambon", "Pate", "Terrines", "Mousses".
    """
    prix_vente = {"Cuisses": 5.2, "Jambon": 3.9, "Pate": 2.1, "Terrines": 3.2, "Mousses": 4.4}
    rep = input("Modifier prix de vente ? O pour oui sinon entrez autre")
    if rep == "O":
        prix_vente["Cuisses"] = saisie_minmax(0,10)
        prix_vente["Jambon"] = saisie_minmax(0,10)
        prix_vente["Pate"] = saisie_minmax(0,10)
        prix_vente["Terrines"] = saisie_minmax(0,10)
        prix_vente["Mousses"] = saisie_minmax(0,10)
    return prix_vente

def saisie_cout_matieres():
    # Coût par type de matière première (au kg)
    couts_matieres = {"porc": 2.0115, "poulet": 2.97, "canard": 4.428, "plastique": 5.427, "fer": 2.214}
    rep = input("Modifier coût des carcasses et bobines ? O pour oui sinon entrez autre")
    if rep == "O":
        couts_matieres["porc"] = saisie_minmax(0,10)
        couts_matieres["poulet"] = saisie_minmax(0,10)
        couts_matieres["canard"] = saisie_minmax(0,10)
        couts_matieres["plastique"] = saisie_minmax(0,10)
        couts_matieres["fer"] = saisie_minmax(0,10)
    return couts_matieres
    
def saisie_personnel():

    # Salaires
    salaires = {"Ouvriers": 1800, "Agents_Maitrise": 2100, "Cadres_Moyens": 3600, "Commerciaux": 1000, 
                "Assistants_Commerciaux": 1700, "Employes": 1800, "Dirigeants": 18000}
    print("Nombre de commerciaux")
    nb_commerciaux = saisie_minmax(0, 100)
    print("Entrer salaires des ouvriers")
    salaires["Ouvriers"] = saisie_minmax(0,10000)
    

    return salaires, nb_commerciaux

personnel = saisie_personnel()
salaires = personnel[0]
nb_commerciaux = personnel[1]
couts_matieres = saisie_cout_matieres()
prix_vente = saisie_prix_vente()
demande_max = calcul_demande()
objectif = saisie_objectif_prod()


# === Produits ===
Cuisses = Produit("Cuisses", prix_vente["Cuisses"], {"cuisse": 0.512, "plastique": 0.064}, 0.512)
Jambon = Produit("Jambon", prix_vente["Jambon"], {"muscles": 0.180, "plastique": 0.073}, 0.180)
Pate = Produit("Pate", prix_vente["Pate"], {"chair_porc": 0.094, "fer": 0.030}, 0.098)
Terrines = Produit("Terrines", prix_vente["Terrines"], {"chair_porc": 0.101, "chair_poulet": 0.030, "chair_canard": 0.020, "fer": 0.080}, 0.156)
Mousses = Produit("Mousses", prix_vente["Mousses"], {"chair_porc": 0.080, "poitrail_canard": 0.045, "chair_canard": 0.040, "plastique": 0.056}, 0.180)

# === Machines ===
Decoupe = Machine("Découpe", {"porc": 60000, "poulet": 45000, "canard": 45000}, 4000, 2)
Broyage = Machine("Broyage", 75000, 3000, 1)
Cuisson = Machine("Cuisson", {"Jambon": 32750, "Pate": 54000, "Terrines": 45000, "Mousses": 100000}, 8000, 3)
Emballage = Machine("Emballage", 40000, 7500, 3)

# === Carcasses ===
Porc = Carcasse("Porc", 100, {"muscles": 15, "chair_porc": 62}, couts_matieres["porc"])
Poulet = Carcasse("Poulet", 2, {"cuisse": 0.64, "chair_poulet": 0.62}, couts_matieres["poulet"])
Canard = Carcasse("Canard", 3, {"poitrail_canard": 0.42, "chair_canard": 1.62}, couts_matieres["canard"])

# === Bobines ===
Fer = Bobine("Fer", 60, couts_matieres["fer"])
Plastique = Bobine("Plastique", 50, couts_matieres["plastique"])


# === Problème ===

problem = LpProblem("Maximisation_du_Benefice", LpMaximize)

# Variables de production
x = {
    p: LpVariable(f"x_{p}", cat="Integer")
    for p in prix_vente
}

# Variables de machines
m_decoupe = LpVariable("m_decoupe", cat="Integer")
m_broyage = LpVariable("m_broyage", cat="Integer")
m_cuisson = LpVariable("m_cuisson", cat="Integer")
m_emballage = LpVariable("m_emballage", cat="Integer")

# Variables de carcasses et bobines
carcasses = {
    "porc": LpVariable("carcasses_porc", cat="Continuous"),
    "poulet": LpVariable("carcasses_poulet", cat="Continuous"),
    "canard": LpVariable("carcasses_canard", cat="Continuous")
}
bobines = {
    "plastique": LpVariable("bobines_plastique", cat="Continuous"),
    "fer": LpVariable("bobines_fer", cat="Continuous")
}

# === Variables de pertes ===
pertes = {
    "chair_porc": LpVariable("pertes_chair_porc", cat="Continuous"),
    "muscles_porc": LpVariable("pertes_muscles_porc", cat="Continuous"),
    "poitrail_canard": LpVariable("pertes_poitrail_canard", cat="Continuous"),
    "chair_canard": LpVariable("pertes_chair_canard", cat="Continuous"),
    "chair_poulet": LpVariable("pertes_chair_poulet", cat="Continuous"),
    "cuisse_poulet": LpVariable("pertes_cuisse_poulet", cat="Continuous")
}

# Variables de personnel
nb_agents_maitrise = LpVariable("nb_agents_maitrise", cat="Integer")
nb_cadres = LpVariable("nb_cadres", cat="Integer")
nb_employes = LpVariable("nb_employes", cat="Integer")
nb_assistants = LpVariable("nb_assistants", cat="Integer")

# === Fonction objectif ===
revenu = lpSum([x[p] * prix_vente[p] for p in x])

# Calcul du coût total des matières premières
cout_matieres = (
    carcasses["porc"] * Porc.poids * Porc.cout_kg +
    carcasses["poulet"] * Poulet.poids * Poulet.cout_kg +
    carcasses["canard"] * Canard.poids * Canard.cout_kg +
    bobines["plastique"] * Plastique.poids * Plastique.cout_kg +
    bobines["fer"] * Fer.poids * Fer.cout_kg
)

# Calcul du coût total des machines
cout_mensuel_total = (
    m_decoupe * Decoupe.cout_mensuel +
    m_broyage * Broyage.cout_mensuel +
    m_cuisson * Cuisson.cout_mensuel +
    m_emballage * Emballage.cout_mensuel
)

# Matières premières nécessaires pour produire une quantité donnée de chaque produit
besoin_chair_porc = (
    x["Pate"] * Pate.recettes["chair_porc"] +
    x["Terrines"] * Terrines.recettes["chair_porc"] +
    x["Mousses"] * Mousses.recettes["chair_porc"]
)

besoin_muscles_porc = x["Jambon"] * Jambon.recettes["muscles"]

besoin_chair_poulet = x["Terrines"] * Terrines.recettes["chair_poulet"]
besoin_cuisse_poulet = x["Cuisses"] * Cuisses.recettes["cuisse"]

besoin_chair_canard = (
    x["Terrines"] * Terrines.recettes["chair_canard"] +
    x["Mousses"] * Mousses.recettes["chair_canard"]
)

besoin_poitrail_canard = x["Mousses"] * Mousses.recettes["poitrail_canard"]

besoin_plastique = (
    x["Cuisses"] * Cuisses.recettes["plastique"] +
    x["Jambon"] * Jambon.recettes["plastique"] +
    x["Mousses"] * Mousses.recettes["plastique"]
)

besoin_fer = (
    x["Pate"] * Pate.recettes["fer"] +
    x["Terrines"] * Terrines.recettes["fer"]
)

# Calcul des ressources disponibles à partir des carcasses et des bobines nécessaires
disponible_chair_porc = carcasses["porc"] * Porc.conversion["chair_porc"]
disponible_muscles_porc = carcasses["porc"] * Porc.conversion["muscles"]

disponible_chair_poulet = carcasses["poulet"] * Poulet.conversion["chair_poulet"]
disponible_cuisse_poulet = carcasses["poulet"] * Poulet.conversion["cuisse"]

disponible_chair_canard = carcasses["canard"] * Canard.conversion["chair_canard"]
disponible_poitrail_canard = carcasses["canard"] * Canard.conversion["poitrail_canard"]

# Calcul des pertes pour chaque matière première
perte_chair_porc = disponible_chair_porc - besoin_chair_porc
perte_muscles_porc = disponible_muscles_porc - besoin_muscles_porc

perte_chair_poulet = disponible_chair_poulet - besoin_chair_poulet
perte_cuisse_poulet = disponible_cuisse_poulet - besoin_cuisse_poulet

perte_chair_canard = disponible_chair_canard - besoin_chair_canard
perte_poitrail_canard = disponible_poitrail_canard - besoin_poitrail_canard

# Calcul des pertes en valeur monétaire
cout_pertes = (
    perte_chair_porc / (Porc.conversion["chair_porc"] / Porc.poids) * Porc.cout_kg +
    perte_muscles_porc / (Porc.conversion["muscles"] / Porc.poids) * Porc.cout_kg +
    perte_chair_poulet / (Poulet.conversion["chair_poulet"] / Poulet.poids) * Poulet.cout_kg +
    perte_cuisse_poulet / (Poulet.conversion["cuisse"] / Poulet.poids) * Poulet.cout_kg +
    perte_chair_canard / (Canard.conversion["chair_canard"] / Canard.poids) * Canard.cout_kg +
    perte_poitrail_canard / (Canard.conversion["poitrail_canard"] / Canard.poids) * Canard.cout_kg
) * 1000

# Calcul du nombre d'ouvriers nécessaire
nb_ouvriers = (
    m_decoupe * Decoupe.nb_ouvriers +
    m_broyage * Broyage.nb_ouvriers +
    m_cuisson * Cuisson.nb_ouvriers +
    m_emballage * Emballage.nb_ouvriers
)

# Calcul du coût total des salaires
cout_salaries = (
    nb_ouvriers * salaires["Ouvriers"] +
    nb_agents_maitrise * salaires["Agents_Maitrise"] +
    nb_cadres * salaires["Cadres_Moyens"] +
    nb_commerciaux * salaires["Commerciaux"] +
    nb_assistants * salaires["Assistants_Commerciaux"] +
    nb_employes * salaires["Employes"] +
    salaires["Dirigeants"]
)

# Calcul du bénéfice
problem += revenu - cout_matieres - cout_mensuel_total - cout_pertes - cout_salaries, "Bénéfice_net"

# === Contraintes ===

# Contraintes de demande maximale pour chaque produit
for prod in demande_max:
    problem += x[prod] <= demande_max[prod] * objectif[prod], f"Demande_{prod}"

# Limite totale de machines
problem += m_decoupe + m_broyage + m_cuisson + m_emballage <= 35, "Limite_machines"

# Calcul du nombre machines de découpe nécessaires
besoin_decoupe = (
    carcasses["porc"] * 100 / Decoupe.capacite["porc"] +
    carcasses["poulet"] * 2 / Decoupe.capacite["poulet"]  +
    carcasses["canard"] * 3 / Decoupe.capacite["canard"]
)
problem += besoin_decoupe <= m_decoupe, "Capacite_decoupe"

# Calcul du nombre machines de broyage nécessaires
besoin_broyage = (
    x["Pate"] * Pate.poids_final +
    x["Terrines"] * Terrines.poids_final +
    x["Mousses"] * Mousses.poids_final
) / Broyage.capacite

problem += besoin_broyage <= m_broyage, "Capacite_broyage"

# Calcul du nombre machines de cuisson nécessaires
besoin_cuisson = (
    x["Jambon"] * Jambon.poids_final / Cuisson.capacite["Jambon"] +
    x["Pate"] * Pate.poids_final / Cuisson.capacite["Pate"] +
    x["Terrines"] * Terrines.poids_final / Cuisson.capacite["Terrines"] +
    x["Mousses"] * Mousses.poids_final / Cuisson.capacite["Mousses"] 
)
problem += besoin_cuisson <= m_cuisson, "Capacite_cuisson"

# Calcul du nombre machines d'emballage nécessaires
besoin_emballage = (
    x["Cuisses"] * Cuisses.poids_final +
    x["Jambon"] * Jambon.poids_final +
    x["Pate"] * Pate.poids_final +
    x["Terrines"] * Terrines.poids_final +
    x["Mousses"] * Mousses.poids_final
) / Emballage.capacite

problem += besoin_emballage <= m_emballage, "Capacite_emballage"

# Matières premières issues des carcasses
problem += x["Cuisses"] * Cuisses.recettes["cuisse"] <= carcasses["poulet"] * Poulet.conversion["cuisse"], "MP_cuisse"
problem += x["Jambon"] * Jambon.recettes["muscles"] <= carcasses["porc"] * Porc.conversion["muscles"], "MP_muscles"
problem += (
    x["Pate"] * Pate.recettes["chair_porc"] +
    x["Terrines"] * Terrines.recettes["chair_porc"] +
    x["Mousses"] * Mousses.recettes["chair_porc"]
) <= carcasses["porc"] * Porc.conversion["chair_porc"], "MP_chair_porc"
problem += x["Terrines"] * Terrines.recettes["chair_poulet"] <= carcasses["poulet"] * Poulet.conversion["chair_poulet"], "MP_chair_poulet"
problem += (
    x["Terrines"] * Terrines.recettes["chair_canard"] +
    x["Mousses"] * Mousses.recettes["chair_canard"]
) <= carcasses["canard"] * Canard.conversion["chair_canard"], "MP_chair_canard"
problem += x["Mousses"] * Mousses.recettes["poitrail_canard"] <= carcasses["canard"] * Canard.conversion["poitrail_canard"], "MP_poitrail"

# Bobines
problem += (
    x["Cuisses"] * Cuisses.recettes["plastique"] +
    x["Jambon"] * Jambon.recettes["plastique"] +
    x["Mousses"] * Mousses.recettes["plastique"]
) <= bobines["plastique"] * Plastique.poids, "MP_plastique"

problem += (
    x["Pate"] * Pate.recettes["fer"] +
    x["Terrines"] * Terrines.recettes["fer"]
) <= bobines["fer"] * Fer.poids, "MP_fer"

problem += nb_agents_maitrise >= nb_ouvriers / 5, "Encadrement_par_agents_maitrise"
problem += nb_cadres >= (nb_agents_maitrise + nb_commerciaux  + nb_ouvriers) / 18, "Encadrement_par_cadres"
problem += nb_assistants >= nb_commerciaux / 5, "Assistants commerciaux"
problem += nb_employes >= (nb_ouvriers + nb_agents_maitrise + nb_cadres + nb_commerciaux + nb_assistants + 1) / 15, "Encadrement_global"

# === Résolution ===
problem.solve()

# === Résultats ===
print("\n--- Produits finis à produire ---")
for prod in x:
    print(f"{prod:<10}: {x[prod].varValue} unités")

print("\n--- Machines nécessaires ---")
print(f"Découpe     : {m_decoupe.varValue:.0f}")
print(f"Broyage     : {m_broyage.varValue:.0f}")
print(f"Cuisson     : {m_cuisson.varValue:.0f}")
print(f"Emballage   : {m_emballage.varValue:.0f}")
print(f"Total       : {(m_decoupe.varValue + m_broyage.varValue + m_cuisson.varValue + m_emballage.varValue):.0f}")

print("\n--- Consommation ---")
for c in carcasses:
    print(f"Carcasses {c:<8}: {ceil(carcasses[c].varValue)} unités")
for b in bobines:
    print(f"Bobines {b:<10}: {ceil(bobines[b].varValue)} unités")

print("\n--- Pertes ---")
print(f"pertes chair porc       = {perte_chair_porc.value():.2f} kg")
print(f"pertes muscles porc     = {perte_muscles_porc.value():.2f} kg")
print(f"pertes chair poulet     = {perte_chair_poulet.value():.2f} kg")
print(f"pertes cuisse poulet    = {perte_cuisse_poulet.value():.2f} kg")
print(f"pertes chair canard     = {perte_chair_canard.value():.2f} kg")
print(f"pertes poitrail canard  = {perte_poitrail_canard.value():.2f} kg")

print("\n--- Personnel nécessaire ---")
print(f"Ouvriers           : {nb_ouvriers.value():.0f}")
print(f"Agents de Maîtrise : {nb_agents_maitrise.value():.0f}")
print(f"Cadres Moyens      : {nb_cadres.value():.0f}")
print(f"Commerciaux        : {nb_commerciaux}")
print(f"Assistants         : {nb_assistants.value():.0f}")
print(f"Employés           : {nb_employes.value():.0f}")

print("\n--- Revenus ---")
print(f"Chiffre d'affaires : {revenu.value():.2f} €")

print("\n--- Charges ---")
print(f"Pertes de carcasses : {cout_pertes.value():.2f} €")
print(f"Matières premières  : {cout_matieres.value():.2f} €")
print(f"Machines            : {cout_mensuel_total.value():.2f} €")
print(f"Salaires            : {cout_salaries.value():.2f} €" )

print(f"\nBénéfice mensuel maximum : {problem.objective.value():.2f} €")

print(f"\nStatut de la solution : {LpStatus[problem.status]}")
if LpStatus[problem.status] != "Optimal":
    print("Aucune solution optimale trouvée.")
    exit()
    