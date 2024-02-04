from flask import request, jsonify
from models import Users, Roles, role_users, Theaters, Movies, Shows, Available, Bookings
from sqlalchemy import desc
from flask_security.utils import verify_password, hash_password
from sqlalchemy import and_, or_
from flask_jwt_extended import JWTManager, create_access_token
from resources import rbac_required, getUser, getDate, getTime, getNow, timeadd, loopday, gettoday, dateadd, getnowDateTime
from app import datastore, db, cache
# from time import perf_counter_ns
import tasks


#▄▄▄ USER MANAGEMENT ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
#===-Signup-=========================================================================================================================================================================================================================   
def Signup():
    data = request.json         
    user = Users.query.filter(Users.username==data["username"]).first()
    mail= Users.query.filter(Users.email==data["email"]).first()
    
    # Check if username exists
    if user is not None:
        return jsonify({"message":"Username already Exists!"}), 406
    
    # Check if email exists
    elif mail is not None:
        return jsonify({"message":"Email already Registered!"}), 406 
    
    # Else Signup user with given username and email
    else:   
        data['password'] = hash_password(data['password'])
        datastore.create_user(**data)
        
        # Commit the creation of user
        try:
            db.session.commit()
            
        # IF nullable intigrety check fails
        except:
            return jsonify({"message":"None of the fields can be Empty!"}), 406           
        
        # Add default USER Role to User by default
        a = Users.query.filter(Users.email==data["email"]).first()
        b = Roles.query.filter(Roles.name=='user').first()
        
        #check there is a user role (which should be initialized at the start of the server)
        if b is None:
            return jsonify({"message":"Something went wrong!"}), 500
        
        # add role and commit
        datastore.add_role_to_user(a, b)
        db.session.commit()
        
    # Get Token
    token = create_access_token(identity=user)
    return jsonify({"user":{"token":token, "role":b.name}}), 201

#====================================================================================================================================================================================================================================    

#===-Login-==========================================================================================================================================================================================================================    
def Login():
    data = request.json
    if data["username"] == "":
        return jsonify({"error":"username cannot be empty!"}), 406
    # elif data["email"] == "":
    #     return jsonify({"error":"email cannot be empty!"}), 400
    elif data['password'] == "":
        return jsonify({"error":"password cannot be empty!"}), 406
        
    else:
        
        user = Users.query.filter(Users.username==data["username"], Users.active==True).first()
        print(user)
        if user is None:
            return jsonify({"error":"invalid username!"}), 406
        elif not (verify_password(data['password'], user.password)):
            return jsonify({"error":"Invalid password!"}), 406
        else:
            token = create_access_token(identity=data['username']) 
            return jsonify({"user":{"token":token, "role":user.roles[0].name}}), 200   
   
#====================================================================================================================================================================================================================================    

#===-Deactivate-=====================================================================================================================================================================================================================  
def Deactivate():
    user = getUser()
    if user is None:
        return jsonify({"error":"No such user"}), 406
    user.active = False
    return jsonify({"message":"user unregistered successfully!"}), 200

#====================================================================================================================================================================================================================================    
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄



#▄▄▄ ADMIN ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
#┼┼┼ Theaters ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼

#===-Create/Retrieve-================================================================================================================================================================================================================  
def TheaterCR():
    # Get current user id
    user = getUser()
    
    # retrieve all theaters given user
    if request.method == "GET":
        theaters = Theaters.query.filter(Theaters.userid==user.id).all()
        if len(theaters):
            theaters_out = [theater.to_json() for theater in theaters]
            return jsonify(theaters_out), 200
        else:
            return jsonify([]), 200
        
    # Add new theater for the user
    if request.method == "POST":
        # print(user.id)
        data = request.json
        
        # Data must contain name (unique), location, and capacity
        if data['name']=='' or data['location']=='' or data['capacity'] == None:
            return jsonify({"error":"None of the fields can be empty!"}), 406
        
        # Check if Theater name already exists for the user
        theater_exists = Theaters.query.filter(Theaters.name==data['name'], Theaters.userid==user.id).first()
        if theater_exists is not None:
            return jsonify({"error":"Theater with the same name exists!"}), 406
        else:
            theater = Theaters(name=data['name'], userid=user.id, location=data['location'], capacity=data['capacity'])
            db.session.add(theater)
            db.session.commit()
            return jsonify({"message":"Theater Created!", "id":theater.id}), 201

#====================================================================================================================================================================================================================================    
#===-Update/Delete-==================================================================================================================================================================================================================  
def TheaterUD(id):
    # Update Existing Theater details
    if request.method == "PUT":
        # Get current User
        user = getUser()
        data = request.json
        print("DATA", data)
        theater = Theaters.query.filter(Theaters.id==id).first()
        
        # Check if a theater with the new name already exists for the user
        th = Theaters.query.filter(Theaters.name==data['name'], Theaters.userid==user.id).first()
        
        if th is not None:
            return jsonify({"error":"Theater with the new name already exists!"}), 406
        if data["name"] and len(data["name"]):
            theater.name=data["name"]
        if data["location"] and len(data["location"]):
            theater.location=data["location"]
        if data["capacity"]:
            theater.capacity=data["capacity"]
        db.session.commit()
        return jsonify({"message":"changed data"}), 200
    
    
    if request.method == "DELETE":
        try:
            theater = Theaters.query.filter(Theaters.id==id).first()
            show = Shows.query.filter(Shows.theaterid==theater.id, Shows.active==True).order_by(desc(Shows.endon)).first()
            if theater is None:
                return jsonify({"error":"so such theater!"}), 406
            elif show is not None and getnowDateTime() < show.endon:
                return jsonify({"error":"cant delete theater that are currently running shows!"}), 403
            else:
                db.session.delete(theater)
                db.session.commit()
                return jsonify({"message":"Deleted Successfully"}), 200
        except:
            return jsonify({"error":"Something went wrong!"}), 500 

#====================================================================================================================================================================================================================================    
#┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
#┼┼┼ Movies ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
#===-Create/Retrieve-================================================================================================================================================================================================================  
def MoviesCR():
    # Get current user
    user = getUser()
    if request.method == "GET":
        movies = Movies.query.filter(Movies.userid==user.id).all()
        if len(movies):
            movies_out = [movie.to_json() for movie in movies]
            return jsonify(movies_out), 200
        else:
            return jsonify([]), 200
    
    if request.method == "POST":
        # print(user.id)
        data = request.json
        
        # Data must contain name (unique) and duration
        if data['name']=='' or data['duration']=='':
            return jsonify({"error":"Name/Duration cannot be empty!"}), 406
        
        # Check if Movie name already exists for the user
        movie_exists = Movies.query.filter(Movies.name==data['name'], Movies.userid==user.id).first()
        if movie_exists is not None:
            return jsonify({"error":"movie with the same name exists!"}), 406
        # elif theater is None:
        #     return jsonify({"error":"Theater with does not exist!"}), 400
        else:
            time = getTime(data['duration'])
            movie = Movies(name=data['name'], userid=user.id, rating=data['rating'], userRating=data['userRating'], tags=data['tags'], duration=time)
            db.session.add(movie)
            db.session.commit()
            return jsonify({"id":movie.id, "message":"movie Created!"}), 201   

#====================================================================================================================================================================================================================================    
#===-Update/Delete-==================================================================================================================================================================================================================  
def MoviesUD(id):
    if request.method == "PUT":
        data = request.json
        user = getUser()
        
        # Get the required movie
        movie = Movies.query.filter(Movies.id==id).first()
        
        # Check if a movie with the same name already exists
        s = Movies.query.filter(Movies.name == data['name'], Movies.userid == user.id).first()
        if s is not None:
            return jsonify({"error":"movie name already exists!"}), 406    
        
        if len(data["name"]):
            movie.name = data["name"]
        if len(data["rating"]):
            movie.rating = data["rating"]
        if data['userRating']:
            movie.userRating = data['userRating']
        if len(data['tags']):
            movie.tags = data['tags']
        db.session.commit()
        return jsonify({"message":"changed data"}), 200
    
    if request.method == "DELETE":
        try:
            movie = Movies.query.filter(Movies.id==id).first()
            if movie is None:
                return jsonify({"error":"No such movie!"}), 406
            else:
                db.session.delete(movie)
                db.session.commit()
                return jsonify({"message":"Deleted Successfully"}), 200
        except:
            return jsonify({"error":"Something went wrong!"}), 500 

#====================================================================================================================================================================================================================================    
#┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
#┼┼┼ Shows ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
#===-Create/Retrieve-================================================================================================================================================================================================================  
def ShowAdd():
    
    # data should have columns theaterid, movieid, title (non null), caption, starton (date, rquired), time (time, required),
    # endon (date, required) and price (required) Calculate active or not
    data = request.json
    if (data['id'] == None) or (data["movie"] == None) or (data['title'] == "") or (data["starton"] == "") or (data["endon"] == "") or (data["time"] == None) or (data["price"] == None):
        return jsonify({"error":"Noneof the reuired fields can be empty!"}), 406
    
    # Check if theater id and movie id are valid
    th = Theaters.query.filter(Theaters.id == data["id"]).first()
    mv = Movies.query.filter(Movies.id == data['movie']).first()
    
    if th is None:
        return jsonify({"error":"No such Theater!"}), 406
    if mv is None:
        return jsonify({"error":"No Such Movie!"}), 406
    
    # Check if starton date starts tomorrow, and endon date is atleast one day away from starton date, time will set the slot
    start = getDate(data['starton'])
    s_time = getTime(data['time'])
    end = getDate(data['endon'])
    e_time = timeadd(data['time'], mv.duration.strftime('%H:%M'))
    
    now = getNow()
    if (start <= now) or (start >= end):
        return jsonify({"error":"Start date has to be before the end date and after today!"}), 406
    
    # Check if there is another show running during the same time in the same theater
    run = Shows.query.filter(Shows.theaterid == data['id']).filter(or_(
        and_(Shows.s_time <= s_time, Shows.e_time >= s_time),
        and_(Shows.s_time <= e_time, Shows.e_time >= e_time)
    )).filter(or_(and_(Shows.starton <= start, Shows.endon >= start), and_(Shows.starton<=end, Shows.endon>=end))).first()
    
    # print(run)
    if run is not None:
        return jsonify({"error":"Another show runs in the same slot!"}), 406
    
    
    show = Shows(theaterid=data['id'], movieid=data['movie'], title=data['title'], caption=data['caption'], starton=start, endon=end, s_time=s_time, e_time=e_time, price=data['price'])
    db.session.add(show)
    db.session.commit()
    # print(show.id)
    a = start
    
    # Create available shows till end date
    while a <= end:
        av = Available(showid = show.id, date=a, s_time = show.s_time, e_time=show.e_time, availableseats = Theaters.query.filter(Theaters.id == show.theaterid).first().capacity)
        db.session.add(av)
        db.session.commit()
        a = loopday(a)
    
    return jsonify({"message":"Successfully mapped"}), 201

#====================================================================================================================================================================================================================================    
#===-Update/Delete-==================================================================================================================================================================================================================  
def ShowUD(id):
    
    # Retrieve all shows for a given THEATER ID
    if request.method == "GET":
        
        # check if there are shows for the given theater
        shows = Shows.query.filter(Shows.theaterid==id, Shows.active==True).all()
        if len(shows):
            show_out = [show.to_json() for show in shows]
            print(show_out)
            return jsonify(show_out), 200
        else:
            return jsonify([]), 200
    
    # Update show based on id
    if request.method == "PUT":
        
        data = request.json
        
        # Check if there are shows with the given id
        show = Shows.query.filter(Shows.id == id, Shows.active==True).first()
        if show is None:
            return jsonify({"error":"No such Show!"}), 406
        
        # update required non null fields
        else:
            if len(data['title']):
                show.title = data['title']
            if len(data['caption']):
                show.caption = data['caption']
            if data['price']:
                show.price = data['price']
            db.session.commit()
            return jsonify({"message": "updated Successfully!"}), 200
    
    
    # Delete show based on id IF ABSOLUTELY NECESSARY!
    if request.method == "DELETE":      
        try:
        # Check if show exists for given id
            show = Shows.query.filter(Shows.id==id).first()
            print(show)
            if show is None:
                return jsonify({"error":"No such show!"}), 406
            else:
                # Check if it is possible to delete the show without problems
                today = gettoday(True)
                today5 = dateadd(today, 5)
                if show.starton > today5:
                    db.session.delete(show)
                    db.session.commit()
                    return jsonify({"message":"Deleted Successfully!"}), 200
                else:
                    return jsonify({"error":"unable to DELETE, try deactivation!"}), 406
        except:
            return jsonify({"error":"Something Went Wrong!"}), 500
     
     
    # Deactivate show rather than delete it    
    if request.method == "PATCH":
        
        # Check if show with given id exists
        show = Shows.query.filter(Shows.id == id).first()
        if show is None:
            return jsonify({"error":"No such show found!"}), 406
        
        # Check if show is alreadt deactive or not
        elif not show.active:
            return jsonify({"error":"Show already inactive!"}), 406
        
        else:
            today = gettoday(True)
            today5 = dateadd(today, 5)
            #check if it is possible to deactivate the show
            theater = Theaters.query.filter(Theaters.id==show.theaterid).first()
            avail = Available.query.filter(Available.showid==show.id, Available.availableseats!=theater.capacity).first()
            if (show.endon < today) and (avail is not None):
                show.active = False
                db.session.commit()
                return jsonify({"message":"Show Deactivated!"}), 200
            else:
                return jsonify({"error":"There are booked shows!"}), 406

#====================================================================================================================================================================================================================================    
#┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄



#▄▄▄ USER QUERY ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
#┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
#===-Get Recent Movies-==============================================================================================================================================================================================================  
def Recent():
    two = getrecents()
    if two is None:
        return jsonify([]), 200
    else:
        sh = [show.id for show in two]
        movies = Movies.query.filter(Movies.id.in_(sh)).all()
        out = [show.to_json2() for show in movies]
        return jsonify(out), 200       

#====================================================================================================================================================================================================================================    

#===-Get All Shows for a Query (Movie based)-========================================================================================================================================================================================
def GetShows():
    name = request.args.get('name')
    value = request.args.get('value')
    objects = user_search_query(name, value)
       
    # If the filter is successful, return objects
    if len(objects):
        if name!='location' and name!='title':
            objects_out = [objct.to_json3() for objct in objects] 
        else:
            objects_out = [objct.to_json() for objct in objects]
        return jsonify(objects_out), 200
    else:
        return jsonify([]), 200
    
#====================================================================================================================================================================================================================================    

#===-Get all Available shows for a perticular Movies show instance-==================================================================================================================================================================  
def GetShow(id):
    today = gettoday(True)
    today5 = dateadd(today, 5)
    shows = Availshows(id)
    if len(shows):
        show = [show.to_json_avail(today, today5) for show in shows]
        return jsonify(show), 200
    else:
        return jsonify([]), 200
 
#====================================================================================================================================================================================================================================    
    
#===-Retrieve and Create Bookings-===================================================================================================================================================================================================  
def Booking():
    if request.method == "POST":
        user = getUser()
        data = request.json
        today = gettoday(True)
        # check if all given id's are valid!
        avail = Available.query.filter(Available.id == data['bookedshow']).first()
        c = ""
        error = False
        if user is None:
            error = True
            c = "No such User!"
        if avail is None:
            error = True
            c = "No such slot available!"
        if (not data["seats"]) or (not data["total"]):
            error = True
            c = "Seats/total must be specified!"
        
        if error:
            return jsonify({"error": c}), 406
        show = Shows.query.filter(Shows.id == avail.showid).first()
        th = Theaters.query.filter(Theaters.id == show.theaterid).first()
        mv = Movies.query.filter(Movies.id == show.movieid).first()
        book = Bookings(userid=user.id, bookingdate=today, bookedshow=avail.id, showid=avail.showid, seats=data['seats'], total=data['total'],
                        theatername=th.name, theaterlocation=th.location, moviename=mv.name, bookedshowdate=avail.date, bookedshowtime=avail.s_time)
        db.session.add(book)
        avail.availableseats -= int(book.seats)
        db.session.commit()
        return jsonify({"message":"show successfully booked!"}), 200    
    
    if request.method == "GET":
        # val = request.args.get('no')
        user = getUser()
        if user is None:
            return jsonify({"error":"No such user!"}), 406
        
        
        bookings = Bookings.query.filter(Bookings.userid == user.id).all()
        if len(bookings):
            book = [book.to_json_user() for book in bookings]
            return jsonify(book), 200
        else:
            return jsonify([]), 200

#====================================================================================================================================================================================================================================    

#┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
def GetCSV(id):
    j = tasks.getbookingsTheater.apply_async([id])
    return str(j), 200 


#▄▄▄ WORKER JOBS ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
#┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼


#┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄



#▄▄▄ PERFORMANCE ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
#┼┼┼ Cached ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
@cache.cached(timeout=50, key_prefix='recent_movies')
def getrecents():
    return Shows.query.filter(Shows.active==True).order_by(desc(Shows.starton)).limit(10).all()

# @cache.memoize(100)
def Availshows(id):
    return Shows.query.filter(Shows.id == id).all()

# @cache.memoize(100)
def user_search_query(name, value):
    objects = []
    
    # Filter Theaters by location
    if name == "location":
        objects = Movies.query.filter(Theaters.location.contains(f"%{value}%")).all()
        
    #Filter Theaters by Title (name)
    if name == "title":
        objects = Movies.query.filter(Theaters.name.contains(f"%{value}%")).all()

        
    #Filter by Movie ID
    if name == "movieid":
        objects = Movies.query.filter(Movies.id == value).all()
    
    # Filter Movies by tags
    if name == "tags":
        terms = value.split(',')
        filterval = [Movies.tags.ilike(f"%{term}%") for term in terms]
        objects = Movies.query.filter(*filterval).all()
    
    # Filter Movies by rating where rating is a valid rating
    if name == "rating":
        objects = Movies.query.filter(Movies.rating==value).all()
    
    # Filter Movies by userRating
    if name == "userRating":
        objects = Movies.query.filter(Movies.userRating >= value).all()
    
    # Filter Movies by name
    if name == "name":
        objects = Movies.query.filter(Movies.name.contains(f"%{value}%")).all()
        
    # If Nothing Works, return empty list
    return objects

#┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
#▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄