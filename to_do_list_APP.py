import tkinter as tk
from tkinter import messagebox
import pickle

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x500")
        self.root.config(bg="#f4f4f4")
        
        # Icon für das Tkinter-Fenster
        try:
            self.root.iconbitmap("E:/Tools/tkinter/icon_test.ico")
        except Exception as e:
            print(f"Icon konnte nicht geladen werden: {e}")

        # Titel Label
        self.title_label = tk.Label(root, text="Meine To-Do Liste", font=("Helvetica", 16, "bold"), bg="#f4f4f4")
        self.title_label.pack(pady=10)

        # Liste der Aufgaben
        self.task_listbox = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE, font=("Helvetica", 12))
        self.task_listbox.pack(pady=10)

        # Eintrag für neue Aufgabe
        self.task_entry = tk.Entry(root, width=45, font=("Helvetica", 12))
        self.task_entry.pack(pady=10)

        #Event-Binding für Enter-Taste
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.add_button = tk.Button(button_frame, text="Hinzufügen", command=self.add_task, width=12, font=("Helvetica", 10))
        self.add_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(button_frame, text="Löschen", command=self.delete_task, width=12, font=("Helvetica", 10))
        self.delete_button.grid(row=0, column=1, padx=5)

        self.done_button = tk.Button(button_frame, text="Erledigt", command=self.mark_as_done, width=12, font=("Helvetica", 10))
        self.done_button.grid(row=0, column=2, padx=5)

        # Bearbeiten-Button
        self.edit_button = tk.Button(button_frame, text="Bearbeiten", command=self.edit_task, width=12, font=("Helvetica", 10))
        self.edit_button.grid(row=1, column=1, padx=5, pady=5)

        # Liste laden, falls vorhanden
        self.load_tasks()
        
        # Attribute für den aktuell bearbeiteten Task
        self.current_edit_index = None  # Speichert den Index der Aufgabe, die gerade bearbeitet wird

    def add_task(self):
        task = self.task_entry.get()
        if task:
            if self.current_edit_index is not None:
                # Wenn eine Aufgabe bearbeitet wird, dann aktualisieren
                self.task_listbox.delete(self.current_edit_index)
                self.task_listbox.insert(self.current_edit_index, task)
                self.current_edit_index = None  # Rücksetzen des Index
            else:
                # Neue Aufgabe hinzufügen
                self.task_listbox.insert(tk.END, task)
            
            self.task_entry.delete(0, tk.END)  # Eingabefeld leeren
        else:
            messagebox.showwarning("Warnung", "Bitte eine Aufgabe eingeben!")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected_task_index)
        except IndexError:
            messagebox.showwarning("Warnung", "Bitte eine Aufgabe auswählen!")

    def mark_as_done(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(selected_task_index)
            if not task.startswith("✔ "):
                self.task_listbox.delete(selected_task_index)
                self.task_listbox.insert(selected_task_index, "✔ " + task)
            else:
                messagebox.showinfo("Info", "Aufgabe bereits als erledigt markiert!")
        except IndexError:
            messagebox.showwarning("Warnung", "Bitte eine Aufgabe auswählen!")

    def edit_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(selected_task_index)
            self.task_entry.delete(0, tk.END)  # Eingabefeld leeren
            self.task_entry.insert(0, task)    # Aufgabe in Eingabefeld einfügen
            self.current_edit_index = selected_task_index  # Index für Bearbeitung speichern
        except IndexError:
            messagebox.showwarning("Warnung", "Bitte eine Aufgabe auswählen!")

    def save_tasks(self):
        tasks = self.task_listbox.get(0, tk.END)
        with open("tasks.pkl", "wb") as file:
            pickle.dump(tasks, file)

    def load_tasks(self):
        try:
            with open("tasks.pkl", "rb") as file:
                tasks = pickle.load(file)
                for task in tasks:
                    self.task_listbox.insert(tk.END, task)
        except FileNotFoundError:
            pass

    def on_closing(self):
        self.save_tasks()
        self.root.destroy()

# Hauptanwendung starten
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()