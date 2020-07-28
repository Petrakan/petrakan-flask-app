from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Настройки проекта
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# Роутинг
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def article():
    articles = Articles.query.order_by(Articles.date.desc()).all()
    return render_template('articles.html', articles=articles)


@app.route('/articles/<int:id>')
def article_detail(id):
    article = Articles.query.get(id)
    return render_template('article_detail.html', article=article)


@app.route('/articles/<int:id>/update', methods=['POST', 'GET'])
def article_update(id):
    article = Articles.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/articles')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template('update_article.html', article=article)


@app.route('/articles/<int:id>/delete')
def article_delete(id):
    article = Articles.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/articles')
    except:
        return 'При удалении статьи произошла ошибка'


@app.route('/create_article', methods=['POST', 'GET'])
def article_create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Articles(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/articles')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create_article.html')


# Модели базы данных
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article - id: {}>'.format(self.id)


if __name__ == '__main__':
    app.run(debug=True)
