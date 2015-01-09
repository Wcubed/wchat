__author__ = 'wybe'


import socket
import tkinter as tk
from tkinter import ttk


ENCODING = "utf-8"  # Text encoding to use
BUFFER = 4096  # Buffer length


# ------------------- SettingsBar --------------------
class SettingsBar(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # ---- Configure scaling ----
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)

        # ---- Add gui parts ----
        self.label_ip = ttk.Label(self, text="Host:")
        self.label_ip.grid(column=0, row=0, sticky="w")

        self.entry_ip = ttk.Entry(self)
        self.entry_ip.grid(column=1, row=0, sticky="we")

        self.label_port = ttk.Label(self, text="Port:")
        self.label_port.grid(column=2, row=0)

        self.entry_port = ttk.Entry(self)
        self.entry_port.grid(column=3, row=0, sticky="we")

        self.label_name = ttk.Label(self, text="Name:")
        self.label_name.grid(column=0, row=1, sticky="w")

        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(column=1, row=1, columnspan=3, sticky="we")

        self.button_connect = ttk.Button(self, text="Connect")
        self.button_connect.grid(column=4, row=0, rowspan=2, sticky="nesw")


# ------------------- Chat window -------------------
class ChatWindow(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # ---- Configure scaling ----
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ---- Styling ----
        self["borderwidth"] = 1
        self["relief"] = "ridge"

        # ---- Add gui parts ----
        # Add a canvas to make a scrollable frame.
        self.canvas = tk.Canvas(self, background="white")
        self.canvas.grid(column=0, row=0, sticky="nesw")

        # Put a frame inside the canvas.
        self.frame_output = ttk.Frame(self.canvas, style="White.TFrame")
        self.canvas.create_window((0, 0), window=self.frame_output, anchor="nw")

        # Add the scrollbar and connect it to the canvas.
        self.scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(column=1, row=0, sticky="ns")
        self.canvas["yscrollcommand"] = self.scrollbar_y.set

        # This is important for the scrolling! (no idea why it doesn't work without)
        self.frame_output.bind("<Configure>", self.onframeconfigure)

        # Test stuff inside frame
        for i in range(50):
            ttk.Label(self.frame_output, text=i, style="White.TLabel").grid(row=i, column=0)
            ttk.Label(self.frame_output, text="my text"+str(i), style="White.TLabel").grid(row=i, column=1)
            ttk.Label(self.frame_output, text="..........", style="White.TLabel").grid(row=i, column=2)

    def onframeconfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


# ------------------- TextInput --------------------
class TextInput(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # ---- Configure scaling ----
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ---- Add gui parts ----
        self.entry_text = ttk.Entry(self)
        self.entry_text.grid(column=0, row=0, sticky="we")


# ------------------- MainApplication --------------------
class MainApplication(ttk.Frame):

    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        # ---- Configure scaling ----
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ---- Add gui parts ----
        self.settingsBar = SettingsBar(self)
        self.settingsBar.grid(column=0, row=0, sticky="nesw")

        self.chatWindow = ChatWindow(self)
        self.chatWindow.grid(column=0, row=1, sticky="nesw")

        self.textInput = TextInput(self)
        self.textInput.grid(column=0, row=2, sticky="nesw")


# -------------------- Main --------------------
def main():
    # ---- Set root ----
    root = tk.Tk()
    MainApplication(root).grid(column=0, row=0, sticky="nesw")
    root.title("Wchat")

    # ------------------- Styles -------------------
    style = ttk.Style()
    style.configure("White.TFrame", background="white")
    style.configure("White.TLabel", background="white")

    # ---- Configure scaling ----
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # ---- Set minimum window size ----
    root.update()
    root.minsize(350, 200)

    # ---- Start mainloop ----
    root.mainloop()
    return


if __name__ == "__main__":
    main()