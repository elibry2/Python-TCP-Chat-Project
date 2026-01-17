# TCP/IP Multithreaded Chat Application & Traffic Analysis 📡

## 📖 Project Overview
This project explores the fundamental principles of TCP/IP networking through two main phases: simulating the encapsulation process and building a distributed multi-client chat application using raw sockets in Python.

The project consists of two parts:
1.  **Data Encapsulation & Analysis:** Simulating packet creation and analyzing network layers.
2.  **Distributed Chat System:** A fully functional Client-Server chat application supporting multi-threading, private messaging, and broadcasting.

---

## 🛠 Tech Stack
* **Language:** Python 3.x
* **Libraries:** `socket`, `threading`, `sys`
* **Networking:** TCP/IPv4, Raw Sockets
* **Tools:** Wireshark (Packet Capture & Analysis), Jupyter Notebook

---

## 🚀 Part 2: The Chat Application

The core of this project is a robust TCP chat server that handles multiple clients simultaneously using **Multithreading**. This ensures that one client's activity does not block others.

### Key Features:
* **Real-time Communication:** Instant message delivery using TCP for reliability.
* **Private Messaging:** Send messages to specific users using routing logic.
* **Broadcast Messaging:** Send messages to all connected users.
* **Active User List:** View who is currently online.
* **Threaded Architecture:** Separate threads for listening (receiving) and sending messages prevents UI freezing.

### Chat Commands:
| Action | Command Syntax | Example |
| :--- | :--- | :--- |
| **Private Message** | `@TargetName Message` | `@Alice Hello, how are you?` |
| **Broadcast (All)** | `all Message` | `all Hello everyone!` |
| **List Users** | `list` | `list` |
| **Exit Chat** | `quit` | `quit` |

---

## 📂 Project Structure

* `server.py` - The server-side script. Manages connections, stores active users in a dictionary, and routes messages.
* `client.py` - The client-side script. Connects to the server, handles user input, and listens for incoming messages in a background thread.
* `part2_chat_capture.pcap` - Wireshark capture file proving successful communication between two distinct physical computers on port 12345.
* `Traffic_Analysis.ipynb` - Jupyter Notebook (Encapsulation simulation).
* `http_input.csv` - Input data for the encapsulation task.

---

## ⚙️ How to Run

### 1. Network Configuration
Before running, open `server.py` and `client.py` and configure the **IP Address**:
* **Localhost (Testing on one PC):** Set `SERVER_IP = '127.0.0.1'`
* **Real Network (Two PCs):** Set `SERVER_IP` to the server's local IP (e.g., `192.168.1.X`).

### 2. Start the Server
Open a terminal and run:
```bash

python server.py
