import asyncio
from contextlib import asynccontextmanager

import ujson
from aiopg.sa import create_engine
from sanic import Sanic, response
from sqlalchemy import select

from database import subscription, weather_state, weather, \
                     user, city, dbpath


app = Sanic(name='dashboard')

WS = {}
COND = {}


def user_update_query(uid):
    cols = [subscription.c.id.label('id'),
            weather_state.c.temperature,
            weather.c.name.label('weather'),
            city.c.name.label('city_name')]
    vtab = subscription.join(weather_state).join(weather).join(city)
    cond = subscription.c.user_id == uid
    query = select(cols).select_from(vtab).where(cond)
    return query


def related_users_query(city_id):
    cols = [user.c.id]
    vtab = subscription.join(user).join(weather_state).join(city)
    cond = city.c.id == city_id
    query = select(cols).select_from(vtab).where(cond)
    return query


async def ws_worker(cond, ws, query):
    while True:
        async with cond:
            await cond.wait()
        """
        it appears that postgres spending too much time persisting
        changes to disk/WAL (or django spending too much time submitting
        query to postgres server) which cause update being sent with old
        version of data. i'm not entierly sure what to do in such cases
        (not even serializable isolation level on both services helped)
        instead of actual polling, so i put that atrocious arbitary sleep
        here instead. as far as user has limited amount of subscriptions
        this should be overly enough for RDBMS to process 5 rows
        """
        await asyncio.sleep(1)  # Important!
        async with fetched(query) as proxy:
            data = {'data': [dict(row) async for row in proxy]}
            await ws.send(ujson.dumps(data))


@asynccontextmanager
async def fetched(query):
    async with create_engine(dbpath) as engine:
        async with engine.acquire() as conn:
            yield conn.execute(query)


@app.websocket('/subscribe/<uid:int>')
async def subscribe(request, ws, uid):
    WS[uid] = ws
    cond = COND[uid] = asyncio.Condition()
    query = user_update_query(uid)
    await ws_worker(cond, ws, query)


@app.post('/notify/<city_id:int>')
async def notify(request, city_id):
    query = related_users_query(city_id)
    async with fetched(query) as proxy:
        async for row in proxy:
            uid = row[0]
            if uid in COND:
                async with COND[uid]:
                    COND[uid].notify()
        return response.text('ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
