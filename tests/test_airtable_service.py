import pprint

from src.services.airtable_service import base

def test_have_access_to_one_table_only():
    tables = base.tables()
    assert len(tables) == 1
    assert tables[0].name == "Backlog"