from typing import Union
from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel, Field

app = FastAPI()

users = []

class User(BaseModel):
    id: int = Field(default_factory=lambda: len(users) + 1)
    username: str = Field(..., min_length=3,
                                max_length=30,
                                description="Name")
    age: int = Field(..., ge=0, 
                        le=120, 
                        discription="The age of the user")

@app.get('/users/')
async def get_users() -> List[User]:
    '''

    '''
    return users

@app.post('/user/{username}/{age}', response_model=User)
async def create_user(username, age) -> User:
    '''
    '''
    new_id = len(users) + 1
    users.append(User(id = new_id, username = username, age = age))
    return User(id = new_id, username = username, age = age)

@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id, username, age) -> str:
    '''
    '''
    try:
        users[int(user_id)] = User(id = user_id, username = username, age = age)
        return f'The user {user_id} is updated'
    except IndexError:
        raise HTTPException(status_code=404, detail=f'User not found {int(user_id)}')
        
@app.delete('/user/{user_id}', response_model=User)
async def delit_user(user_id) -> str:
    '''
    '''
    try:
        users.pop(int(user_id))
        return f'The user {user_id} is delited'
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')
    