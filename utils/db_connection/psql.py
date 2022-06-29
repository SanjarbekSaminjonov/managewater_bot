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
        res = await self.execute(sql, str(telegram_id), fetchval=True)
        return res

    async def get_user_full_name(self, telegram_id):
        sql = 'select id, first_name, last_name from accounts_user where telegram_id = $1'
        user = await self.execute(sql, str(telegram_id), fetchrow=True)
        if user is not None:
            return f'{user[1]} {user[2]}'

    async def get_user_channel_devices(self, telegram_id):
        user_id = await self.get_user_id(telegram_id)
        sql = 'select device_id, name from channels_channeldevice where user_id = $1'
        return await self.execute(sql, user_id, fetch=True)

    async def get_channel_device_info(self, device_id):
        sql = '''
            select device_id, name, phone_number, height, height_conf, user_id
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
            select id h1, h2, w1, w2, vol, bat, net, created_at
            from channels_channelmessage
            where channel_device_id = $1
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
