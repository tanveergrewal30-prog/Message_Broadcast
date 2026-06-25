# LAN Announcement System (Admin Broadcast Only)

This project is a **local network announcement system** built with **Python, Flask, and Socket.IO**.  
An admin can send announcements from a web interface, and all users connected to the same Wi‑Fi/hotspot can see them in real time in their browser.

> Admin can send messages; other users can only read announcements and see who is connected.

---

## Features

- 🔒 **Admin-only announcements**  
  - Admin must enter a password to send an announcement.
- 👥 **Connected users list**  
  - Shows names of all users who have joined.
- 📜 **Announcement history**  
  - New users see previous announcements when they connect.
- 🌐 **LAN / Hotspot support**  
  - Works over local Wi‑Fi or mobile hotspot; no Internet required.
- 🧪 **Simple, self-contained project**  
  - One Python server (`server.py`) and a single HTML template (`templates/index.html`).

---

## Project Structure

```text
.
├─ server.py
├─ requirements.txt
├─ templates/
│  └─ index.html
└─ static/
   └─ socket.io.min.js   # Socket.IO client (matching Flask-SocketIO version)
```

---

## Requirements

- Python **3.10+** (tested with 3.14.6)
- `pip` (Python package manager)
- A local network (Wi‑Fi or hotspot) so other devices can connect

---

## Installation

1. **Clone or download** this repository:

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

2. (Optional but recommended) **Create a virtual environment**:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, you can install directly:

```bash
pip install Flask flask-socketio
```

---

## Running the Server

From the project folder:

```bash
python server.py
```

You should see output similar to:

```text
============================================================
  LAN Announcements Server
============================================================
  Local access  : http://localhost:5001
  Network access: http://<your-local-ip>:5001
  Admin password: admin123
============================================================
```

- `http://localhost:5001` works on the same machine.
- `http://<your-local-ip>:5001` can be opened from other devices on the same Wi‑Fi/hotspot.

---

## Using the Web Interface

1. Open a browser and go to:

   - `http://localhost:5001` (on the server machine), or  
   - `http://<server-ip>:5001` (on client devices in the same network).

2. At the top-right, enter your **name** and click **Join**.
   - You will appear in the **Connected users** list.

3. For the **admin**:
   - Enter the announcement text in the **Admin only – send announcement** area.
   - Enter the **admin password** (default is `admin123`).
   - Click **Send announcement**.
   - All connected users will immediately see the new announcement.

4. Normal users:
   - Can only read announcements and see who is connected.
   - They cannot send announcements without the admin password.

---

## Configuration

In `server.py`:

```python
ADMIN_PASSWORD = "admin123"
```

- Change this to your own strong password before deploying on any shared network.
- Port and host:

```python
socketio.run(app, host="0.0.0.0", port=5001, debug=False)
```

- Change `port=5001` if you need a different port.

---

## How It Works (Overview)

- **Flask** serves the main HTML page (`index.html`).
- **Flask-SocketIO** handles real-time communication:
  - When a client connects, it:
    - Joins a shared room `"announcements"`.
    - Receives existing announcement history.
  - When a user registers a name, the server:
    - Stores their `sid` and name.
    - Broadcasts a system message and updates the user list.
  - When the admin sends an announcement:
    - The server verifies the admin password.
    - Stores the announcement in history.
    - Broadcasts it to all connected clients.

---

## Notes / Limitations

- This is designed for **local networks only** (LAN / hotspot).
- There is **no encryption** (no HTTPS) and only a simple admin password check.
  - Do not expose this directly to the public internet without adding stronger security.
- All announcements are kept in memory (not saved to a database).

---

## Troubleshooting

- **Page does not load or shows connection errors**
  - Make sure the server is running: `python server.py`.
  - Check that the port `5001` is not blocked by a firewall.
- **Socket.IO fails to connect**
  - Ensure `static/socket.io.min.js` exists and matches your Flask-SocketIO version.
- **Other devices cannot connect**
  - Confirm they are on the same Wi‑Fi/hotspot.
  - Use the IP printed as `Network access` in the server console.

---
