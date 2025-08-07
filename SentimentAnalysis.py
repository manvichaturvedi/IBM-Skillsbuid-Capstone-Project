from requests import request
import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
# Define a function to add a header with a YouTube icon
import streamlit as st
from streamlit_player import st_player
from googleapiclient.discovery import build
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm_notebook
sia = SentimentIntensityAnalyzer()
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

youtube = build(
    "youtube", "v3", developerKey='AIzaSyCLj4zvPt9M9eb4Ap13WHy2gR9WV4ZA7tU')

def getcomments(video_url):
  pattern = r"(?:youtu\.be/|youtube\.com/(?:embed/|watch\?v=|v/|watch\?.+&v=))([a-zA-Z0-9_-]{11})"
  match = re.search(pattern, video_url)
  video_url = match.group(1);
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
    nextRequest = youtube.commentThreads().list(part="snippet", videoId=video, maxResults=100, pageToken=nextPageToken)
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

url = st.text_input('Enter URL Of youtube video :')

df = pd.DataFrame()

df2 = getcomments(url)
df = pd.concat([df, df2])    

Comment_data = df
Comment_data.insert(0, 'ID', range(1, 1 + len(Comment_data)))
import tqdm
res = {}

for i,row in tqdm.tqdm(Comment_data.iterrows(), total=len(Comment_data)):
  text = row['text']
  myid = row['ID']
  res[myid] = sia.polarity_scores(text)

vaders = pd.DataFrame(res).T
vaders.rename(columns={'Id': 'ID'}, inplace=True)

vaders = vaders.reset_index().rename(columns={'index':'Id'})
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

def get_comments_by_video_id(videourl):
    pattern = r"(?:youtu\.be/|youtube\.com/(?:embed/|watch\?v=|v/|watch\?.+&v=))([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, videourl)
    video_id = match.group(1);
    video_comments = vaders[vaders['video_id'] == video_id]
    return video_comments['text']


comments = get_comments_by_video_id(url)

def get_value_by_video_id(video_id):
    pattern = r"(?:youtu\.be/|youtube\.com/(?:embed/|watch\?v=|v/|watch\?.+&v=))([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, video_id)
    videoid = match.group(1);
    video_comments = vaders[vaders['video_id'] == videoid]
    sentiment = video_comments['sentiment'].value_counts()
    return sentiment




st.write("\n\n\n\n")

# Define the pages
def home():
    st.write("")

def about():
    st.title("About")
    st.write("This is the about page.")

def contact():
    st.title("Contact")
    st.write("This is the contact page.")


#comments = df
#comments_list = comments['video_id']
#selected_movie = st.selectbox("select a video_id :", comments_list)


#def comm_containers(video_id):
    #video_comment = comments[comments['video_id'] == video_id]
    #sentiment = video_comment['sentiment'].value_counts()
    #positive_sentiment = len(video_comment[video_comment['sentiment']=='Positive'].value_counts())
    #comment_count = len(video_comment['text'])
   
   
    
'''Input for YouTube URL
   #if(video_id == 'Q-6x-FxacR8'):
     #youtube_url = "https://youtu.be/Q-6x-FxacR8?si=beJ6g4G6BYjdrX1N"
    #elif video_id == 'vQXvyV0zIP4':
     #youtube_url = "https://youtu.be/vQXvyV0zIP4?si=msLIf6gKgazn6UDx"
    else :
     youtube_url =  "https://youtu.be/B7oOtTgYEZM?si=OGfwiaxWWyqzOo47"
# Display the video using streamlit-player
    if youtube_url:
     st_player(youtube_url)
    st.markdown(
         f"""
         <div style="border: 2px solid black; font-size: 40px; padding: 10px; border-radius: 5px; background-color: #E29F7C; color: black">
         <p style="font-size: 20px;">Total Number Of Comments Video Got :</p>
         <p>{comment_count}</p>
         </div>
         """,
         unsafe_allow_html=True
       )
    with st.container():
      st.header("Analysis of Comments")
     
    # Data for the pie chart
      labels = ['Positive Comments','Negative Comments','Neutral Comments']
      explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    # Create the pie chart
      fig, ax = plt.subplots()
      ax.pie(sentiment, explode=explode, labels=labels, autopct='%.1f%%', colors=['Pink','orange','purple'],shadow=True, startangle=90)
      ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
     
    # Display the pie chart in Streamlit
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
    for k,j,l in zip(video_comment['author'][:15],video_comment['text'][:15],video_comment['sentiment'][:15]):
        st.markdown(
         f"""
         <div style="border: 2px solid black; padding: 10px; border-radius: 5px; background-color: #C1EF88; color: black">
         <p>{k}</p>
         <p>{j}</p><p>{l}</p>
         </div>
         """,
         unsafe_allow_html=True
       )
        st.write("\n" * 3)
    st.markdown(
        f"""
        <div style="font-size:80px"><p style="font-size:50px">Congratulations User, Your Video Got {positive_sentiment} Positive Comments</p></div>
        """,
         unsafe_allow_html=True
       )



# Create a sidebar for navigation
st.sidebar.title("Youtube Comments Analyzer APP")
st.write("\n" * 40)
page = st.sidebar.radio(" \n "*3,("Home", "About"))


if st.button('show analysis'):
    comm_containers(selected_movie)

'''
# Display the selected page
if page == "Home":
    home()


st.write("\n" * 100)
st.sidebar.header('Created By : Manvi Chaturvedi ')
st.sidebar.write('Technologoies Used : ')
st.sidebar.write('Natural Language Processing')
st.sidebar.write('Machine Learning/AI')
st.sidebar.write('Scrapping Using Youtube API')
