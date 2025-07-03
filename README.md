# Agent Smith 🤖

Agent Smith is a proactive AI-powered task management assistant that helps you organize and maintain your Airtable backlog efficiently.

## Features

- **Proactive Backlog Management**: Automatically reviews and suggests cleanup actions
- **Full CRUD Operations**: Create, read, update, and delete tasks
- **Smart Task Organization**: Identifies duplicates, flags overdue items, and suggests improvements
- **Rate-Limited API**: Built-in rate limiting for Airtable API calls
- **Interactive CLI**: Clean command-line interface for easy interaction

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   # Create .env file with your Airtable credentials
   AIRTABLE_API_KEY=your_api_key_here
   AIRTABLE_BASE_ID=your_base_id_here
   AIRTABLE_BACKLOG_TABLE_ID=your_table_id_here
   OPENAI_API_KEY=your_openai_key_here
   ```

3. **Run Agent Smith**:
   ```bash
   python main.py
   ```

## Usage

When you start Agent Smith, it will:
1. **Automatically review your backlog** and provide a summary
2. **Show task counts by status** and highlight any issues
3. **Suggest cleanup actions** for better organization
4. **Wait for your commands** in an interactive session

### Example Commands:
- "Create a new task for updating the documentation"
- "Show me all pending tasks"
- "Update the status of task XYZ to done"
- "Delete completed tasks from last week"

## Available Tools

- **Create Record**: Add new tasks with fields (Name, Notes, Status, Due date/time, Attachments)
- **Get All Records**: Review current backlog
- **Update Record**: Modify existing tasks
- **Delete Record**: Remove unnecessary tasks

## Task Fields

- **Name**: Task title (required)
- **Notes**: Detailed description (required)
- **Status**: Todo, In progress, or Done
- **Due date / time**: ISO 8601 format (e.g., `2024-12-31T23:59:00.000Z`)
- **Attachments**: File URLs

## Architecture

- **Agent Framework**: OpenAI GPT-powered conversational agent
- **Tool System**: Modular tools for Airtable operations
- **Shared Schemas**: DRY principle with reusable field definitions
- **Error Handling**: Graceful handling of API errors and edge cases

## Exit

Type `quit` or `exit` to end your session with Agent Smith.

---

*Agent Smith, to your service* 🕴️ 