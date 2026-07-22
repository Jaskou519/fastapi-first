from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 注册： 用户名和密码 → str
class User(BaseModel):
    username: str = Field(default="张三", min_length=2, max_length=10, description="用户名，长度要求2-10个字")
    password: str = Field(min_length=3, max_length=20)


@app.post("/register")
async def register(user: User):
    return user


class Book(BaseModel):
    title: str = Field(..., min_length=2, max_length=20, description="书名")
    author: str = Field(min_length=2, max_length=10, description="作者")
    press: str = Field(default="宝睿出版社", description="出版社")
    price: float | int = Field(..., gt=0, description="售价，价格要求大于0")


@app.post("/book")
async def addBook(book: Book):
    return book