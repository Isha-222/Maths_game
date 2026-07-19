import tkinter as tk
from tkinter import ttk
import pygame
from tkinter import messagebox
from tkinter import PhotoImage
import random


class MathsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Game")
        self.root.geometry("800x500")
        self.root.configure(bg="#10274d")
        self.root.resizable(False, False)
        
        self.create_main_menu()

    def create_main_menu(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg="#10274d")
        main_frame.pack(expand=True, fill='both')

        # Button frame for organisation
        button_frame = tk.Frame(main_frame, bg="#10274d")
        button_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Buttons with proper styling and commands.
        tk.Button(button_frame, text="START", width=30, height=3,
                 fg="black", bg="#f7f6f2").place(relx=0.5, y=300, anchor='center')

        tk.Button(button_frame, text="QUIT", width=30, height=3,fg="black",  bg="#f7f6f2",
                 command=self.quit_app).place(relx=0.5, y=400, anchor='center')



    def quit_app(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.quit()
            
# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MathsGame(root)
    root.mainloop()

