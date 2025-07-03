from typing import Dict

from openai.types.shared_params import FunctionDefinition
from openai.types.chat import ChatCompletionToolParam

from src.agents.custom.tools.tool import Tool
from src.agents.custom.tools.airtable_schemas import build_fields_parameter
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
                    "fields": build_fields_parameter(
                        description="A dictionary of Airtable field names and their values.",
                        required_fields=["Name", "Notes"]
                    )
                },
                "required": ["fields"],
            },
        )
    )

    def __call__(self, fields: Dict) -> str:
        record = airtable_service.create_record("Backlog", fields)
        return str(record.items())
