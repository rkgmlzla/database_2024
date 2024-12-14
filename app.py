from flask import Flask, request, render_template
import sqlite3


app = Flask(__name__)


# 별점 / 후기 작성 페이지
@app.route('/performance/review')
def reviewPerformance():
   return render_template('review.html')

# 관람 리스트 페이지
@app.route('/performance/watched')
def watchedPerformance():
   return render_template('watched.html')

# 위시 리스트 페이지
@app.route('/performance/wish')
def wishPerformance():
   return render_template('wish.html')

# 검색 결과 페이지
@app.route('/performance/result', methods=['POST'])
def listPerformance(): 
   query = request.form.get('name')
   db = sqlite3.connect('dbproject.db')
   cursor = db.cursor()
   cursor.execute("SELECT pname, pplace, pdate, pcast, pposter FROM performances WHERE pname LIKE ?", ('%' + query + '%',))
   rows = cursor.fetchall()
   db.close()
   
   results = [
        {
            'pname': row[0],
            'pplace': row[1],
            'pdate' : row[2],
            'pcast': row[3],
            'pposter' : row[4]
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
