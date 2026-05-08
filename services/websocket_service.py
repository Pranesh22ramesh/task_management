from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def notify_event(event_type, data):
    socketio.emit(event_type, data)

def notify_broadcast(message):
    socketio.emit('notification', {'message': message})
