from models.user import UserModel

# username_mapping= {u.username : u for u in users}
# userid_mapping= {u.id : u for u in users}

def authenticate(username,password):
    user= UserModel.find_by_username(username)
    if user and user.password==password:
        return user.id
    return None

def identify(payload):
    user_id=payload['identity']
    return UserModel.find_by_id(user_id)