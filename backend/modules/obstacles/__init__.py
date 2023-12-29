from flask_socketio import emit

from ...main import socketio

@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


# When client use socketio.emit('image', data)
@socketio.on('image')
def image(data):
    print("Image received")
    emit('image', {'message': 'Image received'})