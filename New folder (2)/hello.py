from flask import Flask, render_template,request,redirect,url_for,session
from flask_socketio import SocketIO ,emit,join_room


from os.path import join, dirname, realpath
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahulisbest'
socketio = SocketIO(app,cors_allowed_origins="*")
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\contents')

app.config['UPLOAD_FOLDER']=UPLOADS_PATH

client_user_pass={'rahul':'12345678','palak':'12345678','gudda':'12345678'}
client_profile_name={'rahul':'rahul singh','palak':'palak thakur','gudda':'guddu faujdar'}
client_sid={}
client_classname_user={}
client_friends={'palak':['rahul','gudda'],'rahul':['palak','gudda'],'gudda':['rahul','palak']}
client_friend_online_status={}
all_users={'rahul singh':'rahul','palak thakur':'palak','guddu faujdar':'gudda','rahul loda':'loda'}




@app.route('/')
def homepage():
   return render_template('login.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    return redirect(url_for('homepage'))


@app.route('/uploadimage/<username>',methods=['GET','POST'])
def upload_img(username):
    if request.files['file'].filename != '':
                image = request.files['file']
                image.save(os.path.join(UPLOADS_PATH, username+'.jpg'))  
                return redirect(url_for('homepage'))            
                
        







    





@app.route('/login',methods=['POST','GET'])
def login():
    
    if request.method=='POST':

        global username
        username=request.form['username']
        password=request.form['password']
        if username.strip() and password.strip():

            if client_user_pass.get(username,'0')=='0':

                return redirect(url_for('homepage'))
            elif(client_user_pass.get(username,'0')==password):


                print(username)
                print(password)
                

                return render_template('home_page.html',user_profile_name=client_profile_name[username])
            else:
                 return redirect(url_for('homepage'))

        else:
            return redirect(url_for('homepage'))
    else:
        return redirect(url_for('homepage'))



@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        newpassword=request.form['newpassword']
        newpassword1=request.form['newpassword1']
        if (newpassword.strip()==newpassword1.strip()) and username.strip():
            client_user_pass[username]=newpassword
            if client_profile_name.get(username,'0')=='0':
                client_profile_name[username]='Add Profile Name'
            
            print('username',username)
            print('password',newpassword)
            return redirect(url_for('homepage'))

        else:
            return redirect(url_for('homepage'))
    else:
        return redirect(url_for('homepage'))




@socketio.on('connect')
def connect():   
    print('new user connected')
    
    emit('e1',{'data':username})
    client_sid[username]=request.sid
    client_friend_online_status[username]='true'
    print(client_friend_online_status)
    try:
        os.mkdir('./users_msg/'+username)
    except:
        pass
    
    
    class_name=username+"_f"
    client_classname_user[class_name]=username
    
    emit('active_online_status',{'username':username},broadcast=True)
    
    

    

@socketio.on('send_msg')
def send_message(data):
    receiver_name=data['receiver_name']
    sender_username=data['username_profile_name']
    
    if data.get('msg','')=='':
        sender_msg=data['url']
        data['check_type']='url'
    else:
        sender_msg=data['msg']
        data['check_type']='msg'

    
    if data['check_type']=='msg':
        f=open(f"./users_msg/{sender_username}/{receiver_name}.txt",'a')
        f1=open(f"./users_msg/{receiver_name}/{sender_username}.txt",'a')
        f.write('msg<>'+sender_username+'::'+sender_msg+'\n')
        f1.write('msg<>'+sender_username+'::'+sender_msg+'\n')

    else:
        f=open(f"./users_msg/{sender_username}/{receiver_name}.txt",'a')
        f1=open(f"./users_msg/{receiver_name}/{sender_username}.txt",'a')
        f.write('url<>'+data['filename']+'<1>'+sender_username+'::'+sender_msg+'\n')
        f1.write('url<>'+data['filename']+'<1>'+sender_username+'::'+sender_msg+'\n')




    
    emit('msg_received',data,room=client_sid[receiver_name]);



@socketio.on('get_receiver_username')
def receiver_username(data):
    user_class_name=data['data'];
    
    emit('take_username_name',{'username':client_classname_user[user_class_name]});

@socketio.on('get_friends_list')
def get_friends(data):
    friends_status={}
    friends=client_friends[data['username']]
    for name in friends:
        friends_status[name]=client_friend_online_status[name]
    emit('take_friends_list',{'data':friends,'online_list':friends_status})


@socketio.on('add_friend_mylist')
def add_friend_list(data):
    friend_name=data['friend_username']
    sender_name=data['username']
    if friend_name not in client_friends[sender_name]:
        client_friends[sender_name].append(friend_name)
        friends=client_friends[sender_name]
        emit('take_friends_list',{'data':friends})


@socketio.on('change_profile_name')
def change_profile_name(data):
    username=data['username']
    client_profile_name[username]=data['data']



@socketio.on('client_disconnecting')
def disconnect(data):
    print('client disconnected')
    print(data['username'])
    disconnect_username=data['username']
    client_friend_online_status[disconnect_username]='false'
    print(client_friend_online_status)
    

    emit('update_online_status',{'username':disconnect_username},broadcast=True)

@socketio.on('take_online_status')
def online_status(data):
    username=data['username']
    try:
        emit('get_online_status',{'data':client_friend_online_status[username]})
    except:
        pass

@socketio.on('find_friend')
def find_friends(data):
    msg=data['msg']
    collect_friend=[]
    for profile_name,profile_username in all_users.items():
        if msg in profile_name:
            collect_friend.append([profile_name,profile_username])
    emit('get_find_friend',{'data':collect_friend})

@socketio.on('image-upload')
def imageupload(image):
    emit('send-image',image,broadcast=True)

@socketio.on('video_call_initiate')
def video_call_initiate(data):
    username=data['username']
    receiver_name=data['receiver_name']
    if(client_friend_online_status[receiver_name]=='true'):
        emit('video_attend_notification',data,room=client_sid[receiver_name])

@socketio.on('not_attend_call')
def not_attend_call(data):
    receiver_name=data['receiver_name']
    emit('not_attend_video_call',room=client_sid[receiver_name])

@socketio.on('yes_attend_call')
def yes_attend_call(data):
   
    receiver_name=data['receiver_name']
    emit('yes_attend_video_call',data['id'],room=client_sid[receiver_name])

@socketio.on('call_disconnected')
def call_disconnected(data):
    receiver_name=data['receiver_name']
    emit('call_disconnect_to_receiver',room=client_sid[receiver_name])






    






    
    


@socketio.on('take_past_msg')
def past_msg(data):
    sender_name=data['username']
    receiver_name=data['receiver_name']
    msg_list=[]
    try:
        f=open(f'./users_msg/{sender_name}/{receiver_name}.txt','r')
        while True:
            line=f.readline()
            if not line:
                break
            msg_list.append(line.strip())
        f.close()
        emit('get_past_msg',{'data':msg_list})

    except:
        msg_list.append('Empty Messages')
        emit('get_past_msg',{'data':msg_list})

   


if __name__ == '__main__':
    socketio.run(app,debug=True)