import os
import time
from dataclasses import dataclass
from functools import wraps

from pyairtable import Api
from pyairtable.api.types import WritableFields, RecordDict, RecordDeletedDict

# Simple rate limiter - 5 requests per second max
_last_call_time = 0
_min_interval = 1.0 / 5  # 0.2 seconds between calls

def rate_limit(func):
    """Decorator to rate limit function calls to 5 per second"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        global _last_call_time
        current_time = time.time()
        time_since_last_call = current_time - _last_call_time
        
        if time_since_last_call < _min_interval:
            sleep_time = _min_interval - time_since_last_call
            time.sleep(sleep_time)
        
        _last_call_time = time.time()
        return func(*args, **kwargs)
    return wrapper

@dataclass
class EnvConfig:
    AIRTABLE_API_KEY: str = os.environ["AIRTABLE_API_KEY"]
    AIRTABLE_BASE_ID: str = os.environ["AIRTABLE_BASE_ID"]
    AIRTABLE_BACKLOG_TABLE_ID: str = os.environ["AIRTABLE_BACKLOG_TABLE_ID"]

env_config = EnvConfig()

api = Api(env_config.AIRTABLE_API_KEY)
base = api.base(env_config.AIRTABLE_BASE_ID)

@rate_limit
def create_record(table_name: str, fields: WritableFields) -> RecordDict:
    return base.table(table_name).create(fields)

@rate_limit
def get_all_records(table_name: str) -> list[RecordDict]:
    return base.table(table_name).all()

@rate_limit
def delete_record(table_name: str, record_id: str) -> RecordDeletedDict:
    return base.table(table_name).delete(record_id)

@rate_limit
def update_record(table_name: str, record_id: str, fields: WritableFields) -> RecordDict:
    return base.table(table_name).update(record_id, fields, replace=True)