__author__ = 'wybe'


import tkinter as tk
from tkinter import ttk
import socket
import select
from datetime import datetime

import protocol as prot


PORT = 25565  # Default port


# ------------------- SettingsBar --------------------
class SettingsBar(ttk.Frame):
    def __init__(self, parent, func_connect, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # ---- Configure scaling ----
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)

        # ---- Tk variables ----
        self.ip = tk.StringVar()
        self.port = tk.StringVar()
        self.name = tk.StringVar()

        # ---- Add gui parts ----
        # Ip
        self.label_ip = ttk.Label(self, text="Host:")
        self.label_ip.grid(column=0, row=0, sticky="w")

        self.entry_ip = ttk.Entry(self, textvariable=self.ip)
        self.entry_ip.grid(column=1, row=0, sticky="we")

        # Port
        self.label_port = ttk.Label(self, text="Port:")
        self.label_port.grid(column=2, row=0)

        self.entry_port = ttk.Entry(self, textvariable=self.port)
        self.entry_port.grid(column=3, row=0, sticky="we")
        self.port.set(str(PORT))  # Set default port

        # Name
        self.label_name = ttk.Label(self, text="Name:")
        self.label_name.grid(column=0, row=1, sticky="w")

        self.entry_name = ttk.Entry(self, textvariable=self.name)
        self.entry_name.grid(column=1, row=1, columnspan=3, sticky="we")

        self.button_connect = ttk.Button(self, text="Connect", command=func_connect)
        self.button_connect.grid(column=4, row=0, rowspan=2, sticky="nesw")

    def get_address(self):
        return str(self.ip.get()), int(self.port.get())

    def get_name(self):
        if self.name.get() == '':
            self.name.set("Anonymous")
        return str(self.name.get())

    def lock(self):
        self.entry_ip["state"] = "readonly"
        self.entry_port["state"] = "readonly"
        self.entry_name["state"] = "readonly"
        self.button_connect["text"] = "Disconnect"

    def unlock(self):
        self.entry_ip["state"] = "normal"
        self.entry_port["state"] = "normal"
        self.entry_name["state"] = "normal"
        self.button_connect["text"] = "Connect"


# ------------------- Chat window -------------------
class ChatWindow(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # ---- Variables ----
        self.last_frame = None
        self.last_name = None

        # ---- Configure scaling ----
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ---- Styling ----
        self["borderwidth"] = 1
        self["relief"] = "ridge"

        # ---- Add gui parts ----
        # Add a canvas to make a scrollable frame.
        self.canvas = tk.Canvas(self, background="white", highlightthickness=0)
        self.canvas.grid(column=0, row=0, sticky="nesw")

        # Put a frame inside the canvas.
        self.frame_output = ttk.Frame(self.canvas, style="White.TFrame")
        self.frame_window = self.canvas.create_window((0, 0), window=self.frame_output, anchor="nw")

        # Add the scrollbar and connect it to the canvas.
        self.scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(column=1, row=0, sticky="ns")
        self.canvas["yscrollcommand"] = self.scrollbar_y.set

        # ---- Bind resizing events ----
        self.frame_output.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.frame_output.columnconfigure(0, weight=1)

    def on_frame_configure(self, event):
        # Set canvas scrollregion to the new size of the frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # This resizes the frame to fit the canvas
        self.canvas.config(width=event.width)
        self.canvas.itemconfig(self.frame_window, width=self.canvas["width"])

    def put_separator(self):
        sep = ttk.Separator(self.frame_output, orient="horizontal")
        sep.grid(sticky="ew")

    def put_info(self, info):
        label = ttk.Label(self.frame_output, text=info, style="Info.TLabel")
        label.grid()
        self.last_frame = None
        self.last_name = None
        return

    def put_error(self, error):
        label = ttk.Label(self.frame_output, text=error, style="Error.TLabel")
        label.grid()
        self.last_frame = None
        self.last_name = None
        return

    def put_message(self, name, message):
        if self.last_name != name:
            self.last_frame = ttk.Frame(self.frame_output, style="Message.TFrame")
            self.last_name = name

            self.last_frame.grid(sticky="ew")
            self.last_frame.columnconfigure(0, weight=1)

            line_frame = ttk.Frame(self.last_frame, style="Message.TFrame")
            line_frame.grid(sticky="ew")
            line_frame.columnconfigure(3, weight=1)

            time = datetime.now().time()

            time_label = ttk.Label(line_frame, text="["+str(time.hour)+":"+str(time.minute)+":"+str(time.second)+"]", style="Time.TLabel")
            time_label.grid()

            name_label = ttk.Label(line_frame, text=name + ":", style="Info.TLabel")
            name_label.grid(column=1, row=time_label.grid_info()["row"], columnspan=2, sticky="w")

            message_label = ttk.Label(line_frame, text=message, style="White.TLabel")
            message_label.grid(column=3, row=time_label.grid_info()["row"], sticky="w")
        else:
            line_frame = ttk.Frame(self.last_frame, style="Message.TFrame")
            line_frame.grid(sticky="ew")
            line_frame.columnconfigure(2, weight=1)

            time = datetime.now().time()

            time_label = ttk.Label(line_frame, text="["+str(time.hour)+":"+str(time.minute)+":"+str(time.second)+"]", style="Time.TLabel")
            time_label.grid()

            name_label = ttk.Label(line_frame, text="...", style="Info.TLabel")
            name_label.grid(column=1, row=time_label.grid_info()["row"], sticky="w")

            message_label = ttk.Label(line_frame, text=message, style="White.TLabel")
            message_label.grid(column=2, row=time_label.grid_info()["row"], sticky="w")
        return


# ------------------- TextInput --------------------
class TextInput(ttk.Frame):
    def __init__(self, parent, func_send, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        # ---- Tk variables ----
        self.message = tk.StringVar()

        # ---- Configure scaling ----
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ---- Add gui parts ----
        self.entry_text = ttk.Entry(self, state="readonly", textvariable=self.message)
        self.entry_text.grid(column=0, row=0, sticky="we")
        self.entry_text.bind("<Return>", func_send)

    def get_message(self):
        return self.message.get()

    def lock(self):
        self.entry_text["state"] = "readonly"

    def unlock(self):
        self.entry_text["state"] = "normal"


# ------------------- MainApplication --------------------
class MainApplication(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        # ---- Set variables ----
        self.connected = False
        self.server = None
        self.messbuf = []
        self.names = []

        # ---- Configure scaling ----
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ---- Add gui parts ----
        self.settingsBar = SettingsBar(self, self.toggle_connection)
        self.settingsBar.grid(column=0, row=0, sticky="nesw")

        self.chatWindow = ChatWindow(self)
        self.chatWindow.grid(column=0, row=1, sticky="nesw")

        self.textInput = TextInput(self, self.send_msg)
        self.textInput.grid(column=0, row=2, sticky="nesw")

    def toggle_connection(self):
        if not self.connected:
            try:
                self.chatWindow.put_info("Connecting")
                self.server = socket.create_connection(self.settingsBar.get_address())
            except ConnectionRefusedError:
                self.chatWindow.put_error("Error: Connection refused")
            except (ValueError, socket.gaierror):
                self.chatWindow.put_error("Error: Address not valid")
            except TimeoutError:
                self.chatWindow.put_error("Error: Timeout")
            else:
                self.chatWindow.put_info("Connection established")
                ip, port = self.server.getpeername()
                self.chatWindow.put_info(str(ip) + ":" + str(port))
                self.chatWindow.put_separator()

                self.connected = True
                self.server.setblocking(False)
                self.settingsBar.lock()
                self.textInput.unlock()

                prot.put_tuple(self.server, ("Name", self.settingsBar.get_name()))

                self._root().after(1, self.receive_msg)
        else:
            self.server.close()
            self.chatWindow.put_separator()
            self.chatWindow.put_info("Disconnected")
            self.connected = False
            self.settingsBar.unlock()
            self.textInput.lock()
        return

    def send_msg(self, event):
        if self.connected and self.textInput.get_message() != '':
            prot.put_tuple(self.server, ("Mess", self.textInput.get_message()))
            self.chatWindow.put_message(self.settingsBar.get_name(), self.textInput.get_message())
            self.textInput.message.set('')
        return

    def receive_msg(self):
        if self.connected:
            # Check for messages
            read, write, error = select.select((self.server,), (), (), 0)
            for s in read:
                message = prot.get(s)
                if message == 0:  # Connection is closed
                    self.toggle_connection()
                elif message == '\x00\x00\x00\x00':  # End of message
                    self.parse_msg(self.messbuf)
                    self.messbuf = []
                else:  # Just a normal string
                    self.messbuf.append(message)

            self._root().after(1, self.receive_msg)

    def parse_msg(self, message):
        if message[0] == "Online":
            names = message[1:]
        elif message[0] == "Mess":
            self.chatWindow.put_message(message[1], message[2])

        return


# -------------------- Main --------------------
def main():
    # ---- Set root ----
    root = tk.Tk()
    MainApplication(root).grid(column=0, row=0, sticky="nesw")
    root.title("Wchat")

    # ------------------- Styles -------------------
    style = ttk.Style()
    style.configure("White.TFrame", background="white")
    style.configure("Message.TFrame", background="white")
    style.configure("White.TLabel", background="white")
    style.configure("Info.TLabel", background="white", foreground="blue")
    style.configure("Error.TLabel", background="white", foreground="red")
    style.configure("Time.TLabel", background="white", foreground="gray")

    # ---- Configure scaling ----
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # ---- Set minimum window size ----
    root.minsize(350, 200)

    # ---- Start mainloop ----
    root.mainloop()
    return


if __name__ == "__main__":
    main()