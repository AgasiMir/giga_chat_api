from fastapi import APIRouter, Depends
from sqlalchemy import text

from src.database.db_depends import get_session

router = APIRouter(prefix="/hanlers", tags=["handlers ⚙⚙⚙"])


@router.get('/check_db')
async def check_db(db = Depends(get_session)):
    version = await db.execute(text('SELECT version()'))
    version = version.scalar()
    return {"version": version}
