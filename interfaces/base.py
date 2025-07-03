"""
Base interface for Agent Smith interactions.
Provides common functionality for different interface types.
"""

import logging
from abc import ABC, abstractmethod
from src.agents.custom.agent import Agent
from src.agents.custom.tools.airtable_create_record_tool import AirtableCreateRecordTool
from src.agents.custom.tools.airtable_get_all_records_tool import AirtableGetAllRecordsTool
from src.agents.custom.tools.airtable_update_record_tool import AirtableUpdateRecordTool
from src.agents.custom.tools.airtable_delete_record_tool import AirtableDeleteRecordTool


class BaseInterface(ABC):
    """Base class for Agent Smith interfaces."""
    
    def __init__(self, model: str = "gpt-4o", log_level: int = logging.WARNING):
        """Initialize the base interface with Agent Smith."""
        # Set up logging
        logging.getLogger('src.agents.custom.agent').setLevel(log_level)
        
        # Initialize the agent
        self.agent = Agent(
            model=model,
            system_message=self._get_system_message(),
            tools=[
                AirtableCreateRecordTool(), 
                AirtableGetAllRecordsTool(), 
                AirtableUpdateRecordTool(), 
                AirtableDeleteRecordTool()
            ],
        )
    
    def _get_system_message(self) -> str:
        """Get the system message for Agent Smith."""
        return """You are Agent Smith, a proactive task management assistant with personality! Your primary responsibilities are:

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

Be helpful, efficient, and maintain a clean, organized task management system with style! 🕴️"""
    
    def get_backlog_summary(self) -> str:
        """Get an engaging backlog summary."""
        return self.agent.run(
            "🔍 Please review my current backlog and provide an engaging summary with emojis! "
            "Include: 📊 task counts by status, ⏰ any overdue items, and 🧹 suggestions for cleanup or organization. "
            "Make it visually appealing and easy to scan!"
        )
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and return Agent Smith's response."""
        return self.agent.run(user_input)
    
    @abstractmethod
    def start(self):
        """Start the interface. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def send_message(self, message: str):
        """Send a message through the interface. Must be implemented by subclasses."""
        pass 