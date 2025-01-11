import tkinter as tk
from tkinter import filedialog, messagebox
import os

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Explorateur de fichiers")
        self.root.geometry("800x600")
        self.root.configure(bg='black')  

        self.current_path = tk.StringVar()

        self.create_gradient()
        self.create_widgets()

    def create_gradient(self):
        canvas = tk.Canvas(self.root, height=600, width=800)
        canvas.place(x=0, y=0)

        for i in range(600):
            color_value = max(0, 40 - i // 15) 
            color = f"#{color_value:02x}00{color_value:02x}" 
            canvas.create_line(0, i, 800, i, fill=color)

    def create_widgets(self):
        self.nav_bar = tk.Frame(self.root, bg='#FF6347', height=40)
        self.nav_bar.pack(fill='x', side='top')

        self.back_button = tk.Button(self.nav_bar, text="⬅ Retour", fg='white', bg='#FF6347', font=('Segoe UI', 12, 'bold'), relief='flat', padx=10, pady=5, command=self.go_back)
        self.back_button.pack(side='left', padx=10)

        self.open_button = tk.Button(self.nav_bar, text="Ouvrir un dossier", fg='white', bg='#FF6347', font=('Segoe UI', 12, 'bold'), relief='flat', padx=10, pady=5, command=self.open_folder)
        self.open_button.pack(side='left', padx=10)


        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill='both', expand=True, pady=10)

        self.canvas_scrollbar = tk.Scrollbar(self.canvas_frame, orient='vertical')
        self.canvas = tk.Canvas(self.canvas_frame, yscrollcommand=self.canvas_scrollbar.set, width=780, bg='black')  
        self.canvas.pack(side='left', fill='both', expand=True)

        self.canvas_scrollbar.config(command=self.canvas.yview)
        self.canvas_scrollbar.pack(side='right', fill='y')

        self.frame = tk.Frame(self.canvas, bg='black')
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.display_files(os.path.expanduser("~"))

        self.pseudo_label = tk.Label(self.root, text="By ShitzuDev", fg='#FF6347', bg='black', font=('Segoe UI', 18, 'bold'))
        self.pseudo_label.place(relx=0.92, rely=0.5, anchor='e')

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.current_path.set(folder_path)
            self.display_files(folder_path)

    def display_files(self, path):
        for widget in self.frame.winfo_children():
            widget.destroy()

        try:
            files = os.listdir(path)
            for file in files:
                file_path = os.path.join(path, file)
                if os.path.isdir(file_path):
                    color = '#FF4500' 
                    icon = '📁'  
                elif file.endswith('.exe'): 
                    color = '#32CD32'
                    icon = '🖥️'  
                elif file.endswith(('.py', '.html', '.css', '.js', '.json', '.xml')):
                    color = '#32CD32' 
                    icon = '💻'  
                else:
                    color = '#1E90FF' 
                    icon = '📄' 

                file_button = tk.Button(self.frame, text=f"{icon} {file}", fg=color, bg='black', font=('Segoe UI', 12, 'bold'), relief='flat', anchor='w', padx=10, pady=5, command=lambda path=file_path: self.open_file(path), bd=2, highlightthickness=2, highlightbackground='#8B0000')
                file_button.pack(fill='x', pady=3)

            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le dossier: {e}")

    def open_file(self, path):
        if os.path.isdir(path):
            self.current_path.set(path)
            self.display_files(path)
        else:
            os.startfile(path)

    def go_back(self):
        parent_dir = os.path.dirname(self.current_path.get())
        if parent_dir and parent_dir != self.current_path.get():
            self.current_path.set(parent_dir)
            self.display_files(parent_dir)

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")  
        else:
            self.canvas.yview_scroll(1, "units")  



root = tk.Tk()
app = FileExplorerApp(root)


root.bind_all("<MouseWheel>", app.on_mouse_wheel)


root.mainloop()
