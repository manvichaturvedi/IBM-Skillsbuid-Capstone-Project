import requests 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_player import st_player
from googleapiclient.discovery import build
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm_notebook
import tqdm
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('vader_lexicon')


def add_header():
    st.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: black;
            padding: 10px;
            border-radius: 10px;
        }
        .header img {
            width: 40px;
            height: 40px;
            margin-right: 10px;
        }
        .header h1 {
            font-size: 24px;
            margin: 0;
            color: white;
        }
        </style>
        <div class="header">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="YouTube Icon">
            <h1>Youtube Comments Sentiment Analysis Using NLP</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Add the header to the app
add_header()

url = st.text_input('Enter URL Of youtube video :')


youtube = build(
    "youtube", "v3", developerKey='AIzaSyCLj4zvPt9M9eb4Ap13WHy2gR9WV4ZA7tU')

def getcomments(video_url):
  pattern = r"(?:youtu\.be/|youtube\.com/(?:embed/|watch\?v=|v/|watch\?.+&v=))([a-zA-Z0-9_-]{11})"
  match = re.search(pattern, video_url)
  video_url = match.group(1)
  request = youtube.commentThreads().list(
      part="snippet",
      videoId=video_url,
      maxResults=100
  )

  comments = []

# Execute the request.
  response = request.execute()

# Get the comments from the response.
  for item in response['items']:
      comment = item['snippet']['topLevelComment']['snippet']
      public = item['snippet']['isPublic']
      comments.append([
          comment['authorDisplayName'],
          comment['publishedAt'],
          comment['likeCount'],
          comment['textOriginal'],
          comment['videoId'],
          public
])

  while (1 == 1):
    try:
     nextPageToken = response['nextPageToken']
    except KeyError:
     break
    nextPageToken = response['nextPageToken']
    # Create a new request object with the next page token.
    nextRequest = youtube.commentThreads().list(part="snippet", videoId=video_url, maxResults=100, pageToken=nextPageToken)
    # Execute the next request.
    response = nextRequest.execute()
    # Get the comments from the next response.
    for item in response['items']:
      comment = item['snippet']['topLevelComment']['snippet']
      public = item['snippet']['isPublic']
      comments.append([
          comment['authorDisplayName'],
          comment['publishedAt'],
          comment['likeCount'],
          comment['textOriginal'],
          comment['videoId'],
          public
      ])

  df2 = pd.DataFrame(comments, columns=['author', 'updated_at', 'like_count', 'text','video_id','public'])
  return df2

df = pd.DataFrame()

df2 = getcomments(url)
df = pd.concat([df, df2])  

st_player(url)
Comment_data = df
Comment_data.insert(0, 'ID', range(1, 1 + len(Comment_data)))

sia = SentimentIntensityAnalyzer()

res = {}
for i,row in tqdm.tqdm(Comment_data.iterrows(), total=len(Comment_data)):
  text = row['text']
  myid = row['ID']
  res[myid] = sia.polarity_scores(text)

vaders = pd.DataFrame(res).T
vaders.rename(columns={'Id': 'ID'}, inplace=True)

vaders = vaders.reset_index().rename(columns={'index':'ID'})
vaders = vaders.merge(Comment_data, how='left')

def get_sentiment(text):
    score = sia.polarity_scores(text)['compound']
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Apply function to DataFrame
vaders['sentiment'] = vaders['text'].apply(get_sentiment)

pd.DataFrame(vaders)
video_id = vaders['video_id'][0]
def get_comments_by_video_id(video_id1):
    video_comments = vaders[vaders['video_id'] == video_id1]
    return video_comments['text'][:20]

# Example usage

comments = get_comments_by_video_id(video_id)
col1, col2 = st.columns(2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
fig.set_size_inches(10, 6)

# Generate some data for the pie chart
pie_data = vaders['sentiment'].value_counts()
labels = ['Positive', 'Negative', 'Neutral']
ax1.set_title('Comments Analysis using Pie Chart')
ax1.pie(pie_data,autopct='%1.1f%%', colors=['pink','red','yellow'],labels=labels)
ax2.set_title('Comments Analysis using Bar Chart')
ax2.bar(x='sentiment',height=50 ,data=vaders)
st.pyplot(fig)

st.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: black;
            padding: 10px;
            border-radius: 10px;
        }
        .header img {
            width: 40px;
            height: 40px;
            margin-right: 10px;
        }
        .header h1 {
            font-size: 24px;
            margin: 0;
            color: white;
        }
        </style>
        <div class="header">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="YouTube Icon">
            <h1>Displaying 15 Youtube Comments Of the selected Video</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
st.write("\n" * 3)
positive_sentiment = len(vaders[vaders['sentiment']=='Positive'])

for k,j,l in zip(vaders['author'][:15],vaders['text'][:15],vaders['sentiment'][:15]):
        st.markdown(
         f"""
         <div style="border: 2px solid black; padding: 10px; border-radius: 5px; background-color: #E393E4; color: black">
         <p>{k}</p>
         <p>{j}</p><p>{l}</p>
         </div>
         """,
         unsafe_allow_html=True
       )
        st.write("\n" * 3)
st.markdown(
        f"""
        <div style="font-size:80px"><p style="font-size:50px">Congratulations User, Your Video Got {positive_sentiment} Positive ❤️ Comments</p></div>
        """,
         unsafe_allow_html=True
       )
