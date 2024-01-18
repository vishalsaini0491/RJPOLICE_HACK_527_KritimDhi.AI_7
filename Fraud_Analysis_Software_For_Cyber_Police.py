import numpy as np
import pickle
import streamlit as st
from sklearn.preprocessing import StandardScaler
from PIL import Image, ImageFilter
import requests

# initializing the StandardScaler Object
scaler = StandardScaler()

# loading our model file (model.sav) into this program
model = pickle.load(open('model.sav', 'rb'))

# loading scaler object file in the program
scaler = pickle.load(open('scaler.sav', 'rb'))

# function for prediction
def fraudPrediction(step, pay_type, amount, oldbalanceOrg, oldbalanceDest, isFlaggedFraud):
    input_data = np.array([[step, pay_type, amount, oldbalanceOrg, oldbalanceDest, isFlaggedFraud]])

    # transforming the ndarray values
    input_data_scaler = scaler.transform(input_data)

    # prediction part
    pred = model.predict(input_data_scaler)

    if pred == 0:
        return "**Normal Transaction**👍"
    else:
        return "**Fraud Transaction** ⚠️"


# About section
def about_section():
    st.header("Team Members")

    # Team member information
    team_members = [
        {"name": "Vishal Saini", "role": "", "college": "JECRC College",
         "image_url": r"./2.png"},
        {"name": "Raunak Kumari", "role": "", "college": "S.S. Jain Subodh Girls P.G. Mahila Maha Vidyalaya",
         "image_url":r"./1.png"},
    ]
    
    # Set the desired dimensions (half of the original dimensions)
    new_width = 150
    new_height = 150

    # Create two columns for team members
    col1, col2 = st.columns(2)

    def resize_image(image_path, new_width, new_height, interpolation=Image.LANCZOS):
     original_image = Image.open(image_path)
     resized_image = original_image.resize((new_width, new_height), resample=interpolation)
     return resized_image

    # Displaying information for the first team member
    col1.subheader(team_members[0]["name"])
    resized_image1 = resize_image(team_members[0]["image_url"], new_width, new_height, interpolation=Image.LANCZOS)
    col1.image(resized_image1, use_column_width=False)
    col1.write(f"{team_members[0]['role']}")
    col1.write(f"{team_members[0]['college']}")

    # Displaying information for the second team member
    col2.subheader(team_members[1]["name"])
    resized_image2 = resize_image(team_members[1]["image_url"], new_width, new_height, interpolation=Image.LANCZOS)
    col2.image(resized_image2, use_column_width=False)
    col2.write(f"{team_members[1]['role']}")
    col2.write(f"{team_members[1]['college']}")

# Navigation bar with About section
def create_navbar():
    st.markdown(
        """
        <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            padding: 1rem;
            background-color: #29B6F6;
            color: #ffffff;
            font-size: 1.2rem;
        }
        .navbar a {
            color: #ffffff;
            text-decoration: none;
            margin: 0 1rem;
        }
        </style>
        """
        , unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="navbar">
            <div>Kritimdhi.ai (RJPOLICE_HACK_527)</div>
            <div>
                <a href='#'>Home</a>
                <a href='#about'>Team</a>
            </div>
        </div>
        """
        , unsafe_allow_html=True
    )

# Main function
def main():
    # for wide look
    st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="वित्त सुरक्षा कवच", page_icon="🛡️")
    # about_section()
    create_navbar()


    html_temp = """
    <div style="background-color:#ffffff;padding:(0,0,0,0)">
    <br>
    <h1 style="color:#FF9800;text-align:center;">Financial Security Shield (वित्त सुरक्षा कवच)</h1>
    <br>
    </div>
    """

    st.markdown(html_temp, unsafe_allow_html=True)

    step = int(st.number_input('**Insert time ( 1 unit= 1 hrs)**'))
    payment_type = st.selectbox('**Payment Options?**', ('CASH_OUT', 'PAYMENT', 'CASH_IN', 'TRANSFER', 'DEBIT'))

    if payment_type == 'CASH_OUT':
        payment_type = int(5)
    elif payment_type == 'PAYMENT':
        payment_type = int(4)
    elif payment_type == 'CASH_IN':
        payment_type = int(3)
    elif payment_type == 'TRANSFER':
        payment_type = int(2)
    else:
        payment_type = int(1)

    amount = float(st.number_input('**Insert Amount :-**'))
    oldbalanceOrg = float(st.number_input('**What was sender old balance :-**'))
    oldbalanceDest = float(st.number_input('**What was receiver old balance :-**'))

    isFlaggedFraud = st.selectbox('**is transaction flagged fraud ?**', ('YES (1)', 'No (0)'))

    if isFlaggedFraud == 'YES (1)':
        isFlaggedFraud = int(1)
    else:
        isFlaggedFraud = int(0)

    # creating the object, for displaying the predicted string
    whichCategory = ''

    # button for prediction
    if st.button("**Predict**"):
        whichCategory = fraudPrediction(step, payment_type, amount, oldbalanceOrg, oldbalanceDest, isFlaggedFraud)

    st.success(whichCategory)
    
    st.markdown("<h2>Fraudulent Transactions Analysis And Their Investigation Status</h2>", unsafe_allow_html=True)
    st.markdown(
    """
    <style>
    .dashboard-container {
        display: flex;
        justify-content: flex-start;
    }
    .dashboard-iframe {
        margin-left: 0;
        width: 100%;
    }
    </style>
    <div class="dashboard-container">
        <iframe class="dashboard-iframe" title="hack" width="1568" height="744" 
        src="https://app.powerbi.com/reportEmbed?reportId=de818098-db7d-4bdb-910b-704e923692d9&autoAuth=true&ctid=e7564c33-eb36-434c-9646-b92ac5d17d51&hideBorder=true&navContentPaneEnabled=false" 
        frameborder="0" allowFullScreen="true"></iframe>
    </div>
    """,
    unsafe_allow_html=True
)


    # About section anchor
    st.markdown("<a id='about'></a>", unsafe_allow_html=True)
    
    
    # Display the About section
    about_section()


if __name__ == '__main__':
    main()
