import tkinter as tk

class ConsoleGUI(tk.Frame):
    def __init__(self, master=None):
        self.master = master
        super().__init__(master)
        self.pack()

        self.console = tk.Text(self)
        self.console.insert(tk.END, 'Esto es una interfaz grafica')
        self.console.pack(expand=True, fill='both')
        self.console.tag_configure('center', justify='center')
        self.console.tag_add('center', 1.0, 'end')

root = tk.Tk()
app = ConsoleGUI(master=root)
app.mainloop()
