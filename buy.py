from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.buy_model import get_movie_description, get_movie_tickets, buy_tickets


@app.route('/buy/<session_id>/', methods=['get', 'post'])
def buy(session_id):
    conn = get_db_connection()
    df_desc = get_movie_description(conn, int(session_id))
    df_tickets = get_movie_tickets(conn, int(session_id))
    # ticket_count1 = ticket_count2 = ticket_count3 = 0

    if request.values.get('Купить'):
        seat = request.values.get('Купить')
        if seat == 'buy1':
            count = request.values.get('count1')
        elif seat == 'buy2':
            count = request.values.get('count1')
        elif seat == 'buy3':
            count = request.values.get('count1')
        print(session_id)
        print(seat)
        print(count)
        buy_tickets(conn, session_id, seat, count)
        df_tickets = get_movie_tickets(conn, int(session_id))

    #     ticket_count1 = request.values.get('count1')
    #     print(ticket_count1)
    # if request.values.get('count2'):
    #     ticket_count2 = request.values.get('count2')
    #     print(ticket_count2)
    # if request.values.get('count3'):
    #     ticket_count3 = request.values.get('count3')
    #     print(ticket_count3)

    html = render_template(
        'buy.html',
        session_id=session_id,
        # ticket_count1=ticket_count1,
        # ticket_count2=ticket_count2,
        # ticket_count3=ticket_count3,
        desc_box=df_desc,
        tickets_box=df_tickets,
        len=len,
        int=int,
        str=str
    )
    return html
