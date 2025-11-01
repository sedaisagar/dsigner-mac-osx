"""
UI Dashboard Launcher - Opens Tkinter dashboard when specific events are received.
"""
import tkinter as tk
from tkinter import messagebox
import logging
import threading
from typing import Dict, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventNotificationWindow:
    """A simple notification window that appears when events are received."""
    
    _open_windows = 0
    _max_windows = 3  # Limit concurrent windows
    
    @staticmethod
    def create_notification(event_type: str, event_data: Dict[str, Any]):
        """Create a notification window for an event."""
        if EventNotificationWindow._open_windows >= EventNotificationWindow._max_windows:
            logger.warning("Too many notification windows open")
            return
        
        EventNotificationWindow._open_windows += 1
        logger.info(f"Creating notification window for event: {event_type}")
        
        # Create window in a new thread to avoid blocking
        def show_window():
            try:
                root = tk.Tk()
                root.withdraw()  # Hide main window
                
                # Create modal notification
                EventNotificationWindow._create_modal_notification(
                    root, event_type, event_data
                )
            except Exception as e:
                logger.error(f"Error showing notification window: {e}", exc_info=True)
            finally:
                EventNotificationWindow._open_windows -= 1
        
        thread = threading.Thread(target=show_window, daemon=False)
        thread.start()
        logger.info("Notification thread started")
    
    @staticmethod
    def _create_modal_notification(parent, event_type: str, event_data: Dict[str, Any]):
        """Create and show a modal notification dialog."""
        # Create a toplevel window
        top = tk.Toplevel(parent)
        top.title("Event Notification")
        top.geometry("500x400")
        top.resizable(False, False)
        
        # Configure styling
        top.configure(bg="#f6f8fa")
        
        # Center the window
        top.update_idletasks()
        x = (top.winfo_screenwidth() // 2) - (500 // 2)
        y = (top.winfo_screenheight() // 2) - (400 // 2)
        top.geometry(f"500x400+{x}+{y}")
        
        # Make it modal
        top.transient(parent)
        top.grab_set()
        
        # Header
        header_frame = tk.Frame(top, bg="#2a5b74", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📢 Event Received",
            font=("Segoe UI", 16, "bold"),
            bg="#2a5b74",
            fg="white"
        ).pack(pady=15)
        
        # Content frame
        content_frame = tk.Frame(top, bg="#f6f8fa", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Event type
        tk.Label(
            content_frame,
            text="Event Type:",
            font=("Segoe UI", 10, "bold"),
            bg="#f6f8fa"
        ).pack(anchor="w")
        
        tk.Label(
            content_frame,
            text=event_type,
            font=("Segoe UI", 10),
            bg="#f6f8fa",
            fg="#2a5b74"
        ).pack(anchor="w", pady=(5, 15))
        
        # Timestamp
        timestamp = event_data.get('timestamp', datetime.now().isoformat())
        tk.Label(
            content_frame,
            text="Received:",
            font=("Segoe UI", 9),
            bg="#f6f8fa",
            fg="#666"
        ).pack(anchor="w")
        
        tk.Label(
            content_frame,
            text=timestamp,
            font=("Segoe UI", 9),
            bg="#f6f8fa",
            fg="#666"
        ).pack(anchor="w", pady=(5, 15))
        
        # Event data (scrollable)
        tk.Label(
            content_frame,
            text="Event Data:",
            font=("Segoe UI", 10, "bold"),
            bg="#f6f8fa"
        ).pack(anchor="w")
        
        # Scrollable text area
        scroll_frame = tk.Frame(content_frame, bg="#f6f8fa")
        scroll_frame.pack(fill="both", expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_area = tk.Text(
            scroll_frame,
            wrap="word",
            font=("Consolas", 9),
            bg="white",
            fg="#222",
            yscrollcommand=scrollbar.set,
            padx=10,
            pady=10,
            height=10
        )
        text_area.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_area.yview)
        
        # Insert formatted event data
        import json
        formatted_data = json.dumps(event_data, indent=2)
        text_area.insert("1.0", formatted_data)
        text_area.config(state="disabled")  # Make read-only
        
        # Button frame
        button_frame = tk.Frame(top, bg="#f6f8fa", pady=10)
        button_frame.pack(fill="x")
        
        def close_window():
            top.destroy()
            parent.quit()
            parent.destroy()
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=close_window,
            font=("Segoe UI", 10, "bold"),
            bg="#43a047",
            fg="white",
            activebackground="#378a3b",
            padx=30,
            pady=8,
            cursor="hand2",
            relief="flat"
        )
        close_btn.pack()
        
        # Handle window close
        top.protocol("WM_DELETE_WINDOW", close_window)
        
        # Focus the window
        top.focus_force()
        
        # Run the notification
        parent.mainloop()


class DashboardLauncher:
    """Launches the full dashboard when events require it."""
    
    @staticmethod
    def launch_full_dashboard(event_type: str, event_data: Dict[str, Any]):
        """Launch the full dashboard application."""
        def launch():
            try:
                from ui.dashboard import DashboardApp
                import tkinter as tk
                
                root = tk.Tk()
                app = DashboardApp(root)
                
                # Show a message about why this dashboard opened
                messagebox.showinfo(
                    "Dashboard Opened by Event",
                    f"Dashboard opened due to event: {event_type}\n\n"
                    f"Check the event data in the console for details."
                )
                
                logger.info(f"Launched full dashboard for event: {event_type}")
                
                root.mainloop()
            except Exception as e:
                logger.error(f"Error launching dashboard: {e}")
        
        # Launch in a separate thread to avoid blocking
        thread = threading.Thread(target=launch, daemon=True)
        thread.start()


def create_event_handler(launch_type='notification'):
    """
    Create an event handler that shows UI based on event type.
    
    Args:
        launch_type: 'notification' (default) or 'full_dashboard'
    """
    if launch_type == 'full_dashboard':
        def handler(topic: str, event_data: Dict[str, Any]):
            event_type = event_data.get('event_type', 'unknown')
            logger.info(f"Launching dashboard for event: {event_type}")
            DashboardLauncher.launch_full_dashboard(event_type, event_data)
        
        return handler
    else:
        def handler(topic: str, event_data: Dict[str, Any]):
            event_type = event_data.get('event_type', 'unknown')
            logger.info(f"Showing notification for event: {event_type}")
            EventNotificationWindow.create_notification(event_type, event_data)
        
        return handler


# Convenience functions for different event types
def handle_key_submission_with_ui(topic: str, event_data: Dict[str, Any]):
    """Handle key submission events with UI notification."""
    logger.info(f"Key submission received: {event_data.get('key_value', 'N/A')}")
    EventNotificationWindow.create_notification("Key Submission", event_data)


def handle_profile_event_with_ui(topic: str, event_data: Dict[str, Any]):
    """Handle profile events with UI notification."""
    event_type = event_data.get('event_type', 'Profile Event')
    logger.info(f"Profile event received: {event_type}")
    
    # Show notification
    EventNotificationWindow.create_notification(f"Profile Event: {event_type}", event_data)
    
    # For important profile changes, you might want to launch full dashboard
    important_events = ['profile_deleted', 'profile_created']
    if event_type in important_events:
        DashboardLauncher.launch_full_dashboard(event_type, event_data)


def handle_processing_result_with_ui(topic: str, event_data: Dict[str, Any]):
    """Handle processing results with UI notification."""
    logger.info(f"Processing result: {event_data.get('event_type', 'unknown')}")
    EventNotificationWindow.create_notification("Processing Result", event_data)

