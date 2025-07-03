import json
import logging
from typing import Optional, Dict, List

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam, 
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam, 
    ChatCompletionMessage, 
    ChatCompletionAssistantMessageParam, 
    ChatCompletion,
    ChatCompletionMessageToolCall, 
    ChatCompletionToolMessageParam
)

from src.agents.custom.tools.tool import Tool
from src.agents.custom.tools.airtable_create_record_tool import AirtableCreateRecordTool
from src.agents.custom.tools.airtable_get_all_records_tool import AirtableGetAllRecordsTool
from src.agents.custom.tools.airtable_delete_record_tool import AirtableDeleteRecordTool
from src.agents.custom.tools.airtable_update_record_tool import AirtableUpdateRecordTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Custom exception for Agent-related errors."""
    pass


class Agent:
    """
    An AI agent that can execute tool calls using OpenAI's chat completion API.
    
    This agent maintains a conversation loop, executing tools as requested by the AI model
    until either a final response is generated or the maximum number of steps is reached.
    """
    
    def __init__(
        self,
        model: str,
        tools: Optional[List[Tool]] = None,
        system_message: str = "Use tool calls to solve the user's request.",
        max_steps: int = 10,
        api_key: Optional[str] = None,
    ) -> None:
        """
        Initialize the Agent.
        
        Args:
            model: The OpenAI model to use (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            tools: List of available tools for the agent to use
            system_message: System prompt to guide the agent's behavior
            max_steps: Maximum number of conversation steps before stopping
            api_key: OpenAI API key (if not provided, uses environment variable)
        """
        self.model = model
        self.system_message = system_message
        self.tools: Dict[str, Tool] = {tool.name: tool for tool in tools} if tools else {}
        self.max_steps = max_steps
        
        try:
            self.client = OpenAI(api_key=api_key)
        except Exception as e:
            raise AgentError(f"Failed to initialize OpenAI client: {e}")
        
        logger.info(f"Agent initialized with model '{model}' and {len(self.tools)} tools")

    def run(self, initial_prompt: str) -> Optional[str]:
        """
        Run the agent with an initial prompt.

        This method starts a conversation loop, calling the OpenAI API and executing
        tool calls as needed until a final response is generated or max_steps is reached.

        Args:
            initial_prompt: The initial user prompt to start the conversation.

        Returns:
            The final response from the agent, or None if max_steps is reached.
            
        Raises:
            AgentError: If there's an error during execution that cannot be recovered from.
        """
        if not initial_prompt.strip():
            raise ValueError("Initial prompt cannot be empty")
            
        logger.info(f"Starting agent run with prompt: {initial_prompt[:100]}...")
        
        messages = self._initialize_messages(initial_prompt)
        
        for step in range(self.max_steps):
            logger.debug(f"Agent step {step + 1}/{self.max_steps}")
            
            try:
                response = self._call_openai(messages)
                assistant_message = response.choices[0].message
                messages.append(self._convert_message_to_param(assistant_message))

                if tool_calls := assistant_message.tool_calls:
                    logger.info(f"Executing {len(tool_calls)} tool call(s)")
                    for tool_call in tool_calls:
                        tool_response = self._execute_tool_call(tool_call)
                        messages.append(tool_response)
                else:
                    logger.info("Agent completed successfully")
                    return assistant_message.content
                    
            except Exception as e:
                logger.error(f"Error in agent step {step + 1}: {e}")
                raise AgentError(f"Agent execution failed at step {step + 1}: {e}")
        
        logger.warning(f"Agent reached maximum steps ({self.max_steps}) without completion")
        return None

    def _initialize_messages(self, initial_prompt: str) -> List[ChatCompletionMessageParam]:
        """Initialize the conversation with system and user messages."""
        system_message = ChatCompletionSystemMessageParam(
            role="system", 
            content=self.system_message
        )
        user_message = ChatCompletionUserMessageParam(
            role="user", 
            content=initial_prompt
        )
        return [system_message, user_message]

    def _convert_message_to_param(
        self, 
        message: ChatCompletionMessage
    ) -> ChatCompletionAssistantMessageParam:
        """
        Convert OpenAI's ChatCompletionMessage to ChatCompletionAssistantMessageParam.
        
        Args:
            message: The message to convert
            
        Returns:
            Converted message parameter
        """
        return ChatCompletionAssistantMessageParam(
            role="assistant",
            content=message.content,
            tool_calls=[
                {
                    "id": tool_call.id,
                    "function": {
                        "arguments": tool_call.function.arguments,
                        "name": tool_call.function.name,
                    },
                    "type": "function",
                }
                for tool_call in message.tool_calls
            ] if message.tool_calls else None
        )

    def _call_openai(self, messages: List[ChatCompletionMessageParam]) -> ChatCompletion:
        """
        Call the OpenAI API with the given messages.
        
        Args:
            messages: List of messages to send to the API
            
        Returns:
            The API response
            
        Raises:
            AgentError: If the API call fails
        """
        try:
            tools = [tool.function_definition for tool in self.tools.values()] if self.tools else None
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
            )
            
            logger.debug(f"OpenAI API call successful, tokens used: {response.usage.total_tokens if response.usage else 'unknown'}")
            return response
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise AgentError(f"Failed to get response from OpenAI: {e}")

    def _execute_tool_call(
        self, 
        tool_call: ChatCompletionMessageToolCall
    ) -> ChatCompletionToolMessageParam:
        """
        Execute a tool call based on the OpenAI API's request.
        
        Args:
            tool_call: The tool call request from OpenAI
            
        Returns:
            The tool response message
        """
        tool_name = tool_call.function.name
        logger.info(f"Executing tool: {tool_name}")

        try:
            if tool_name not in self.tools:
                error_msg = f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
                logger.error(error_msg)
                return self._create_tool_response(tool_call.id, error_msg)

            args = json.loads(tool_call.function.arguments)
            logger.debug(f"Tool arguments: {args}")

            tool_response = self.tools[tool_name](**args)
            logger.info(f"Tool '{tool_name}' executed successfully")
            
            return self._create_tool_response(tool_call.id, str(tool_response))
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in tool arguments: {e}"
            logger.error(error_msg)
            return self._create_tool_response(tool_call.id, error_msg)
            
        except Exception as e:
            error_msg = f"Tool execution failed: {e}"
            logger.error(error_msg)
            return self._create_tool_response(tool_call.id, error_msg)

    def _create_tool_response(
        self, 
        tool_call_id: str, 
        content: str
    ) -> ChatCompletionToolMessageParam:
        """Create a standardized tool response message."""
        return ChatCompletionToolMessageParam(
            role="tool",
            tool_call_id=tool_call_id,
            content=content,
        )

if __name__ == "__main__":
    # Set logger to WARNING level for cleaner interactive interface
    logger.setLevel(logging.WARNING)
    
    print("Agent Smith, to your service")
    agent = Agent(
        model="gpt-4o",
        system_message="""You are Agent Smith, a proactive task management assistant. Your primary responsibilities are:

1. **Task Management**: Help users create, view, and manage tasks in their Airtable backlog
2. **Proactive Cleanup**: Whenever possible, review the backlog and suggest or perform cleanup actions:
   - Remove completed tasks that are no longer needed
   - Identify and consolidate duplicate or similar tasks
   - Flag overdue tasks and suggest updates
   - Organize tasks by priority or due date
   - Remove tasks with incomplete or unclear information

3. **Available Tools**: Use these tools efficiently:
   - `airtable_get_all_records`: Review the current backlog
   - `create_airtable_record`: Add new tasks with proper fields (Name, Notes, Status, Due date/time)
   - `update_airtable_record`: Modify existing tasks (change status, update notes, set due dates, etc.)
   - `delete_airtable_record`: Remove completed or unnecessary tasks

4. **Best Practices**:
   - Always check the backlog before creating new tasks to avoid duplicates
   - Suggest improvements to task descriptions and organization
   - Be proactive in maintaining a clean, organized backlog
   - Ask clarifying questions when task requirements are unclear

Be helpful, efficient, and maintain a clean, organized task management system.""",
        tools=[AirtableCreateRecordTool(), AirtableGetAllRecordsTool(), AirtableUpdateRecordTool(), AirtableDeleteRecordTool()],
    )
    
    # Automatically review backlog and provide summary
    print("\n🔍 Reviewing your backlog...")
    backlog_summary = agent.run("Please review my current backlog and provide a summary. Include task counts by status, any overdue items, and suggestions for cleanup or organization.")
    if backlog_summary:
        print(f"\n📋 Backlog Summary:\n{backlog_summary}")
    
    print("\n" + "="*50)
    print("Ready for your commands! (Type 'quit' or 'exit' to end)")
    
    user_in = input("> ")
    user_in = user_in.strip()
    while user_in not in ("quit", "exit"):
        result = agent.run(user_in)
        if result:
            print(result)
        user_in = input("> ")
        user_in = user_in.strip()