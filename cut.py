#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def split_file(input_file, nb_files, output_folder):
    # Lecture des lignes du fichier source en supprimant les espaces superflus
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    total_lines = len(lines)
    if nb_files <= 0:
        raise ValueError("Le nombre de fichiers doit être supérieur à 0.")
    if total_lines == 0:
        raise ValueError("Le fichier source est vide.")

    # Calcul du nombre de lignes par fichier
    base_lines_per_file = total_lines // nb_files
    extra = total_lines % nb_files  # Les 'extra' premiers fichiers recevront une ligne en plus

    start = 0
    output_files = []
    for i in range(nb_files):
        num_lines = base_lines_per_file + (1 if i < extra else 0)
        output_lines = lines[start:start+num_lines]
        start += num_lines

        # Création d'un nom de fichier de sortie
        base, ext = os.path.splitext(os.path.basename(input_file))
        output_file = os.path.join(output_folder, f"{base}_part{i+1}{ext}")
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for line in output_lines:
                f_out.write(line + "\n")
        output_files.append(output_file)
    return output_files

def select_input_file():
    filename = filedialog.askopenfilename(
        title="Sélectionnez le fichier source",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    if filename:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filename)

def select_output_folder():
    folder = filedialog.askdirectory(title="Sélectionnez le dossier de sortie")
    if folder:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder)

def on_split():
    input_file = input_entry.get()
    output_folder = output_entry.get()
    try:
        nb_files = int(nb_files_entry.get())
    except ValueError:
        messagebox.showerror("Erreur", "Le nombre de fichiers doit être un entier.")
        return

    if not input_file:
        messagebox.showerror("Erreur", "Veuillez sélectionner le fichier source.")
        return
    if not output_folder:
        messagebox.showerror("Erreur", "Veuillez sélectionner le dossier de sortie.")
        return

    try:
        output_files = split_file(input_file, nb_files, output_folder)
        messagebox.showinfo("Succès", f"Fichier découpé avec succès !\n{len(output_files)} fichiers générés.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Découpage de fichier de numéros de téléphone")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Sélection du fichier source
tk.Label(frame, text="Fichier source :").grid(row=0, column=0, sticky="e")
input_entry = tk.Entry(frame, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Parcourir...", command=select_input_file).grid(row=0, column=2, padx=5, pady=5)

# Sélection du dossier de sortie
tk.Label(frame, text="Dossier de sortie :").grid(row=1, column=0, sticky="e")
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Parcourir...", command=select_output_folder).grid(row=1, column=2, padx=5, pady=5)

# Saisie du nombre de fichiers de sortie
tk.Label(frame, text="Nombre de fichiers de sortie :").grid(row=2, column=0, sticky="e")
nb_files_entry = tk.Entry(frame, width=10)
nb_files_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
nb_files_entry.insert(0, "3")  # Valeur par défaut

# Bouton de déclenchement du découpage
tk.Button(frame, text="Découper", command=on_split).grid(row=3, column=1, pady=10)

root.mainloop()
