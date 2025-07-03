from openai.types.chat import ChatCompletionToolParam

from src.agents.custom.tools.tool import Tool

import src.services.airtable_service as airtable_service

class AirtableDeleteRecordTool(Tool):
    function_definition = ChatCompletionToolParam(
        type="function",
        function={
            "name": "delete_airtable_record",
            "description": "Delete a record from an Airtable table by record ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "record_id": {
                        "type": "string",
                        "description": "The ID of the record to delete"
                    }
                },
                "required": ["record_id"]
            }
        }
    )
    
    def __call__(self, record_id: str) -> str:
        try:
            deleted_record = airtable_service.delete_record("Backlog", record_id)
            
            if deleted_record.get("deleted", False):
                return f"Successfully deleted record with ID: {record_id}"
            else:
                return f"Failed to delete record with ID: {record_id}"
                
        except Exception as e:
            return f"Error deleting record {record_id}: {str(e)}"