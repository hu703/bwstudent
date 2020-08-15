# 数据库设计
class students(db.Model):
    <!-- 学号 -->
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    <!-- 姓名 -->
    name = db.Column(db.String(10),nullable=False)
    <!-- 年龄 -->
    age = db.Column(db.Integer,nullable=False)
    <!-- 性别 -->
    sex = db.Column(db.String(1),nullable=False)
    <!-- 英语成绩 -->
    english = db.Column(db.Integer,default=0)
    <!-- C语言成绩 -->
    c = db.Column(db.Integer,default=0)
    <!-- python成绩 -->
    python = db.Column(db.Integer,default=0)