# Shared Airtable field schemas for tools

# Common field definitions used by both create and update tools
AIRTABLE_FIELDS_SCHEMA = {
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
    "Due date / time": {
        "type": "string",
        "description": "Due date and time in ISO 8601 format (e.g., '2024-12-31T23:59:00.000Z' or '2024-12-31T15:30:00')."
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
}

def build_fields_parameter(description: str, required_fields: list = None):
    """
    Build a fields parameter object for Airtable tools.
    
    Args:
        description: Description for the fields parameter
        required_fields: List of required field names (optional)
    
    Returns:
        Dictionary representing the fields parameter schema
    """
    schema = {
        "type": "object",
        "description": description,
        "properties": AIRTABLE_FIELDS_SCHEMA.copy()
    }
    
    if required_fields:
        schema["required"] = required_fields
        
    return schema 