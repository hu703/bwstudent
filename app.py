from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy


# 链接数据库
host = "127.0.0.1"
port = 3306
username = 'huhu'
password = 'root'
database = 'bwstudent_db'
db_url = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8mb4'.format(username,password,host,port,database)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# 数据库设计
class students(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(10),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    sex = db.Column(db.String(1),nullable=False)
    english = db.Column(db.Integer,default=0)
    c = db.Column(db.Integer,default=0)
    python = db.Column(db.Integer,default=0)



# 首页
@app.route('/',endpoint='index')
def index():
    # db.create_all()
    return render_template('index.html')

# 录入信息
@app.route('/add/',endpoint='add',methods=['post','get'])
def add():
    if request.method.lower() == 'post':
        name = request.form.get('name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        english = request.form.get('english')
        python1 = request.form.get('python1')
        c = request.form.get('c')
        if not all([name,age,sex,english,python1,c]):
            return render_template('add.html',err='请输入完整信息')
        if sex == 'f':
            sex1 = '女'
        elif sex == 'm':
            sex1 = '男'
        student = students(name=name,age=age,sex=sex1,english=int(english),python=int(python1),c=int(c))
        db.session.add(student)
        db.session.commit()
        return render_template('add.html',ok='录入成功！')
    return render_template('add.html')

# 删除信息
@app.route('/remove/',endpoint='remove',methods=['post','get'])
def remove():
    if request.method.lower() == 'get':
        return render_template('remove.html')
    sign = request.args.get('sign')
    if sign == 'xz':
        pk = request.form.get('pk')
        if pk:
            student = students.query.filter(students.id==int(pk)).all()
            if student:
                return render_template('remove.html',pk=pk)
            return render_template('remove.html',err='查询不到该学生！')
        return render_template('remove.html',err='请保证数据完整!')
    elif sign == 'qr':
        xz  = request.form.get('xz')
        print(xz)
        if xz == 'y':
            id = request.args.get('id')
            students.query.filter(students.id==id).delete()
            db.session.commit()
            return render_template('remove.html',ok='删除成功！')
        elif xz == 'n':
            return render_template('remove.html')
    

# 修改信息
@app.route('/alter/',endpoint='alter',methods=['post','get'])
def alter():
    if request.method.lower() == 'get':
        return render_template('alter.html')
    sign = request.args.get('sign')
    if sign == 'xz':
        pk = request.form.get('pk')
        student = students.query.filter(students.id==pk).all()
        if student:
            return render_template('alter.html',stu=student[0])
        else:
            return render_template('alter.html',err='查询不到该学生！')
    if sign == 'alt':
        id = request.args.get('id')
        name = request.form.get('name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        english = request.form.get('english')
        python1 = request.form.get('python1')
        c = request.form.get('c')
        if not all([name,age,sex,english,python1,c]):
            return render_template('alter.html',err='请输入完整信息')
        if sex == 'f':
            sex1 = '女'
        elif sex == 'm':
            sex1 = '男'
        students.query.filter(students.id==id).update({students.name:name,students.age:age,students.sex:sex,students.english:english,students.python:python1,students.c:c})
        db.session.commit()
        return render_template('alter.html',ok='修改成功！')

# 查询信息
@app.route('/find/',endpoint='find',methods=['post','get'])
def find():
    if request.method.lower() == 'get':
        return render_template('find.html')
    pk = request.form.get('pk')
    student = students.query.filter(students.id==pk).all()
    if student:
        return render_template('find.html',stu=student[0])
    return render_template('find.html',err='查询不到该学生！')


# 信息排序
@app.route('/order/',endpoint='order',methods=['post','get'])
def order():
    if request.method.lower() == 'get':
        return render_template('order.html')
    score = request.form.get('score')
    px = request.form.get('px')
    if px == 'z':
        if score == 'english':
            stu = students.query.order_by(students.english).all()
        elif score == 'python':
            stu = students.query.order_by(students.python).all()
        elif score == 'c':
            stu = students.query.order_by(students.c).all()
        return render_template('order.html',stu=stu)
    elif px == 'd':
        if score == 'english':
            stu = students.query.order_by(students.english.desc()).all()
        elif score == 'python':
            stu = students.query.order_by(students.python.desc()).all()
        elif score == 'c':
            stu = students.query.order_by(students.c.desc()).all()
        return render_template('order.html',stu=stu)    
    return render_template('order.html')


# 学生人数
@app.route('/num/',endpoint='num',methods=['post','get'])
def num():
    count = students.query.count()
    return render_template('num.html',count=count)

# 全部信息
@app.route('/total/',endpoint='total',methods=['post','get'])
def total():
    student = students.query.all()
    return render_template('total.html',student=student)











if __name__ =="__main__":
    app.run(debug=True)