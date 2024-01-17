import numpy as np
import pickle
import streamlit as st
from sklearn.preprocessing import StandardScaler
from datetime import datetime


scaler = StandardScaler()

# loading our model file (model.sav) into this program
model = pickle.load(open('model.sav', 'rb'))

# loading scaler object file in the program
scaler = pickle.load(open('scaler.sav', 'rb'))

# Function for prediction
def fraudPrediction(step, pay_type, amount, oldbalanceOrg, oldbalanceDest, isFlaggedFraud):
    input_data = np.array([[step, pay_type, amount, oldbalanceOrg, oldbalanceDest, isFlaggedFraud]])

    # Transforming the ndarray values
    input_data_scaler = scaler.transform(input_data)

    # Prediction part
    pred = model.predict(input_data_scaler)

    if pred == 0:
        return "**Normal Transaction**👍"
    else:
        return "**Fraud Transaction** ⚠️"


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
        prediction_result = fraudPrediction(step, payment_type, amount, sender_balance, receiver_balance, isFlaggedFraud)
        st.success(prediction_result)

        # Check if the prediction is fraud, stop the transaction
        if "**Fraud Transaction** ⚠️" in prediction_result:
            st.warning("Transaction is flagged as Fraud. Transaction stopped.")
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
