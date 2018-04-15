from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(2000))
    pub_date = db.Column(db.DATETIME)

    def __init__(self,title,content, pub_date=None):
        self.title = title
        self.content = content
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    
@app.route('/')
def index():
    blog_id = request.args.get("id")
    if blog_id:
        blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('oldpost.html', title = blog.title, content = blog.content)
    else:
        posts = Blog.query.order_by("pub_date desc").all()
        return render_template('index.html', posts = posts)


   
@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']

        if blog_title == "":
            title_error = "You did not include a title for your blog"
        else:
            title_error = ""

        if blog_content == "":
            content_error = "You did not include any content"
        else:
            content_error = ""
        
        if content_error or title_error:
            return render_template('newpost.html', title= blog_title, content= blog_content, title_error = title_error, content_error = content_error)
        else:
            new_blog = Blog(blog_title, blog_content)
            db.session.add(new_blog)
            db.session.commit()
            id_str = str(new_blog.id)

            return redirect('/?id='+id_str)
    
    return render_template('newpost.html', title = "", content= "", title_error = "", content_error = "")

if __name__ == '__main__':
    app.run() 







