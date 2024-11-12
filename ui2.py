import streamlit as st
import pickle
import pandas as pd

# Load the model from .pkl
with open('xgboost_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

st.title("Phishing URL Detection")

# Display form for manual input of all features
with st.form("feature_input_form"):
    st.subheader("Input Features for Analysis")

    # TLD features
    TLD_0 = st.number_input("TLD_0", min_value=0.0, format="%.1f", value=0.0)
    TLD_1 = st.number_input("TLD_1", min_value=0.0, format="%.1f", value=0.0)
    TLD_2 = st.number_input("TLD_2", min_value=0.0, format="%.1f", value=0.0)
    TLD_3 = st.number_input("TLD_3", min_value=0.0, format="%.1f", value=0.0)
    TLD_4 = st.number_input("TLD_4", min_value=0.0, format="%.1f", value=0.0)
    TLD_5 = st.number_input("TLD_5", min_value=0.0, format="%.1f", value=0.0)
    TLD_6 = st.number_input("TLD_6", min_value=0.0, format="%.1f", value=0.0)
    TLD_7 = st.number_input("TLD_7", min_value=0.0, format="%.1f", value=0.0)
    TLD_8 = st.number_input("TLD_8", min_value=0.0, format="%.1f", value=0.0)
    TLD_9 = st.number_input("TLD_9", min_value=0.0, format="%.1f", value=1.0)

    # Other URL-related features
    LetterRatioInURL = st.number_input("LetterRatioInURL", min_value=0.0, max_value=1.0, format="%.5f", value=0.72093)
    NoOfOtherSpecialCharsInURL = st.number_input("NoOfOtherSpecialCharsInURL", min_value=0, format="%d", value=10)
    SpacialCharRatioInURL = st.number_input("SpacialCharRatioInURL", min_value=0.0, max_value=1.0, format="%.5f", value=0.23256)
    IsHTTPS = st.number_input("IsHTTPS", min_value=0, max_value=1, format="%d", value=1)

    # HTML content-related features
    LineOfCode = st.number_input("LineOfCode", min_value=0, format="%d", value=88)
    LargestLineLength = st.number_input("LargestLineLength", min_value=0, format="%d", value=463750)
    DomainTitleMatchScore = st.number_input("DomainTitleMatchScore", min_value=0.0, max_value=1.0, format="%.2f", value=0.0)
    HasDescription = st.number_input("HasDescription", min_value=0, max_value=1, format="%d", value=1)
    HasSocialNet = st.number_input("HasSocialNet", min_value=0, max_value=1, format="%d", value=0)
    HasSubmitButton = st.number_input("HasSubmitButton", min_value=0, max_value=1, format="%d", value=0)
    HasCopyrightInfo = st.number_input("HasCopyrightInfo", min_value=0, max_value=1, format="%d", value=1)

    # Resources on the webpage
    NoOfImage = st.number_input("NoOfImage", min_value=0, format="%d", value=0)
    NoOfCSS = st.number_input("NoOfCSS", min_value=0, format="%d", value=6)
    NoOfJS = st.number_input("NoOfJS", min_value=0, format="%d", value=50)
    NoOfSelfRef = st.number_input("NoOfSelfRef", min_value=0, format="%d", value=25)
    NoOfExternalRef = st.number_input("NoOfExternalRef", min_value=0, format="%d", value=30)

    # Submit button
    submit_button = st.form_submit_button("Analyze")

# Perform prediction if form is submitted
if submit_button:
    # Collect features into a dictionary
    features = {
        'TLD_0': TLD_0, 'TLD_1': TLD_1, 'TLD_2': TLD_2, 'TLD_3': TLD_3, 'TLD_4': TLD_4, 
        'TLD_5': TLD_5, 'TLD_6': TLD_6, 'TLD_7': TLD_7, 'TLD_8': TLD_8, 'TLD_9': TLD_9, 
        'LetterRatioInURL': LetterRatioInURL, 'NoOfOtherSpecialCharsInURL': NoOfOtherSpecialCharsInURL, 
        'SpacialCharRatioInURL': SpacialCharRatioInURL, 'IsHTTPS': IsHTTPS, 'LineOfCode': LineOfCode, 
        'LargestLineLength': LargestLineLength, 'DomainTitleMatchScore': DomainTitleMatchScore, 
        'HasDescription': HasDescription, 'HasSocialNet': HasSocialNet, 'HasSubmitButton': HasSubmitButton, 
        'HasCopyrightInfo': HasCopyrightInfo, 'NoOfImage': NoOfImage, 'NoOfCSS': NoOfCSS, 
        'NoOfJS': NoOfJS, 'NoOfSelfRef': NoOfSelfRef, 'NoOfExternalRef': NoOfExternalRef
    }

    # Convert to DataFrame
    feature_df = pd.DataFrame([features])

    # Predict with the model
    prediction = model.predict(feature_df)

    # Display result
    if prediction[0] == 0:
        st.error("Warning: This URL is likely a phishing site!")
    else:
        st.success("This URL appears to be safe.")
