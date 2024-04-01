# PyThrottler

pythrottler is an intuitive throttler that supports various backends and throttling algorihms, it can be used in distributed application for throttling web-api and any regular function.

- [PyThrottler](#pythrottler)
  - [Feature](#feature)
  - [Usage](#usage)
  - [Install](#install)
  - [Advanced Usage](#advanced-usage)
    - [Keyspace](#keyspace)
  - [Supported Backend](#supported-backend)
  - [Supported Algorithms](#supported-algorithms)
  - [requirements](#requirements)

## Feature

- Distributed throttling via redis or other backend.
- Support asyncio mode
- Support various throttling algorithms
- Designed to be highly customizable and extensible.

## Usage

1; decorate functions to be throttled

```python
from pythrottler import limits, throttler, ThrottleAlgo

@limits(quota=quota, duration_s=5, algo=ThrottleAlgo.FIX_WINDOW)
def add(a: int, b: int) -> int:
    res = a + b
    return res
```

## Install

```bash
pip install pythrottler
```

## Advanced Usage

### Keyspace

by default, pythrottler creates keyspace of this format for throttled functions

{keyspace}:{module}:{funcname}:{algorithm}

where:

| name | explain | default |
| -  | -  | -|
| keyspace | customized string provided by user | "" |
| module | module name where function is defined in | func.\_\_module__ |
| funcname | name of the function | func.\_\_name__ |
| algorithm | throttling algorithm of the function | fixed_window |



2; config throttler when app starts

```python
redis = Redis.from_url("redis://@127.0.0.1:6379/0")
throttler.config(quota_counter=RedisCounter(redis=redis))
```

## Supported Backend

| backend | supported|
| - | - |
| redis | True|
| memory | True|

## Supported Algorithms

| algorithm | supported |
| - | -|
| fixed window | True |
| sliding window | True |
| leaky bucket | True |
| token bucket | True |

## requirements

python >= 3.10
redis >= 5.0.3
