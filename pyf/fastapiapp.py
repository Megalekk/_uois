from fastapi import FastAPI, Depends

import models.BaseEntities as BaseEntities
import models.FacilityEntities as FacilityEntities
import models.TimeTableEntities as TimeTableEntities

def attachFastApi(app, prepareSession=None):
    assert callable(prepareSession), 'prepareSession must be callable'
    apiapp = FastAPI()
    print('attaching attachFastApi')

    UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = BaseEntities.GetModels()
    EventModel = TimeTableEntities.GetModels()
    AreaModel, BuildingModel, RoomModel = FacilityEntities.GetModels()

    print('got models')

    @apiapp.get("/items/{item_id}")
    async def apif_read_item(item_id: int):
        
        return {"item_id": item_id}

    @apiapp.get("/")
    async def apif_root():
        return {"message": "Hello World"}


    @apiapp.get("/users/{id}")
    async def users_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(UserModel).get(id)
        return result

    @apiapp.get("/users/")
    async def users_get_all(skip: int = 0, limit: int = 10, session=Depends(prepareSession)):
        result = []
        result = session.query(UserModel).offset(skip).limit(limit).all()
        return result

    @apiapp.get("/users/{id}")
    async def users_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(UserModel).get(id)
        return result

    @apiapp.get("/groups/")
    async def groups_get_all(skip: int = 0, limit: int = 10, session=Depends(prepareSession)):
        result = []
        result = session.query(GroupModel).offset(skip).limit(limit).all()
        return result

    @apiapp.get("/groups/{id}")
    async def groups_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(GroupModel).get(id)
        return result

    @apiapp.get("/rooms/")
    async def rooms_get_all(skip: int = 0, limit: int = 10, session=Depends(prepareSession)):
        result = []
        result = session.query(RoomModel).offset(skip).limit(limit).all()
        return result

    @apiapp.get("/rooms/{id}")
    async def rooms_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(RoomModel).get(id)
        return result

    @apiapp.get("/events/")
    async def events_get_all(skip: int = 0, limit: int = 10, session=Depends(prepareSession)):
        result = []
        result = session.query(EventModel).offset(skip).limit(limit).all()
        return result

    @apiapp.get("/events/{id}")
    async def events_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(EventModel).get(id)
        return result

    app.mount('/api', apiapp)
    print('attaching attachFastApi finished')