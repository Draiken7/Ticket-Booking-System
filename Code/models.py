from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, Security
from sqlalchemy import Time
# UserMixin adds useful functions that are ready to use directly, as does RoleMixin

db = SQLAlchemy()


#▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐ DATABASE MODELS ▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐
#-------------- Association Schemas -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#============== Roles and Users Association Table ===================================================================================================================================================================================
role_users = db.Table('role_users',
                      db.Column('users_id', db.Integer(),
                                db.ForeignKey('users.id')),
                      db.Column('roles_id', db.Integer(),
                                db.ForeignKey('roles.id')))

#====================================================================================================================================================================================================================================
#====================================================================================================================================================================================================================================
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
# ------------- Users Schema ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable = False, unique = True)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean())
    theater = db.relationship('Theaters', cascade='delete')
    movies = db.relationship('Movies', cascade='delete')
    bookings = db.relationship('Bookings')
    fs_uniquifier = db.Column(db.String(255), unique = True, nullable = False)
    roles = db.relationship('Roles', secondary=role_users,
                           backref=db.backref('users', lazy='dynamic'))
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
# ------------- Roles Schema ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Roles(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False, unique = True)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
# ------------- Theaters Schema ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Theaters(db.Model):
    __tablename__='theaters'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    userid = db.Column(db.Integer, db.ForeignKey(Users.id))
    name = db.Column(db.String, nullable = False, unique = True)
    location = db.Column(db.String, nullable = False)
    capacity = db.Column(db.Integer, nullable = False)
    showing = db.relationship('Shows', cascade="delete")
    
    
    def to_json(self):
        show_out = []
        for i in self.showing:
            if i.active:
                show_out.append(i.to_json())
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'capacity': self.capacity,
            'shows': show_out,
        }
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
# ------------- Movies Schema --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    userid = db.Column(db.Integer, db.ForeignKey(Users.id))
    name = db.Column(db.String, unique = True, nullable = False)
    rating = db.Column(db.String)
    userRating = db.Column(db.Float)
    tags = db.Column(db.String)
    duration = db.Column(Time, nullable = False)
    shows = db.relationship('Shows')
    
    def to_json(self):
        show_out = []
        for i in self.shows:
            if i.active:
                show_out.append(i.to_json())
        return {
            'id': self.id,
            'name': self.name,
            'rating': self.rating,
            'userRating': self.userRating,
            'tags':self.tags,
            'duration':self.duration.strftime('%H:%M'),
            'shows': show_out
        }
        
    def to_json2(self):
        show_out = []
        for i in self.shows:
            if i.active:
                show_out.append(i.to_json2())
        return {
            'id': self.id,
            'name': self.name,
            'rating': self.rating,
            'userRating': self.userRating,
            'tags':self.tags,
            'duration':self.duration.strftime('%H:%M'),
            'shows': show_out
        }
        
    def to_json3(self):
        show_out = []
        for i in self.shows:
            if i.active:
                show_out.append(i.to_json2())
        return {
            'id': self.id,
            'name': self.name,
            'rating': self.rating,
            'userRating': self.userRating,
            'tags':self.tags,
            'duration':self.duration.strftime('%H:%M'),
            'shows': show_out
        }
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
# ------------- Shows Schema ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    theaterid = db.Column(db.Integer, db.ForeignKey(Theaters.id))
    movieid = db.Column(db.Integer, db.ForeignKey(Movies.id))
    title = db.Column(db.String, nullable = False)
    caption = db.Column(db.Text)
    starton = db.Column(db.DateTime, nullable=False)
    endon = db.Column(db.DateTime, nullable=False)
    s_time = db.Column(Time, nullable=False)
    e_time = db.Column(Time, nullable=False)
    price = db.Column(db.Float, nullable = False)
    active = db.Column(db.Boolean, default=True)
    availableShows = db.relationship('Available', cascade = 'delete')
    
    def to_json(self):
        return {
            'id': self.id,
            'theaterid':self.theaterid,
            'movieid':self.movieid,
            'title': self.title,
            'caption':self.caption,
            'starton': self.starton.strftime('%Y-%m-%d'),
            'endon': self.endon.strftime('%Y-%m-%d'),
            'time':self.s_time.strftime('%H:%M'),
            'price':self.price
        }
    
    
    def to_json2(self):
        theater = Theaters.query.filter(Theaters.id==self.id).first()
        return {
            'id': self.id,
            'theaterid':self.theaterid,
            'name':theater.name,
            'location':theater.location,
            'movieid':self.movieid,
            'title': self.title,
            'caption':self.caption,
            'starton': self.starton.strftime('%Y-%m-%d'),
            'endon': self.endon.strftime('%Y-%m-%d'),
            'time':self.s_time.strftime('%H:%M'),
            'price':self.price
        }
    
        
    def to_json_avail(self, t, t5):
        avail = []
        for i in self.availableShows:
            if i.date >= t and i.date <= t5 and i.availableseats > 0:
                avail.append(i.to_json())
        return{
            'id': self.id,
            'theaterid':self.theaterid,
            'movieid':self.movieid,
            'title': self.title,
            'caption':self.caption,
            'starton': self.starton.strftime('%Y-%m-%d'),
            'endon': self.endon.strftime('%Y-%m-%d'),
            'time':self.s_time.strftime('%H:%M'),
            'availableShows':avail
        }
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------- Available Schema -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Available(db.Model):
    __tablename__='available'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    showid = db.Column(db.Integer,db.ForeignKey(Shows.id))
    date = db.Column(db.DateTime, nullable = False)
    s_time = db.Column(Time, nullable = False)
    e_time = db.Column(Time, nullable = False)
    availableseats = db.Column(db.Integer, nullable = False)
    bookings = db.relationship("Bookings")
    
    def to_json(self):
        # get dynamic Price
        show = Shows.query.filter(Shows.id == self.showid).first()
        theater = Theaters.query.filter(Theaters.id == show.theaterid).first()
        price = 0
        max_seats = 0
        if show:
            price = show.price
            max_seats = theater.capacity
        else:
            price = 0
        
        if max_seats > 0:
            a =  (self.availableseats*100)/max_seats
            if a > 90:
                price = price*0.95
            elif 90 >= a > 60:
                price = price*0.975
            elif 60 >= a > 25:
                pass
            elif 25 >= a > 10:
                price = price*1.05
            else:
                price = price*1.11
            
        return{
            "id":self.id,
            "showid":self.showid,
            "date":self.date.strftime('%Y-%m-%d'),
            "s_time":self.s_time.strftime('%H:%M'),
            "seats":self.availableseats,
            "price":price
        }
        pass

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------- Bookings Schema ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Bookings(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    userid = db.Column(db.Integer, db.ForeignKey(Users.id))
    bookingdate = db.Column(db.DateTime, nullable = False)
    bookedshow = db.Column(db.Integer,db.ForeignKey(Available.id))
    showid = db.Column(db.Integer, db.ForeignKey(Shows.id))
    theatername = db.Column(db.String)
    theaterlocation = db.Column(db.String)
    moviename = db.Column(db.String)
    bookedshowdate = db.Column(db.DateTime, nullable = False)
    bookedshowtime = db.Column(Time, nullable = False)
    seats = db.Column(db.Integer, nullable = False, default = 1)
    total = db.Column(db.Float, nullable = False)
    
    # date, time, theatername ,location , movie, booking date, seats, total
    def to_json_user(self):
        # avail = Available.query.filter()
        return{
            "bookingdate":self.bookingdate.strftime('%Y-%m-%d'),
            "theater": self.theatername,
            "location": self.theaterlocation,
            "movie":self.moviename,
            "showdate": self.bookedshowdate.strftime('%Y-%m-%d'),
            "showtime":self.bookedshowtime.strftime('%H:%M'),
            "seats":self.seats,
            "total":self.total          
        }
     
    def to_json_report(self):
        return{
            "bookingdate":self.bookingdate.strftime('%Y-%m-%d'),
            "theater": self.theatername,
            "location": self.theaterlocation,
            "movie":self.moviename,
            "showdate": self.bookedshowdate.strftime('%Y-%m-%d'),
            "showtime":self.bookedshowtime.strftime('%H:%M'),
            "seats":self.seats,
            "total":self.total          
        }
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------