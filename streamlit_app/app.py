import streamlit as st

from PIL import Image
import pandas as pd

from model import make_prediction


def show_main_page():
    image = Image.open('streamlit_app/images/money.png')
    st.set_page_config(
        layout='wide',
        initial_sidebar_state='auto',
        page_title='Credit Scoring',
        page_icon=image
    )

    t1, t2 = st.columns((0.13, 1))
    t1.image(image, width=120)
    t2.title('Machine learning service for predicting the risk of payment delinquency of a bank customer')


def get_age_group(age):
    if age < 21:
        return 1
    elif 21 <= age <= 34:
        return 2
    elif 35 <= age <= 49:
        return 3
    elif 50 <= age <= 64:
        return 4
    elif 65 <= age <= 100:
        return 5


def get_cred_group(num_of_creds):
    if num_of_creds <= 7:
        return 1
    elif 7 < num_of_creds <= 15:
        return 2
    elif 15 < num_of_creds <= 24:
        return 3
    elif 24 < num_of_creds <= 35:
        return 4
    elif num_of_creds > 35:
        return 5


def input_user_data():
    st.sidebar.header('Enter your information and find out if you will be granted credit!')
    age = st.sidebar.slider('Age', min_value=18, max_value=100, value=18, step=1)
    m_income = st.sidebar.text_input('Monthly income', value=1)
    m_expenses = st.sidebar.text_input('Monthly expenses', value=1)
    cred_rem = st.sidebar.text_input('Total credit balance', value=1)
    cred_lims = st.sidebar.text_input('The amount of credit limits', value=1)
    num_of_creds = st.sidebar.slider('Number of open loans', min_value=0, max_value=100, value=0, step=1)
    past_due_59 = st.sidebar.slider('How many times in the last 2 years have you been 30-59 days late on a loan?',
                                    min_value=0, max_value=25, value=0, step=1)
    past_due_89 = st.sidebar.slider('How many times in the last 2 years have you been 60-89 days late on a loan?',
                                    min_value=0, max_value=12, value=0, step=1)
    past_due_90 = st.sidebar.slider(
        'How many times in the last 2 years have you been more than 90 days late on a loan?',
        min_value=0, max_value=10, value=0, step=1)
    num_of_deps = st.sidebar.slider('Number of dependents (spouses, children, etc.)',
                                    min_value=0, max_value=30, value=0, step=1)

    age_group = get_age_group(age)
    cred_group = get_cred_group(num_of_creds)
    try:
        debt_ratio = float(m_expenses) / float(m_income)
        rev_util = float(cred_rem) / float(cred_lims)
    except ZeroDivisionError:
        rev_util, debt_ratio = 0, 0
        st.warning('Monthly income/expenses, loan balance and the amount of credit limits must be greater than 0.')

    data = {
        'RevolvingUtilizationOfUnsecuredLines': rev_util,
        'age': int(age),
        'NumberOfTime30-59DaysPastDueNotWorse': int(past_due_59),
        'DebtRatio': debt_ratio,
        'MonthlyIncome': float(m_income),
        'NumberOfOpenCreditLinesAndLoans': int(num_of_creds),
        'NumberOfTimes90DaysLate': int(past_due_90),
        'NumberOfTime60-89DaysPastDueNotWorse': int(past_due_89),
        'NumberOfDependents': int(num_of_deps),
        'RealEstateLoansOrLines': int(cred_group),
        'GroupAge': int(age_group)
    }
    df = pd.DataFrame(data, index=[0])

    st.write('## The data you entered:')
    st.write(df[[col for col in df.columns[:7]]])
    st.write(df[[col for col in df.columns[7:]]])

    return df


def wirte_prediction():
    df = input_user_data()
    if st.button('Predict!'):
        with st.spinner('Predicting...'):
            pred, prob = make_prediction(df)
            st.write('## Prediction:')
            st.write(f'### {pred}')
            st.write(f'Probability that you will be more than 90 days overdue is {round(prob, 2) * 100}%')


if __name__ == '__main__':
    show_main_page()
    wirte_prediction()
