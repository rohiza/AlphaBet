from flask.cli import FlaskGroup


from project import app,socketio as socket


# cli = FlaskGroup(app)
#

if __name__ == "__main__":
    socket.run(app,debug=True)

