from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__, template_folder='template')

# Load the model
model = pickle.load(open(r'C:\Users\srira\OneDrive\Desktop\akhil\productivity4.pkl', 'rb'))

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/happy1')
def happy1():
    return render_template('about1.html')

@app.route('/happy2')
def happy2():
    return render_template('department1.html')



@app.route('/happy')
def happy():
    return render_template('predict.html')

@app.route('/predict', methods=['POST']) 
def predict():
    quarter = int(request.form['Quarter'])

    # Map department to numerical values
    department = request.form['Department'].lower()
    if department == 'sewing':
        department = 1
    elif department == 'finishing':
        department = 0
    else:
        department = -1  # Handle unexpected input

    # Map day to numerical values
    day = request.form['Day of the week'].lower()
    day_map = {
        'monday': 0,
        'tuesday': 4,
        'wednesday': 5,
        'thursday': 3,
        'friday': 6,
        'saturday': 1,
        'sunday': 2
    }
    day = day_map.get(day, -1)  # Use -1 for unexpected input

    # Convert remaining form inputs to integers
    team_number = int(request.form['Team Number'])
    time_allocated = int(request.form['Time Allocated'])
    unfinished_items = int(request.form['Unfinished Items'])
    over_time = int(request.form['Over time'])
    incentive = int(request.form['Incentive'])
    idle_time = int(request.form['Idle Time'])
    idle_men = int(request.form['Idle Men'])
    style = int(request.form['Style Change'])
    workers = int(request.form['Number of Workers'])

    # Create a DataFrame with the input data
    input_data = pd.DataFrame([[quarter, department, day, team_number, time_allocated, unfinished_items, over_time, incentive, idle_time, idle_men, style, workers]],
                              columns=['quarter', 'department', 'day', 'team_number', 'time_allocated', 'unfinished_items', 'over_time', 'incentive', 'idle_time', 'idle_men', 'style_change', 'no_of_workers'])

    # Make the prediction
    input_data=np.array(input_data)
    prediction = model.predict(input_data)

    # Format the prediction
    prediction = (np.round(prediction[0], 4)) * 100
    text="Hence,based on calculation, the predicted Garment worker is:"
    output = prediction
    print(output)
    return render_template('productivity1.html',prediction_text=text + str(output))

if __name__ == '__main__':
    app.run(debug=False,port=5000) 
