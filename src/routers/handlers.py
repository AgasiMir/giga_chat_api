from fastapi import APIRouter, Depends
from sqlalchemy import text

from src.database.db_depends import get_session

router = APIRouter(prefix="/handlers", tags=["handlers ⚙⚙⚙"])


@router.get('/check_db')
async def check_db(db = Depends(get_session)):
    response = await db.execute(text("SELECT 'Hello World!'"))
    response = response.scalar()
    return {"response": response}
