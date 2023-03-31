from flask import Flask,request,render_template
import re
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer 
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
tokenizer = Tokenizer()

model = load_model("solutionChalange.h5")

arr = ['suicide', 'loneliness', 'Emotional distress', 'General sadness', 'depressed',
       'Overwhelm', 'sleep', 'Work stress', 'scared', 'worthless', 'anxious', 'General stress',
       'Academic stress', 'death']

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def model_predict():
    if request.method == 'POST': 
        query = next(request.form.items())[0]
        print("Query received:", query)
        print(query)
        
        text = []
        txt = re.sub('[^a-zA-Z\']', ' ', query)
        txt = txt.lower()
        txt = txt.split()
        txt = " ".join(txt)

        text.append(txt)
        print(text)

        tokenizer.fit_on_texts(text)
        x_test = tokenizer.texts_to_sequences(text)
        # print(x_test)
        
        x_test = np.array(x_test).squeeze()
        # print(x_test)

        x_test = pad_sequences([x_test], padding='post', maxlen=42)
        # print(x_test)
        
        y_pred = model.predict(x_test)
        y_pred = y_pred.argmax()

        # print(y_pred)
        # print(arr[y_pred])

        return (arr[y_pred])
    return None

if __name__ == '__main__':
    app.run(debug=True)