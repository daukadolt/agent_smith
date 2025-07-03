#!/usr/bin/env python3
"""
Agent Smith - Proactive AI Task Management Assistant

Main entry point for the Agent Smith application.
Supports multiple interfaces: CLI and Telegram Bot.
"""

import argparse
import sys
import os
from dotenv import load_dotenv

load_dotenv()


def show_interface_menu() -> str:
    """Show interactive interface selection menu."""
    print("🕴️ Agent Smith - Interface Selection")
    print("=" * 40)
    print("1. 💻 CLI (Command Line Interface)")
    print("2. 🤖 Telegram Bot")
    print("3. ❌ Exit")
    print()
    
    while True:
        try:
            choice = input("Select interface (1-3): ").strip()
            if choice == "1":
                return "cli"
            elif choice == "2":
                return "telegram"
            elif choice == "3":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)


def start_cli_interface():
    """Start the CLI interface."""
    try:
        from interfaces.cli import CLIInterface
        cli = CLIInterface()
        cli.start()
    except Exception as e:
        print(f"❌ Failed to start CLI interface: {e}")
        sys.exit(1)


def start_telegram_interface():
    """Start the Telegram bot interface."""
    # Check if Telegram bot token is available
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set")
        print("💡 To use Telegram interface:")
        print("   1. Create a bot with @BotFather on Telegram")
        print("   2. Set TELEGRAM_BOT_TOKEN=your_bot_token")
        print("   3. Install telegram dependencies: pip install python-telegram-bot")
        sys.exit(1)
    
    try:
        from interfaces.telegram_bot import TelegramInterface
        bot = TelegramInterface()
        bot.start()
    except Exception as e:
        print(f"❌ Failed to start Telegram bot: {e}")
        sys.exit(1)


def main():
    """Main entry point for Agent Smith."""
    parser = argparse.ArgumentParser(
        description="🕴️ Agent Smith - Proactive AI Task Management Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Interactive interface selection
  python main.py --cli         # Start CLI directly
  python main.py --telegram    # Start Telegram bot directly
  python main.py --help        # Show this help

Environment Variables:
  TELEGRAM_BOT_TOKEN           # Required for Telegram bot interface
  OPENAI_API_KEY              # Required for AI functionality
  AIRTABLE_API_KEY            # Required for Airtable integration
  AIRTABLE_BASE_ID            # Required for Airtable integration
  AIRTABLE_BACKLOG_TABLE_ID   # Required for Airtable integration
        """
    )
    
    # Interface selection arguments
    interface_group = parser.add_mutually_exclusive_group()
    interface_group.add_argument(
        "--cli", 
        action="store_true", 
        help="Start CLI (Command Line Interface) directly"
    )
    interface_group.add_argument(
        "--telegram", 
        action="store_true", 
        help="Start Telegram bot interface directly"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Determine which interface to start
    if args.cli:
        interface = "cli"
    elif args.telegram:
        interface = "telegram"
    else:
        # No arguments provided, show interactive menu
        interface = show_interface_menu()
    
    # Start the selected interface
    print(f"\n🚀 Starting {interface.upper()} interface...\n")
    
    if interface == "cli":
        start_cli_interface()
    elif interface == "telegram":
        start_telegram_interface()
    else:
        print(f"❌ Unknown interface: {interface}")
        sys.exit(1)


if __name__ == "__main__":
    main() 