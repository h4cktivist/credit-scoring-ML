# 🤖 Machine learning service for predicting the risk of payment delinquency of a bank customer
The project was created as part of the ["ML Service Development: From Idea to MVP"](https://stepik.org/course/176820/promo) (RU) course, run by the team of online master's programme ["Machine Learning and Data-Intensive Systems"](https://www.hse.ru/en/ma/mlds/) of the Faculty of Computer Science of the Higher School of Economics.

[_Dataset_](https://github.com/evgpat/stepik_from_idea_to_mvp/blob/main/datasets/credit_scoring.csv) |
[_Model file_](https://drive.google.com/uc?export=download&id=13TLGYSEBtBiS179Vlmtq0lyXVdWelLvr) |
[_Streamlit web-application_](https://credit-scoring-ml.streamlit.app/)
## 📂 Files
- `Credit_scoring.ipynb`: the main Jupyter Notebook of the project, in which data analysis and model building were conducted
- `streamlit_app/app.py`: Streamlit application main file to run the web interface of the model
- `streamlit_app/model.py`: a script in which the model is loaded and the target variable is predicted

## ⚙️ Technologies
- _Pandas_ and _NumPy_ libraries were used for data processing.
- Data analysis and graphing were performed using the _Matplotlib_ and _Seaborn_ libraries.
- The _scikit-learn_ library was used for machine learning, and in particular:
  - the _RandomForestClassifier_ classification model
  - the _RandomizedSearchCV_ method for finding the optimal hyperparameters of the model
  - methods for key model metrics estimating
  - the _MinMaxScaler_ method for features scaling
- The _pickle_ library was used to save the model.
- Using the _Streamlit_ framework, a web service was created to interact with the model.

## 💻 Local run
To start the web interface, install the requirements and run the `app.py` file using the `streamlit` tool:
```sh
pip install -r requirements.txt
streamlit run ./streamlit_app/app.py
```
The application will then be available at http://localhost:8501/
