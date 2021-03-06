from typing import Union

import asyncpg

from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST
        )

    async def execute(
            self, command, *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def get_user_id(self, telegram_id):
        sql = 'select id from accounts_user where telegram_id = $1'
        return await self.execute(sql, str(telegram_id), fetchval=True)

    async def get_user_telegram_id(self, user_id):
        sql = 'select telegram_id from accounts_user where id = $1'
        return await self.execute(sql, user_id, fetchval=True)

    async def get_user_full_name(self, telegram_id):
        sql = 'select id, first_name, last_name from accounts_user where telegram_id = $1'
        user = await self.execute(sql, str(telegram_id), fetchrow=True)
        if user is not None:
            return f'{user[1]} {user[2]}'

    async def get_user_info(self, telegram_id):
        sql = '''
            select username, first_name, last_name, region, city, org_name
            from accounts_user 
            where telegram_id = $1
        '''
        user = await self.execute(sql, str(telegram_id), fetchrow=True)
        if user is not None:
            return {
                'username': user[0],
                'first_name': user[1],
                'last_name': user[2],
                'region': user[3],
                'city': user[4],
                'org_name': user[5]
            }
        return {}

    async def get_user_channel_devices(self, telegram_id):
        user_id = await self.get_user_id(telegram_id)
        sql = 'select device_id, name from channels_channeldevice where user_id = $1'
        return await self.execute(sql, user_id, fetch=True)

    async def get_channel_device_info(self, device_id):
        sql = '''
            select device_id, name, phone_number, height, full_height, height_conf
            from channels_channeldevice 
            where device_id = $1
        '''
        return await self.execute(sql, device_id, fetchrow=True)

    async def get_channel_device_location(self, device_id):
        sql = '''
            select latitude, longitude
            from channels_channeldevice 
            where device_id = $1
        '''
        return await self.execute(sql, device_id, fetchrow=True)

    async def get_last_channel_device_message(self, device_id):
        sql = '''
            select h, water_volume, bat, is_charging, net, created_at
            from channels_channelmessage
            where device_id = $1
            order by created_at desc 
            limit 1
        '''
        return await self.execute(sql, device_id, fetchrow=True)

    async def get_base_device_type(self, device_id):
        sql = 'select type from exist_devices_device where id = $1'
        return await self.execute(sql, device_id, fetchval=True)

    async def change_state_base_device(self, is_active, device_id):
        sql = '''
            update exist_devices_device
            set is_active = $1
            where id = $2;
        '''
        await self.execute(sql, is_active, device_id, execute=True)

    async def add_new_channel_device(self, data):
        user_id = data.get('user_id')
        height_conf = data.get('height_conf')
        device_id = data.get('device_id')
        name = data.get('name')
        phone_number = data.get('phone_number')
        height = data.get('height')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        sql = '''
            insert into channels_channeldevice 
            (device_id, name, phone_number, height, height_conf, latitude, longitude, user_id)
            values ($1, $2, $3, $4, $5, $6, $7, $8)
        '''
        await self.execute(
            sql,
            device_id, name, phone_number, height, height_conf, latitude, longitude, user_id,
            execute=True
        )
        await self.change_state_base_device(True, device_id)

    async def check_user_and_device(self, watcher_id, device_id):
        sql = '''
            select id, connected_at 
            from watchers_channelwatcher 
            where watcher_id = $1 and device_id = $2
        '''
        return await self.execute(sql, watcher_id, device_id, fetchrow=True)

    async def add_new_channel_watcher(self, device_id, watcher_id):
        import datetime
        import pytz

        tz = pytz.timezone('Asia/Tashkent')
        now = datetime.datetime.now(tz)

        sql = '''
            insert into watchers_channelwatcher (connected_at, device_id, watcher_id)
            values ($1, $2, $3)
        '''
        await self.execute(sql, now, device_id, watcher_id, execute=True)
