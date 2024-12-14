from flask import Flask, render_template, redirect, url_for, request
import sqlite3


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('dbproject.db')
    conn.row_factory = sqlite3.Row
    return conn


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

# 리뷰 작성 페이지
@app.route('/performance/review/<string:performance_id>', methods=['GET'])
def reviewPerformance(performance_id):
    conn = get_db_connection()
    performance = conn.execute('SELECT * FROM performances WHERE pid = ?', (performance_id,)).fetchone()
    conn.close()
    # 공연 정보를 리뷰 페이지로 전달
    return render_template('review.html', performance=performance)


# 리뷰 저장 라우트
@app.route('/performance/review/<string:performance_id>', methods=['POST'])
def saveReview(performance_id):
    review_star = request.form.get('review_star', type=int)  # 별점 (int)
    review_text = request.form.get('review_text')           # 리뷰 텍스트 (TEXT)

    conn = get_db_connection()
    
    # 해당 pid에 대한 리뷰가 이미 존재하는지 확인
    existing_review = conn.execute('SELECT * FROM reviews WHERE pid = ?', (performance_id,)).fetchone()
    if existing_review:
        conn.close()
        # 이미 리뷰가 존재하면 에러 메시지 페이지로 이동
        return render_template('reviewerror.html', performance_id=performance_id)
    
    # 리뷰 저장
    conn.execute('INSERT INTO reviews (pid, review_star, review_text) VALUES (?, ?, ?)',
                 (performance_id, review_star, review_text))
    conn.commit()
    conn.close()
    
    # 저장 완료 후 관람 리스트 페이지로 리디렉션
    return redirect(url_for('watched'))



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
