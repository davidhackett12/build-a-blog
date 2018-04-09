from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(2000))

    def __init__(self,title,content):
        self.title = title
        self.content = content

    
@app.route('/')
def index():
    posts = Blog.query.all()
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
            return redirect('/')
    
    return render_template('newpost.html', title = "", content= "", title_error = "", content_error = "")

if __name__ == '__main__':
    app.run() 







