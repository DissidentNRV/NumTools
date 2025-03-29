import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
import datetime
import requests  # Nécessaire pour actualiser la base de données depuis internet

# --- Base de données locale des indicatifs (code pays et longueur de numéros) ---
# Pour certains pays, la "longueur" est définie selon un format réaliste (à ajuster si besoin).
indicatifs = {
    "France":      {"code": "33", "longueur": 9},
    "États-Unis":  {"code": "1",  "longueur": 10},
    "Canada":      {"code": "1",  "longueur": 10},
    "Royaume-Uni": {"code": "44", "longueur": 10},
    "Belgique":    {"code": "32", "longueur": 8},
    "Allemagne":   {"code": "49", "longueur": 10},
    "Brésil":      {"code": "55", "longueur": 10},
    "Inde":        {"code": "91", "longueur": 10},
    "Chine":       {"code": "86", "longueur": 11},
    "Australie":   {"code": "61", "longueur": 9},
    "Russie":      {"code": "7",  "longueur": 10}
    # ... d'autres pays peuvent être ajoutés ou mis à jour via la fonction d'actualisation
}

# --- Fonction de génération d'une liste de numéros pour un pays donné ---
def generer_numeros():
    pays = var_pays.get()
    try:
        nb = int(var_nombre.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")
        return

    # Validation des entrées
    if not pays or pays not in indicatifs:
        messagebox.showerror("Erreur", "Veuillez choisir un pays valide.")
        return
    if nb < 1:
        messagebox.showerror("Erreur", "Le nombre de numéros doit être au moins 1.")
        return

    # Récupérer l'indicatif et la longueur pour le pays sélectionné
    code_pays = indicatifs[pays]["code"]
    longueur_num = indicatifs[pays]["longueur"]

    # Générer les numéros aléatoires
    numeros = []
    for _ in range(nb):
        # Générer une séquence de chiffres aléatoires de la longueur spécifiée
        suite_chiffres = "".join(random.choice("0123456789") for _ in range(longueur_num))
        numero = code_pays + suite_chiffres
        numeros.append(numero)

    # Créer le dossier de sortie s'il n'existe pas
    dossier_sortie = "numeros_generes"
    os.makedirs(dossier_sortie, exist_ok=True)

    # Construire le nom de fichier (pays + timestamp pour le rendre unique)
    horodatage = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    nom_fichier = f"{pays}_{horodatage}.txt"
    chemin_fichier = os.path.join(dossier_sortie, nom_fichier)

    # Écrire les numéros dans le fichier
    try:
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            for numero in numeros:
                f.write(numero + "\n")
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'enregistrement du fichier:\n{e}")
        return

    # Notification de succès à l'utilisateur
    messagebox.showinfo("Succès", 
                        f"{nb} numéro(s) généré(s) pour {pays}.\n"
                        f"Enregistré dans le fichier :\n{chemin_fichier}")

# --- Fonction d'actualisation de la base de données via internet ---
def actualiser_base_donnees():
    try:
        # Récupère toutes les informations de l'API Rest Countries
        response = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de récupérer les données depuis internet.\n{e}")
        return

    compteur = 0
    for country in data:
        # Vérifier la présence de l'information sur l'IDD
        if "idd" in country and country["idd"]:
            idd = country["idd"]
            root = idd.get("root")
            suffixes = idd.get("suffixes", [])
            if root:
                # On enlève le '+' et on ajoute le premier suffixe s'il existe
                code = root.replace("+", "")
                if suffixes and suffixes[0]:
                    code += suffixes[0]
                # Récupérer le nom commun du pays
                nom = country.get("name", {}).get("common", None)
                if nom:
                    # Si le pays existe déjà dans notre base, on garde l'ancienne longueur
                    if nom in indicatifs:
                        pass
                    else:
                        # Définir une longueur par défaut en fonction du code
                        if code == "1":
                            longueur = 10  # NANP (États-Unis, Canada, etc.)
                        elif code == "86":
                            longueur = 11  # Exemple pour la Chine
                        elif code == "91":
                            longueur = 10  # Exemple pour l'Inde
                        else:
                            longueur = 9  # Par défaut
                        indicatifs[nom] = {"code": code, "longueur": longueur}
                        compteur += 1

    # Mise à jour du menu déroulant avec les nouveaux pays
    choix_pays["values"] = list(indicatifs.keys())
    messagebox.showinfo("Mise à jour", f"Base de données actualisée avec {compteur} nouveaux pays.")

# --- Configuration de la fenêtre principale Tkinter ---
fenetre = tk.Tk()
fenetre.title("Générateur de numéros de téléphone")
fenetre.resizable(False, False)  # Empêcher le redimensionnement de la fenêtre

# Label et menu déroulant pour le choix du pays
label_pays = tk.Label(fenetre, text="Pays :")
label_pays.grid(row=0, column=0, padx=5, pady=5, sticky="e")
var_pays = tk.StringVar(value=list(indicatifs.keys())[0])  # Valeur par défaut
choix_pays = ttk.Combobox(fenetre, textvariable=var_pays, values=list(indicatifs.keys()), state="readonly")
choix_pays.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Label et champ pour le nombre de numéros à générer
label_nombre = tk.Label(fenetre, text="Nombre de numéros :")
label_nombre.grid(row=1, column=0, padx=5, pady=5, sticky="e")
var_nombre = tk.StringVar(value="1")
spin_nombre = tk.Spinbox(fenetre, from_=1, to=1000, textvariable=var_nombre, width=5)
spin_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Bouton pour lancer la génération
bouton_generer = tk.Button(fenetre, text="Générer", command=generer_numeros)
bouton_generer.grid(row=2, column=0, columnspan=2, pady=10)

# Bouton pour actualiser la base de données depuis internet
bouton_actualiser = tk.Button(fenetre, text="Actualiser la base de données", command=actualiser_base_donnees)
bouton_actualiser.grid(row=3, column=0, columnspan=2, pady=5)

# Boucle principale Tkinter
fenetre.mainloop()
