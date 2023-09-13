from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


db= SQLAlchemy(app)
migrate=Migrate(app,db)
marshmallow = Marshmallow(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    body = db.Column(db.Text)

    def __init__(self, title, author, body):
        self.title = title
        self.author = author
        self.body = body

class BlogSchema(marshmallow.Schema):
    class Meta:
        fields=('id','title','author','body')


blog_schema=BlogSchema()
blogs_schema=BlogSchema(many=True)

@app.route('/blog/create', methods=['POST'])
def create_blog():
    title = request.json['title']
    body = request.json['body']
    author = request.json['author']
    new_blog = Blog(title,body,author)
    db.session.add(new_blog)
    db.session.commit()
    return blog_schema.jsonify(new_blog), 201

@app.route('/blog/all', methods=['GET'])
def get_all_blog():
    all_blogs=Blog.query.all()
    result=blogs_schema.dump(all_blogs)
    return jsonify(result)

@app.route('/blog/<id>', methods=['GET'])
def get_blog(id):
    blog=Blog.query.get(id)
    return blog_schema.jsonify(blog)

@app.route('/blog/<id>', methods=['PUT'])
def update_blog(id):
    title = request.json['title']
    body = request.json['body']
    author = request.json['author']
    blog = Blog.query.get(id)
    blog.title=title
    blog.body=body
    blog.author=author
    db.session.commit()
    return blog_schema.jsonify(blog)

@app.route('/blog/delete/<id>', methods=['DELETE'])
def delete_blog(id):
    blog=Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    return blog_schema.jsonify(blog)

if __name__ == '__main__':
    app.run(debug=True)