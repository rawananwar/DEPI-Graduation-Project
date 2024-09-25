import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie

All_Customers_df = pd.read_csv("Notebooks/Preprocessing Notebooks/Final Sheets/All_Customers.csv")
All_Customers_Address_df = pd.read_csv("Notebooks/Preprocessing Notebooks/Final Sheets/All_Customers_Address.csv")
Transactions_df = pd.read_csv("Notebooks/Preprocessing Notebooks/Final Sheets/Transactions.csv")

st.set_page_config(page_title="Home Page", initial_sidebar_state='expanded')

st.image("pages/assets/Main/DEPI-Graduation-Project.jpg")

tab1,tab2 = st.tabs(["About Dataset", "Data Preparation"])
with tab1:
    st.markdown('''
    ##### The dataset provides information on bike store transactions for the year 2017 in Australia. The dataset contains sheets with valuable insights into customer demographics, addresses, and transactions.
                
    #### **Customer Demographic:**
    * Contains details about the customers' age, gender, Job, and other demographic information, helping us understand the customer base.
    * **Meta Data**:
    ''')
    Customers_Sheets = pd.DataFrame({
    'Column':['customer_id', 'first_name', 'last_name', 'gender', 'DOB', 'past_3_years_bike_related_purchases', 'job_title', 'job_industry_category', 'wealth_segment', 'deceased_indicator','owns_car', 'tenure'],
    'Datatype':['Number', 'Text', 'Text', 'Text', 'Date', 'Number', 'Text', 'Text', 'Text', 'Text', 'Text', 'Number'],
    'Description':['Unique identifier for customers (Primary Key)',
                    'Customer\'s first name',
                    'Customer\'s last name',
                    'Customer\'s gender',
                    'Customer\'s date of birth',
                    'Number of bike-related purchases in the last 3 years',
                    'Customer\'s job title',
                    'The industry category in which the customer works',
                    'Classification based on customer\'s wealth (Mass, Affluent, High Net Worth)',
                    'Indicates if the customer is deceased (Y for yes, N for no)',
                    'Indicates if the customer owns a car (yes or No)',
                    'The length of time (in years) the customer has been associated with store.']})
    st.dataframe(Customers_Sheets)

    with st.expander("Show Customers Sample Data"):
        st.dataframe(All_Customers_df.sample(10),use_container_width=True)
        st.write(f"###### Customers Dataframe Shape = **{All_Customers_df.shape}**")

    st.markdown('''     
    #### **Customer Address:**
    * Provides the geographical information for each customer, including address, state, and postal code, which can be useful for regional analysis and customer distribution.
    * **Meta Data**:
    ''')
    Customers_Address_Sheet = pd.DataFrame({
        'Column':['customer_id', 'address', 'postcode', 'state', 'country', 'property_valuation'],
        'Datatype':['Number', 'Text', 'Text', 'Text', 'Text', 'Number'],
        'Description':['Unique identifier for customers (Foreign Key).',
                    'The full address of the customer (street number and name).',
                    'The postal code associated with the customer\'s address.',
                    'The state where the customer resides (New South Wales, QLD, VIC).',
                    'The country of residence (Australia in this case).',
                    'A numeric value representing the property valuation rating (possibly on a scale of 1-12).']})
    st.dataframe(Customers_Address_Sheet)

    with st.expander("Show Customers Address Sample Data"):
        st.dataframe(All_Customers_Address_df.sample(10),use_container_width=True)
        st.write(f"###### Customers Address Dataframe Shape = **{All_Customers_Address_df.shape}**")

    st.markdown('''     
    #### **Transactions:**
    *  Contains transaction details such as transaction ID, date, product details, and total purchase amount, providing insights into customer purchasing behavior and store performance.

    * **Meta Data**:
    ''')
    Transactions_Sheet = pd.DataFrame({
        'Column':['transaction_id', 'product_id', 'customer_id', 'transaction_date', 'online_order', 'order_status', 'brand', 'product_line', 'product_class', 'product_size', 'list_price', 'standard_cost', 'product_first_sold_date'],
        'Datatype':['Number', 'Number', 'Number', 'Short date', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Currency', 'Currency', 'Date'],
        'Description':['A unique identifier for each transaction. (Primary key)',
                        'Identifies the product involved in the transaction.(Foreign Key)',
                        'Identifies the customer involved in the transaction.(Foreign Key)',
                        'The date when the transaction occurred.',
                        'Indicates whether the transaction was an online order (TRUE for online, FALSE for offline).',
                        'The status of the order (Approved, Cancelled).',
                        'The brand of the product involved in the transaction.',
                        'Specifies the product line, such as Road, Touring, Standard, or Mountain.',
                        'Classification of the product in terms of quality or level, such as high, medium, or low.',
                        'The size of the product, for example, large, medium, or small.',
                        'The product’s price at the time of the transaction.',
                        'The cost incurred by the company to produce or purchase the product.',
                        'Represents the date when the product was first sold.']})
    
    st.dataframe(Transactions_Sheet)
    
    with st.expander("Show Transactions Sample Data"):
        st.dataframe(Transactions_df.sample(10),use_container_width=True)
        st.write(f"###### Transactions Dataframe Shape = **{Transactions_df.shape}**")

with tab2:
    st.markdown('''
    #### **Data Preparation:**''')

    st.image("pages/assets/Main/Data Preparation process.png")

    st.markdown('''
    ##### **Problem 1: Invalid Data:**
    * **Gender:** The 'gender’ column had inconsistent values such as 'F', 'Femal', 'M', and ‘U’.
        * **Solution:** Standardized all values to 'Female', 'Male', and 'Unknown' to ensure consistency across the dataset.
    
    * **Unrealistic Age Values:** Some age values, such as 174, were clearly invalid and impacted data quality.
        * **Solution:** Deleted the rows containing these outlier values to maintain the accuracy of the dataset.
    
    * **Invalid Tenure for New Customers:** The tenure column had unrealistic values, like 15 or 9 years, for new customers.
        * **Solution:** Corrected these values by filling the tenure column with 0 for all new customers to reflect their accurate status.

    * **State Abbreviation:** The 'state' column contained both full state names and abbreviations, like 'NSW' and 'New South Wales’.
        * **Solution:** Replaced all abbreviations with full state names for consistency.
    
    * **Missing Customer IDs:** Certain customer IDs were found in the address table but were missing in the main customer table.
        * **Solution:** Removed these entries from the address table to ensure that all customer IDs in the dataset had corresponding records in the main table.

    ##### **Problem 2: Missing Values:**
    1. **Customers Table**
    * **Missing Last Names:** Some customer records had missing values in the last_name column, leading to incomplete customer names.
        * **Solution:** I created a new name column by concatenating the first_name and last_name columns.

    * **Missing Job Titles, Industry Categories, and Tenure:** Some records had missing values, creating data gaps.
        * **Solution:** I filled missing values in the job_title and job_industry_category columns with 'N/A' to indicate that this information was unavailable and filled the missing tenure values with 0.

    * **Missing Age values:** The age column had missing values in some customer records, making the data incomplete for analysis.
        * **Solution:** Applied the K-Nearest Neighbors (KNN) imputer method to fill in the missing age values. This method considers the 3 nearest neighbors based on the existing data and imputes the missing values with approximate values derived from similar customers.

    2. **Transactions Table**
    Several columns, including ***`brand`***, ***`product_line`***, ***`product_class`***, and ***`product_size`***, had missing values, leading to incomplete records in the dataset.

        * **Solution:** Systematically handled these missing values in two steps:
        1. **Fill missing categorical values with 'N/A’:**
        Used .fillna('N/A') to ensure that all missing categorical values are replaced with 'N/A' for consistency and better handling in analysis.

        2. **Fill missing numerical values in key columns using KNN Imputer:**
        Applied the KNN imputation method to fill the missing values in online_order, standard_cost, and product_first_sold_date. By leveraging the 3 nearest neighbors, missing values were imputed with the most approximate values based on the patterns in the data.
                ''')
    
    st.markdown(f"""
    <style>
        .hover-div {{
            padding: 10px;
            border-radius: 10px;
            background-color: #2c413c;
            margin-bottom: 10px;
            display: flex;
            justify-content: center;  /* Centers horizontally */
            align-items: center;  /* Centers vertically */
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;  /* Makes the div look clickable */
            text-decoration: none;  /* Remove underline from the text */
        }}
        .hover-div:hover {{
            background-color: #1e7460; /* Slightly lighter background color on hover */
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2); /* Adds a shadow on hover */
        }}
        h4 {{
            margin: 0; /* Remove any default margin */
            text-align: center; /* Center the text */
        }}
    </style>
    <a href="https://github.com/MohamedHossam606/DEPI-Graduation-Project/tree/main/Notebooks/Preprocessing%20Notebooks" target="_blank" class="hover-div">
        <h4 style="color: white;">View Full Data Preparation Notebooks</h4>
    </a>""", unsafe_allow_html=True)
st.divider()

st.write('## **Dashboard**')

images = [
    "pages/assets/Main/Dashboard/Bickes Store Visualization_page-0002.jpg",
    "pages/assets/Main/Dashboard/Bickes Store Visualization_page-0003.jpg",
    "pages/assets/Main/Dashboard/Bickes Store Visualization_page-0004.jpg"
]

# Custom CSS for modern button styles
st.markdown("""
    <style>
    .btn-style {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease-in-out;
    }
    .btn-style:hover {
        background-color: #45a049;
    }
    .slider-indicators {
        text-align: center;
        margin-top: 10px;
    }
    .slider-indicators span {
        height: 15px;
        width: 15px;
        margin: 0 5px;
        display: inline-block;
        background-color: #bbb;
        border-radius: 50%;
    }
    .slider-indicators .active {
        background-color: #717171;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for image index and auto-slide timer
if "carousel_index" not in st.session_state:
    st.session_state.carousel_index = 0


# Display the current image
st.image(images[st.session_state.carousel_index], width=700)

# Navigation buttons (Previous/Next)
prev, _, next = st.columns([1, 10, 1])

# Handle the previous button click
if prev.button("◀", key="prev", help="Previous image", type="primary"):
    st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(images)

# Handle the next button click
if next.button("▶", key="next", help="Next image", type="primary"):
    st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(images)

# Extra description or metadata
st.write(f"Image {st.session_state.carousel_index + 1} of {len(images)}")

st.markdown(f"""
    <style>
        .hover-div {{
            padding: 10px;
            border-radius: 10px;
            background-color: #2c413c;
            margin-bottom: 10px;
            display: flex;
            justify-content: center;  /* Centers horizontally */
            align-items: center;  /* Centers vertically */
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;  /* Makes the div look clickable */
            text-decoration: none;  /* Remove underline from the text */
        }}
        .hover-div:hover {{
            background-color: #1e7460; /* Slightly lighter background color on hover */
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2); /* Adds a shadow on hover */
        }}
        h4 {{
            margin: 0; /* Remove any default margin */
            text-align: center; /* Center the text */
        }}
    </style>
    <a href="https://app.powerbi.com/links/sgzZ23FXw_?ctid=878ae732-59c5-40e3-8d49-91e7988bccfd&pbi_source=linkShare" target="_blank" class="hover-div">
        <h4 style="color: white;">View Dashboard</h4>
    </a>""", unsafe_allow_html=True)

# Load the Lottie animation from the URL
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# animation = load_lottieurl('https://lottie.host/af744217-f85d-455c-8dd5-0c8bd672c6a8/CajIat0YS0.json')
# if animation is not None:
#     st_lottie(animation, speed=0.80, quality='high',  height=200)
# else:
#     st.error("Animation failed to load.")

st.divider()

st.write('## **Presentation**')
st.markdown(f"""
    <style>
        .hover-div {{
            padding: 10px;
            border-radius: 10px;
            background-color: #2c413c;
            margin-bottom: 10px;
            display: flex;
            justify-content: center;  /* Centers horizontally */
            align-items: center;  /* Centers vertically */
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;  /* Makes the div look clickable */
            text-decoration: none;  /* Remove underline from the text */
        }}
        .hover-div:hover {{
            background-color: #1e7460; /* Slightly lighter background color on hover */
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2); /* Adds a shadow on hover */
        }}
        h4 {{
            margin: 0; /* Remove any default margin */
            text-align: center; /* Center the text */
        }}
    </style>
    <a href="https://drive.google.com/drive/folders/1TL_3geXkXLWuHkv0V8MHhyG0jTeUY3c_?usp=sharing" target="_blank" class="hover-div">
        <h4 style="color: white;">View Our Presentation</h4>
    </a>""", unsafe_allow_html=True)
