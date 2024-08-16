from flask import Flask,render_template,request
import pandas as pd
import numpy as np

import pickle
#popular_dataframe = pickle.load(open('popular.pkl','rb'))


#popular_df = pickle.load(open('popular.pkl','rb'))
with open('popular.pkl','rb') as file:
    popular_df=pd.read_pickle(file)
popular_df['Image-URL-M'] = popular_df['Image-URL-M'].str.replace('http://', 'https://', regex=False)


with open('books.pkl','rb') as file1:
    books=pd.read_pickle(file1)
books['Image-URL-M'] = books['Image-URL-M'].str.replace('http://', 'https://', regex=False)


with open('pt.pkl','rb') as file2:
    pt=pd.read_pickle(file2)

with open('similarity.pkl','rb') as file3:
    similarity_scores=pd.read_pickle(file3)

print(popular_df['Book-Title'])
app = Flask(__name__)
@app.route('/')
def index():
    #print("L")
    #print(list(popular_df['Book-Title']))
    return render_template('index.html',book_name=list(popular_df['Book-Title'].values),author=list(popular_df['Book-Author'].values),image=list(popular_df['Image-URL-M'].values),votes=list(popular_df['num-ratings'].values),rating=list(popular_df['avg-ratings'].values))
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index=np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]

    data=[]
    for i in similar_items:
        item = []
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)
if __name__ == '__main__':
    app.run(debug=True)
