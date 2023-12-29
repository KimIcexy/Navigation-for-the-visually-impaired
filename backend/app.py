from main import create_app, socketio, db

if __name__ == '__main__':
    app = create_app()
    db.init_db()
    socketio.run(app, debug=True)