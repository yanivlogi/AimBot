import tkinter as tk
import pyautogui
import time
import keyboard
import win32api, win32con

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def start_script():
    instructions_text.config(state=tk.NORMAL)
    instructions_text.insert(tk.END, "\nThe script is now running. Press 'q' to stop it.\n")
    instructions_text.config(state=tk.DISABLED)

    target_color = (int(red_entry.get()), int(green_entry.get()), int(blue_entry.get()))
    time.sleep(2)

    while not keyboard.is_pressed('q'):
        flag = 0
        pic = pyautogui.screenshot(region=(0, 0, 2560, 1440))

        width, height = pic.size

        for x in range(0, width, 4):
            for y in range(0, height, 4):
                r, g, b = pic.getpixel((x, y))

                if (r, g, b) == target_color:
                    flag = 1
                    click(x, y)
                    time.sleep(0.01)
                    break

            if flag == 1:
                break

    instructions_text.config(state=tk.NORMAL)
    instructions_text.insert(tk.END, "The script has been stopped.\n")
    instructions_text.config(state=tk.DISABLED)

def sample_color():
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")  # Save the screenshot for display

    # Create a new window to display the screenshot
    overlay_window = tk.Toplevel()
    overlay_window.title("Color Sampling")
    overlay_window.attributes("-fullscreen", True)  # Fullscreen
    overlay_window.configure(bg="black")

    # Create a label to display the screenshot
    img = tk.PhotoImage(file="screenshot.png")  # Load the screenshot
    label = tk.Label(overlay_window, image=img)
    label.image = img  # Keep a reference to avoid garbage collection
    label.pack()

    # Instructions for color sampling
    instructions_text.config(state=tk.NORMAL)
    instructions_text.insert(tk.END, "\nClick on the desired color.\n")
    instructions_text.config(state=tk.DISABLED)

    # Create a canvas for zoomed area
    zoomed_canvas = tk.Canvas(overlay_window, width=200, height=200, bg="white")
    zoomed_canvas.pack()

    # Bind mouse movement to update zoomed color
    overlay_window.bind("<Motion>", lambda event: update_zoom(event, zoomed_canvas))

    # Wait for mouse click to capture the color
    overlay_window.bind("<Button-1>", lambda event: capture_color(event, overlay_window))

def update_zoom(event, zoomed_canvas):
    # Get the mouse position
    x, y = event.x, event.y
    
    # Take a screenshot to zoom in
    screenshot = pyautogui.screenshot()

    # Define zoom area (50x50 pixels) around the cursor position
    zoom_area = screenshot.crop((x - 25, y - 25, x + 25, y + 25))
    
    # Resize to zoom (200x200 pixels)
    zoomed_image = zoom_area.resize((200, 200))

    # Display the zoomed image
    zoomed_image.save("zoomed.png")  # Save for display
    img = tk.PhotoImage(file="zoomed.png")
    zoomed_canvas.create_image(100, 100, image=img)
    zoomed_canvas.image = img  # Keep a reference to avoid garbage collection

def capture_color(event, overlay_window):
    x, y = event.x, event.y  # Get the clicked position
    r, g, b = pyautogui.screenshot().getpixel((x, y))  # Get pixel color at that position
    red_entry.delete(0, tk.END)
    green_entry.delete(0, tk.END)
    blue_entry.delete(0, tk.END)
    red_entry.insert(0, r)
    green_entry.insert(0, g)
    blue_entry.insert(0, b)

    # Display the selected color
    color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')

    overlay_window.destroy()  # Close the overlay window

# Create the main window
root = tk.Tk()
root.title("Automation Tool")
root.geometry("500x500")

# Create instructions label
instructions_label = tk.Label(root, text="Instructions for using this software:", font=("Arial", 12, "bold"))
instructions_label.pack(pady=10)

# Create instructions text box
instructions_text = tk.Text(root, height=10, width=50, wrap=tk.WORD, bg="lightgrey", font=("Arial", 10))
instructions_text.pack(pady=10)
instructions_text.insert(tk.END,
    "1. Enter RGB values for the color you want to target.\n"
    "2. Click 'Sample Color' to capture the color at the mouse cursor.\n"
    "3. Click 'Start' to run the automation script.\n"
    "4. To stop the script, press the 'q' key.\n"
    "\n"
    "This software was created by Yaniv Logi."
)
instructions_text.config(state=tk.DISABLED)  # Make the text box read-only

# RGB input fields
rgb_frame = tk.Frame(root)
rgb_frame.pack(pady=10)

tk.Label(rgb_frame, text="R:").grid(row=0, column=0)
red_entry = tk.Entry(rgb_frame, width=5)
red_entry.grid(row=0, column=1)

tk.Label(rgb_frame, text="G:").grid(row=0, column=2)
green_entry = tk.Entry(rgb_frame, width=5)
green_entry.grid(row=0, column=3)

tk.Label(rgb_frame, text="B:").grid(row=0, column=4)
blue_entry = tk.Entry(rgb_frame, width=5)
blue_entry.grid(row=0, column=5)

# Sample color button
sample_button = tk.Button(root, text="Sample Color", command=sample_color)
sample_button.pack(pady=10)

# Color display label
color_display = tk.Label(root, text="Selected Color", width=20, height=2, bg="white")
color_display.pack(pady=10)

# Create start button
start_button = tk.Button(root, text="Start", command=start_script)
start_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
