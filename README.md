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
   # Create .env file with your credentials
   AIRTABLE_API_KEY=your_api_key_here
   AIRTABLE_BASE_ID=your_base_id_here
   AIRTABLE_BACKLOG_TABLE_ID=your_table_id_here
   OPENAI_API_KEY=your_openai_key_here
   
   # For Telegram bot interface (optional):
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

3. **Run Agent Smith**:
   ```bash
   # Interactive interface selection
   python main.py
   
   # Or start specific interface directly:
   python main.py --cli         # Command line interface
   python main.py --telegram    # Telegram bot (requires TELEGRAM_BOT_TOKEN)
   ```

## Interfaces

Agent Smith supports multiple interfaces:

### 💻 CLI (Command Line Interface)
- Interactive terminal-based interface
- Perfect for developers and power users
- Auto-reviews backlog on startup

![CLI Demo](assets/cli_demo.gif)

### 🤖 Telegram Bot
- Chat with Agent Smith via Telegram
- Mobile-friendly with rich formatting
- Commands: `/start`, `/help`, `/summary`
- Natural language processing

![Telegram Demo](assets/telegram_demo.gif)

## Usage

When you start Agent Smith, you can:
1. **Choose your interface** (CLI or Telegram)
2. **Get automatic backlog review** and summary
3. **Interact naturally** - just tell Agent Smith what you need
4. **Use commands or natural language** to manage tasks

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