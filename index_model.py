import pandas

pandas.set_option('display.width', 800)
pandas.set_option('display.max_columns', None)


def get_movie(conn):
    return pandas.read_sql('''
        SELECT movie_id, 
            movie_name
        FROM movie
    ''', conn)


def get_genre(conn):
    return pandas.read_sql('''
        SELECT genre_id, 
            genre_name
        FROM genre
    ''', conn)


def get_actor(conn):
    return pandas.read_sql('''
        SELECT actor_id, 
            actor_name
        FROM actor
    ''', conn)


def get_age(conn):
    return pandas.read_sql('''
        SELECT age_id, 
            age_name
        FROM age
    ''', conn)


def get_director(conn):
    return pandas.read_sql('''
        SELECT director_id, 
            director_name
        FROM director
    ''', conn)


def get_country(conn):
    return pandas.read_sql('''
        SELECT country_id, 
            country_name
        FROM country
    ''', conn)


def get_hall(conn):
    return pandas.read_sql('''
        SELECT hall_id, 
            hall_capacity
        FROM hall    
    ''', conn)


def get_time_type(conn):
    return pandas.read_sql('''
        SELECT time_type_id, 
            time_type_name
        FROM time_type
    ''', conn)


def buy_tickets(conn, session_id, count1, count2, count3):
    cur = conn.cursor()
    cur.execute('''
        UPDATE ticket
        SET free_tickets = free_tickets - :c1
        WHERE session_id = :s and seat_type_id = 1
    ''', {"s": session_id, "c1": count1})
    cur.execute('''
        UPDATE ticket
        SET free_tickets = free_tickets - :c2
        WHERE session_id = :s and seat_type_id = 2
    ''', {"s": session_id, "c2": count2})
    cur.execute('''
        UPDATE ticket
        SET free_tickets = free_tickets - :c3
        WHERE session_id = :s and seat_type_id = 3
    ''', {"s": session_id, "c3": count3})


def get_filter_table(conn, movie, genre, country, actor, director, age, hall, date, time):
    m = g = c = ac = di = ag = h = d = t = ''
    if not movie:
        for i in range(11):
            m += str(i+1) + ', '
        m = m[:-2]
    if not genre:
        for i in range(7):
            g += str(i+1) + ', '
        g = g[:-2]
    if not country:
        for i in range(6):
            c += str(i+1) + ', '
        c = c[:-2]
    if not actor:
        for i in range(31):
            ac += str(i+1) + ', '
        ac = ac[:-2]
    if not director:
        for i in range(11):
            di += str(i+1) + ', '
        di = di[:-2]
    if not age:
        for i in range(4):
            ag += str(i+1) + ', '
        ag = ag[:-2]
    if not hall:
        for i in range(3):
            h += str(i+1) + ', '
        h = h[:-2]
    if not date:
        d = '"19.01.2024", "20.01.2024", "21.01.2024", "22.01.2024", "23.01.2024", "24.01.2024", "25.01.2024"'
    if (not time) or (time == '0'):
        t = '1, 2, 3'

    if not m:
        for i in range(len(movie)):
            if i == len(movie)-1:
                m = m + str(movie[i])
            else:
                m = m + str(movie[i]) + ', '
    if not g:
        for i in range(len(genre)):
            if i == len(genre)-1:
                g = g + str(genre[i])
            else:
                g = g + str(genre[i]) + ', '
    if not c:
        for i in range(len(country)):
            if i == len(country)-1:
                c = c + str(country[i])
            else:
                c = c + str(country[i]) + ', '
    if not ac:
        for i in range(len(actor)):
            if i == len(actor)-1:
                ac = ac + str(actor[i])
            else:
                ac = ac + str(actor[i]) + ', '
    if not di:
        for i in range(len(director)):
            if i == len(director)-1:
                di = di + str(director[i])
            else:
                di = di + str(director[i]) + ', '
    if not ag:
        for i in range(len(age)):
            if i == len(age)-1:
                ag = ag + str(age[i])
            else:
                ag = ag + str(age[i]) + ', '
    if not h:
        for i in range(len(hall)):
            if i == len(hall)-1:
                h = h + str(hall[i])
            else:
                h = h + str(hall[i]) + ', '
    if not d:
        d = f'"{date}"'
    if not t:
        t = f'{time}'

    return pandas.read_sql(f'''
        SELECT 
            date as Дата,
            time as Время,
            movie_name as Название,
            genre_name as Жанр,
            country_name as Страна,
            actor_name as Актеры,
            director_name as Режиссер,
            duration as Длительность,
            age_name as Возраст,
            hall_id as Зал,
            session_id as Сеанс, 
            sum(free_tickets) as Билет
        FROM (
            SELECT 
                date,
                time,
                movie_name,
                genre_name,
                country_name,
                group_concat(actor_name) as actor_name,
                director_name,
                age_name,
                duration,
                hall_id,
                session_id
            FROM 
                movie
                natural join country
                natural join genre
                natural join movie_actor
                natural join actor
                natural join director
                natural join age
                natural join session
                natural join hall
            WHERE 
                movie_id in ({m}) and 
                genre_id in ({g}) and 
                country_id in ({c}) and 
                actor_id in ({ac}) and 
                director_id in ({di}) and 
                age_id in ({ag}) and 
                hall_id in ({h}) and 
                date in ({d}) and
                time_type_id in ({t})
            GROUP BY movie_id, session_id ) x
            natural join ticket
        GROUP BY session_id    
    ''', conn)
