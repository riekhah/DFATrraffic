from flask import Flask, request, jsonify, render_template
import logging

# Initialize the Flask application
app = Flask(__name__)

# Configure logging without date and time
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Initial state of the traffic light
state = "NS_Green_EW_Red"

# Flag to track if a car is detected in EW
ew_car_waiting = False

# Function to handle state transitions
def handle_event(current_state, input_signal):
    global ew_car_waiting

    # Log the current state and input
    logging.info(f"Current State: {current_state}, Input: {input_signal}")

    # Determine the next state based on DFA logic
    if current_state == "NS_Green_EW_Red":
        if input_signal == 1:  # Car detected in EW
            ew_car_waiting = True
            next_state = "NS_Yellow_EW_Red"  # Transition to NS yellow
        else:
            next_state = "NS_Green_EW_Red"  # NS continues green if no car detected

    elif current_state == "NS_Yellow_EW_Red":
        next_state = "NS_Red_EW_Green"  # Transition to EW green

    elif current_state == "NS_Red_EW_Green":
        if ew_car_waiting:  # If a car is waiting in EW
            ew_car_waiting = False  # Clear waiting flag
            next_state = "NS_Red_EW_Yellow"  # Transition to EW yellow
        else:
            next_state = "NS_Red_EW_Yellow"  # Transition to EW yellow if no additional cars

    elif current_state == "NS_Red_EW_Yellow":
        next_state = "NS_Green_EW_Red"  # Transition back to NS green

    # Log the mathematical formula for the transition
    logging.info(f"Formula: δ({current_state}, {input_signal}) = {next_state}")
    logging.info(f"Next State: {next_state}")
    return next_state

# Route to serve the main HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle state updates
@app.route('/update_state', methods=['POST'])
def update_state():
    global state
    input_signal = request.json.get('input', 0)  # Get input signal
    logging.info(f"Received Input: {input_signal}")
    state = handle_event(state, input_signal)  # Update state based on DFA logic
    logging.info(f"Updated State: {state}")
    return jsonify({'state': state})  # Return updated state to frontend

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
