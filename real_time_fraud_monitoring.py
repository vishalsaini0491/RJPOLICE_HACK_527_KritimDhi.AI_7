import numpy as np
import pickle
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from datetime import datetime

# Load the model and scaler
model = pickle.load(open('model.sav', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

# Check if the fraud_alerts.csv file exists, if not create it
try:
    fraud_alert_data = pd.read_csv("fraud_alerts.csv")
except FileNotFoundError:
    fraud_alert_data = pd.DataFrame(columns=["Sender_Account", "Receiver_Account", "Amount", "Payment_Type", "Old_Balance_Sender", "Old_Balance_Receiver"])

# Function for prediction and transaction handling
def handle_transaction(sender_account, receiver_account, sender_balance, receiver_balance, step, payment_type, amount, isFlaggedFraud):
    input_data = np.array([[step, payment_type, amount, sender_balance, receiver_balance, isFlaggedFraud]])

    # Transforming the ndarray values
    input_data_scaler = scaler.transform(input_data)

    # Prediction part
    pred = model.predict(input_data_scaler)

    if pred == 0:
        # Normal Transaction
        return "**Normal Transaction**👍"
    else:
        # Fraud Transaction
        # Create alert message for fraud transactions
        alert_message = f"Fraud Alert: Suspicious transaction involving {amount} from {sender_account} to {receiver_account}."

        # Save the fraudulent alert data to CSV file
        fraud_alert_data.loc[len(fraud_alert_data)] = [sender_account, receiver_account, amount, payment_type, sender_balance, receiver_balance]
        fraud_alert_data.to_csv("fraud_alerts.csv", index=False)

        return alert_message

def main():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Kritimdhi.ai Online Banking Services Simulation")

    html_temp = """
    <div style="background-color:#ffffff;padding:(0,0,0,0)">
    <br>
    <h1 style="color:#FF9800;text-align:center;">Kritimdhi.ai Online Banking Services Simulation</h1>
    <br>
    </div>
    """

    st.markdown(html_temp, unsafe_allow_html=True)

    # User account selection
    st.subheader("Select Sender and Receiver Accounts:")
    sender_account = st.selectbox("Sender Account:", ["Cyber Police Rajasthan", "Kritimdhi.ai"])
    receiver_account = st.selectbox("Receiver Account:", ["Cyber Police Rajasthan", "Kritimdhi.ai"])

    # Hypothetical balance input
    st.subheader("Hypothetical Balance:")
    sender_balance = st.number_input(f"Balance for {sender_account} (oldbalanceOrg):", min_value=0.0)
    receiver_balance = st.number_input(f"Balance for {receiver_account} (oldbalanceDest):", min_value=0.0)

    # Transaction input
    st.subheader("Transaction Details:")
    step = st.number_input('Insert time (1 unit = 1 hr):', value=int(datetime.now().hour))
    payment_type = st.selectbox('Payment Options?', ('CASH_OUT', 'PAYMENT', 'CASH_IN', 'TRANSFER', 'DEBIT'))
    
    if payment_type == 'CASH_OUT':
        payment_type = 5
    elif payment_type == 'PAYMENT':
        payment_type = 4
    elif payment_type == 'CASH_IN':
        payment_type = 3
    elif payment_type == 'TRANSFER':
        payment_type = 2
    else:
        payment_type = 1

    amount = st.number_input('Insert Transaction Amount:')
    
    isFlaggedFraud = st.selectbox('**Is transaction flagged fraud ?**', ('YES (1)', 'No (0)'))

    if isFlaggedFraud == 'YES (1)':
        isFlaggedFraud = int(1)
    else:
        isFlaggedFraud = int(0)

    # Prediction and Transaction
    if st.button("Initiate Transaction"):
        prediction_result = handle_transaction(sender_account, receiver_account, sender_balance, receiver_balance, step, payment_type, amount, isFlaggedFraud)
        st.success(prediction_result)

        # Check if the prediction is fraud, stop the transaction
        if "Fraud Alert" in prediction_result:
            st.warning("Transaction is flagged as Fraud. Transaction stopped. Needs Review.")
            return

        # Deduct or Add money based on pay_type
        if payment_type == 2:  # Transfer
            sender_balance -= amount
            receiver_balance += amount
        elif payment_type == 3:  # Cash-In
            sender_balance -= amount
            receiver_balance += amount
        elif payment_type == 4:  # Payment
            sender_balance -= amount
            receiver_balance += amount
        elif payment_type == 5:  # Cash-Out
            sender_balance -= amount
            receiver_balance += amount

        st.write(f"Transaction Successful! Updated Balances - {sender_account}: {sender_balance}, {receiver_account}: {receiver_balance}")

    # Button to check balances after transaction
    if st.button("Check Balances"):
        st.write(f"Balances - {sender_account}: {sender_balance}, {receiver_account}: {receiver_balance}")

    if st.button("Reset Simulation"):
        st.success("Simulation Reset Successfully!")

if __name__ == '__main__':
    main()
