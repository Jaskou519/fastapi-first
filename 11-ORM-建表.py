from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()


# 1. 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_first?charset=utf8mb4"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 可选，输出 SQL 日志
    pool_size=10,  # 设置连接池活跃的连接数
    max_overflow=20  # 允许额外的连接数
)


# 2. 定义模型类： 基类 + 表对应的模型类
# 基类：创建时间、更新时间；书籍表：id、书名、作者、价格、出版社
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, onupdate=func.now(), comment="修改时间")


class Book(Base):               # 1. 继承 Base（相当于 Java 继承基础实体类）
    __tablename__ = "book"      # 2. 告诉框架：我对应数据库的 book 表

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")    # 3. 映射到 book 表的 id 列（主键）
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")     # 4. 映射到 book 表的 bookname 列
    author: Mapped[str] = mapped_column(String(255), comment="作者")       # 5. 映射到 book 表的 author 列
    price: Mapped[float] = mapped_column(Float, comment="价格")       # 6. 映射到 book 表的 price 列
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")   # 7. 映射到 book 表的 publisher 列


# 3. 建表：定义函数建表 → FastAPI 启动的时候调用建表的函数
async def create_tables():
    # 获取异步引擎，创建事务 - 建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Base 模型类的元数据创建


@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}
