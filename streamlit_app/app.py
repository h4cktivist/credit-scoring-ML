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
    t2.title('Модель машинного обучения для прогнозирования риска просрочки у клиента некоторого банка')


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
    st.sidebar.header('Введите данные о Вас и узнайте, будет ли Вам выдан кредит!')
    age = st.sidebar.slider('Возраст', min_value=18, max_value=100, value=18, step=1)
    m_income = st.sidebar.text_input('Доход в месяц', value=1)
    m_expenses = st.sidebar.text_input('Ежемесячные расходы', value=1)
    cred_rem = st.sidebar.text_input('Общий остаток по кредитам', value=1)
    cred_lims = st.sidebar.text_input('Сумма размеров лимитов по кредитам', value=1)
    num_of_creds = st.sidebar.slider('Кол-во открытых кредитов', min_value=0, max_value=100, value=0, step=1)
    past_due_59 = st.sidebar.slider('Сколько раз за последние 2 года Вы задержали выплату по кредиту на 30-59 дней?',
                                    min_value=0, max_value=25, value=0, step=1)
    past_due_89 = st.sidebar.slider('Сколько раз за последние 2 года Вы задержали выплату по кредиту на 60-89 дней?',
                                    min_value=0, max_value=12, value=0, step=1)
    past_due_90 = st.sidebar.slider(
        'Сколько раз за последние 2 года Вы задержали выплату по кредиту более, чем на 90 дней?',
        min_value=0, max_value=10, value=0, step=1)
    num_of_deps = st.sidebar.slider('Кол-во иждивенцев на попечении (супруги, дети и др.)',
                                    min_value=0, max_value=30, value=0, step=1)

    age_group = get_age_group(age)
    cred_group = get_cred_group(num_of_creds)
    debt_ratio = float(m_expenses) / float(m_income)
    rev_util = float(cred_rem) / float(cred_lims)

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

    st.write('## Ваши данные:')
    st.write(df[[col for col in df.columns[:7]]])
    st.write(df[[col for col in df.columns[7:]]])

    return df


def wirte_prediction():
    df = input_user_data()
    if st.button('Предсказать!'):
        with st.spinner('Предсказываем...'):
            pred, prob = make_prediction(df)
            st.write('## Предсказание:')
            st.write(f'### {pred}')
            st.write(f'Вероятность того, что Вы просрочите выплату на более, чем 90 дней: {round(prob, 2) * 100}%')


if __name__ == '__main__':
    show_main_page()
    wirte_prediction()
