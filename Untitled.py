#!/usr/bin/env python
# coding: utf-8

# In[41]:


import numpy as np
import pandas as pd


# In[42]:


books=pd.read_csv('Books.csv')
users=pd.read_csv('Users.csv')
ratings=pd.read_csv('Ratings.csv')


# In[43]:


# ratings.head()
# print(books.shape)


# ## Popularity Based Recommender

# In[44]:


ratings_with_name=ratings.merge(books,on='ISBN')


# In[45]:


num_rating_df=ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating':'num-ratings'},inplace=True)
# num_rating_df


# In[46]:


avg_rating_df=ratings_with_name.groupby('Book-Title').mean()['Book-Rating'].reset_index()
avg_rating_df.rename(columns={'Book-Rating':'avg-ratings'},inplace=True)
# avg_rating_df


# In[47]:


popularity_df = num_rating_df.merge(avg_rating_df,on='Book-Title')
# popularity_df

print("JK")

# In[48]:


popularity_df = popularity_df[popularity_df['num-ratings']>=250].sort_values('avg-ratings',ascending=False).head(50)


# In[49]:


popularity_df.merge(books,on='Book-Title').drop_duplicates('Book-Title')


# In[50]:


popularity_df=popularity_df.merge(books,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Image-URL-M','num-ratings','avg-ratings']]


# In[51]:


popularity_df


# ## Collaborative Filtering based Recommender System

# In[52]:


x=ratings_with_name.groupby('User-ID').count()['Book-Rating']>200
padhe_likhe_users = x[x].index


# In[53]:


filtered_ratings=ratings_with_name[ratings_with_name['User-ID'].isin(padhe_likhe_users)]


# In[54]:


y=filtered_ratings.groupby('Book-Title').count()['Book-Rating']>=50
Famous_Books=y[y].index


# In[55]:


final_ratings=filtered_ratings[filtered_ratings['Book-Title'].isin(Famous_Books)]


# In[56]:


final_ratings.drop_duplicates()


# In[57]:


pt=final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')
pt.fillna(0,inplace=True)


# In[58]:


pt


# In[59]:


from sklearn.metrics.pairwise import cosine_similarity


# In[60]:


Similarity_Score=cosine_similarity(pt)


# In[61]:


Similarity_Score


# In[62]:


def recommend(book_name):
    index=np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(Similarity_Score[index])),key=lambda x:x[1],reverse=True)[1:6]
    for i in similar_items:
        print(pt.index[i[0]])
    


# In[63]:


sorted(list(enumerate(Similarity_Score[0])),key=lambda x:x[1],reverse=True)[1:6]


# In[64]:


recommend('Message in a Bottle')


# In[65]:


pt


# In[66]:


final_ratings["Image-URL-L"][63]


# In[39]:


p#ip install --upgrade numpy pandas


# In[67]:


import pickle
pickle.dump(popularity_df,open('popular.pkl','wb'))


# In[68]:


#pip show pandas


# In[69]:


with open('popular.pkl','rb') as file:
    popular_df=pd.read_pickle(file)


# In[72]:


popular_df['Book-Title']


# In[ ]:




