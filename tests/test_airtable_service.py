from dotenv import load_dotenv

load_dotenv()

from src.services.airtable_service import base, create_record, delete_record, get_all_records

def test_have_access_to_one_table_only():
    tables = base.tables()
    assert len(tables) == 1
    assert tables[0].name == "Backlog"

def test_all_records():
    test_record = create_record("Backlog", {"Name": "Daulet record"})
    records = get_all_records("Backlog")
    assert len(records) > 0
    deleted_record = delete_record("Backlog", test_record["id"])
    assert deleted_record["deleted"] == True
    assert deleted_record["id"] == test_record["id"]