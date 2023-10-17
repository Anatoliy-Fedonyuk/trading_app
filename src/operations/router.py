from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
import time

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
@cache(expire=60)
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).filter(operation.c.type == operation_type)
        result = await session.execute(query)
        return {"status": "success",
                "data": result.mappings().all(),
                "details": None}
    except Exception as e:
        # Логируйте ошибку и возвращайте более информативное сообщение.
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(e)})


@router.post("")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(operation).values(**new_operation.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "Add operation success"}
    except Exception as ex:
        # Логируйте ошибку и возвращайте более информативное сообщение.
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(ex)})
