from flask import Flask, render_template, redirect, url_for, request
import sqlite3


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('dbproject.db')
    conn.row_factory = sqlite3.Row
    return conn


# 별점 / 후기 작성 페이지
@app.route('/performance/review')
def reviewPerformance():
   return render_template('review.html')

# 관람 리스트 페이지
@app.route('/performance/watched')
def watched():
    conn = get_db_connection()
    # `myperformances`와 `performances`를 JOIN
    watched_performances = conn.execute('''
        SELECT p.* FROM myperformances m
        JOIN performances p ON m.pid = p.pid
    ''').fetchall()
    conn.close()
    return render_template('watched.html', watched_performances=watched_performances)

# 관람 리스트에 공연 정보 추가
@app.route('/add_to_watched/<string:performance_id>', methods=['POST'])
def add_to_watched(performance_id):
    conn = get_db_connection()
    # `myperformances` 테이블에 `pid`만 추가
    exists = conn.execute('SELECT * FROM myperformances WHERE pid = ?', (performance_id,)).fetchone()
    if not exists:
        conn.execute('INSERT INTO myperformances (pid) VALUES (?)', (performance_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('watchedaddsuccess'))

# 관람 리스트 추가 성공 페이지
@app.route('/watchedaddsuccess')
def watchedaddsuccess():
    return render_template('watchedsuccess.html')

# 위시 리스트 로딩 페이지
@app.route('/performance/wish')
def LoadwishPerformance():
   return render_template('wish.html')


# 위시 리스트에 공연 정보 추가 
@app.route('/performance/add_wish', methods=['POST'])
def AddwishPerformance():
   return


# 검색 결과 페이지
@app.route('/performance/result', methods=['POST'])
def listPerformance(): 
   query = request.form.get('name')
   db = sqlite3.connect('dbproject.db')
   cursor = db.cursor()
   cursor.execute("SELECT pid, pname, pplace, pdate, pcast, pposter FROM performances WHERE pname LIKE ? OR pplace LIKE ? OR pcast LIKE ?", ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
   rows = cursor.fetchall()
   db.close()
   
   results = [
        {
            'pid' : row[0],
            'pname': row[1],
            'pplace': row[2],
            'pdate' : row[3],
            'pcast': row[4],
            'pposter' : row[5]
        }
        for row in rows
    ] 
   
   print(results)
   return render_template('result.html', results=results)
    
# 검색 엔진 페이지 
@app.route('/performance/search', methods=['GET', 'POST'])
def searchPerformance():
   return render_template('search.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
