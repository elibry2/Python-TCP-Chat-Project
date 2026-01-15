import socket
import threading
import customtkinter as ctk  
from tkinter import messagebox

# --- Configuration Constants ---
# These must match the settings in your server.py file
SERVER_IP = '127.0.0.1'  # Localhost (your own computer)
SERVER_PORT = 12345      # The port the server is listening on

# --- UI Theme Setup ---
# Sets the application to "Dark" mode (black/gray background)
ctk.set_appearance_mode("System") 
# Sets the accent color for buttons and highlights to blue
ctk.set_default_color_theme("green") 

class ModernChatClient(ctk.CTk):
    """
    Main client class that inherits from ctk.CTk (the main window).
    It handles both the GUI (Graphical User Interface) and the Networking logic.
    """
    def __init__(self):
        super().__init__()  # Initialize the parent class (ctk.CTk)
        
        # Window configuration
        self.title("Modern Chat")
        self.geometry("700x550")  
        
        # --- Layout Configuration (Grid System) ---
        # Column 0 will expand to fill available width (weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Row 0 (Chat area) will expand to fill available height (weight=1)
        self.grid_rowconfigure(0, weight=1) 
        # Row 1 (Input area) will stay fixed size (weight=0)
        self.grid_rowconfigure(1, weight=0) 

        # --- Networking Setup ---
        # Create a TCP/IP socket (IPv4, Stream)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ""

        # --- Initialization ---
        self.create_widgets() # Build the UI elements
        
        # Delay connection by 100ms to ensure the window loads first
        self.after(100, self.connect_to_server)

    def create_widgets(self):
        """Creates and places all visual elements on the window."""
        
        # 1. Chat Area (The big text box)
        # state="disabled" prevents the user from typing directly into the chat log
        self.chat_area = ctk.CTkTextbox(self, state="disabled", font=("Roboto", 14))
        # grid placement: row 0, stick to all sides (North, South, East, West)
        self.chat_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # 2. Input Frame (Container for entry field and button)
        # fg_color="transparent" makes it blend with the background
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # 3. Message Entry Field
        self.msg_entry = ctk.CTkEntry(input_frame, placeholder_text="Type message (@Name...)", font=("Roboto", 14))
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Bind the "Enter" key on the keyboard to the send_message function
        self.msg_entry.bind("<Return>", self.send_message) 

        # 4. Send Button
        send_btn = ctk.CTkButton(input_frame, text="Send", command=self.send_message, width=100)
        send_btn.pack(side="right")

    def connect_to_server(self):
        """Handles the initial connection handshake."""
        try:
            # Attempt to connect to the server
            self.client_socket.connect((SERVER_IP, SERVER_PORT))
            
            # Show a popup dialog to ask for the username
            dialog = ctk.CTkInputDialog(text="Enter your username:", title="Login")
            self.username = dialog.get_input()
            
            # If user pressed Cancel or entered nothing, close the app
            if not self.username:
                self.destroy()
                return

            # Start a background thread to listen for incoming messages.
            # daemon=True ensures this thread dies when the main app closes.
            threading.Thread(target=self.receive_messages, daemon=True).start()
            
        except ConnectionRefusedError:
            # Show an error popup if the server is offline
            messagebox.showerror("Error", "Server not found. Please run server.py")
            self.destroy() # Close the app

    def add_message(self, message):
        """Helper function to safely add text to the read-only chat area."""
        self.chat_area.configure(state="normal")  # Unlock widget to write
        self.chat_area.insert("end", message + "\n") # Append message at the end
        self.chat_area.configure(state="disabled") # Lock widget again
        self.chat_area.yview("end") # Auto-scroll to the bottom

    def receive_messages(self):
        """
        Runs in a separate thread.
        Constantly listens for data from the server.
        """
        while True:
            try:
                # Wait to receive data (buffer size 1024 bytes)
                message = self.client_socket.recv(1024).decode('utf-8')
                
                # If message is empty, connection is broken
                if not message:
                    self.client_socket.close()
                    break

                # --- Handshake Logic ---
                # Check if server is asking for the name (Protocol defined in server.py)
                if message == "ENTER_NAME":
                    self.client_socket.send(self.username.encode('utf-8'))
                else:
                    # Normal message, display it
                    self.add_message(message)
                    
            except Exception:
                # On any error (like server crash), close connection
                self.client_socket.close()
                break

    def send_message(self, event=None):
        """Gets text from input, sends it to server, and clears input."""
        msg = self.msg_entry.get() # Get text from entry widget
        
        if msg:
            # Handle local quit command
            if msg.lower() == 'quit':
                self.destroy()
                return
            
            try:
                # Send the message to the server
                self.client_socket.send(msg.encode('utf-8'))
                self.msg_entry.delete(0, "end") # Clear the input box
            except:
                self.add_message("[Error sending message]")

if __name__ == "__main__":
    # Create an instance of the client and start the main event loop
    app = ModernChatClient()
    app.mainloop()