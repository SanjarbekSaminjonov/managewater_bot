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
        sql = 'SELECT id FROM accounts_user WHERE telegram_id = $1'
        res = await self.execute(sql, str(telegram_id), fetchval=True)
        return res

    async def get_user_full_name(self, telegram_id):
        sql = 'SELECT id, first_name, last_name FROM accounts_user WHERE telegram_id = $1'
        user = await self.execute(sql, str(telegram_id), fetchrow=True)
        if user is not None:
            return f'{user[1]} {user[2]}'
