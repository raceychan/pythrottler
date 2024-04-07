import json
from typing import Generic

from redis import Redis
from redis.asyncio.client import Redis as AioRedis

from premier._types import _K, _V, AsyncQuotaCounter, QuotaCounter, T


class MemoryCounter(Generic[_K, _V], QuotaCounter[_K, _V]):
    def __init__(self):
        self._map = dict[_K, _V]()

    def get(self, key: _K, default: T = None) -> _V | T:
        return self._map.get(key, default)

    def set(self, key: _K, val: _V):
        self._map[key] = val

    def clear(self, keyspace: str = ""):
        if not keyspace:
            self._map.clear()

        keys = [key for key in self._map if key.startswith(keyspace)]  # type: ignore
        for k in keys:
            self._map.pop(k, None)


class AsyncMemoryCounter(MemoryCounter, Generic[_K, _V], AsyncQuotaCounter[_K, _V]):
    def __init__(self):
        super().__init__()

    async def get(self, key: _K, default: T = None) -> _V | T:
        return super().get(key, default)

    async def set(self, key: _K, val: _V):
        super().set(key, val)

    async def clear(self, keyspace: str = ""):
        super().clear(keyspace)


class RedisCounter(Generic[_K, _V], QuotaCounter[_K, _V]):
    def __init__(self, redis: Redis, *, ex_s: int = 30) -> None:
        self._redis = redis
        self._ex_s = ex_s

    def get(self, key: _K, default: T = None) -> _V | T:
        val = self._redis.get(key)  # type: ignore
        val = json.loads(val) if val else default  # type: ignore
        return val

    def set(self, key: _K, value: _V):
        val = json.dumps(value)
        self._redis.set(key, val, ex=self._ex_s)  # type: ignore

    def clear(self, keyspace: str = ""):
        script = """
        return redis.call('del', unpack(redis.call('keys', ARGV[1])))
        """
        self._redis.eval(
            script,
            0,
            f"{keyspace}:*",
        )


class AsyncRedisCounter(Generic[_K, _V], AsyncQuotaCounter[_K, _V]):
    def __init__(self, redis: AioRedis, *, ex_s: int = 30) -> None:
        self._redis = redis
        self._ex_s = ex_s

    async def get(self, key: _K, default: T = None) -> _V | T:
        val = await self._redis.get(key)  # type: ignore
        val = json.loads(val) if val else default  # type: ignore
        return val

    async def set(self, key: _K, value: _V):
        val = json.dumps(value)
        await self._redis.set(key, val, ex=self._ex_s)  # type: ignore

    async def clear(self, keyspace: str = ""):
        script = """
        return redis.call('del', unpack(redis.call('keys', ARGV[1])))
        """
        await self._redis.eval(
            script,
            0,
            f"{keyspace}:*",
        )
