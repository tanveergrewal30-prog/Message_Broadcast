import socket
import datetime
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "lan_messenger_secret_2024"

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

MAX_HISTORY = 500
announce_history = []
users = {}  # sid -> {"name": str, "joined_at": str}
ADMIN_PASSWORD = "admin123"
ROOM = "announcements"

def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_trimmed(lst, msg):
    lst.append(msg)
    if len(lst) > MAX_HISTORY:
        del lst[:-MAX_HISTORY]

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def broadcast_user_list():
    user_list = [
        {"sid": sid, "name": info["name"], "joined_at": info["joined_at"]}
        for sid, info in users.items()
    ]
    socketio.emit("user_list", user_list, room=ROOM)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def on_connect():
    sid = request.sid
    join_room(ROOM)
    emit("history", {"announcements": announce_history})

@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    if sid in users:
        left_name = users[sid]["name"]
        del users[sid]
        socketio.emit(
            "system_message",
            {"text": f"{left_name} left.", "timestamp": now_str()},
            room=ROOM,
        )
        broadcast_user_list()

@socketio.on("register_name")
def on_register_name(data):
    sid = request.sid
    name = (data.get("name") or "").strip()
    if not name:
        emit("error_message", {"text": "Name is required."})
        return

    users[sid] = {"name": name, "joined_at": now_str()}

    socketio.emit(
        "system_message",
        {"text": f"{name} joined.", "timestamp": now_str()},
        room=ROOM,
    )
    broadcast_user_list()

@socketio.on("send_announcement")
def on_send_announcement(data):
    text = (data.get("text") or "").strip()
    sender = (data.get("sender") or "Admin").strip() or "Admin"
    password = data.get("admin_password") or ""

    if not text:
        return

    if password != ADMIN_PASSWORD:
        emit("error_message", {"text": "Invalid admin password."})
        return

    msg = {
        "type": "announcement",
        "sender": f"📢 {sender}",
        "text": text,
        "timestamp": now_str(),
    }
    add_trimmed(announce_history, msg)
    socketio.emit("announcement_message", msg, room=ROOM)

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("=" * 60)
    print("LAN Announcements Server")
    print("=" * 60)
    print("Local access  :", "http://localhost:5001")
    print("Network access:", f"http://{local_ip}:5001")
    print("Admin password:", ADMIN_PASSWORD)
    print("=" * 60)
    socketio.run(app, host="0.0.0.0", port=5001, debug=False, allow_unsafe_werkzeug=True)