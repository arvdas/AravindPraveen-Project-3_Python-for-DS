from flask import Flask, render_template, request, jsonify, redirect
import pandas as pd
import pickle

app = Flask(__name__)


with open('loan_status_model.pkl', 'rb') as f:
    model = pickle.load(f)

users_db = {
    1: {'username': 'user1', 'password': 'password1'},
    2: {'username': 'user2', 'password': 'password2'}
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():

    username = request.form.get('username')
    password = request.form.get('password')


    new_user_id = len(users_db) + 1
    users_db[new_user_id] = {'username': username, 'password': password}

    return jsonify({'message': 'Registration successful!'})


@app.route('/login', methods=['POST'])
def login():

    username = request.form.get('username')
    password = request.form.get('password')


    for user_id, user_info in users_db.items():
        if user_info['username'] == username and user_info['password'] == password:
            return jsonify({'message': 'Login successful!'})

    return jsonify({'message': 'Invalid credentials. Please try again.'})


@app.route('/enter_details')
def enter_details():
    return render_template('predict.html')


@app.route('/predict', methods=['POST'])
def predict( ):

    gender = request.form.get('gender')
    married = request.form.get('married')
    dependents = request.form.get('dependents')
    self_employed = request.form.get('selfEmployed')
    education = request.form.get('education')
    applicant_income = float(request.form.get('applicantIncome'))
    coapplicant_income = float(request.form.get('coApplicantIncome'))
    loan_amount = float(request.form.get('loanAmount'))
    loan_amount_term = float(request.form.get('loanAmountTerm'))
    credit_history = int(request.form.get('creditHistory'))
    property_area = request.form.get('propertyArea')


    gender_encoded = label_encoder.transform([gender])[0]
    married_encoded = label_encoder.transform([married])[0]
    dependents_encoded = label_encoder.transform([dependents])[0]
    self_employed_encoded = label_encoder.transform([self_employed])[0]
    education_encoded = label_encoder.transform([education])[0]
    property_area_encoded = label_encoder.transform([property_area])[0]


    user_input = pd.DataFrame({
        'Gender': [gender_encoded],
        'Married': [married_encoded],
        'Dependents': [dependents_encoded],
        'Self employed': [self_employed_encoded],
        'Education': [education_encoded],
        'Applicant Income': [applicant_income],
        'Co Applicant Income': [coapplicant_income],
        'Loan Amount': [loan_amount],
        'Loan Amount Term': [loan_amount_term],
        'Credit History': [credit_history],
        'Property area': [property_area_encoded]
    })


    prediction = model.predict(user_input)[0]


    eligibility = 'Approved' if prediction == 1 else 'Not Approved'

    return jsonify({'eligibility': eligibility})


@app.route('/logout')
def logout():

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
