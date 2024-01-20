from app import app
from flask import render_template, request, session
from utils import get_db_connection
import datetime
from models.index_model import get_movie, get_genre, get_age, get_hall, get_actor, get_country, \
    get_director, get_time_type, get_filter_table, buy_tickets


@app.route('/', methods=['get', 'post'])
def index():
    conn = get_db_connection()
    df_movie = get_movie(conn)
    df_genre = get_genre(conn)
    df_age = get_age(conn)
    df_hall = get_hall(conn)
    df_actor = get_actor(conn)
    df_country = get_country(conn)
    df_director = get_director(conn)
    df_time = get_time_type(conn)
    checked_list_movie = []
    checked_list_genre = []
    checked_list_age = []
    checked_list_hall = []
    checked_list_actor = []
    checked_list_country = []
    checked_list_director = []
    date_type = 'all'
    time = 0
    date = ''
    # new_date = ''
    # f = False

    today = datetime.date.today()
    if request.values.get('reset'):
        a = 0
    elif request.values.get('pay'):
        print(request.values.get('pay'))
        val = request.values.get('pay').split('/')
        session_id = val[0]
        c1 = val[1]
        c2 = val[2]
        c3 = val[3]
        # buy_tickets(conn, session_id, c1, c2, c3)
    elif request.values.get('search') or request.values.get('all') or request.values.get('today') \
            or request.values.get('tomorrow') or request.values.get('time'):
        checked_list_movie = request.values.getlist('movie')
        checked_list_genre = request.values.getlist('genre')
        checked_list_age = request.values.getlist('age')
        checked_list_hall = request.values.getlist('hall')
        checked_list_actor = request.values.getlist('actor')
        checked_list_country = request.values.getlist('country')
        checked_list_director = request.values.getlist('director')
        if request.values.get('time'):
            time = request.values.get('time')

        if request.values.get('today'):
            date_type = 'today'
            d = today.day
            m = today.month
            y = today.year
            if d < 10:
                d = '0' + str(d)
            if m < 10:
                m = '0' + str(m)
            date = f"{d}.{m}.{y}"
        elif request.values.get('tomorrow'):
            date_type = 'tomorrow'
            t = today + datetime.timedelta(days=1)
            d = t.day
            m = t.month
            y = t.year
            if d < 10:
                d = '0' + str(d)
            if m < 10:
                m = '0' + str(m)
            date = f"{d}.{m}.{y}"

    df_session = get_filter_table(conn, checked_list_movie, checked_list_genre, checked_list_country,
                                  checked_list_actor, checked_list_director, checked_list_age,
                                  checked_list_hall, date, time)

    # elif request.values.get('ok'):
    #     f = True
    #     if request.values.get('new_date'):
    #         new_date = request.values.get('new_date')
    #         n = new_date.split('-')
    #         new_date = n[2] + '.' + n[1] + '.' + n[0]
    #     else:
    #         d = today.day
    #         m = today.month
    #         y = today.year
    #         if d < 10:
    #             d = '0' + str(d)
    #         if m < 10:
    #             m = '0' + str(m)
    #         new_date = f"{d}.{m}.{y}"
    #     date_type = 'new_date'

    print(request.values)
    html = render_template(
        'index.html',
        session_box=df_session,
        movie_box=df_movie,
        genre_box=df_genre,
        age_box=df_age,
        hall_box=df_hall,
        actor_box=df_actor,
        country_box=df_country,
        director_box=df_director,
        time_box=df_time,
        checked_list_movie=checked_list_movie,
        checked_list_genre=checked_list_genre,
        checked_list_age=checked_list_age,
        checked_list_hall=checked_list_hall,
        checked_list_actor=checked_list_actor,
        checked_list_country=checked_list_country,
        checked_list_director=checked_list_director,
        time=time,
        date_type=date_type,
        today=today,
        # new_date=new_date,
        # f=f,
        len=len,
        str=str,
        int=int
    )
    return html
