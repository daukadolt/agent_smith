import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

from pyairtable import Api
from pyairtable.api.types import WritableFields, RecordDict

@dataclass
class EnvConfig:
    AIRTABLE_API_KEY: str = os.environ["AIRTABLE_API_KEY"]
    AIRTABLE_BASE_ID: str = os.environ["AIRTABLE_BASE_ID"]
    AIRTABLE_BACKLOG_TABLE_ID: str = os.environ["AIRTABLE_BACKLOG_TABLE_ID"]

env_config = EnvConfig()

api = Api(env_config.AIRTABLE_API_KEY)
base = api.base(env_config.AIRTABLE_BASE_ID)

def create_record(table_name: str, fields: WritableFields) -> RecordDict:
    return base.table(table_name).create(fields)