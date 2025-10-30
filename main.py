from ui.dashboard import DashboardApp
import tkinter as tk
if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)  # Trigger close function on window close
    root.mainloop()