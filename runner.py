from customtkinter import *
from tkinter import messagebox
import subprocess

def main():
    window = CTk()
    window.title("Rescuing the Princess | Visualizer")
    window.configure(bg="#242424")
  # Set the geometry of the Tkinter window
    app_width = 420
    app_height = 260
    # Get the screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # Calculate x and y coordinates for the Tkinter window to be in the center of the screen
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    window.resizable(0, 0)

    label1 = CTkLabel(window, text="Algorithm", fg_color="transparent", font=("calibri", 15), text_color="#00FF89")
    label1.place(relx=0.5, rely=0.15, anchor=CENTER)

    choice = StringVar()
    combobox1 = CTkComboBox(window, values=["BFS Algorithm", "A* Algorithm"], variable=choice, state="readonly", button_color="#00FF89")
    combobox1.set("A* Algorithm")
    combobox1.place(relx=0.5, rely=0.30, anchor=CENTER)

    label2 = CTkLabel(window, text="Grid Dimension", fg_color="transparent", font=("calibri", 15), text_color="#FF0099")
    label2.place(relx=0.5, rely=0.50, anchor=CENTER)

    gridDimension = StringVar()
    entryGridDimension = CTkEntry(window, textvariable=gridDimension, width=120, placeholder_text="e.g., 10x10")
    entryGridDimension.place(relx=0.5, rely=0.65, anchor=CENTER)

    def parse_grid_dimensions(dim_str):
        parts = dim_str.split('x')
        if len(parts) != 2:
            messagebox.showerror("Invalid Format", "Please enter dimensions in the format 'NxN', such as '10x10'.")
            return None
        try:
            rows, cols = map(int, parts)
            if rows != cols:
                messagebox.showerror("Invalid Dimensions", "Rows and columns must be equal for a square grid.")
                return None
            if rows <= 0:
                raise ValueError("Dimensions must be greater than zero.")
            return (rows, cols)
        except ValueError:
            messagebox.showerror("Invalid Input", "Dimensions must be positive integers.")
            return None

    def runner():
        grid_dims = parse_grid_dimensions(gridDimension.get())
        algorithm_choice = choice.get()
        if grid_dims:
            # Map the combobox choice to the corresponding algorithm name expected by the Pygame script.
            algorithm_name = "astar" if algorithm_choice == "A* Algorithm" else "bfs"
            # Start the Pygame script with the grid size and the algorithm as command line arguments.
            subprocess.Popen(['python', 'game.py', str(grid_dims[0]), algorithm_name])
        else:
            messagebox.showerror("Error", "Invalid grid dimensions. Please enter a square grid dimension like '10x10'.")


    submit_button = CTkButton(window, text="Start", command=runner, font=('calibri', 12, 'bold'))
    submit_button.place(relx=0.5, rely=0.85, anchor=CENTER)

    window.mainloop()

if __name__ == "__main__":
    main()
