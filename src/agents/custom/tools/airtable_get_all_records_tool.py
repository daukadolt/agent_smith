from openai.types.chat import ChatCompletionToolParam

from src.agents.custom.tools.tool import Tool

import src.services.airtable_service as airtable_service

class AirtableGetAllRecordsTool(Tool):
    function_definition = ChatCompletionToolParam(
        type="function",
        function={
            "name": "airtable_get_all_records",
            "description": "Get all records from an Airtable table",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }
    )

    def __call__(self, *args) -> str:
        return str(airtable_service.get_all_records("Backlog"))