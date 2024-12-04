from flask import Flask, render_template


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
@app.route('/performance/result')
def listPerformance(): 
   return render_template('result.html')
    
# 검색 엔진 페이지 
@app.route('/performance/search', methods=['POST'])
def searchPerformance():
  return render_template('search.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
