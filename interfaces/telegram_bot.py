#!/usr/bin/env python3
"""
Telegram Bot Interface for Agent Smith.

To use this interface:
1. Install: pip install python-telegram-bot
2. Set TELEGRAM_BOT_TOKEN environment variable
3. Run: python interfaces/telegram_bot.py
"""

import os
from typing import Optional
from .base import BaseInterface

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

class TelegramInterface(BaseInterface):
    """Telegram bot interface for Agent Smith."""
    
    def __init__(self, bot_token: Optional[str] = None, **kwargs):
        """Initialize Telegram interface."""
        super().__init__(**kwargs)
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable or bot_token parameter required")
        
        self.application = Application.builder().token(self.bot_token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up Telegram bot command and message handlers."""
        # Commands
        self.application.add_handler(CommandHandler("start", self._start_command))
        self.application.add_handler(CommandHandler("help", self._help_command))
        self.application.add_handler(CommandHandler("summary", self._summary_command))
        
        # Regular messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
    
    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """🕴️ **Agent Smith, to your service**

I'm your proactive AI task management assistant! I can help you:

📝 **Manage Tasks**: Create, update, view, and organize your Airtable backlog
🧹 **Clean & Organize**: Automatically review and suggest improvements
⚡ **Be Proactive**: Flag overdue items, find duplicates, and maintain order

**Commands:**
/summary - Get current backlog overview
/help - Show available commands

Just send me a message to get started! 🚀"""
        
        await self.send_message_async(update, welcome_message)
        
        # Auto-send backlog summary
        try:
            summary = self.get_backlog_summary()
            if summary:
                await self.send_message_async(update, f"📋 **Current Backlog:**\n{summary}")
        except Exception as e:
            await self.send_message_async(update, f"⚠️ Couldn't get backlog summary: {str(e)}")
    
    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = """🛠️ **Agent Smith Commands & Usage**

**Commands:**
/start - Welcome message and backlog summary
/summary - Get current backlog overview  
/help - Show this help message

**Natural Language Examples:**
• "Create a new task to update documentation"
• "Show me all pending tasks"
• "Update task XYZ status to done"
• "Delete completed tasks from last week"
• "Clean up my backlog"
• "What's overdue?"

**Tips:**
✨ I understand natural language - just tell me what you need!
📊 I'll automatically suggest cleanup and organization improvements
🔄 I can handle complex task management operations

Send me any message to get started! 🚀"""
        
        await self.send_message_async(update, help_message)
    
    async def _summary_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /summary command."""
        try:
            await update.message.reply_text("🔍 Reviewing your backlog...")
            summary = self.get_backlog_summary()
            if summary:
                await self.send_message_async(update, f"📋 **Backlog Summary:**\n{summary}")
            else:
                await self.send_message_async(update, "⚠️ Couldn't generate backlog summary")
        except Exception as e:
            await self.send_message_async(update, f"❌ Error getting summary: {str(e)}")
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        user_message = update.message.text
        
        try:
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Process with Agent Smith
            response = self.process_user_input(user_message)
            
            if response:
                await self.send_message_async(update, response)
            else:
                await self.send_message_async(update, "🤔 I couldn't process that request. Try rephrasing or use /help for guidance.")
                
        except Exception as e:
            await self.send_message_async(update, f"❌ Sorry, I encountered an error: {str(e)}")
    
    async def send_message_async(self, update: Update, message: str):
        """Send message via Telegram with proper formatting."""
        # Split long messages if needed (Telegram has a 4096 character limit)
        if len(message) > 4000:
            parts = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for part in parts:
                await update.message.reply_text(part, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')
    
    def send_message(self, message: str):
        """Synchronous send_message (not used in Telegram interface)."""
        # This is required by the base class but not used in async Telegram context
        pass
    
    def start(self):
        """Start the Telegram bot."""
        print("🤖 Starting Agent Smith Telegram Bot...")
        print(f"🔑 Token: {self.bot_token[:10]}...")
        print("🚀 Bot is running! Send /start to begin.")
        
        # Run the bot
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point for Telegram bot."""
    try:
        bot = TelegramInterface()
        bot.start()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Set your TELEGRAM_BOT_TOKEN environment variable")
    except Exception as e:
        print(f"❌ Bot startup failed: {e}")


if __name__ == "__main__":
    main() 