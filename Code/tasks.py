# from celery import AsyncResults
from workers import celery_app
from app import app, db, datastore
from models import Theaters, Users, Bookings, Movies, Shows, Available, role_users
from sqlalchemy import desc
from datetime import datetime
from resources import pastMonth
from mail import send_notifsReports


import pandas as pd
import random

bodys = [
"Unlock the Magic of Cinema: Book Your Showtime Today!",
"Lights, Camera, Tickets: Your Front Row to Blockbusters!",
"Cinematic Delights Await: Secure Your Seats in Seconds!",
"Elevate Your Movie Experience: Reserve Your Seats Now!",
"Seize the Screen: Book Tickets, Make Memories!",
"Silver Screens, Golden Moments: Book Your Movie Escape!",
"From Couch to Cinema: Your Ticket to Movie Magic!",
"Movie Nights Redefined: Grab Your Tickets and Popcorn!",
"Epic Adventures Begin Here: Book Your Movie Journey!",
"Don't Miss a Frame: Your Ticket to Unforgettable Cinema!"
]

# generate CSV
@celery_app.task
def getbookingsTheater(id):
    with app.app_context():
        th = Theaters.query.filter(Theaters.id==id).first()
        shows = Shows.query.filter(Shows.theaterid == id).all()
        mv = []
        rt = []
        bk = []
        er = []
        for show in shows:
            temp = Movies.query.filter(Movies.id==show.movieid).first()
            mv.append(temp.name)
            rt.append(temp.userRating)
            s = 0
            s2= 0
            temp2 = Available.query.filter(Available.showid==show.id).all()
            for av in temp2:
                s2 += len(av.bookings)
                for book in av.bookings:
                    s += book.total
            er.append(s)
            bk.append(s2)
            
        d = {
            "Dates":[show.starton.strftime('%Y-%m-%d') for show in shows],
            "Shows":[show.title for show in shows],
            "Movie":mv,
            "Rating":rt,
            "Bookings":bk,
            "Earnings":er
        }
        u = Users.query.filter(Users.id == th.userid).first()
        pd.DataFrame(d).to_csv(f"./generated/theater{th.id}.csv")
        data = {
            "user": {
                "name": u.username,
                "email": u.email
            },
            "theater":th.name
        }   
        send_notifsReports(data, 0, f"./generated/theater{th.id}.csv")
        return

# generate reminders
@celery_app.task
def sendVisitNotif():
    data= {}
    with app.app_context():
        now = datetime.now()
        role_users = datastore.find_role('user').users
        user = [user for user in role_users]
        for user in role_users:
            book = Bookings.query.filter(Bookings.userid == user.id).order_by(desc(Bookings.bookedshowdate)).first()
            if (book is None) or ((now-book.bookedshowdate).days > 2):
                a = random.randint(0, len(bodys)-1)
                print(a)
                data = {
                        "user": {
                                "name": user.username,
                                "email": user.email
                            },
                        "message":bodys[a]
                        }
                send_notifsReports(data, 1)
        
    return
    
# generate monthly reports
@celery_app.task
def sendMonthlyReports():
    with app.app_context():
        role_users = datastore.find_role('user').users
        then = pastMonth()
        now = datetime.now()
        for user in role_users:
            books = Bookings.query.filter(Bookings.id==user.id, Bookings.bookedshowdate<now, Bookings.bookedshowdate>=then).order_by(desc(Bookings.bookedshowdate)).limit(10)
            book_out = [book.to_json_report() for book in books]
            data = {
                "user": {
                    "name": user.username,
                    "email": user.email
                },
                "data":book_out
            }
            send_notifsReports(data, 2)
    return
                        