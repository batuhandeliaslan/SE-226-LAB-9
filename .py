import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",      
            password="",      
            database="StudentDatabase"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Bağlantı Hatası", f"Veritabanına bağlanılamadı: {err}")
        return None

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SE 226 - Lab #9 Solution")
        self.root.geometry("600x600")
        self.root.configure(padx=20, pady=20)

        tk.Label(root, text="ÖĞRENCİ KAYIT SİSTEMİ", font=("Arial", 14, "bold")).pack(pady=10)

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Öğrenci Adı:").grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(input_frame, width=30)
        self.entry_name.grid(row=0, column=1, pady=5)

        tk.Label(input_frame, text="Puan (1-100):").grid(row=1, column=0, sticky="w")
        self.entry_score = tk.Entry(input_frame, width=30)
        self.entry_score.grid(row=1, column=1, pady=5)

        self.btn_save = tk.Button(root, text="Veritabanına Kaydet", command=self.save_student, bg="#4CAF50", fg="white", width=20)
        self.btn_save.pack(pady=5)

        tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=15)

        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="Puan Eşiği:").grid(row=0, column=0)
        self.entry_filter = tk.Entry(filter_frame, width=10)
        self.entry_filter.grid(row=0, column=1, padx=5)
        
        self.btn_filter = tk.Button(filter_frame, text="Filtrele (Yüksek Puanlar)", command=self.fetch_high_scores, bg="#2196F3", fg="white")
        self.btn_filter.grid(row=0, column=2, padx=5)

        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Score"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Öğrenci Adı")
        self.tree.heading("Score", text="Puan")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.display_students()

    def save_student(self):
        name = self.entry_name.get()
        score = self.entry_score.get()

        if not name or not score:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO Students (Name, Score) VALUES (%s, %s)"
            cursor.execute(query, (name, int(score)))
            conn.commit()
            conn.close()
            
            self.entry_name.delete(0, tk.END)
            self.entry_score.delete(0, tk.END)
            self.display_students()
            messagebox.showinfo("Başarılı", "Kayıt eklendi.")

    def display_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Students")
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
            conn.close()

    def fetch_high_scores(self):
        threshold = self.entry_filter.get()
        if not threshold:
            self.display_students()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Students WHERE Score > %s"
            cursor.execute(query, (int(threshold),))
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
