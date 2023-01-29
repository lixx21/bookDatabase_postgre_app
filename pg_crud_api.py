import random
from pg_connection import db_connect
from flask import Flask, jsonify, request

app = Flask(__name__)


connection, cursor = db_connect()

@app.route('/showData', methods=['GET'])
def showData():
     
    cursor.execute('SELECT * FROM book_list')
    data = cursor.fetchall()

    if len(data)  == 1:
        response_json = {
            "book_id" : data[0],
            "book_title": data[1],
            "author": data[2],
            "year_release": data[3],
        }
    else:
        response_json = {}
        for index in range(len(data)):
            response_json.update({
                f"book_{index}":
                {
                "book_id" : data[index][0],
                "book_title": data[index][1],
                "author": data[index][2],
                "year_release": data[index][3],
                }
            })

    return jsonify(response_json)
    
@app.route("/inputData", methods=["POST"])
def inputData():
    number = ""
    for i in range(6):
        number = number + str(random.randrange(0, 9))
    book_id = int(number)

    new_book_title = request.form.get('book_title')
    new_book_title = new_book_title.title()
    new_author = request.form.get('author')
    new_year_release = request.form.get('year_release')
    

    cursor.execute(f"INSERT INTO book_list \
                   (book_id, book_title, author, year_release) VALUES \
                   ({book_id},'{new_book_title}','{new_author}','{new_year_release}')")
    connection.commit()
    response_json = {
        'book_id':book_id, 
        'book_title':new_book_title,
        'author':new_author,
        'year_release':new_year_release
        }
    
    return jsonify(response_json) 

@app.route("/updateData", methods=["POST"])
def updateData():

    old_book_title = request.form.get('old_book_title')
    old_book_title = old_book_title.title()

    new_book_title = request.form.get('new_book_title')
    new_book_title = new_book_title.title()

    cursor.execute(f"SELECT book_id FROM book_list WHERE book_title = '{old_book_title}'")

    # book_id = cursor.fetchone()

    cursor.execute(f"UPDATE book_list SET book_title = '{new_book_title}' WHERE book_title = '{old_book_title}'")
    connection.commit()
    response_json = {
        "old_book_title": old_book_title,
        "new_book_title": new_book_title
    }

    return response_json

@app.route('/deleteData', methods=["POST"])
def deleteBook():
    delete_book_title = request.form.get('book_title')
    delete_book_title = delete_book_title.title()
    cursor.execute(f"DELETE FROM book_list WHERE book_title = '{delete_book_title}'")
    connection.commit()

    repsonse_json = {
        'deleted_book_title': delete_book_title
    } 

    return jsonify(repsonse_json)

# @app.after_request
# def after_request(response):
#     connection.close()
#     print('connection closed')
    
#     return response
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

    # connection.close()
    # print('connection closed')