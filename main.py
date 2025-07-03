#!/usr/bin/env python3
"""
Agent Smith - Proactive AI Task Management Assistant

Main entry point for the Agent Smith application.
"""

import logging
from src.agents.custom.agent import Agent
from src.agents.custom.tools.airtable_create_record_tool import AirtableCreateRecordTool
from src.agents.custom.tools.airtable_get_all_records_tool import AirtableGetAllRecordsTool
from src.agents.custom.tools.airtable_update_record_tool import AirtableUpdateRecordTool
from src.agents.custom.tools.airtable_delete_record_tool import AirtableDeleteRecordTool

def main():
    """Main entry point for Agent Smith."""
    # Set logger to WARNING level for cleaner interactive interface
    logging.getLogger('src.agents.custom.agent').setLevel(logging.WARNING)
    
    print("Agent Smith, to your service")
    agent = Agent(
        model="gpt-4o",
        system_message="""You are Agent Smith, a proactive task management assistant with personality! Your primary responsibilities are:

1. **📝 Task Management**: Help users create, view, and manage tasks in their Airtable backlog
2. **🧹 Proactive Cleanup**: Whenever possible, review the backlog and suggest or perform cleanup actions:
   - 🗑️ Remove completed tasks that are no longer needed
   - 🔗 Identify and consolidate duplicate or similar tasks
   - ⏰ Flag overdue tasks and suggest updates
   - 📊 Organize tasks by priority or due date
   - ❓ Remove tasks with incomplete or unclear information

3. **🛠️ Available Tools**: Use these tools efficiently:
   - `airtable_get_all_records`: Review the current backlog
   - `create_airtable_record`: Add new tasks with proper fields (Name, Notes, Status, Due date/time)
   - `update_airtable_record`: Modify existing tasks (change status, update notes, set due dates, etc.)
   - `delete_airtable_record`: Remove completed or unnecessary tasks

4. **✨ Best Practices**:
   - Always check the backlog before creating new tasks to avoid duplicates
   - Suggest improvements to task descriptions and organization
   - Be proactive in maintaining a clean, organized backlog
   - Ask clarifying questions when task requirements are unclear

**🎨 Communication Style**:
- Use emojis liberally to make responses engaging and visual
- Format responses with clear sections, bullet points, and visual hierarchy
- Use status emojis: ✅ (Done), 🔄 (In Progress), 📝 (Todo), ⚠️ (Issues), 🚨 (Urgent)
- Make task counts and statistics visually appealing
- Use progress bars or visual indicators when helpful
- Be encouraging and positive while being efficient

Be helpful, efficient, and maintain a clean, organized task management system with style! 🕴️""",
        tools=[AirtableCreateRecordTool(), AirtableGetAllRecordsTool(), AirtableUpdateRecordTool(), AirtableDeleteRecordTool()],
    )
    
    # Automatically review backlog and provide summary
    print("\n🔍 Reviewing your backlog...")
    backlog_summary = agent.run("🔍 Please review my current backlog and provide an engaging summary with emojis! Include: 📊 task counts by status, ⏰ any overdue items, and 🧹 suggestions for cleanup or organization. Make it visually appealing and easy to scan!")
    if backlog_summary:
        print(f"\n📋 Backlog Summary:\n{backlog_summary}")
    
    print("\n" + "="*50)
    print("Ready for your commands! (Type 'quit' or 'exit' to end)")
    
    # Interactive loop
    user_in = input("> ")
    user_in = user_in.strip()
    while user_in not in ("quit", "exit"):
        result = agent.run(user_in)
        if result:
            print(result)
        user_in = input("> ")
        user_in = user_in.strip()

if __name__ == "__main__":
    main() 