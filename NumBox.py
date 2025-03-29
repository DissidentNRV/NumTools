import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import os

# Variables globales
input_files = []   # Liste des fichiers d'entrée sélectionnés
output_path = ""   # Chemin de base pour le fichier de sortie

def choose_input():
    """Permet de choisir un fichier unique ou plusieurs fichiers en fonction du mode d'entrée."""
    global input_files
    if input_mode.get() == 1:  # Fichier unique
        file_path = filedialog.askopenfilename(
            title="Sélectionnez le fichier TXT contenant les numéros",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            input_files = [file_path]
            input_entry.config(state='normal')
            input_entry.delete(0, tk.END)
            input_entry.insert(0, file_path)
            input_entry.config(state='readonly')
    else:  # Fusionner plusieurs fichiers
        files = filedialog.askopenfilenames(
            title="Sélectionnez les fichiers TXT à fusionner",
            filetypes=[("Text Files", "*.txt")]
        )
        if files:
            input_files = list(files)
            input_entry.config(state='normal')
            input_entry.delete(0, tk.END)
            input_entry.insert(0, "; ".join(input_files))
            input_entry.config(state='readonly')

def choose_output():
    """Permet de choisir le chemin de base de sortie."""
    global output_path
    output_path = filedialog.asksaveasfilename(
        title="Choisissez l'emplacement de sortie",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if output_path:
        output_entry.config(state='normal')
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)
        output_entry.config(state='readonly')

def mode_changed():
    """Active ou désactive le champ 'Nombre de numéros désiré' selon le mode de traitement choisi."""
    if process_mode.get() == 1:
        entry_count.config(state="normal")
    else:
        entry_count.config(state="disabled")

def get_prefix(phone_number):
    """
    Extrait l'indicatif international à partir des deux premiers chiffres.
    
    - Si le numéro commence par '+', on extrait les deux premiers chiffres après le '+'.
    - Sinon, on extrait les deux premiers chiffres et on ajoute un '+' devant.
    - Si le numéro ne comporte pas de chiffres, on retourne 'Autres'.
    """
    phone_number = phone_number.strip()
    if phone_number.startswith('+'):
        match = re.match(r"^\+(\d{1,2})", phone_number)
        if match:
            return f"+{match.group(1)}"
    else:
        match = re.match(r"^(\d{1,2})", phone_number)
        if match:
            return f"+{match.group(1)}"
    return "Autres"

def remove_plus_if_desired(phone_number):
    """
    Supprime le caractère '+' au début du numéro si l'option est activée.
    """
    if remove_plus_option.get() and phone_number.startswith('+'):
        return phone_number[1:]
    return phone_number

def process_file():
    global input_files, output_path
    # Vérifier qu'au moins un fichier d'entrée a été sélectionné
    if not input_files:
        messagebox.showerror("Erreur", "Veuillez sélectionner un ou plusieurs fichiers source.")
        return

    # Vérification de l'emplacement de sortie
    if not output_path:
        messagebox.showerror("Erreur", "Veuillez choisir un emplacement de sortie.")
        return

    # Récupérer le nombre désiré si le mode est "Nombre exact de numéros"
    if process_mode.get() == 1:
        try:
            desired_count = int(entry_count.get())
            if desired_count <= 0:
                messagebox.showerror("Erreur", "Veuillez entrer un nombre positif pour le nombre de numéros désiré.")
                return
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide pour le nombre de numéros désiré.")
            return

    # Lecture et fusion des fichiers sélectionnés
    all_lines = []
    total_lines_count = 0
    for file in input_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                all_lines.extend(lines)
                total_lines_count += len(lines)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier {file} : {e}")
            return

    if not all_lines:
        messagebox.showerror("Erreur", "Aucun contenu trouvé dans les fichiers sélectionnés.")
        return

    progress_bar["maximum"] = total_lines_count
    processed_numbers = []
    seen = set()
    current_line = 0

    # Traitement : suppression des espaces inutiles et élimination des doublons
    for line in all_lines:
        current_line += 1
        cleaned = line.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            processed_numbers.append(cleaned)
        progress_bar["value"] = current_line
        window.update_idletasks()

    if not processed_numbers:
        messagebox.showerror("Erreur", "Aucun numéro trouvé après traitement.")
        return

    # Regroupement des numéros par indicatif international (sur la base des 2 premiers chiffres)
    groups = {}
    for number in processed_numbers:
        prefix = get_prefix(number)
        groups.setdefault(prefix, []).append(number)

    errors = []
    base, ext = os.path.splitext(output_path)
    # Pour chaque groupe, appliquer le mode de traitement et sauvegarder dans un fichier distinct
    for prefix, numbers in groups.items():
        if process_mode.get() == 1:
            # Mode "Nombre exact de numéros"
            if len(numbers) < desired_count:
                errors.append(f"Le groupe {prefix} ne contient que {len(numbers)} numéro(s).")
                continue
            output_numbers = numbers[:desired_count]
        else:
            # Mode "Suppression des doublons uniquement"
            output_numbers = numbers

        # Création du nom de fichier (on enlève le '+' pour éviter des problèmes dans le nom)
        safe_prefix = prefix.replace('+', '')
        output_filename = f"{base}_{safe_prefix}{ext}"
        try:
            with open(output_filename, "w", encoding="utf-8") as f:
                for num in output_numbers:
                    # Supprimer le '+' si l'option est activée
                    f.write(remove_plus_if_desired(num) + "\n")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier pour {prefix} : {e}")
            return

    if errors:
        messagebox.showwarning("Avertissement", "Certains groupes n'ont pas assez de numéros :\n" + "\n".join(errors))
    else:
        messagebox.showinfo("Succès", "Les fichiers ont été traités et sauvegardés avec succès.")

# --- Interface graphique Tkinter ---

window = tk.Tk()
window.title("Traitement de numéros de téléphone")

# Conteneur principal
frame = ttk.Frame(window, padding=10)
frame.pack(fill="x", expand=True)

# 1. Section : Mode d'entrée (Fichier unique ou fusion de plusieurs fichiers)
input_mode = tk.IntVar(value=1)  # 1 = Fichier unique, 2 = Fusionner plusieurs fichiers
input_mode_frame = ttk.LabelFrame(frame, text="Mode d'entrée", padding=10)
input_mode_frame.pack(fill="x", expand=True, pady=(0, 10))

radio_single = ttk.Radiobutton(input_mode_frame, text="Fichier unique", variable=input_mode, value=1)
radio_single.pack(anchor="w", padx=5, pady=2)
radio_merge = ttk.Radiobutton(input_mode_frame, text="Fusionner plusieurs fichiers", variable=input_mode, value=2)
radio_merge.pack(anchor="w", padx=5, pady=2)

input_button = ttk.Button(input_mode_frame, text="Sélectionner le(s) fichier(s)", command=choose_input)
input_button.pack(fill="x", expand=True, padx=5, pady=5)

input_entry = ttk.Entry(input_mode_frame, state="readonly")
input_entry.pack(fill="x", expand=True, padx=5, pady=(0,5))

# 2. Section : Mode de traitement
process_mode = tk.IntVar(value=1)  # 1 = Nombre exact de numéros, 2 = Suppression des doublons uniquement
process_mode_frame = ttk.LabelFrame(frame, text="Mode de traitement", padding=10)
process_mode_frame.pack(fill="x", expand=True, pady=(0, 10))

radio_exact = ttk.Radiobutton(process_mode_frame, text="Nombre exact de numéros", variable=process_mode, value=1, command=mode_changed)
radio_exact.pack(anchor="w", padx=5, pady=2)
radio_unique = ttk.Radiobutton(process_mode_frame, text="Suppression des doublons uniquement", variable=process_mode, value=2, command=mode_changed)
radio_unique.pack(anchor="w", padx=5, pady=2)

# Champ pour le nombre de numéros désiré (actif uniquement en mode exact)
label_count = ttk.Label(frame, text="Nombre de numéros désiré :")
label_count.pack(fill="x", expand=True, pady=(0, 5))
entry_count = ttk.Entry(frame)
entry_count.pack(fill="x", expand=True)
entry_count.insert(0, "10")

# 3. Section : Option pour supprimer le '+' dans les numéros
remove_plus_option = tk.BooleanVar(value=False)
remove_plus_frame = ttk.LabelFrame(frame, text="Options supplémentaires", padding=10)
remove_plus_frame.pack(fill="x", expand=True, pady=(0, 10))
remove_plus_check = ttk.Checkbutton(remove_plus_frame, text="Supprimer le '+' dans les numéros", variable=remove_plus_option)
remove_plus_check.pack(anchor="w", padx=5, pady=2)

# 4. Section : Emplacement de sortie
output_frame = ttk.Frame(frame)
output_frame.pack(fill="x", expand=True, pady=(10, 0))
output_label = ttk.Label(output_frame, text="Emplacement de sortie :")
output_label.pack(side="left", padx=(0,5))
output_entry = ttk.Entry(output_frame, state="readonly", width=40)
output_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
output_button = ttk.Button(output_frame, text="Choisir...", command=choose_output)
output_button.pack(side="left")

# 5. Barre de progression
progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
progress_bar.pack(fill="x", expand=True, pady=10)

# 6. Bouton pour démarrer le traitement
button_process = ttk.Button(frame, text="Traiter les fichiers", command=process_file)
button_process.pack(fill="x", expand=True)

# Initialisation de l'état du champ de saisie pour le nombre de numéros désiré
mode_changed()

# Boucle principale de l'application
window.mainloop()
