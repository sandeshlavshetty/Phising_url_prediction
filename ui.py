# import streamlit as st
# import pickle
# import pandas as pd
# from extract import extract_features  # Adjust based on your file structure

# # Load the model from .pkl
# with open('xgboost_model.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)

# st.title("Phishing URL Detection")

# # Input for URL
# url = st.text_input("Enter URL for Analysis", "")

# # Button to extract features and predict
# if st.button("Analyze URL"):
#     if url:
#         # Extract features
#         features = extract_features(url)

#         # Display extracted features before handling missing values
#         st.subheader("Extracted Features")
#         st.write(features)

#         # List of expected features for model prediction
#         expected_features = [
#             'TLD_0', 'TLD_1', 'TLD_2', 'TLD_3', 'TLD_4', 'TLD_5', 'TLD_6', 'TLD_7', 'TLD_8', 'TLD_9', 
#             'LetterRatioInURL', 'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL', 'IsHTTPS', 
#             'LineOfCode', 'LargestLineLength', 'DomainTitleMatchScore', 'HasDescription', 'HasSocialNet', 
#             'HasSubmitButton', 'HasCopyrightInfo', 'NoOfImage', 'NoOfCSS', 'NoOfJS', 'NoOfSelfRef', 
#             'NoOfExternalRef'
#         ]

#         # Identify missing features
#         missing_features = [feature for feature in expected_features if feature not in features or features[feature] is None]

#         # Prompt user for missing values and collect inputs
#         if missing_features:
#             st.warning("Some features could not be extracted automatically. Please provide them manually:")
#             for feature in missing_features:
#                 features[feature] = st.number_input(f"Enter value for {feature}", min_value=0.0, format="%.2f")

#             # Recheck if all missing values are filled in
#             if any(features[feature] is None for feature in missing_features):
#                 st.warning("Please fill in all required missing features before proceeding.")
#             else:
#                 # Prepare data for prediction with the completed feature set
#                 feature_df = pd.DataFrame([{f: features.get(f, 0) for f in expected_features}])

#                 # Predict with the model
#                 prediction = model.predict(feature_df)

#                 # Display result
#                 if prediction[0] == 1:
#                     st.error("Warning: This URL is likely a phishing site!")
#                 else:
#                     st.success("This URL appears to be safe.")
#         else:
#             # Prepare data for prediction when no features are missing
#             feature_df = pd.DataFrame([{f: features.get(f, 0) for f in expected_features}])
#             prediction = model.predict(feature_df)

#             # Display result
#             if prediction[0] == 1:
#                 st.error("Warning: This URL is likely a phishing site!")
#             else:
#                 st.success("This URL appears to be safe.")
#     else:
#         st.error("Please enter a URL for analysis.")


import streamlit as st
import pickle
import pandas as pd
from extract import extract_features  # Adjust based on your file structure

# Load the model from .pkl
with open('xgboost_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

st.title("Phishing URL Detection")

# Input for URL
url = st.text_input("Enter URL for Analysis", "")

# Initialize session state to store features
if "features" not in st.session_state:
    st.session_state.features = {}

if st.button("Analyze URL"):
    if url:
        # Extract features
        extracted_features = extract_features(url)
        st.session_state.features.update(extracted_features)

        # Display extracted features before handling missing values
        st.subheader("Extracted Features")
        st.write(st.session_state.features)

        # List of expected features for model prediction
        expected_features = [
            'TLD_0', 'TLD_1', 'TLD_2', 'TLD_3', 'TLD_4', 'TLD_5', 'TLD_6', 'TLD_7', 'TLD_8', 'TLD_9', 
            'LetterRatioInURL', 'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL', 'IsHTTPS', 
            'LineOfCode', 'LargestLineLength', 'DomainTitleMatchScore', 'HasDescription', 'HasSocialNet', 
            'HasSubmitButton', 'HasCopyrightInfo', 'NoOfImage', 'NoOfCSS', 'NoOfJS', 'NoOfSelfRef', 
            'NoOfExternalRef'
        ]

        # Identify missing features
        missing_features = [feature for feature in expected_features if feature not in st.session_state.features or st.session_state.features[feature] is None]

        # Collect missing features manually
        if missing_features:
            st.warning("Some features could not be extracted automatically. Please provide them manually:")
            for feature in missing_features:
                st.session_state.features[feature] = st.number_input(f"Enter value for {feature}", min_value=0.0, format="%.2f")

            # Ensure all missing values are filled in
            if any(st.session_state.features[feature] is None for feature in missing_features):
                st.warning("Please fill in all required missing features before proceeding.")
                
            # Display extracted features before handling missing values
            st.subheader("Extracted Features Manual")
            st.write(st.session_state.features)
        else:
            # Prepare data for prediction if no features are missing
            feature_df = pd.DataFrame([{f: st.session_state.features.get(f, 0) for f in expected_features}])

            # Predict with the model
            prediction = model.predict(feature_df)
            print(prediction)
            # Display result
            if prediction[0] == 0:
                st.error("Warning: This URL is likely a phishing site!")
            else:
                st.success("This URL appears to be safe.")
    else:
        st.error("Please enter a URL for analysis.")
