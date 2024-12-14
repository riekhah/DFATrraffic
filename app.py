from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Initial state of the traffic light
state = "NS_Green_EW_Red"

# Flag to track if a car is detected in EW
ew_car_waiting = False

def handle_event(current_state, input_signal):
    global ew_car_waiting

    if current_state == "NS_Green_EW_Red":
        if input_signal == 1:  # Car detected in EW
            ew_car_waiting = True
            return "NS_Yellow_EW_Red"  # Transition to NS yellow
        return "NS_Green_EW_Red"  # NS continues green if no car detected

    elif current_state == "NS_Yellow_EW_Red":
        return "NS_Red_EW_Green"  # Transition to EW green

    elif current_state == "NS_Red_EW_Green":
        if ew_car_waiting:  # If a car is waiting in EW
            ew_car_waiting = False  # Clear waiting flag
            return "NS_Red_EW_Yellow"  # Transition to EW yellow
        return "NS_Red_EW_Yellow"  # Transition to EW yellow if no additional cars

    elif current_state == "NS_Red_EW_Yellow":
        return "NS_Green_EW_Red"  # Transition back to NS green

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update_state', methods=['POST'])
def update_state():
    global state
    input_signal = request.json.get('input', 0)  # Get input signal
    state = handle_event(state, input_signal)  # Update state based on DFA logic
    return jsonify({'state': state})  # Return updated state

if __name__ == '__main__':
    app.run(debug=True)
