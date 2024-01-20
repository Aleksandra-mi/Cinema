import pandas

pandas.set_option('display.width', 800)
pandas.set_option('display.max_columns', None)


def get_movie_description(conn, session_id):
    return pandas.read_sql(f'''
        SELECT session_id,
            movie_name as Название,
            date as Дата,
            time as Время,
            hall_id as Зал
        FROM session 
            natural join movie
        WHERE 
            session_id={session_id}
    ''', conn)


def get_movie_tickets(conn, session_id):
    return pandas.read_sql(f'''
        SELECT
            seat_type_name as 'Тип места',
            cost as 'Цена за билет',
            free_tickets as 'Осталось билетов',
            0 as 'Выбрано билетов',
            0 as 'Покупка'
        FROM session 
            natural join ticket
            natural join seat_type
        WHERE 
            session_id={session_id}
    ''', conn)


def buy_tickets(conn, session_id, seat_type, count):
    if seat_type == 'buy1':
        seat_type = 1
    elif seat_type == 'buy2':
        seat_type = 2
    elif seat_type == 'buy3':
        seat_type = 3
    session_id = int(session_id)
    count = int(count)

    cur = conn.cursor()
    cur.execute('''
        UPDATE ticket
        SET free_tickets = free_tickets - :c
        WHERE session_id = :s and :s_t = 1
    ''', {"s": session_id, "c": count, "s_t": seat_type})
