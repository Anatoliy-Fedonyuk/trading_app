from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
import time

from src.auth.base_config import current_user
from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/long_operation")
@cache(expire=60)
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"


@router.get("")
# @cache(expire=60)
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).filter(operation.c.type == operation_type)
        result = await session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        records = [dict(zip(columns, row)) for row in rows]
        return {
            "status": "success",
            "data": records,
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам - Логировать!
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


# @router.get("/main") # Глупость какая-то
# async def main(session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(1))
#     rows = result.fetchall()
#     columns = result.keys()
#     records = [dict(zip(columns, row)) for row in rows]
#     return records
