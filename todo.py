import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import mysql.connector

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        
        self.dark_mode = False

        self.tasks = []

        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ashu@123",
            database="todo_db"
        )
        self.cursor = self.conn.cursor()
        
        self.load_tasks()

        # Task frame and scrollbar
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(self.task_frame, yscrollcommand=self.scrollbar.set, selectmode=tk.SINGLE)
        self.task_listbox.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.task_listbox.yview)

      
        self.task_entry = tk.Entry(self.root)
        self.task_entry.pack(fill=tk.X, padx=5, pady=5)

        
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)

        
        self.add_task_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_task_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task_action)
        self.delete_task_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_task_button = tk.Button(self.button_frame, text="Edit Task", command=self.edit_task)
        self.edit_task_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.mark_complete_button = tk.Button(self.button_frame, text="Mark Complete", command=self.mark_complete)
        self.mark_complete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.color_task_button = tk.Button(self.button_frame, text="Change Color", command=self.change_color)
        self.color_task_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.toggle_theme_button = tk.Button(self.button_frame, text="Toggle Dark Mode", command=self.toggle_theme)
        self.toggle_theme_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.update_task_listbox()

    def load_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        self.tasks = self.cursor.fetchall()

    def save_task(self, task):
        self.cursor.execute("INSERT INTO tasks (text, completed, color) VALUES (%s, %s, %s)", (task['text'], task['completed'], task['color']))
        self.conn.commit()
        self.load_tasks()

    def update_task(self, task_id, text, completed, color):
        self.cursor.execute("UPDATE tasks SET text = %s, completed = %s, color = %s WHERE id = %s", (text, completed, color, task_id))
        self.conn.commit()
        self.load_tasks()

    def delete_task_from_db(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        self.conn.commit()
        self.load_tasks()

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            task = {'text': task_text, 'completed': False, 'color': None}
            self.save_task(task)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task_action(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_id = self.tasks[selected_task_index[0]][0]
            self.delete_task_from_db(task_id)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            new_task_text = simpledialog.askstring("Edit Task", "Edit the task:", initialvalue=task[1])
            if new_task_text:
                self.update_task(task[0], new_task_text, task[2], task[3])
                self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to edit.")

    def mark_complete(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            new_completed_status = not task[2]
            self.update_task(task[0], task[1], new_completed_status, task[3])
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to mark as complete.")

    def change_color(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            color = colorchooser.askcolor()[1]
            if color:
                self.update_task(task[0], task[1], task[2], color)
                self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to change color.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = task[1]
            if task[2]:
                display_text += " (completed)"
            self.task_listbox.insert(tk.END, display_text)
            color = task[3]
            if color:
                self.task_listbox.itemconfig(tk.END, {'bg': color})
        self.apply_theme()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.root.config(bg='#2e2e2e')
            self.task_frame.config(bg='#2e2e2e')
            self.task_listbox.config(bg='#3e3e3e', fg='#ffffff', selectbackground='#575757', selectforeground='#ffffff')
            self.task_entry.config(bg='#3e3e3e', fg='#ffffff', insertbackground='#ffffff')
            self.button_frame.config(bg='#2e2e2e')
            self.add_task_button.config(bg='#575757', fg='#ffffff', activebackground='#2e2e2e', activeforeground='#ffffff')
            self.delete_task_button.config(bg='#575757', fg='#ffffff', activebackground='#2e2e2e', activeforeground='#ffffff')
            self.edit_task_button.config(bg='#575757', fg='#ffffff', activebackground='#2e2e2e', activeforeground='#ffffff')
            self.mark_complete_button.config(bg='#575757', fg='#ffffff', activebackground='#2e2e2e', activeforeground='#ffffff')
            self.color_task_button.config(bg='#575757', fg='#ffffff', activebackground='#2e2e2e', activeforeground='#ffffff')
            self.toggle_theme_button.config(bg='#575757', fg='#ffffff', activebackground='#2e2e2e', activeforeground='#ffffff')
        else:
            self.root.config(bg='#f0f0f0')
            self.task_frame.config(bg='#f0f0f0')
            self.task_listbox.config(bg='#ffffff', fg='#000000', selectbackground='#c0c0c0', selectforeground='#000000')
            self.task_entry.config(bg='#ffffff', fg='#000000', insertbackground='#000000')
            self.button_frame.config(bg='#f0f0f0')
            self.add_task_button.config(bg='#e0e0e0', fg='#000000', activebackground='#d0d0d0', activeforeground='#000000')
            self.delete_task_button.config(bg='#e0e0e0', fg='#000000', activebackground='#d0d0d0', activeforeground='#000000')
            self.edit_task_button.config(bg='#e0e0e0', fg='#000000', activebackground='#d0d0d0', activeforeground='#000000')
            self.mark_complete_button.config(bg='#e0e0e0', fg='#000000', activebackground='#d0d0d0', activeforeground='#000000')
            self.color_task_button.config(bg='#e0e0e0', fg='#000000', activebackground='#d0d0d0', activeforeground='#000000')
            self.toggle_theme_button.config(bg='#e0e0e0', fg='#000000', activebackground='#d0d0d0', activeforeground='#000000')

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
