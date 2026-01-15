import socket
import threading

# --- Server Settings ---
SERVER_IP = '0.0.0.0'  
SERVER_PORT = 12345       
MAX_CLIENTS = 5        

# Dictionary to store connected clients: { "username": socket_object }
connected_clients = {} 

def handle_client(client_socket, client_address):
    """
    This function runs in a separate Thread for each client.
    It handles message routing between clients.
    """
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    current_username = None
    
    try:
        # Step 1: Registration
        client_socket.send("ENTER_NAME".encode('utf-8'))
        current_username = client_socket.recv(1024).decode('utf-8')
        
        # Check if the name is already taken
        if current_username in connected_clients:
            client_socket.send("Name already taken. Reconnect with a different name.".encode('utf-8'))
            client_socket.close()
            return

        connected_clients[current_username] = client_socket
        print(f"[REGISTERED] User '{current_username}' added to directory.")

        # Join messange

        join_msg = f"[SERVER] {current_username} has joined the chat!"
        for name, sock in connected_clients.items():
            if name != current_username:
                sock.send(join_msg.encode('utf-8'))
        
        # Send welcome message with instructions
        online_users = ", ".join(connected_clients.keys())
        
        welcome_msg = f"Welcome {current_username}!\nTo send a message, type: @Username YourMessage\nExample: @Bob Hi there!\n\nOnline users: {online_users}\n Write to all Users star your message:all"
        client_socket.send(welcome_msg.encode('utf-8'))

        # Step 2: Message Routing Loop
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break 
            
            print(f"[{current_username}] sent: {msg}")
            
            # --- Routing Logic ---
            if msg.startswith('@'):
                # Format: @TargetName Message...
                try:
                    # Split the message at the first space only
                    target_name, content = msg.split(' ', 1)
                    target_name = target_name[1:] # Remove the @ from the name
                    
                    if target_name in connected_clients:
                        target_socket = connected_clients[target_name]
                        # Construct the final message
                        final_msg = f"[From {current_username}]: {content}"
                        target_socket.send(final_msg.encode('utf-8'))
                    else:
                        error_msg = f"[SERVER]: User '{target_name}' not found."
                        client_socket.send(error_msg.encode('utf-8'))
                        
                except ValueError:
                    # Case where the user wrote only @Name without a message
                    client_socket.send("[SERVER]: Message format error. Use: @Name Message".encode('utf-8'))
            
            elif msg.lower() == 'list':
                # Bonus feature: Show list of connected users
                online_users = ", ".join(connected_clients.keys())
                client_socket.send(f"[SERVER] Online users: {online_users}".encode('utf-8'))
                
            elif msg.lower().startswith('all'):
                final_msg = f'[{current_username}]: {msg}'
                print(f'[BRODCAST] {current_username}, write to all users:{msg}')

                for user_name, user_socket in connected_clients.items():
                    try:
                        user_socket.send(final_msg.encode('utf-8'))
                    except Exception as e:
                        print(f"[ERROR], faield to send messange {user_name} : {e}")
            
    except Exception as e:
        print(f"[ERROR] with user {current_username}: {e}")
        
    finally:
        # Cleanup on disconnect
        if current_username and current_username in connected_clients:
            del connected_clients[current_username]
            leave_msg=f"User: {current_username}, has left the chat."
            print(leave_msg)
            for user_name, user_socket in connected_clients.items():
                try:
                    user_socket.send(leave_msg.encode("utf-8"))
                except Exception as e:
                    print(f'[ERROR] Could not set to {user_name}: {e}')
        client_socket.close()
        print(f"[DISCONNECT] {client_address} disconnected.")

def start_server():
    """
    The main function that sets up the server and listens for incoming connections
    """
    # 1. Create a TCP socket (SOCK_STREAM) and IPv4 (AF_INET)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Bind the socket to the address and port
    server.bind((SERVER_IP, SERVER_PORT))
    
    # 3. Start listening
    server.listen(MAX_CLIENTS)
    print(f"[LISTENING] Server is listening on {SERVER_IP}:{SERVER_PORT}")
    
    while True:
        # 4. Accept new connection (blocking operation - waits for a connection)
        client_sock, addr = server.accept()
        
        # 5. Create a new Thread to handle the client, so the server remains free to accept more clients
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()
        
        # Print active threads (minus 1 for the main thread) = number of clients
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()