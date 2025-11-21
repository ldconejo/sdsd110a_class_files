from abc import ABC, abstractmethod
from typing import List
import copy

class Command(ABC):
    @abstractmethod
    def execute(self):
        """Execute the command"""
        pass
    
    @abstractmethod
    def undo(self):
        """Undo the command"""
        pass
    
    @abstractmethod
    def description(self) -> str:
        """Get command description"""
        pass

class Document:
    def __init__(self):
        self.content = ""
        self.cursor_position = 0
    
    def insert_text(self, text, position=None):
        """Insert text at specified position"""
        if position is None:
            position = self.cursor_position
        
        self.content = (self.content[:position] + 
                       text + 
                       self.content[position:])
        self.cursor_position = position + len(text)
    
    def delete_text(self, start, length):
        """Delete text from start position"""
        deleted_text = self.content[start:start + length]
        self.content = self.content[:start] + self.content[start + length:]
        self.cursor_position = start
        return deleted_text
    
    def get_content(self):
        return self.content

# Concrete Commands
class InsertTextCommand(Command):
    def __init__(self, document: Document, text: str, position: int = None):
        self.document = document
        self.text = text
        self.position = position if position is not None else document.cursor_position
        self.original_cursor = document.cursor_position
    
    def execute(self):
        """Execute the insert command"""
        self.document.insert_text(self.text, self.position)
    
    def undo(self):
        """Undo the insert command"""
        self.document.delete_text(self.position, len(self.text))
        self.document.cursor_position = self.original_cursor
    
    def description(self) -> str:
        return f"Insert '{self.text}' at position {self.position}"

class DeleteTextCommand(Command):
    def __init__(self, document: Document, start: int, length: int):
        self.document = document
        self.start = start
        self.length = length
        self.deleted_text = ""
        self.original_cursor = document.cursor_position
    
    def execute(self):
        """Execute the delete command"""
        self.deleted_text = self.document.delete_text(self.start, self.length)
    
    def undo(self):
        """Undo the delete command"""
        self.document.insert_text(self.deleted_text, self.start)
        self.document.cursor_position = self.original_cursor
    
    def description(self) -> str:
        return f"Delete {self.length} characters from position {self.start}"

# Command Manager with Undo/Redo
class CommandManager:
    def __init__(self):
        self.history: List[Command] = []
        self.current_index = -1
        self.max_history = 100
    
    def execute_command(self, command: Command):
        """Execute a command and add to history"""
        # Remove any commands after current index (for redo branch pruning)
        self.history = self.history[:self.current_index + 1]
        
        # Execute the command
        command.execute()
        
        # Add to history
        self.history.append(command)
        self.current_index += 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_index -= 1
        
        print(f"✅ Executed: {command.description()}")
    
    def undo(self):
        """Undo the last command"""
        if self.can_undo():
            command = self.history[self.current_index]
            command.undo()
            self.current_index -= 1
            print(f"↩️  Undid: {command.description()}")
            return True
        else:
            print("❌ Nothing to undo")
            return False
    
    def redo(self):
        """Redo the next command"""
        if self.can_redo():
            self.current_index += 1
            command = self.history[self.current_index]
            command.execute()
            print(f"↪️  Redid: {command.description()}")
            return True
        else:
            print("❌ Nothing to redo")
            return False
    
    def can_undo(self):
        """Check if undo is possible"""
        return self.current_index >= 0
    
    def can_redo(self):
        """Check if redo is possible"""
        return self.current_index < len(self.history) - 1
    
    def get_history(self):
        """Get command history"""
        return [cmd.description() for cmd in self.history]

# Text Editor Example
class TextEditor:
    def __init__(self):
        self.document = Document()
        self.command_manager = CommandManager()
    
    def insert_text(self, text, position=None):
        """Insert text using command pattern"""
        command = InsertTextCommand(self.document, text, position)
        self.command_manager.execute_command(command)
    
    def delete_text(self, start, length):
        """Delete text using command pattern"""
        command = DeleteTextCommand(self.document, start, length)
        self.command_manager.execute_command(command)
    
    def undo(self):
        """Undo last operation"""
        return self.command_manager.undo()
    
    def redo(self):
        """Redo last undone operation"""
        return self.command_manager.redo()
    
    def get_content(self):
        """Get current document content"""
        return self.document.get_content()
    
    def show_history(self):
        """Show command history"""
        history = self.command_manager.get_history()
        current = self.command_manager.current_index
        
        print("\n📜 Command History:")
        for i, cmd in enumerate(history):
            marker = "▶️ " if i == current else "   "
            print(f"{marker}{i}: {cmd}")

# Demonstration
def demonstrate_command_pattern():
    editor = TextEditor()
    
    print("📝 Text Editor with Command Pattern\n")
    
    # Perform some operations
    editor.insert_text("Hello")
    print(f"Content: '{editor.get_content()}'")
    
    editor.insert_text(" World")
    print(f"Content: '{editor.get_content()}'")
    
    editor.insert_text("!", 11)
    print(f"Content: '{editor.get_content()}'")
    
    editor.delete_text(5, 6)  # Delete " World"
    print(f"Content: '{editor.get_content()}'")
    
    # Show history
    editor.show_history()
    
    # Undo operations
    print(f"\n🔄 Undoing operations:")
    while editor.undo():
        print(f"Content: '{editor.get_content()}'")

if __name__ == "__main__":
    demonstrate_command_pattern()