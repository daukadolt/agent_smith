from typing import Dict

from openai.types.chat import ChatCompletionToolParam

from src.agents.custom.tools.tool import Tool
from src.agents.custom.tools.airtable_schemas import build_fields_parameter

import src.services.airtable_service as airtable_service

class AirtableUpdateRecordTool(Tool):
    function_definition = ChatCompletionToolParam(
        type="function",
        function={
            "name": "update_airtable_record",
            "description": "Update an existing record in an Airtable table by record ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "record_id": {
                        "type": "string",
                        "description": "The ID of the record to update"
                    },
                    "fields": build_fields_parameter(
                        description="A dictionary of Airtable field names and their new values."
                    )
                },
                "required": ["record_id", "fields"]
            }
        }
    )
    
    def __call__(self, record_id: str, fields: Dict) -> str:
        try:
            updated_record = airtable_service.update_record("Backlog", record_id, fields)
            return f"Successfully updated record {record_id}: {str(updated_record.get('fields', {}))}"
        except Exception as e:
            return f"Error updating record {record_id}: {str(e)}"