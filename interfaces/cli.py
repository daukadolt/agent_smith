#!/usr/bin/env python3
"""
CLI Interface for Agent Smith.
"""

from .base import BaseInterface


class CLIInterface(BaseInterface):
    """Command-line interface for Agent Smith."""
    
    def start(self):
        """Start the CLI interface."""
        print("Agent Smith, to your service")
        
        # Automatically review backlog and provide summary
        print("\n🔍 Reviewing your backlog...")
        backlog_summary = self.get_backlog_summary()
        if backlog_summary:
            self.send_message(f"📋 Backlog Summary:\n{backlog_summary}")
        
        print("\n" + "="*50)
        print("Ready for your commands! (Type 'quit' or 'exit' to end)")
        
        # Interactive loop
        user_in = input("> ")
        user_in = user_in.strip()
        while user_in not in ("quit", "exit"):
            result = self.process_user_input(user_in)
            if result:
                self.send_message(result)
            user_in = input("> ")
            user_in = user_in.strip()
    
    def send_message(self, message: str):
        """Send a message to the CLI (print to console)."""
        print(message)


def main():
    """Main entry point for CLI interface."""
    cli = CLIInterface()
    cli.start()


if __name__ == "__main__":
    main() 