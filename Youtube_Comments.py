from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = 'AIzaSyBrYNXLB7mhwUsmUJTJTgXW8s99Jrge4ig'
channel_id = 'UCqECaJ8Gagnn7YCbPEzWH6g'
youtube = build('youtube', 'v3', developerKey=api_key)
search_key = 'all too well'


def search_stat(youtube, search_key):
    request = youtube.search().list(
        part="id",
        maxResults=5,
        q=search_key

    )
    response = request.execute()
    global vid_id
    vid_id = []
    print(response)
    for i in range(0, 5):
        vid_id.append(response['items'][i]['id']['videoId'])
    return vid_id


if __name__ == "__search_stat__":
    search_stat()

search_stat(youtube, search_key)


def comment_stat(youtube, vid_id):
    request1 = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=vid_id,
        order='relevance'

    )
    response = request1.execute()
    global comment_original
    comment_original = []
    for i in range(0, 10):
        try:
            comment_original.append(
                response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
        except:
            comment_original.append(0)

    return comment_original


if __name__ == "__comment_stat__":
    comment_stat()
comment = []
for i in range(0, 5):
    comment.append((comment_stat(youtube, vid_id[i])))
# print(comment)
for i in range(0, len(comment)):
    global com
    com = []
    com = comment[i]
#     for j in com:
#         print(j)


a = {'comments': comment, 'vid_id': vid_id}
df = pd.DataFrame.from_dict(a, orient='index')
df = df.transpose()
df2 = pd.DataFrame(df.comments.tolist(), index=df.vid_id).stack().reset_index(
    level=1, drop=True).reset_index(name='comments')[['comments', 'vid_id']]
column_titles = ["comments", "vid_id"]


def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df


df2 = swap_columns(df2, 'comments', 'vid_id')
# print(df2)


def comment_thread(youtube, vid):
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=vid,
        order='relevance'
    )
    response = request.execute()
    global replies
    replies = []
    for i in range(0, 10):
        if response['items'][i]['snippet']['totalReplyCount'] == 0:
            replies.append(0)
        else:
            replies.append(response['items'][i]['snippet']['totalReplyCount'])
    return replies

if __name__ == "__comment_thread__":
    comment_thread()

reply = []
for i in range(0, 5):
    reply.append((comment_thread(youtube, vid_id[i])))
# print(reply)

comment_replies=[]
for i in range (0,5):
    r=reply[i]
    for j in range(0,10):
        comment_replies.append(r[j])
# print(comment_replies)
df2['Reply_count']=comment_replies
# print(df2)

def reply_thread(youtube, vid):
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=vid,
        order='relevance'
    )
    response = request.execute()
    global reps
    reps = []
    for i in range(0, 10):
        if response['items'][i]['snippet']['totalReplyCount'] == 0:
            reps.append(0)
        else:
            reps.append(response['items'][i]['replies']['comments'][0]['snippet']['textDisplay'])
    return reps

if __name__ == "__reply_thread__":
    reply_thread()

rep = []
for i in range(0, 5):
    rep.append((reply_thread(youtube, vid_id[i])))
# print(rep)

comment_reps=[]
for i in range (0,5):
    r=rep[i]
    for j in range(0,10):
        comment_reps.append(r[j])
print(comment_reps)
df2['Replies']=comment_reps

print(rep)
print(df2)

