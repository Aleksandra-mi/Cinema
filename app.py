from flask import Flask, session


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# здесь необходимо указать все контроллеры страниц
# закомментировать еще не реализованные
import controllers.index
import controllers.buy
