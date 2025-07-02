from typing import Dict

from openai.types.shared_params import FunctionDefinition
from openai.types.chat import ChatCompletionToolParam

from src.agents.custom.tools.tool import Tool
import src.services.airtable_service as airtable_service


class AirtableCreateRecordTool(Tool):
    function_definition = ChatCompletionToolParam(
        type="function",
        function=FunctionDefinition(
            name="create_airtable_record",
            description="Creates a new record in Airtable.",
            parameters={
                "type": "object",
                "properties": {
                    "fields": {
                        "type": "object",
                        "description": "A dictionary of Airtable field names and their values.",
                        "properties": {
                            "Name": {
                                "type": "string",
                                "description": "A short name or title for the record."
                            },
                            "Notes": {
                                "type": "string",
                                "description": "Additional details or description."
                            },
                            "Status": {
                                "type": "string",
                                "enum": ["Todo", "In progress", "Done"],
                                "description": "The current status of the record."
                            },
                            "Attachments": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "url": {
                                            "type": "string",
                                            "description": "Publicly accessible URL to an attachment."
                                        }
                                    },
                                    "required": ["url"]
                                },
                                "description": "List of file URLs to attach to the record."
                            }
                        },
                        "required": ["Name", "Notes"]
                    }
                },
                "required": ["fields"],
            },
        )
    )

    def __call__(self, fields: Dict) -> str:
        record = airtable_service.create_record("Backlog", fields)
        return str(record.items())
