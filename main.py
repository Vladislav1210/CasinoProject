import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Калькулятор")
        self.create_widgets()

    def create_widgets(self):
        self.entry = tk.Entry(self.master, width=30, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        buttons = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "C", "+"]

        row = 1
        col = 0
        for button in buttons:
            command = lambda x=button: self.button_click(x)
            tk.Button(self.master, text=button, padx=40, pady=20, command=command).grid(row=row, column=col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        equal_button = tk.Button(self.master, text="=", padx=90, pady=20, command=self.calculate)
        equal_button.grid(row=5, column=0, columnspan=4)

    def button_click(self, button):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(current) + str(button))

    def calculate(self):
        current = self.entry.get()
        try:
            result = eval(current)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Ошибка")

root = tk.Tk()
my_calc = Calculator(root)
root.mainloop()

