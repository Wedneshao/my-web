from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # 必須設置，以使用 flash 消息
db = SQLAlchemy(app)

# 定義 Anime 模型
class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)

# 首頁路由
@app.route('/')
def home():
    anime_list = Anime.query.all()
    return render_template('home.html', anime_list=anime_list)

# 新增動漫路由
@app.route('/add_anime', methods=['GET', 'POST'])
def add_anime():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        if not title or not author or not content:
            flash('所有欄位皆為必填！')
            return redirect(url_for('add_anime'))

        new_anime = Anime(title=title, author=author, content=content)
        db.session.add(new_anime)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_anime.html')

# 動漫詳細資訊頁面路由
@app.route('/anime/<int:id>')
def anime_detail(id):
    anime = Anime.query.get_or_404(id)
    return render_template('anime.html', anime=anime)

@app.route('/delete_anime/<int:id>', methods=['POST'])
def delete_anime(id):
    anime = Anime.query.get_or_404(id)
    db.session.delete(anime)
    db.session.commit()
    flash('動漫已成功刪除！')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 確保資料庫表格被創建
    app.run(debug=True)
