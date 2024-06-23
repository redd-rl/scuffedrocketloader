import tkinter as tk
# We found two installations, choose your preferred installation for us to load custom maps to.
def select_platform_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Create a custom Toplevel dialog
    dialog = tk.Toplevel(root)
    dialog.title("Select Platform")

    # Label with instructions
    label = tk.Label(dialog, text="We found two installations.\nChoose your preferred installation for us to load custom maps to.")
    label.pack(pady=10)

    # Variable to store the selected platform
    selected_platform = tk.StringVar()

    # Function to handle button click and return the platform
    def button_clicked(platform):
        selected_platform.set(platform)
        dialog.quit()  # Breaks the mainloop
        dialog.destroy()  # Close the dialog

    # Button for Steam
    btn_steam = tk.Button(dialog, text="Steam", width=10,
                          command=lambda: button_clicked("Steam"))
    btn_steam.pack(pady=5)

    # Button for Epic Games
    btn_epic = tk.Button(dialog, text="Epic Games", width=10,
                         command=lambda: button_clicked("Epic Games"))
    btn_epic.pack(pady=5)

    # Set minimum width of the dialog to fit the title and content
    dialog.update_idletasks()
    min_width = max(dialog.winfo_width(), 300)  # Adjust 300 as needed
    dialog.minsize(min_width, dialog.winfo_height())

    # Center the dialog on the screen
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'+{x}+{y}')

    # Run the tkinter main loop
    root.mainloop()

    # Return the selected platform after the dialog is closed
    return selected_platform.get()

if __name__ == "__main__":
    platform = select_platform_dialog()
    print(f"Selected platform: {platform}")
