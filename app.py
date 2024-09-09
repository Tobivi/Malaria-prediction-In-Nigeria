import streamlit as st
import pickle
from PIL import Image
import matplotlib.pyplot as plt

st.title("Malaria Prediction in Nigeria")
image = Image.open('Medicine-Higher-Life-Foundation.jpg')
st.image(image, caption='Malaria Prediction', use_column_width=True)

st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #f5f5f5;
    padding: 20px;
    font-family: Arial, sans-serif;
}
.sidebar .sidebar-header {
    font-size: 1.5em;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Input Parameters")
    st.markdown("""
    **Pregnancies:** The number of times the individual has been pregnant.
    
    **Treated Net:** Availability of treated nets (Yes/No).
    
    **Environment Sanitization:** Is the environment sanitized (Yes/No)?
    
    **Laboratory Equipments:** Adequate or not?
    
    **Location:** Urban or Rural?
    
    **Lab Diagnosis:** Complicated or Uncomplicated (based on malaria parasite density).
    
    **Additional Inputs:** Includes numerical values for various parameters.
    """)
    
    st.write("**Developed by:** Temitope Atoyebi")

pickle_in = open('Multinomial2.pkl', 'rb')
classifier = pickle.load(pickle_in)

Name = st.text_input("Name")
Pregnancies = st.number_input("The amount of times the individual got pregnant:")
Availaibility_of_treated_net = st.selectbox("Were treated nets available?", ['No', 'Yes'])
Season_Level_of_Rainfall_Stagnant_water_breeding = st.number_input("The level of rainfall")
High_Rate_of_Mal_Infection_Lab_Diagnosis = st.number_input("The high rate of malaria infection (Lab diagnosis)")
Malaria_Parasite_Density_Fever_Rapid_Diagnostic_TestStrip = st.number_input("The malaria Parasite Density fever rapid diagnostic")
Complaints_Symptoms = st.number_input("The complaints or symptoms of the individual")
Age = st.number_input("The age of the individual")
Electricity = st.selectbox('Was there availability of electricity?', ['No', 'Yes'])
Environment_Sanitised_or_not = st.selectbox("Is the environment sanitized or not", ['Yes', 'No'])
Doctor_to_Patient = st.selectbox("Doctor to patient", ['High', 'Low'])
Laboratory_Equipments = st.selectbox("Laboratory Equipments", ['Not Adequate', 'Adequate'])
Location = st.selectbox("Location (Urban or Rural)", ['Urban', 'Rural'])
Complicated_Uncomplicated_Lab_Diagnosis = st.selectbox("Lab Diagnosis (Complicated or Uncomplicated)", ['Uncomplicated', 'Complicated'])
submit = st.button("Predict")

if submit:
    input_data = [Pregnancies, Availaibility_of_treated_net, Season_Level_of_Rainfall_Stagnant_water_breeding,
                  High_Rate_of_Mal_Infection_Lab_Diagnosis, Complaints_Symptoms, Age, Electricity,
                  Environment_Sanitised_or_not, Doctor_to_Patient, Laboratory_Equipments,
                  Malaria_Parasite_Density_Fever_Rapid_Diagnostic_TestStrip, Location, Complicated_Uncomplicated_Lab_Diagnosis]

    input_data[1] = 1 if Availaibility_of_treated_net == 'Yes' else 0
    input_data[8] = 1 if Doctor_to_Patient == 'High' else 0
    input_data[9] = 1 if Laboratory_Equipments == 'Adequate' else 0
    input_data[7] = 0 if Environment_Sanitised_or_not == "No" else 1
    input_data[11] = 1 if Location == "Urban" else 0
    input_data[-1] = 1 if Complicated_Uncomplicated_Lab_Diagnosis == "Complicated" else 0
    input_data[6] = 1 if Electricity == 'Yes' else 0

    prediction = classifier.predict([input_data])

    if prediction == 0:
        st.write(f'Congratulations, {Name}, you do not have malaria.')
        st.write("Hence the Lab Diagnosis states that the malaria you have is Uncomplicated, indicating it's less than 70%")

        fig, ax = plt.subplots()
        ax.bar(["Malaria Negative", "Malaria Positive"], [1, 0], color=['#4CAF50', '#F44336'])
        ax.set_ylabel('Prediction')
        ax.set_title('Malaria Prediction Result')
        st.pyplot(fig)
    else:
        st.write(f'{Name}, we are really sorry to say, but it seems like you have malaria.')
        st.write("Hence the Lab Diagnosis states that the malaria you have is Complicated, indicating it's greater than 70%")

        fig, ax = plt.subplots()
        ax.bar(["Malaria Negative", "Malaria Positive"], [0, 1], color=['#4CAF50', '#F44336'])
        ax.set_ylabel('Prediction')
        ax.set_title('Malaria Prediction Result')
        st.pyplot(fig)
