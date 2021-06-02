from flask import Flask,render_template,request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

sid={}


@app.route('/<name>')
def homepage(name):
    global my_name
    my_name=name
    return render_template('test.html')

@socketio.on('connect')
def connected():
    print('connect')
    sid[my_name]=request.sid
    join_room('rahul1');
    print(sid)

@socketio.on('video_call')
def new_connection(data):
    emit('new_user',data,room=sid['rahul'])
  
    
    
    
@socketio.on('disconnect')
def disconnect():
    print('disconnect')

@socketio.on('cancel_video')
def cancel():
    emit('cancel_req',broadcast=True)
   


if __name__ == '__main__':
    socketio.run(app,debug=True)