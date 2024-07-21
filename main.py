import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from functools import partial
from tkinter import messagebox
import time
import EvolutionaryAlgorithms

# --------------------------- #
# -- Variable declarations -- #
# --------------------------- #
global min_board_size 
global max_board_size
min_board_size = 4
max_board_size = 60

# -- Genetic Algorithm: default variables -- #
population_size = 250
mutation_rate = 0.8
crossover_rate = 0.3
generations = 10000

# -- Bee Colony Optimization: default variables -- #
ns = 100    # number of scout bees
nb = 10     # number of best sites
ne = 5      # number of elite sites
nrb = 3     # recruited bees for remaining 
nre = 2     # recruited bees for elite sites 
stlim = 35  # number of cycles after which a site is abandoned

# -- Ant Colony Optimization: default variables -- #
num_ants = 20           # number of ants
num_iterations = 500    # max number of generations/iterations
evaporation_rate = 0.5  # evaporation rate to discard local bests

# -- Particle Swarm Optimization -- #
num_particles = 20           # number of particles
max_iterations = 500    # max number of generations/iterations


# -- Algorithm selection options -- #
options = ["Genetic Algorithm", "Particle Swarm Optimization Algorithm", "Ant Colony Optimization Algorithm", "Bee Colony Optimization Algorithm"]

class MainScreen:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x300")
        
        title_label = tk.Label(root, text="N-Queens Problem", font=("Helvetica", 18, "bold"))
        title_label.pack()
        
        # Create an empty spacer label
        spacer_label = tk.Label(root, text="")
        spacer_label.pack()
        
        # Create a dictionary to store default values at input
        self.input_values = {
            "board_size": "",
            "pos_entry": "",
            "Genetic Algorithm": {
                "Population size": population_size,
                "Generations": generations,
                "Crossover rate": crossover_rate,
                "Mutation rate": mutation_rate
            },
            "Particle Swarm Optimization Algorithm": {
                "Particles": num_particles,
                "Number of iterations": max_iterations
            },
            "Ant Colony Optimization Algorithm": {
                "Number of ants": num_ants,
                "Number of iterations": num_iterations,
                "Evaporation rate": evaporation_rate
            },
            "Bee Colony Optimization Algorithm": {
                "Scout bees": ns,
                "Best sites": nb,
                "Elite sites": ne,
                "Cycles b/abandon": stlim,
                "Recruited remain": nrb, 
                "Recruited elite": nre 
            }
        }
        
        # Create a label for the dropdown menu
        label = tk.Label(root, text="Select an Evolutionary Algorithm option:")
        label.pack()
        
        # Create a dropdown menu
        self.option_var = tk.StringVar()
        self.option_var.set("Genetic Algorithm") # Set the default option
        self.option_menu = ttk.Combobox(root, textvariable=self.option_var, values=options, width=35)
        self.option_menu.pack()
        
        # Create an empty spacer label
        spacer_label = tk.Label(root, text="")
        spacer_label.pack()
        
        # Create an input field for 'n' variable
        n_label = tk.Label(root, text="Enter 'n' for board size:")
        n_label.pack()
        self.n_entry = tk.Entry(root,width=10)
        self.n_entry.pack()
        
        # Create an input field for queen starting positions
        pos_label = tk.Label(root, text="Enter queen starting positions (separated by spaces):")
        pos_label.pack()
        self.pos_entry = tk.Entry(root)
        self.pos_entry.pack()
        
        # Set a minimum width for the queens initial position entry
        self.pos_entry.config(width=10)  # Initial width
        self.min_pos_entry_width = 10
        
        
        # Create an empty spacer label
        spacer_label = tk.Label(root, text="")
        spacer_label.pack()
        
        # Create a Run button
        run_button = tk.Button(root, text="Run", command=self.run_results_screen)
        run_button.pack()
        
        self.pos_entry.bind('<KeyRelease>', self.on_pos_entry_text_changed)
        
    def on_pos_entry_text_changed(self, event):
        # Update the width of the n_entry based on the text content
        new_width = max(self.min_pos_entry_width, len(self.pos_entry.get()))
        self.pos_entry.config(width=new_width)
        
    def validate_n(self):
        # Get the input value from the entry field
        n_input = self.n_entry.get()
        try:
            n = int(n_input)
            if n >= min_board_size and n <= max_board_size:
                print("Board size set to", n)
                return True
            else:
                messagebox.showerror("Error", f"Board size must be at least {min_board_size} and at most {max_board_size}!")
        except ValueError:
            messagebox.showerror("Error", f"Invalid input: Please provide an integer number between {min_board_size} and {max_board_size}.")
            
    def validate_positions(self):
        # Get the input value for queen positions
        positions_input = self.pos_entry.get().strip()
        try:
            user_positions = [int(pos) for pos in positions_input.split()]  # Collect positions as integers
            n = int(self.n_entry.get())  # Get the board size value

            if len(user_positions) == n and all(1 <= pos <= n for pos in user_positions):
                print(f"Starting positions set to {user_positions}")
                return True
            else:
                messagebox.showerror("Error", f"Please provide {n} positions between 1 and {n}")
        except ValueError:
            messagebox.showerror("Error", f"Invalid input: Please only provide integer numbers between 1 and {n}")

    def run_results_screen(self):
        # Call validate_n to validate the board size
        if self.validate_n():
            # The first validation passed, now validate the queens positions
            if self.validate_positions():
                # Both validations passed, proceed to the next screen
                selected_option = self.option_var.get()
                n = int(self.n_entry.get())
                initial_pos = self.pos_entry.get().strip()
                self.input_values["board_size"] = n
                self.input_values["pos_entry"] = initial_pos
                
                # Close the first screen
                self.root.destroy()
                # Record the start time of execution of an EA
                start_time = time.time()
                if selected_option == "Genetic Algorithm":
                    solution = EvolutionaryAlgorithms.runGeneticAlgorithm(n,initial_pos,population_size,mutation_rate,crossover_rate,generations)
                    
                if selected_option == "Ant Colony Optimization Algorithm":    
                    solution = EvolutionaryAlgorithms.runAntColonyOptimization(n, num_ants, num_iterations, initial_pos, evaporation_rate)
                
                if selected_option == "Bee Colony Optimization Algorithm":  
                    solution = EvolutionaryAlgorithms.runBeesAlgorithm(n, ns, nb, ne, nrb, nre, stlim)
#******************************************************************                
                if selected_option == "Particle Swarm Optimization Algorithm":  
                    solution = EvolutionaryAlgorithms.runBeesAlgorithm(n, num_particles, max_iterations)
                    
                # Record the execution end time
                end_time = time.time()
                # Calculate the elapsed execution time in seconds by simple substraction
                execution_time = end_time - start_time
                execution_time = round(execution_time, 5)
                # Call the function to create and display the results screen
                create_results_screen(selected_option, n, solution, execution_time, self.input_values)
                
class ChessboardApp:
    def __init__(self, master, n, queens_rows, execution_time, selected_option, input_values):
        self.master = master
        self.master.geometry("850x600")
        
        self.option_var = tk.StringVar()
        self.option_var.set(f"{selected_option}")  # Set the default option
        
        self.queens_rows = queens_rows
        self.n = n
        
        self.input_values = input_values
        print(input_values)
        # Create a dropdown menu
        self.option_menu = ttk.Combobox(self.master, textvariable=self.option_var, values=options, width=35)
        self.option_menu.place(x=600, y=20)
        
        # Create labels and input boxes
        #### GENETIC ALGORITHM ####
        self.labelGA1 = tk.Label(self.master, text="Population size:")
        self.labelGA1.place(x=600, y=70)
        self.inputGA1 = tk.Entry(self.master)
        self.inputGA1.place(x=700, y=70)
        self.inputGA1.insert(0, self.input_values["Genetic Algorithm"]["Population size"]) 
        
        self.labelGA2 = tk.Label(self.master, text="# Generations:")
        self.labelGA2.place(x=600, y=100)
        self.inputGA2 = tk.Entry(self.master)
        self.inputGA2.place(x=700, y=100)
        self.inputGA2.insert(0, self.input_values["Genetic Algorithm"]["Generations"]) 
        
        self.labelGA3 = tk.Label(self.master, text="Crossover rate:")
        self.labelGA3.place(x=600, y=130)
        self.inputGA3 = tk.Entry(self.master)
        self.inputGA3.place(x=700, y=130)
        self.inputGA3.insert(0, self.input_values["Genetic Algorithm"]["Crossover rate"]) 
        
        self.labelGA4 = tk.Label(self.master, text="Mutation rate:")
        self.labelGA4.place(x=600, y=160)
        self.inputGA4 = tk.Entry(self.master)
        self.inputGA4.place(x=700, y=160)
        self.inputGA4.insert(0, self.input_values["Genetic Algorithm"]["Mutation rate"]) 
        
        #### ANT COLONY OPTIMIZATION ALGORITHM ####
        self.labelACO1 = tk.Label(self.master, text="Number of ants:")
        self.labelACO1.place(x=600, y=70)
        self.inputACO1 = tk.Entry(self.master)
        self.inputACO1.place(x=700, y=70)
        self.inputACO1.insert(0, self.input_values["Ant Colony Optimization Algorithm"]["Number of ants"]) 
        
        self.labelACO2 = tk.Label(self.master, text="# Iterations:")
        self.labelACO2.place(x=600, y=100)
        self.inputACO2 = tk.Entry(self.master)
        self.inputACO2.place(x=700, y=100)
        self.inputACO2.insert(0, self.input_values["Ant Colony Optimization Algorithm"]["Number of iterations"]) 
        
        self.labelACO3 = tk.Label(self.master, text="Evaporation rate:")
        self.labelACO3.place(x=600, y=130)
        self.inputACO3 = tk.Entry(self.master)
        self.inputACO3.place(x=700, y=130)
        self.inputACO3.insert(0, self.input_values["Ant Colony Optimization Algorithm"]["Evaporation rate"]) 
        
        #### BEE COLONY OPTIMIZATION ALGORITHM ####
        print("this is supposed to show: ")
        print(self.input_values)
        self.labelBCO1 = tk.Label(self.master, text="Scout bees:")
        self.labelBCO1.place(x=600, y=70)
        self.inputBCO1 = tk.Entry(self.master)
        self.inputBCO1.place(x=700, y=70)
        self.inputBCO1.insert(0, self.input_values["Bee Colony Optimization Algorithm"]["Scout bees"]) 
                
        self.labelBCO2 = tk.Label(self.master, text="Best sites:")
        self.labelBCO2.place(x=600, y=100)
        self.inputBCO2 = tk.Entry(self.master)
        self.inputBCO2.place(x=700, y=100)
        self.inputBCO2.insert(0, self.input_values["Bee Colony Optimization Algorithm"]["Best sites"]) 
        
        self.labelBCO3 = tk.Label(self.master, text="Elite sites:")
        self.labelBCO3.place(x=600, y=130)
        self.inputBCO3 = tk.Entry(self.master)
        self.inputBCO3.place(x=700, y=130)
        self.inputBCO3.insert(0, self.input_values["Bee Colony Optimization Algorithm"]["Elite sites"]) 
        
        self.labelBCO4 = tk.Label(self.master, text="Cycles b/abandon:")
        self.labelBCO4.place(x=600, y=160)
        self.inputBCO4 = tk.Entry(self.master)
        self.inputBCO4.place(x=710, y=160)
        self.inputBCO4.insert(0, self.input_values["Bee Colony Optimization Algorithm"]["Cycles b/abandon"]) 
        
        self.labelBCO5 = tk.Label(self.master, text="Recruited remain:")
        self.labelBCO5.place(x=600, y=190)
        self.inputBCO5 = tk.Entry(self.master)
        self.inputBCO5.place(x=710, y=190)
        self.inputBCO5.insert(0, self.input_values["Bee Colony Optimization Algorithm"]["Recruited remain"]) 
        
        self.labelBCO6 = tk.Label(self.master, text="Recruited elite:")
        self.labelBCO6.place(x=600, y=220)
        self.inputBCO6 = tk.Entry(self.master)
        self.inputBCO6.place(x=710, y=220)
        self.inputBCO6.insert(0, self.input_values["Bee Colony Optimization Algorithm"]["Recruited elite"]) 
                
        #### PARTICLE SWARM OPTIMIZATION ####
        self.labelA = tk.Label(self.master, text="Particles:")
        self.labelA.place(x=600, y=70)
        self.inputA = tk.Entry(self.master)
        self.inputA.place(x=700, y=70)
        self.inputA.insert(0, self.input_values["Particle Swarm Optimization Algorithm"]["Particles"]) 
        
        self.labelB = tk.Label(self.master, text="Number of iterations:")
        self.labelB.place(x=600, y=100)
        self.inputB = tk.Entry(self.master)
        self.inputB.place(x=700, y=100)
        self.inputB.insert(0, self.input_values["Particle Swarm Optimization Algorithm"]["Number of iterations"]) 
        
        
        # Store all input fields in a dictionary for easier access
        self.input_fields = {
            "Genetic Algorithm": [self.inputGA1, self.inputGA2, self.inputGA3, self.inputGA4],
            "Ant Colony Optimization Algorithm": [self.inputACO1, self.inputACO2, self.inputACO3],
            "Bee Colony Optimization Algorithm": [self.inputBCO1, self.inputBCO2, self.inputBCO3, self.inputBCO4, self.inputBCO5, self.inputBCO6],
            "Particle Swarm Optimization Algorithm": [self.inputA, self.inputB]
        }
        
        # Create a label widget to display the checkerboard
        self.label = tk.Label(self.master)
        self.label.place(x=10, y=10)
        
        # Load the queen image with a transparent background
        self.queen_image = Image.open("queen.png")  # Load the queen image
        self.tk_image = None  # Initialize tk_image
        
        # Bind the event handler with partial to pass additional arguments
        self.option_menu.bind("<<ComboboxSelected>>", self.on_option_select)
        
        # Update the checkerboard image initially
        self.update_checkerboard_image()
        
        # Display the execution time for any algorithm executed
        self.ExTime = tk.Label(self.master, text=f"Execution time: {execution_time} seconds")
        self.ExTime.place(x=600, y=360)
        
        
        # Create a button to trigger the retrieval of input values
        button_font = ("Helvetica", 12, "bold") 
        self.retrieve_button = tk.Button(self.master, text="Reload", command=self.retrieve_inputs, height=3, width=10, bg="#00CBCE", font=button_font, fg="#FFFFFF")
        self.retrieve_button.place(x=670, y=400)  # Adjust the position
        
       
    def validate_inputs(self, selected_option):
            input_fields = {
                "Genetic Algorithm": [self.inputGA1, self.inputGA2, self.inputGA3, self.inputGA4],
                "Particle Swarm Optimization Algorithm": [self.inputA, self.inputB],
                "Ant Colony Optimization Algorithm": [self.inputACO1, self.inputACO2, self.inputACO3],
                "Bee Colony Optimization Algorithm": [self.inputBCO1, self.inputBCO2, self.inputBCO3, self.inputBCO4, self.inputBCO5, self.inputBCO6]
            }
            input_values = {
                "Genetic Algorithm": ["Population size", "Generations", "Crossover rate", "Mutation rate"],
                "Particle Swarm Optimization Algorithm": ["Particles", "Number of iterations"],
                "Ant Colony Optimization Algorithm": ["Number of ants", "Number of iterations", "Evaporation rate"],
                "Bee Colony Optimization Algorithm": ["Scout bees", "Best sites", "Elite sites", "Cycles b/abandon", "Recruited remain", "Recruited elite"]
            }

            values = []
            for input_field in input_fields[selected_option]:
                value = input_field.get()
                values.append(value)

            if all(values):
                self.input_values[selected_option] = {k: v for k, v in zip(input_values[selected_option], values)}
                return True
            else:
                messagebox.showerror("Error", "Please fill in all fields.")
                return False
    
    def retrieve_inputs(self):
        # Validate input fields
        selected_option = self.option_var.get()
        if self.validate_inputs(selected_option):
            # Retrieve input values and store them in global variables
            input_values = self.input_values[selected_option]
            
            #print("Input values updated:", input_values)
            #print("Input values global:", self.input_values)

            # Update the input values when reloading
            self.update_input_fields(selected_option)
            self.reload_results_screen(selected_option,self.input_values)
            
    def update_input_fields(self, selected_option):
        # Set the input values in the input fields
        input_values = self.input_values[selected_option]
        input_fields = self.input_fields[selected_option]
        
        for input_field, (key, value) in zip(input_fields, input_values.items()):
            input_field.delete(0, tk.END)
            input_field.insert(0, value)
        
    # Recreate the results screen with new input values
    def reload_results_screen(self, selected_option, input_values):
        start_time = time.time()
        if selected_option == "Genetic Algorithm":
            solution = EvolutionaryAlgorithms.runGeneticAlgorithm(input_values["board_size"],
                                                                  self.input_values["pos_entry"],
                                                                  int(input_values[selected_option]["Population size"]),
                                                                  float(input_values[selected_option]["Mutation rate"]),
                                                                  float(input_values[selected_option]["Crossover rate"]),
                                                                  int(input_values[selected_option]["Generations"]))
        if selected_option == "Ant Colony Optimization Algorithm":    
            solution = EvolutionaryAlgorithms.runAntColonyOptimization(input_values["board_size"], 
                                                                       int(input_values[selected_option]["Number of ants"]), 
                                                                       int(input_values[selected_option]["Number of iterations"]), 
                                                                       self.input_values["pos_entry"], 
                                                                       float(input_values[selected_option]["Evaporation rate"]))
        if selected_option == "Bee Colony Optimization Algorithm":    
            solution = EvolutionaryAlgorithms.runBeesAlgorithm(int(input_values["board_size"]), 
                                                               int(input_values[selected_option]["Scout bees"]), 
                                                               int(input_values[selected_option]["Best sites"]), 
                                                               int(input_values[selected_option]["Elite sites"]), 
                                                               int(input_values[selected_option]["Recruited remain"]), 
                                                               int(input_values[selected_option]["Recruited elite"]), 
                                                               int(input_values[selected_option]["Cycles b/abandon"]))
#****************************************************************** 
        #### Update with correct EA name and expected input
        if selected_option == "Particle Swarm Optimization Algorithm":    
            solution = EvolutionaryAlgorithms.runAntColonyOptimization(input_values["board_size"], 
                                                                       int(input_values[selected_option]["Particles"]), 
                                                                       int(input_values[selected_option]["Number of iterations"]))
              
        # Record the execution end time
        end_time = time.time()
        # Calculate the elapsed execution time in seconds by simple substraction
        execution_time = end_time - start_time
        execution_time = round(execution_time, 5)
        
        # Bind the event handler with partial to pass additional arguments
        print("******* evolutionary algorithm used: ", selected_option)
        print("******* execution time: ", execution_time)
        print("******* new solution: ", solution)
        self.queens_rows = solution
        # Display the execution time for any algorithm executed
        self.ExTime = tk.Label(self.master, text=f"Execution time: {execution_time} seconds")
        self.ExTime.place(x=600, y=360)
        
        self.update_checkerboard_image()
        
    def on_option_select(self, event):
        self.update_checkerboard_image()
    
    def update_checkerboard_image(self):
        # Create a blank image for the checkerboard
        cell_width = 580 // self.n
        cell_height = 550 // self.n
        board = Image.new("RGB", (cell_width * self.n, cell_height * self.n), "white")
        
        bg = (0, 0, 0)  # Black color
        
        for i in range(self.n):
            for j in range(self.n):
                if (i + j) % 2 == 0:
                    cell = Image.new("RGBA", (cell_width, cell_height), bg)
                    board.paste(cell, (i * cell_width, j * cell_height))
        
        # Paste the queen images on the board
        for col, row in enumerate(self.queens_rows):
            x = (col * cell_width)
            y = ((self.n - row) * cell_height) # Shows the result from bottom to top
            queen_image_resized = self.queen_image.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
            board.paste(queen_image_resized, (x, y), queen_image_resized)
        
        # Convert the PIL image to a PhotoImage
        self.tk_image = ImageTk.PhotoImage(board)
        
        if self.tk_image:  # Check if the image was created successfully
            # Update the label image
            self.label.config(image=self.tk_image)
        
        selected_option = self.option_var.get()
        # Hide all labels and input boxes by default
        self.labelGA1.place_forget()
        self.inputGA1.place_forget()
        self.labelGA2.place_forget()
        self.inputGA2.place_forget()
        self.labelGA3.place_forget()
        self.inputGA3.place_forget()
        self.labelGA4.place_forget()
        self.inputGA4.place_forget()

        self.labelACO1.place_forget()
        self.inputACO1.place_forget()
        self.labelACO2.place_forget()
        self.inputACO2.place_forget()
        self.labelACO3.place_forget()
        self.inputACO3.place_forget()
        
        self.labelBCO1.place_forget()
        self.inputBCO1.place_forget()
        self.labelBCO2.place_forget()
        self.inputBCO2.place_forget()
        self.labelBCO3.place_forget()
        self.inputBCO3.place_forget()
        self.labelBCO4.place_forget()
        self.inputBCO4.place_forget()
        self.labelBCO5.place_forget()
        self.inputBCO5.place_forget()
        self.labelBCO6.place_forget()
        self.inputBCO6.place_forget()
        
        self.labelA.place_forget()
        self.inputA.place_forget()
        self.labelB.place_forget()
        self.inputB.place_forget()
        
        if selected_option == "Genetic Algorithm":
            # Show Label 1 and Input 1
            self.labelGA1.place(x=600, y=70)
            self.inputGA1.place(x=700, y=70)
            
            # Show Label 2 and Input 2
            self.labelGA2.place(x=600, y=100)
            self.inputGA2.place(x=700, y=100)
            
            # Show Label 3 and Input 3
            self.labelGA3.place(x=600, y=130)
            self.inputGA3.place(x=700, y=130)
            
            # Show Label 4 and Input 4
            self.labelGA4.place(x=600, y=160)
            self.inputGA4.place(x=700, y=160)
            
        elif selected_option == "Particle Swarm Optimization Algorithm":
            # Show Label A and Input A
            self.labelA.place(x=600, y=70)
            self.inputA.place(x=700, y=70)
            
            # Show Label B and Input B
            self.labelB.place(x=600, y=100)
            self.inputB.place(x=700, y=100)
            
        
        elif selected_option == "Ant Colony Optimization Algorithm":
            # Show Label A and Input A
            self.labelACO1.place(x=600, y=70)
            self.inputACO1.place(x=700, y=70)
            
            # Show Label B and Input B
            self.labelACO2.place(x=600, y=100)
            self.inputACO2.place(x=700, y=100)
            
            # Show Label 3 and Input 3
            self.labelACO3.place(x=600, y=130)
            self.inputACO3.place(x=700, y=130)
        
        elif selected_option == "Bee Colony Optimization Algorithm":
            # Show Label A and Input A
            self.labelBCO1.place(x=600, y=70)
            self.inputBCO1.place(x=700, y=70)
            
            # Show Label B and Input B
            self.labelBCO2.place(x=600, y=100)
            self.inputBCO2.place(x=700, y=100)
            
            # Show Label 3 and Input 3
            self.labelBCO3.place(x=600, y=130)
            self.inputBCO3.place(x=700, y=130)
            
            # Show Label 3 and Input 3
            self.labelBCO4.place(x=600, y=160)
            self.inputBCO4.place(x=710, y=160)
            
            # Show Label 3 and Input 3
            self.labelBCO5.place(x=600, y=190)
            self.inputBCO5.place(x=710, y=190)
            
            # Show Label 3 and Input 3
            self.labelBCO6.place(x=600, y=220)
            self.inputBCO6.place(x=710, y=220)
            

def create_results_screen(selected_option, n, initial_pos, execution_time, input_values):
     root = tk.Tk()
     # Convert the initial_pos to a list of integers
     #initial_pos = [int(pos) for pos in initial_pos.split()]
     app = ChessboardApp(root, n, initial_pos, execution_time, selected_option, input_values)
     root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainScreen(root)
    root.mainloop()