import warnings
warnings.filterwarnings('ignore')

# Qiskit imports
import qiskit
from qiskit import QuantumCircuit
from qiskit.visualization import visualize_transition

# Tkinter imports for GUI components
from tkinter import Tk, PhotoImage, Label, Text, Button, Entry, LabelFrame, LEFT, END, DISABLED, NORMAL

# Additional libraries
import numpy as np

# Circuit initialization function
def initialize_circuit():
    """
    Initializes a single-qubit quantum circuit.

    This function creates a global variable `circuit` and assigns to it an 
    instance of Qiskit's QuantumCircuit class, initialized with a single qubit. 
    The global assignment allows this circuit to be accessible across functions 
    in the module, supporting circuit manipulation and visualization.
    """
    global circuit
    circuit = QuantumCircuit(1)  # Create a quantum circuit with one qubit


# 'About' Information Display Function
def about():
    """
    Creates a new window displaying information about the Bloch Sphere Visualizer.

    This function generates a separate tkinter window that provides users with 
    detailed information about the Bloch Sphere Visualizer tool. It outlines 
    the purpose, creator information, and command details for various gate 
    operations used within the application. Additionally, it specifies limitations 
    on visualization and angle range for rotation gates RX, RY, and RZ.
    
    Window Components:
    - A title label with "About Bloch Sphere Visualizer" in a designated font.
    - A text widget displaying instructions and descriptions of each gate.
    
    Functionality:
    - The new window is non-resizable with a fixed size.
    - The information includes command mappings for gates and a note on the 
      allowable rotation range.
    - If circuit visualization fails due to an error, the application closes 
      automatically.

    Usage:
    Invoke this function when the user selects the 'About' button to provide 
    guidance on tool usage and gate functions.
    """
    # Initialize new info window with title and fixed size
    info = Tk()
    info.title('About')
    info.geometry('1125x625')
    info.resizable(0, 0)

    # Configure and pack label
    label = Label(info, text='About Bloch Sphere Visualizer')
    label.config(font=('IBM Plex Sans', 12))
    label.pack()

    # Insert informational text with gate details
    text = Text(info, height=20, width=20)
    text_to_display = '''
    This is a visualization tool for 'Single Qubit Rotation' on Bloch Sphere

    Created by : Anup Das
    Created by using : Qiskit, Tkinter

    Information about gate buttons and corresponding Qiskit commands:
    
    X = Flips the state of qubit                                                circuit.x()
    Y = Rotates the state vector about the y-axis                               circuit.y()
    Z = Flips the phase by PI radians                                           circuit.z()
    RX = Parameterized rotation about the x-axis                                circuit.rx()
    RY = Parameterized rotation about the y-axis                                circuit.ry()
    RZ = Parameterized rotation about the z-axis                                circuit.rz()
    S = Rotates the state vector about the z-axis by PI/2 radians               circuit.s()
    T = Rotates the state vector about the z-axis by PI/4 radians               circuit.t()
    SD = Rotates the state vector about the z-axis by -PI/2 radians             circuit.s()
    TD = Rotates the state vector about the z-axis by -PI/4 radians             circuit.t()
    H = Creates the state of superposition                                      circuit.h()
    
    Note : 
    For RX, RY, and RZ, theta (i.e., the rotation angle) in this application is [-2*PI, 2*PI]

    In case of any visualization errors, the application closes automatically, indicating the circuit visualization is not possible.

    At maximum, only ten operations can be visualized at one time.
    '''
    text.pack(fill='both', expand=True)
    text.insert(END, text_to_display)

    # Start the main event loop for the information window
    info.mainloop()


def display_gate(gate_input):
    """
    Displays the selected gate in the input display and tracks the number of gates used.

    This function takes a gate input, adds it to the tkinter display, and then calculates 
    the total number of gates used, taking into account specific double-character gate labels 
    (e.g., 'R' and 'D') that count as single gates. Once the limit of 10 gates is reached, 
    it disables further gate button interactions to prevent exceeding visualization limits.

    Parameters:
    gate_input (str): The identifier for the gate being added (e.g., 'X', 'Y', 'Z').

    Procedure:
    - Insert the selected gate into the display.
    - Calculate the current count of gates, with adjustments for double-character gates.
    - If 10 gates are in use, disable all gate buttons to restrict additional entries.

    Notes:
    - Gates are represented by button instances (e.g., `x_gate`, `y_gate`), which are disabled 
      by setting their `state` to `DISABLED` once the maximum count is reached.
    """
    # Add the gate input to the display entry field
    display.insert(END, gate_input)
    
    # Retrieve the full list of gate inputs
    input_gates = display.get()
    num_gates_pressed = len(input_gates)
    
    # Convert input string to list and adjust for double-character gate labels
    list_input_gates = list(input_gates)
    search_word = ['R', 'D']
    count_double_Valued_gates = [list_input_gates.count(i) for i in search_word]
    num_gates_pressed -= sum(count_double_Valued_gates)
    
    # Disable all gate buttons if the count reaches the maximum allowed limit
    if num_gates_pressed == 10:
        gates = [x_gate, y_gate, z_gate, Rx_gate, Ry_gate, Rz_gate, s_gate, sd_gate, t_gate, td_gate, hadamard]
        for gate in gates:
            gate.config(state=DISABLED)


def change_theta(num, window, circuit, key):
    """
    Applies a parameterized rotation to the circuit based on the input angle and specified axis.

    This function calculates a rotation angle `theta` by multiplying `num` by `pi`, then applies 
    this rotation to the quantum circuit on the axis defined by `key` ('x', 'y', or 'z'). Once 
    the rotation is applied, `theta` is reset to zero, and the input window is closed.

    Parameters:
    num (float): Multiplier for `pi` to define the rotation angle.
    window (tkinter.Tk): The tkinter window used for collecting the rotation input.
    circuit (QuantumCircuit): The QuantumCircuit object where the rotation gate is applied.
    key (str): Specifies the axis of rotation ('x', 'y', or 'z').

    Procedure:
    - Calculate the angle `theta` by scaling `num` with `pi`.
    - Apply a rotation gate (`rx`, `ry`, or `rz`) on the circuit based on the axis `key`.
    - Close the input window and reset `theta` for the next operation.

    Notes:
    - This function leverages global access to `theta` for real-time adjustments, but `theta` 
      is reset to zero after each gate application to ensure accurate successive operations.
    """
    # Calculate the angle for rotation
    global theta
    theta = num * np.pi
    
    # Apply the rotation gate based on the specified axis
    if key == 'x':
        circuit.rx(theta, 0)
    elif key == 'y':
        circuit.ry(theta, 0)
    else:
        circuit.rz(theta, 0)
    
    # Reset theta and close the input window
    theta = 0
    window.destroy()


def user_input(circuit, key):
    """
    Creates a pop-up window for selecting a rotation angle for a quantum gate, applied to the given circuit.

    This function presents users with a GUI to select predefined rotation values, expressed as multiples of pi,
    for a specified axis of rotation (`key`) in the quantum circuit. The function calls `change_theta()` to 
    apply the chosen angle to the circuit.

    Parameters:
    circuit (QuantumCircuit): The QuantumCircuit object to apply the rotation on.
    key (str): Specifies the axis for rotation ('x', 'y', or 'z').

    GUI Layout:
    - A pop-up window with buttons for angles (PI/4, PI/2, PI, 2*PI) and their negative equivalents.
    - A text widget provides instructions and indicates valid angle ranges.

    Angle Buttons:
    - Each button specifies a rotation angle (positive or negative) for `theta`.
    - When clicked, `change_theta()` is called with the selected angle multiplier to apply the rotation.

    Example Usage:
    - user_input(circuit, 'x') prompts the user to select a rotation angle for the x-axis.

    Notes:
    - The input range for `theta` is restricted to [-2*PI, 2*PI].
    """
    # Initialize pop-up window
    get_input = Tk()
    get_input.title('Get Theta')
    get_input.geometry('360x360')
    get_input.resizable(0, 0)

    # Define positive rotation buttons
    val1 = Button(get_input, height=2, width=10, bg=buttons, font=('IBM Plex Sans', 10), text='PI/4', command=lambda: change_theta(0.25, get_input, circuit, key))
    val2 = Button(get_input, height=2, width=10, bg=buttons, font=('IBM Plex Sans', 10), text='PI/2', command=lambda: change_theta(0.50, get_input, circuit, key))
    val3 = Button(get_input, height=2, width=10, bg=buttons, font=('IBM Plex Sans', 10), text='PI', command=lambda: change_theta(1.0, get_input, circuit, key))
    val4 = Button(get_input, height=2, width=10, bg=buttons, font=('IBM Plex Sans', 10), text='2*PI', command=lambda: change_theta(2.0, get_input, circuit, key))
    
    val1.grid(row=0, column=0)
    val2.grid(row=0, column=1)
    val3.grid(row=0, column=2)
    val4.grid(row=0, column=3, sticky='W')

    # Define negative rotation buttons
    nval1 = Button(get_input, height=2, width=10, bg=buttons, font=('IBM Plex Sans', 10), text='-PI/4', command=lambda: change_theta(-0.25, get_input, circuit, key))
    nval2 = Button(get_input, height=2, width=10, bg=buttons, font=('IBM Plex Sans', 10), text='-PI/2', command=lambda: change_theta(-0.5, get_input, circuit, key))
    nval3 = Button(get_input, height=2, width=10, bg=buttons, font=('IBM Plex Sans', 10), text='-PI', command=lambda: change_theta(-1.0, get_input, circuit, key))
    nval4 = Button(get_input, height=2, width=10, bg=buttons, font=('IBM Plex Sans', 10), text='-2*PI', command=lambda: change_theta(-2.0, get_input, circuit, key))
    
    nval1.grid(row=1, column=0)
    nval2.grid(row=1, column=1)
    nval3.grid(row=1, column=2)
    nval4.grid(row=1, column=3, sticky='W')

    # Instructional text widget
    text_object = Text(get_input, height=20, width=20, bg='light cyan')
    note = '''
    Enter the value for theta.
    Valid range: [-2*PI, 2*PI]
    '''
    text_object.grid(sticky='WE', columnspan=4)
    text_object.insert(END, note)

    # Run the GUI loop
    get_input.mainloop()



def clear():
    """
    Clears the display and reinitializes the quantum circuit, restoring gate functionality.

    This function performs the following actions:
    - Clears the display area to reset user input.
    - Reinitializes the quantum circuit by calling `initialize_circuit()`, which prepares it for new inputs.
    - Checks if any gates are currently disabled (e.g., maximum gate limit reached). 
      If so, it re-enables all gates to allow new operations.


    Steps:
    - `display.delete(0, END)`: Clears any displayed gate input.
    - `initialize_circuit()`: Resets the quantum circuit state.
    - `gate.config(state=NORMAL)`: Re-enables each gate if previously disabled.

    Example Usage:
    - Call `clear(circuit)` when starting a new operation or when resetting the circuit state is required.
    """
    # Clear display content
    display.delete(0, END)
    
    # Reinitialize the circuit
    initialize_circuit()

    # Check and reset gate states if disabled
    if x_gate['state'] == DISABLED:
        gates = [x_gate, y_gate, z_gate, Rx_gate, Ry_gate, Rz_gate, s_gate, sd_gate, t_gate, td_gate, hadamard]
        for gate in gates:
            gate.config(state=NORMAL)


def visualize_circuit(circuit, window):
    """
    Attempts to visualize the quantum circuit's state transition on the Bloch sphere.
    
    Parameters:
    - circuit (QuantumCircuit): The QuantumCircuit object to visualize.
    - window (Tkinter window): The Tkinter window that will be closed if visualization fails.
    
    Description:
    - This function calls `visualize_transition()` to render the Bloch sphere visualization of
      the `circuit` parameter, allowing insight into state transitions of the quantum circuit.
    - If visualization is not feasible (e.g., due to circuit incompatibility or a `VisualizationError`), 
      the function catches the error and safely closes the `window` to prevent the application from hanging.
    
    Example Usage:
    - `visualize_circuit(circuit, window)` renders the visualization or closes the window on failure.
    """
    try:
        # Attempt visualization of the circuit's state transition
        visualize_transition(circuit=circuit)
    except qiskit.visualization.exceptions.VisualizationError:
        # Close the Tkinter window if visualization fails
        window.destroy()


# Initialize the main application window for the Bloch Sphere Visualization tool
root = Tk()
root.title('Bloch Sphere Visualizer')

# Set the application icon (ensure the icon is in PNG format)
icon = PhotoImage(file='app_icon.png')  # Convert your .ico file to .png first
root.iconphoto(True, icon)

# Configure the window size and properties
root.geometry('399x430')
root.resizable(0, 0)  # Disable resizing options to maintain a fixed layout

# Define color scheme and font styles for the application
background = '#384B70'  # Background color for the main window
buttons = '#FCFAEE'     # Color for standard buttons
special_buttons = '#B8001F'  # Color for special buttons (e.g., reset)
button_font = ('IBM Plex Sans', 18)  # Font style and size for buttons
display_font = ('IBM Plex Sans', 32)  # Font style and size for display text


# Initialize the quantum circuit and set the rotation angle (theta) to zero
initialize_circuit()  # Create a new instance of the quantum circuit
theta = 0  # Initialize the rotation angle to zero for subsequent operations


# Define the layout of the application
# Create frames for organizing the display and buttons
display_frame = LabelFrame(root)  # Frame for the display area
button_frame = LabelFrame(root, bg='black')  # Frame for buttons with a black background

# Pack the frames into the main window
display_frame.pack()  # Add display frame to the root window
button_frame.pack(fill='both', expand=True)  # Add button frame and allow it to expand

# Define the layout of the display frame
display = Entry(display_frame, width=120, font=display_font, bg=background, borderwidth=10, justify=LEFT)
display.pack(padx=3, pady=4)  # Add the entry widget to the display frame with padding


# Defining the first row of buttons for basic gates
x_gate = Button(button_frame, font=button_font, bg=buttons, text='X', command=lambda: [display_gate('X'), circuit.x(0)])
y_gate = Button(button_frame, font=button_font, bg=buttons, text='Y', command=lambda: [display_gate('Y'), circuit.y(0)])
z_gate = Button(button_frame, font=button_font, bg=buttons, text='Z', command=lambda: [display_gate('Z'), circuit.z(0)])
# Position buttons in the first row of the grid
x_gate.grid(row=0, column=0, ipadx=45, pady=1)
y_gate.grid(row=0, column=1, ipadx=45, pady=1)
z_gate.grid(row=0, column=2, ipadx=53, pady=1, sticky='E')  # E = East

# Defining the second row of buttons for rotation gates
Rx_gate = Button(button_frame, font=button_font, bg=buttons, text='RX', command=lambda: [display_gate('Rx'), user_input(circuit, 'x')])
Ry_gate = Button(button_frame, font=button_font, bg=buttons, text='RY', command=lambda: [display_gate('Ry'), user_input(circuit, 'y')])
Rz_gate = Button(button_frame, font=button_font, bg=buttons, text='RZ', command=lambda: [display_gate('Rz'), user_input(circuit, 'z')])
# Position buttons in the second row of the grid
Rx_gate.grid(row=1, column=0, columnspan=1, sticky='WE', pady=1)
Ry_gate.grid(row=1, column=1, columnspan=1, sticky='WE', pady=1)
Rz_gate.grid(row=1, column=2, columnspan=1, sticky='WE', pady=1)

# Defining the third row of buttons for phase gates and Hadamard gate
s_gate = Button(button_frame, font=button_font, bg=buttons, text='S', command=lambda: [display_gate('S'), circuit.s(0)])
sd_gate = Button(button_frame, font=button_font, bg=buttons, text='SD', command=lambda: [display_gate('SD'), circuit.sdg(0)])
hadamard = Button(button_frame, font=button_font, bg=buttons, text='H', command=lambda: [display_gate('H'), circuit.h(0)])
# Position buttons in the third row of the grid
s_gate.grid(row=2, column=0, columnspan=1, sticky='WE', pady=1)
sd_gate.grid(row=2, column=1, columnspan=1, sticky='WE', pady=1)
hadamard.grid(row=2, column=2, rowspan=2, sticky='WENS', pady=1)

# Defining the fourth row of buttons for T gates
t_gate = Button(button_frame, font=button_font, bg=buttons, text='T', command=lambda: [display_gate('T'), circuit.t(0)])
td_gate = Button(button_frame, font=button_font, bg=buttons, text='TD', command=lambda: [display_gate('TD'), circuit.tdg(0)])
# Position buttons in the fourth row of the grid
t_gate.grid(row=3, column=0, sticky='WE', pady=1)
td_gate.grid(row=3, column=1, sticky='WE', pady=1)

# Defining the quit and visualize buttons
quit = Button(button_frame, font=button_font, bg=buttons, text='Quit', command=root.destroy)
visualize = Button(button_frame, font=button_font, bg=buttons, text='Visualize', command=lambda: visualize_circuit(circuit, root))
# Position quit and visualize buttons in the grid
quit.grid(row=4, column=0, columnspan=2, sticky='WE', ipadx=5, pady=1)
visualize.grid(row=4, column=2, columnspan=1, sticky='WE', ipadx=8, pady=1)

# Defining the clear button for resetting the circuit
clear_button = Button(button_frame, font=button_font, bg=special_buttons, text="Clear", command=lambda: clear())
clear_button.grid(row=5, column=0, columnspan=3, sticky='WE')

# Defining the about button to display information about the application
about_button = Button(button_frame, font=button_font, bg=special_buttons, text='About', command=about)
about_button.grid(row=6, column=0, columnspan=3, sticky='WE')

# Start the main event loop for the Tkinter application
# This keeps the application running and responsive to user inputs until the window is closed.
root.mainloop()