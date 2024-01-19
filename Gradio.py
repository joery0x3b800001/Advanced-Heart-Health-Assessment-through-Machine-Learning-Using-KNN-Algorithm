# -*- coding: utf-8 -*-
"""Gradio.ipynb

Automatically generated by Colaboratory.

"""

"""#KNN


"""

import warnings
import os
warnings.filterwarnings('ignore')
import numpy as np
from scipy import stats
import concurrent.futures
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score
import gradio as gr
import pandas as pd
from io import StringIO
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

algorithms = ["Logistic Regression", "KNN", "SVC", "Random Forest", "Gradient Boosting", "All"]

df = pd.read_csv('/content/heart.csv')
test_data = pd.read_csv('/content/test.csv');
#Drop the partient_id
df.drop(columns=['Patient_ID'], inplace=True)

# Separating features from the target we want to predict
X = df.drop('HeartDisease', axis=1)
y = df['HeartDisease']

# Performing one-hot encoding for the categorical features
X = pd.get_dummies(X, drop_first=True)

# Splitting our data into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

# Standard scaling
scaler = StandardScaler()
st_scaled_X_train = scaler.fit_transform(X_train)
st_scaled_X_test = scaler.transform(X_test)

# Normal scaling
scaler = MinMaxScaler()
normal_scaled_X_train = scaler.fit_transform(X_train)
normal_scaled_X_test = scaler.transform(X_test)

# Storing out three types of data
X_train_datasets = [X_train, st_scaled_X_train, normal_scaled_X_train]
X_test_datasets = [X_test, st_scaled_X_test, normal_scaled_X_test]

def knn():
    knn = KNeighborsClassifier(n_neighbors=24, weights='distance')
    knn = knn.fit(st_scaled_X_train, y_train)

    predictions_knn = knn.predict(st_scaled_X_test)

    knn_scores = []

    knn_scores.append( score(y_test, predictions_knn, average='weighted')[0] )
    knn_scores.append( score(y_test, predictions_knn, average='weighted')[1] )
    knn_scores.append( score(y_test, predictions_knn, average='weighted')[2] )
    knn_scores.append( accuracy_score(y_test, predictions_knn) )

    df_knn = pd.DataFrame(knn_scores, columns=['knn'],
                index=['Precision', 'Recall', 'f1_score', 'Accuracy'])

    df_knn['knn'] = np.round(df_knn['knn'], 3)

    return df_knn

"""#Logistic Regression"""

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV

def logistic_reg():
    # Setting up our three logistic regression models.

    lr = LogisticRegression(solver='liblinear')
    lr_l1 = LogisticRegressionCV(Cs=10, cv=5, penalty='l1', solver='liblinear')
    lr_l2 = LogisticRegressionCV(Cs=10, cv=5, penalty='l2', solver='liblinear')

    models = [lr, lr_l1, lr_l2]
    precision = []
    recall = []
    f1_score = []
    accuracy = []

    for X_train_data, X_test_data in zip(X_train_datasets, X_test_datasets):
        for model in models:

            model.fit(X_train_data, y_train)

            predictions = model.predict(X_test_data)

            precision.append( score(y_test, predictions, average='weighted')[0] )
            recall.append( score(y_test, predictions, average='weighted')[1] )
            f1_score.append( score(y_test, predictions, average='weighted')[2] )
            accuracy.append( accuracy_score(y_test, predictions) )
    scores = [precision, recall, f1_score, accuracy]

    df_lr = round(pd.DataFrame(scores,
                index=['Precision', 'Recall', 'f1_score', 'Accuracy'],
                columns=['lr', 'lr_l1', 'lr_l2',
                        'lr_st', 'lr_l1_st', 'lr_l2_st',
                        'lr_normal', 'lr_l1_normal', 'lr_l2_normal']), 3)

    # Our chosen logistic regression model
    # And trained on data without scaling

    lr = LogisticRegression(solver='liblinear').fit(X_train, y_train)
    predictions_lr = lr.predict(X_test)

    # Storing the scores

    df_lr = df_lr['lr'].to_frame()
    return df_lr

"""#SVC"""

from sklearn.svm import SVC

def svc():
    svc = SVC()
    svc = svc.fit(st_scaled_X_train, y_train)

    predictions_svc = svc.predict(st_scaled_X_test)

    svc_scores = []

    svc_scores.append( score(y_test, predictions_svc, average='weighted')[0] )
    svc_scores.append( score(y_test, predictions_svc, average='weighted')[1] )
    svc_scores.append( score(y_test, predictions_svc, average='weighted')[2] )
    svc_scores.append( accuracy_score(y_test, predictions_svc) )

    df_svc = pd.DataFrame(svc_scores, columns=['svc'],
                index=['Precision', 'Recall', 'f1_score', 'Accuracy'])

    df_svc['svc'] = np.round(df_svc['svc'], 3)

    return df_svc

"""#Random Forest"""

from sklearn.ensemble import RandomForestClassifier

RF = RandomForestClassifier(oob_score=True,
                            random_state=42,
                            warm_start=True,
                            n_jobs=-1)

def random_forest():
    rf = RF.set_params(n_estimators=100, warm_start=False)
    rf = rf.fit(X_train, y_train)

    predictions_rf = rf.predict(X_test)

    rf_scores = []

    rf_scores.append( score(y_test, predictions_rf, average='weighted')[0] )
    rf_scores.append( score(y_test, predictions_rf, average='weighted')[1] )
    rf_scores.append( score(y_test, predictions_rf, average='weighted')[2] )
    rf_scores.append( accuracy_score(y_test, predictions_rf) )

    df_rf = pd.DataFrame(rf_scores, columns=['rf'],
                index=['Precision', 'Recall', 'f1_score', 'Accuracy'])

    df_rf['rf'] = np.round(df_rf['rf'], 3)

    return df_rf

"""#Gradient Boosting"""

from sklearn.ensemble import GradientBoostingClassifier

def gradient_boosting():
    gb = GradientBoostingClassifier(n_estimators=30, random_state=42)
    gb = gb.fit(X_train, y_train)

    predictions_gb = gb.predict(X_test)

    gb_scores = []

    gb_scores.append( score(y_test, predictions_gb, average='weighted')[0] )
    gb_scores.append( score(y_test, predictions_gb, average='weighted')[1] )
    gb_scores.append( score(y_test, predictions_gb, average='weighted')[2] )
    gb_scores.append( accuracy_score(y_test, predictions_gb) )

    df_gb = pd.DataFrame(gb_scores, columns=['gb'],
                index=['Precision', 'Recall', 'f1_score', 'Accuracy'])

    df_gb['gb'] = np.round(df_gb['gb'], 3)

    return df_gb

def all():
    return pd.concat([logistic_reg(), knn(), svc(), random_forest(), gradient_boosting()], axis=1)

max_acc_lr = logistic_reg()['lr'].values[3]
max_acc_knn = knn()['knn'].values[3]
max_acc_svc = svc()['svc'].values[3]
max_acc_rf = random_forest()['rf'].values[3]
max_acc_gb = gradient_boosting()['gb'].values[3]

simple = pd.DataFrame(
    {
        "Algorithms": ["KNN", "Logistic Regression", "SVC", "Random Forest", "Gradient Boosting"],
        "Accuracy": [max_acc_knn, max_acc_lr, max_acc_svc, max_acc_rf, max_acc_gb],
    }
)

accuracy_data = simple.set_index('Algorithms')['Accuracy'].to_dict()

def test_algorithms(algorithm, features):
    predictions = None
    y = df['HeartDisease']

    X = pd.get_dummies(df[features])
    X_test = pd.get_dummies(test_data[features])

    scaler = StandardScaler()
    st_scaled_X_train = scaler.fit_transform(X)
    st_scaled_X_test = scaler.transform(X_test)

    if algorithm == "KNN":
        model = KNeighborsClassifier(n_neighbors=24, weights='distance')
        model.fit(st_scaled_X_train, y)
        predictions = model.predict(st_scaled_X_test)

    elif algorithm == "Logistic Regression":
        model = LogisticRegression(solver='liblinear')
        model.fit(X, y)
        predictions = model.predict(X_test)

    elif algorithm == "SVC":
        model = SVC()
        model.fit(st_scaled_X_train, y)
        predictions = model.predict(st_scaled_X_test)


    elif algorithm == "Random Forest":
        model = RandomForestClassifier(oob_score=True,
                            random_state=42,
                            warm_start=True,
                            n_jobs=-1).set_params(n_estimators=150, warm_start=False)
        model.fit(X, y)
        predictions = model.predict(X_test)

    elif algorithm == "Gradient Boosting":
        model = GradientBoostingClassifier(n_estimators=30, random_state=42)
        model.fit(X, y)
        predictions = model.predict(X_test)

    elif algorithm == "All":
        predictions = None

    for dirname, _, filenames in os.walk('/content'):
            for filename in filenames:
                if filename == 'submission.csv':
                    os.remove(os.path.join(dirname, filename))

    output = pd.DataFrame({'Patient_ID' : test_data.Patient_ID, 'HeartDisease' : predictions})

    output.to_csv('submission.csv', index=False)

    first_five_output = pd.read_csv('submission.csv', nrows=10)

    return first_five_output

# Function to execute functions concurrently and gather results (Parallel Code)
def show_df(algorithm):
    functions = {
        "Logistic Regression": logistic_reg,
        "KNN": knn,
        "SVC": svc,
        "Random Forest": random_forest,
        "Gradient Boosting": gradient_boosting,
        "All": all
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.submit(functions[algorithm])
        return result.result()

# Sorting the accuracy values
sorted_accuracy = {k: v for k, v in sorted(accuracy_data.items(), key=lambda item: item[1], reverse=True)}

# Function to display accuracy line plot
def display_accuracy():
    plt.figure(figsize=(10, 6))
    plt.plot(list(sorted_accuracy.keys()), list(sorted_accuracy.values()), marker='o', linestyle='-', color='b')
    plt.title('Accuracy of Different Algorithms')
    plt.xlabel('Algorithms')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt

# Function to display accuracy bar plot
def bar_plot_fn():
        return gr.BarPlot(
            simple,
            x="Algorithms",
            y="Accuracy",
            title="Algorithm Accuracy Comparison",
            tooltip=["Algorithms", "Accuracy"],
            y_lim=[0.0, 1.0],
        )

# Creating Gradio interface1
with gr.Blocks() as interface1:
    with gr.Tab("Line Plot"):
        gr.Interface(
            fn=display_accuracy,
            title='Algorithm Accuracy Comparison',
            description='Line plot showing accuracy of different algorithms',
            inputs=None,
            outputs=gr.Plot(label="Accuracy Plot")
        )
    with gr.Tab("Bar Plot"):
        plot = gr.BarPlot()
    interface1.load(fn=bar_plot_fn, inputs=None, outputs=plot)

# Creating Gradio interface2
interface2 = gr.Interface(
    fn = show_df,
    inputs = gr.Dropdown(choices=algorithms, label="Select an Algorithm"),
    outputs = gr.DataFrame(headers=['lr', 'knn', 'svc', 'rf', 'gb'], label="Output", row_count=4, col_count=5)
)

# Creating Gradio interface3
with gr.Blocks() as interface3:
    with gr.Tab("Test"):
        with gr.Row():
            with gr.Column():
                choice = gr.Dropdown(choices=algorithms, label="Select an Algorithm")
                submit_btn = gr.Button("Submit")
            with gr.Column():
                feature_choice = gr.CheckboxGroup(["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope", "Age",
                                        "RestingBP", "Cholesterol", "FastingBS", "MaxHR", "Oldpeak"],
                                        label="Feature Selection")

        output = gr.DataFrame(label="Output", headers=['Patient_ID', 'HeartDisease'], col_count=2, row_count=10)
        # output = gr.Text(label="Output", type="text")
        submit_btn.click(fn=test_algorithms, inputs=[choice, feature_choice], outputs=output, api_name='Heart')


# Creating Gradio TabbedInterface
interface = gr.TabbedInterface([interface2, interface1, interface3], ["Compare Algorithms", "Plot the Accuracy", "Test the Output"])

if __name__ == "__main__":
    interface.launch()

