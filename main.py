from urllib.parse import quote_plus
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker

#数据库连接信息
DB_USER = 'root@mysql001'
DB_PASSWORD = 'MySql123456.@'
DB_HOST = '127.0.0.1'
DB_PORT = 2881
DB_NAME = 'test'

#对用户名和密码进行 URL 编码，处理特殊字符
encoded_user = quote_plus(DB_USER)
encoded_password = quote_plus(DB_PASSWORD)

#创建数据库连接 URL
DATABASE_URL = f"mysql+mysqldb://{encoded_user}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#创建引擎
engine = create_engine(DATABASE_URL)

#创建基类
Base = declarative_base()

#定义模型
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', age={self.age})>"

#创建表
Base.metadata.create_all(engine)

#创建会话
Session = sessionmaker(bind=engine)
session = Session()

#插入数据
new_users = [
    User(name='John', age=20),
    User(name='Lucy', age=25),
    User(name='Tom', age=30)
]
session.add_all(new_users)
session.commit()

#更新数据
user = session.query(User).filter_by(name='Lucy').first()
if user:
    user.age = 26
    session.commit()

#查询数据
users = session.query(User).all()
for user in users:
    print(user)

#关闭会话
session.close()
