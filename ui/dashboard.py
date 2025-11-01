import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from services.db import initialize_db, fetch_profiles, fetch_profile_by_id, insert_profile, update_profile, delete_profile
import tkinter.filedialog as fd
import os

# Basic color palette to resemble the provided design (softer tones)
ACCENT = "#2a5b74"
LIGHT_BG = "#f6f8fa"
SUCCESS = "#43a047"        # softer green
SUCCESS_HOVER = "#378a3b"
ERROR = "#e25555"          # softer red
ERROR_HOVER = "#cc4a4a"
BORDER = "#dfe5ea"         # soft border color

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1200x720")

        # Initialize the database
        initialize_db()

        # Typography defaults
        self.font_heading = ("Segoe UI", 18, "bold")
        self.font_body = ("Segoe UI", 10)
        self.font_button = ("Segoe UI", 10, "bold")
        # Apply defaults to classic Tk widgets
        self.root.option_add("*Font", self.font_body)
        self.root.option_add("*Button.Font", self.font_button)
        self.root.option_add("*Label.Font", self.font_body)
        self.root.option_add("*Entry.Font", self.font_body)

        # Remove top bar; only set window icon if available
        try:
            self.logo_img = tk.PhotoImage(file="logo.png")
            self.root.iconphoto(True, self.logo_img)
        except Exception:
            self.logo_img = None

        # Footer band (pack bottom BEFORE side frames so it spans full width)
        self.footer = tk.Frame(self.root, bg="#8c9bab", height=56)
        self.footer.pack(side="bottom", fill="x")
        tk.Label(self.footer, text="POWERED BY RADIANT INFOTECH", bg="#8c9bab", fg="white").pack(side="left", padx=18)
        if self.logo_img is not None:
            self.logo_footer = self.logo_img.subsample(2, 2)
            tk.Label(self.footer, image=self.logo_footer, bg="#8c9bab").pack(side="left", padx=18)
        else:
            tk.Label(self.footer, text="RADIANT InfoTech Nepal", bg="#8c9bab", fg="white").pack(side="left", padx=18)
        tk.Label(self.footer, text="CC RADIANT INFOTECH", bg="#8c9bab", fg="white").pack(side="right", padx=18)

        # Body frame between topbar and footer, holds sidebar and main area
        self.body = tk.Frame(self.root, bg=LIGHT_BG)
        self.body.pack(side="top", fill="both", expand=True)

        # Sidebar frame (1.5x wider)
        self.sidebar = tk.Frame(self.body, bg="#8c9bab", width=330)
        self.sidebar.pack(side="left", fill="y")

        # Ensure the main content adjusts to the remaining space
        self.main_content = tk.Frame(self.body, bg=LIGHT_BG)
        self.main_content.pack(side="right", fill="both", expand=True)

        
      
        # Home button in the sidebar with full clickable area
        # Update hover_bg to use the specified color
        self.home_btn_canvas = self._create_rounded_button(
            self.sidebar,
            text="Home",
            command=self.show_home,
            bg="SystemButtonFace",  # Default inactive background
            hover_bg="#22495e",  # Updated hover color
            fg="black",  # Default inactive text color
            padding_x=20,
            padding_y=10,
            radius=15,  # Border radius
            pack_kwargs={"pady": 10, "padx": 10, "fill": "x"}
        )

        # Profile button in the sidebar with full clickable area
        self.profiles_btn_canvas = self._create_rounded_button(
            self.sidebar,
            text="Profile",
            command=self.show_profiles,
            bg="SystemButtonFace",  # Default inactive background
            hover_bg="#22495e",  # Updated hover color
            fg="black",  # Default inactive text color
            padding_x=20,
            padding_y=10,
            radius=15,  # Border radius
            pack_kwargs={"pady": 10, "padx": 10, "fill": "x"}
        )


        # Footer already created above

        # Ensure the app closes properly
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        # Show default screen (Home dashboard)
        self.show_home()

    def _create_rounded_button(self, parent, text, command, bg, hover_bg, fg="white", padding_x=16, padding_y=8, radius=10, pack_kwargs=None):
        # Canvas-based rounded button
        pack_kwargs = pack_kwargs or {}
        parent_bg = parent.cget("bg")
        font_obj = tkfont.Font(font=self.font_button)
        text_width = font_obj.measure(text)
        text_height = font_obj.metrics("linespace")
        width = text_width + padding_x * 2
        height = text_height + padding_y * 2

        canvas = tk.Canvas(parent, width=width, height=height, bg=parent_bg, highlightthickness=0, bd=0, cursor="hand2")
        canvas.is_active = False

        # draw the button; text_color defaults to fg
        def draw_button(fill_color, text_color=None):
            canvas.delete("btn")
            r = radius
            w = width
            h = height
            # Draw background halo (to hide jagged edges) slightly larger using parent bg
            pb = parent_bg
            canvas.create_arc(-1, -1, 2*r+1, 2*r+1, start=90, extent=90, style="pieslice", fill=pb, outline=pb, tags="btn")
            canvas.create_arc(w-2*r-1, -1, w+1, 2*r+1, start=0, extent=90, style="pieslice", fill=pb, outline=pb, tags="btn")
            canvas.create_arc(-1, h-2*r-1, 2*r+1, h+1, start=180, extent=90, style="pieslice", fill=pb, outline=pb, tags="btn")
            canvas.create_arc(w-2*r-1, h-2*r-1, w+1, h+1, start=270, extent=90, style="pieslice", fill=pb, outline=pb, tags="btn")
            canvas.create_rectangle(r, -1, w-r, h+1, fill=pb, outline=pb, tags="btn")
            canvas.create_rectangle(-1, r, w+1, h-r, fill=pb, outline=pb, tags="btn")

            # Foreground rounded button
            canvas.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, style="pieslice", fill=fill_color, outline=fill_color, tags="btn")
            canvas.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90, style="pieslice", fill=fill_color, outline=fill_color, tags="btn")
            canvas.create_arc(0, h-2*r, 2*r, h, start=180, extent=90, style="pieslice", fill=fill_color, outline=fill_color, tags="btn")
            canvas.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90, style="pieslice", fill=fill_color, outline=fill_color, tags="btn")
            canvas.create_rectangle(r, 0, w-r, h, fill=fill_color, outline=fill_color, tags="btn")
            canvas.create_rectangle(0, r, w, h-r, fill=fill_color, outline=fill_color, tags="btn")
            # Use a separate tag for the label so we can recolor text without affecting shapes
            canvas.create_text(w/2, h/2, text=text, fill=(text_color or fg), font=self.font_button, tags=("btn", "label"))

        draw_button(bg)

        def on_enter(_):
            # If active, keep active style; otherwise show hover
            if canvas.is_active:
                draw_button(hover_bg, text_color="white")
            else:
                draw_button(hover_bg, text_color="white")

        def on_leave(_):
            # Restore based on active state
            if canvas.is_active:
                draw_button(hover_bg, text_color="white")
            else:
                draw_button(bg, text_color=fg)

        def on_click(_):
            if callable(command):
                command()

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)
        canvas.pack(**pack_kwargs)
        canvas.draw_button = draw_button
        # Active state uses hover_bg and white text; inactive uses bg and provided fg
        def _set_active(active):
            canvas.is_active = bool(active)
            draw_button(hover_bg if canvas.is_active else bg, text_color=("white" if canvas.is_active else fg))
        canvas.set_active = _set_active
        return canvas

    def show_home(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Set active style for Home button
        self.home_btn_canvas.set_active(True)
        # Set inactive style for Profile button
        self.profiles_btn_canvas.set_active(False)

        # --- Card 1: Active token display
        token_panel = tk.Frame(self.main_content, bg="white")
        token_panel.pack(fill="x", padx=16, pady=(16, 8))
        tk.Label(token_panel, text="Welcome to Home", bg="white", fg="#22495e", font=self.font_heading).pack(anchor="w", pady=(0, 8))
        from services.db import fetch_active_profile
        active_profile = fetch_active_profile()
        token_name = active_profile[3] if active_profile else "(None active)"
      

        # --- Card 2: Key input form styled like render_profile_form
        def handle_key_submit(values):
            key_val = values.get("key", "").strip()
            if not key_val:
                messagebox.showerror("Empty Key", "Key cannot be empty.")
                return
            messagebox.showinfo("Key Submitted", f"Submitted key: {key_val}")
            
        # Instead of DLL/Token fields, just key field
        self.render_profile_form(
            title="Enter Key",
            defaults={"key": "", "token_name": token_name},
            on_submit=handle_key_submit,
            include_active=False,
            custom_fields="key_form"
        )

    def show_profiles(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Set active style for Profile button
        self.profiles_btn_canvas.set_active(True)

        # Set inactive style for Home button
        self.home_btn_canvas.set_active(False)

        # Add content for Profile view
        panel = tk.Frame(self.main_content, bg="white")
        panel.pack(fill="x", padx=16, pady=16)
        tk.Label(panel, text="Profile Section", bg="white", fg="#22495e", font=self.font_heading).pack(anchor="w", pady=(0, 8))

        # Header with title and "+ Profile" button
        header = tk.Frame(self.main_content, bg="white", width=600)  # Set the width explicitly
        header.pack(fill="x", padx=16, pady=16)
        tk.Label(header, text="Profiles", bg="white", fg=ACCENT, font=self.font_heading).pack(side="left")
        self._create_rounded_button(
            header,
            text="+ Profile",
            command=self.add_new_profile,
            bg=ACCENT,
            hover_bg="#22495e",
            pack_kwargs={"side": "right", "padx": (0, 12)}
        )

        # Create a treeview for the table
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="#222", rowheight=28, fieldbackground="white")
        style.configure("Treeview.Heading", background="#eef3f7", foreground="#222", relief="flat", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10))
        style.map("Treeview", background=[["selected", "#e8f0f5"]])

        # Card to wrap table
        card = tk.Frame(self.main_content, bg="white", highlightthickness=0, bd=0)
        card.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columns = ("ID", "Active", "DLL Path", "Token Name", "Edit", "Delete")
        tree = ttk.Treeview(card, columns=columns, show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Active", text="Active")
        tree.heading("DLL Path", text="DLL Path")
        tree.heading("Token Name", text="Token Name")
        tree.heading("Edit", text="Edit")
        tree.heading("Delete", text="Delete")

        tree.column("ID", width=50)
        tree.column("Active", width=100)
        tree.column("DLL Path", width=480)
        tree.column("Token Name", width=150)
        tree.column("Edit", width=80, anchor="center")
        tree.column("Delete", width=80, anchor="center")

        tree.pack(fill="both", expand=True)

        rows = fetch_profiles()

        for row in rows:
            active_status = "Yes" if int(row[1]) == 1 else "No"
            tree.insert("", "end", values=(row[0], active_status, row[2], row[3], "Edit", "Delete"))

        # Add edit and delete functionality
        def on_tree_select(event):
            selected_item = tree.selection()[0] if tree.selection() else None
            if not selected_item:
                return
            values = tree.item(selected_item, "values")
            column = tree.identify_column(event.x)

            if column == "#5":  # Edit column
                self.edit_profile(values[0])
            elif column == "#6":  # Delete column
                self.delete_profile(values[0])

        tree.bind("<Button-1>", on_tree_select)

    def edit_profile(self, profile_id):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        profile = fetch_profile_by_id(profile_id)

        if not profile:
            messagebox.showerror("Error", "Profile not found!")
            self.show_profiles()
            return

        def on_submit(values):
            update_profile(profile_id, values.get("active", True), values["dll_path"], values["token_name"])
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.show_profiles()

        self.render_profile_form(
            title="Edit Profile",
            defaults={
                "active": bool(int(profile[1])),
                "dll_path": profile[2],
                "token_name": profile[3],
            },
            include_active=True,
            on_submit=on_submit,
        )

    def add_new_profile(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        def on_submit(values):
            insert_profile(0, values["dll_path"], values["token_name"])
            messagebox.showinfo("Success", "Profile added successfully!")
            self.show_profiles()

        # In create form, active switch is not shown
        self.render_profile_form(
            title="Create Profile",
            defaults={"dll_path": "", "token_name": ""},
            include_active=False,
            on_submit=on_submit,
        )

    def render_profile_form(self, title, defaults, on_submit, include_active=True, custom_fields=None):
        # Card-like centered form reused by create/edit
        container = tk.Frame(self.main_content, bg=LIGHT_BG, width=600)
        container.pack(fill="both", expand=True)

        form_frame = tk.Frame(container, bg="white")
        form_frame.pack(padx=24, pady=24, fill="x")
        # Make the input column expand to fill space
        form_frame.grid_columnconfigure(1, weight=1)

        tk.Label(form_frame, text=title, font=self.font_heading, bg="white", fg=ACCENT).grid(row=0, column=0, columnspan=3, pady=16)
        row_idx = 1
        if custom_fields == "key_form":
            # Show the token name as in the Home panel, then a single Key entry
            tk.Label(form_frame, text="Token Name:", bg="white", fg=ACCENT).grid(row=row_idx, column=0, sticky="e", padx=(16, 8), pady=10)
            tk.Label(form_frame, text=defaults.get("token_name", ""), bg="white", fg="#22495e", font=("Segoe UI", 11, "bold")).grid(row=row_idx, column=1, sticky="w", padx=(0, 8), pady=10)
            row_idx += 1
            tk.Label(form_frame, text="Key", bg="white", fg=ACCENT).grid(row=row_idx, column=0, sticky="e", padx=(16, 8), pady=10)
            key_var = tk.StringVar(value=defaults.get("key", ""))
            tk.Entry(form_frame, textvariable=key_var).grid(row=row_idx, column=1, sticky="we", padx=(0, 8), pady=10)
            key_error_var = tk.StringVar(value="")
            tk.Label(form_frame, textvariable=key_error_var, fg="#c62828", bg="white").grid(row=row_idx+1, column=1, sticky="w", padx=(0, 8))
            row_idx += 2
            # Actions row
            def key_submit_action():
                key_error_var.set("")
                key_val = key_var.get().strip()
                if not key_val:
                    key_error_var.set("Key is required")
                    return
                on_submit({"key": key_val})
            actions = tk.Frame(form_frame, bg="white")
            actions.grid(row=row_idx, column=1, columnspan=2, pady=16, sticky="w", padx=(0, 8))
            self._create_rounded_button(
                actions,
                text="Submit",
                command=key_submit_action,
                bg=SUCCESS,
                hover_bg=SUCCESS_HOVER,
                pack_kwargs={"side": "left", "padx": (0, 10)}
            )
            return
        # (original render_profile_form continues as before)

        active_var = tk.BooleanVar(value=defaults.get("active", True))
        if include_active:
            tk.Label(form_frame, text="Active", bg="white", fg=ACCENT).grid(row=row_idx, column=0, sticky="e", padx=(16, 8), pady=10)
            tk.Checkbutton(form_frame, variable=active_var, bg="white", onvalue=True, offvalue=False).grid(row=row_idx, column=1, sticky="w", padx=(0, 8), pady=10)
            row_idx += 1

        tk.Label(form_frame, text="DLL Path", bg="white", fg=ACCENT).grid(row=row_idx, column=0, sticky="e", padx=(16, 8), pady=10)
        dll_path_var = tk.StringVar(value=defaults.get("dll_path", ""))
        tk.Entry(form_frame, textvariable=dll_path_var).grid(row=row_idx, column=1, sticky="we", padx=(0, 8), pady=10)

        def select_dll_path():
            current = dll_path_var.get().strip()
            start_dir = None
            if current:
                try:
                    maybe_dir = os.path.dirname(current) if os.path.isfile(current) else current
                    if os.path.isdir(maybe_dir):
                        start_dir = maybe_dir
                except Exception:
                    start_dir = None
            file_path = fd.askopenfilename(
                title="Select File",
                initialdir=start_dir,
                filetypes=[("All Files", "*.*"), ("DLL Files", "*.dll")],
            )
            if file_path:
                dll_path_var.set(file_path)

        # Holder frame uses grid; rounded button inside uses pack (no mixing in same parent)
        browse_holder = tk.Frame(form_frame, bg="white")
        browse_holder.grid(row=row_idx, column=2, padx=(0, 16), pady=10)
        self._create_rounded_button(
            browse_holder,
            text="Browse",
            command=select_dll_path,
            bg="#a9b5c1",
            hover_bg="#94a3af",
            padding_x=12,
            padding_y=4,
        )
        # Inline error for dll path
        dll_error_var = tk.StringVar(value="")
        tk.Label(form_frame, textvariable=dll_error_var, fg="#c62828", bg="white").grid(row=row_idx+1, column=1, sticky="w", padx=(0, 8))
        row_idx += 2

        tk.Label(form_frame, text="Token Name", bg="white", fg=ACCENT).grid(row=row_idx, column=0, sticky="e", padx=(16, 8), pady=10)
        token_name_var = tk.StringVar(value=defaults.get("token_name", ""))
        tk.Entry(form_frame, textvariable=token_name_var).grid(row=row_idx, column=1, sticky="we", padx=(0, 8), pady=10)
        token_error_var = tk.StringVar(value="")
        tk.Label(form_frame, textvariable=token_error_var, fg="#c62828", bg="white").grid(row=row_idx+1, column=1, sticky="w", padx=(0, 8))
        row_idx += 2

        def handle_submit():
            dll_error_var.set("")
            token_error_var.set("")
            dll_path = dll_path_var.get().strip()
            token_name = token_name_var.get().strip()

            has_error = False
            if not dll_path:
                dll_error_var.set("DLL path is required")
                has_error = True
            elif not os.path.isfile(dll_path):
                dll_error_var.set("Please select a valid file path")
                has_error = True

            if not token_name:
                token_error_var.set("Token name is required")
                has_error = True

            if has_error:
                return

            values = {
                "dll_path": dll_path,
                "token_name": token_name,
            }
            if include_active:
                values["active"] = active_var.get()
            on_submit(values)

        actions = tk.Frame(form_frame, bg="white")
        actions.grid(row=row_idx, column=1, columnspan=2, pady=16, sticky="w", padx=(0, 8))
        self._create_rounded_button(
            actions,
            text="💾  Save",
            command=handle_submit,
            bg=SUCCESS,
            hover_bg=SUCCESS_HOVER,
            pack_kwargs={"side": "left", "padx": (0, 10)}
        )
        self._create_rounded_button(
            actions,
            text="✖  Cancel",
            command=self.show_profiles,
            bg=ERROR,
            hover_bg=ERROR_HOVER,
        )

    def delete_profile(self, profile_id):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this profile?")
        if confirm:
            delete_profile(profile_id)

            messagebox.showinfo("Success", "Profile deleted successfully!")
            self.show_profiles()

    def close_app(self):
        self.root.destroy()
        self.root.quit()
