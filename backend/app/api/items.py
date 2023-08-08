from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select,distinct
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.responses import Response

from app.deps.db import get_async_session
from app.deps.request_params import parse_react_admin_params
from app.deps.users import current_user
from app.models.item import Item
from app.models.user import User
from app.schemas.item import Item as ItemSchema
from app.schemas.item import ItemCreate, ItemUpdate
from app.schemas.request_params import RequestParams
from datetime import datetime


router = APIRouter(prefix="/items")


@router.get("/get_all", response_model=List[ItemSchema])
async def get_all_items(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    request_params: RequestParams = Depends(parse_react_admin_params(Item)),
) -> Any:
    total = await session.scalar(
        select(func.count(Item.id))
    )
    items = (
        (
            await session.execute(
                select(Item)
                .offset(request_params.skip)
                .limit(request_params.limit)
                .order_by(request_params.order_by)
            )
        )
        .scalars()
        .all()
    )
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(items)}/{total}"
    return items


@router.get("/completed-count", response_model=int)
async def get_completed_count(
    session: AsyncSession = Depends(get_async_session),
) -> int:
    completed_count = await session.scalar(
        select(func.count(Item.id))
        .where(Item.completed == True)  # Filter by completed=True
    )
    return completed_count



@router.get("/average_per_user")
async def get_average_todos_per_user(session: AsyncSession = Depends(get_async_session)) -> Any:
    total_todos = await session.scalar(
        select(func.count(Item.id))
    )
    total_users = await session.scalar(
        select(func.count(distinct(Item.user_id)))
    )

    if total_users > 0:
        average_per_user = total_todos / total_users
    else:
        average_per_user = 0

    return {"average_per_user": average_per_user}


@router.get("/average_duration_completed", response_model=float)
async def get_average_duration_completed(
    session: AsyncSession = Depends(get_async_session),
) -> float:
    average_duration = (
        await session.scalar(
            select(func.avg(Item.duration))
            .where(Item.completed == True)  # Filter completed items
        )
    )
    return average_duration


@router.get("/totals",response_model=float)
async def get_average_all_duration(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Item.user_id, func.avg(Item.duration))
        .group_by(Item.user_id)
        .where(Item.completed == True)  # Filter only completed items
    )

    average_durations = [
        {"user_id": user_id, "average_duration": avg_duration}
        for user_id, avg_duration in result
    ]

    result = await session.execute(
        select(func.count(User.id))
    )

    total_users = result.scalar()

    total_average_duration = sum(item["average_duration"] for item in average_durations)
    overall_average_duration = (
        total_average_duration / total_users
    ) if total_users > 0 else 0

    return {
        "total_users": total_users,
        "overall_average_duration": overall_average_duration,
        "average_durations_per_user": average_durations,
    }

@router.post("ite", response_model=ItemSchema, status_code=201)
async def create_it(
    item_data: ItemCreate,  # Accept item data from the request body
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    item = Item(**item_data.dict())
    session.add(item)
    await session.commit()
    return item



@router.get("", response_model=List[ItemSchema])
async def get_current_user_items(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
    request_params: RequestParams = Depends(parse_react_admin_params(Item)),
) -> Any:
    total = await session.scalar(
        select(func.count(Item.id))
        .where(Item.user_id == user.id)
    )
    items = (
        (
            await session.execute(
                select(Item)
                .where(Item.user_id == user.id)
                .offset(request_params.skip)
                .limit(request_params.limit)
                .order_by(request_params.order_by)
            )
        )
        .scalars()
        .all()
    )
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(items)}/{total}"
    return items


@router.post("", response_model=ItemSchema, status_code=201)
async def create_item(
    item_in: ItemCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Any:
    item = Item(**item_in.dict(), user_id=user.id)
    session.add(item)
    await session.commit()

    if item.completed:
        completed_time = datetime.now()  # Get the current time
        print(f"Item '{item.name}' completed at: {completed_time}")

    return item


@router.put("/{item_id}", response_model=ItemSchema)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Any:
    item: Optional[Item] = await session.get(Item, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(404)
    update_data = item_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    session.add(item)
    await session.commit()
    return item


@router.get("/{item_id}", response_model=ItemSchema)
async def get_item(
    item_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Any:
    item: Optional[Item] = await session.get(Item, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(404)
    return item


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Any:
    item: Optional[Item] = await session.get(Item, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(404)
    await session.delete(item)
    await session.commit()
    return {"success": True}


@router.get("/average-duration/{item_id}")
async def get_average_duration(
    item_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    item: Optional[Item] = await session.get(Item, item_id)
    
    if item:
        query = select(
            func.avg(
                func.extract("epoch", Item.updated - Item.created) / 60
            )
        ).where(Item.id == item_id)
        
        average_duration = await session.scalar(query)
        
        if average_duration is None:
            average_duration = 0.0
        
        return {"average_duration_minutes": average_duration}
    
    return {"error": "Item not found"}

