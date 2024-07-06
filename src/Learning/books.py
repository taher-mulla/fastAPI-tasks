from fastapi import *

app = FastAPI()

BOOKS = [
    {"Title":"Name one", "author":"Auth one"},
    {"Title":"Name two", "author":"Auth two"},
    {"Title":"Name three", "author":"Auth three"},
    {"Title":"Name four", "author":"Auth four"},
]

# general GET request
@app.get("/hello_world")
def helloworld():
    return{"message": "Hello World"}

@app.get("/books")
async def get_books():
    return BOOKS

@app.get("/string")
def rand():
    rand="this is random"
    return rand

@app.get("/list")
def rand():
    rand=["this", "is", "random"]
    return rand

# Path Parameter example
@app.get("/books/{dynamic_param}")
def dynamicP(dynamic_param):
    return dynamic_param

# Query Parameter example
@app.get("/parameters")
def queryP(title):
    return "this is /books/ "+title

# Path & Query Parameter example
@app.get("/parameters/{pathParam}/")
def dynamicPqueryP(pathParam, queryParam):
    return "this is /books/ "+pathParam+" this is dynamic "+queryParam

# basic POST methord with body
# POST should be used to create a entry/create data
@app.post("/books/createbook")
def createbook(book=Body()):
    BOOKS.append(book)
    return BOOKS


# basic PUT methord with body
# PUT should be used to update entry/create data
@app.put("/books/updatebook")
def updateBook(book_change=Body()):
    for i in BOOKS:
        if i.get("Title").casefold() == book_change.get("Title").casefold():
            i["author"]=book_change["author"]
    return BOOKS


# basic DELETE methord with body
@app.delete("/books/deletebook")
def deleteBook(book_change=Body()):
    for i in BOOKS:
        if i.get("Title").casefold() == book_change.get("Title").casefold():
            BOOKS.pop(BOOKS.index(i))
    return BOOKS


# basic DELETE methord
@app.delete("/books/deleteallbook")
def deleteallBooksBk():
    return BOOKS














