from googleapiclient.discovery import build
import csv

api_key = 'AIzaSyC9H7rts5dmfuPFn1pCfFtgPn_1mIr7rQg'
youtube = build('youtube', 'v3', developerKey=api_key)

def get_playlist_items(playlist_id):
    videos = []
    nextPageToken = None
    
    while True:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails", 
            playlistId=playlist_id,
            maxResults=50, 
             pageToken=nextPageToken
        )
        response = request.execute()

        for item in response['items']:
            video_title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            video_published_at = item['snippet']['publishedAt']
            video_tags = item['snippet']['tags'] if 'tags' in item['snippet'] else []
            video_response = youtube.videos().list(
                part="statistics,player",
                id=video_id
            ).execute()
            new_video_response = youtube.videos().list(
                part="snippet",
                id=video_id
            ).execute()
            new_video_items = new_video_response.get('items', [])
            if new_video_items:
                video_owner_title = new_video_items[0]['snippet']['channelTitle']
            else:
                video_owner_title = "Unknown" 
            if 'items' in video_response and video_response['items']:
                view_count = video_response['items'][0]['statistics'].get('viewCount', 0)
            else:
                view_count = 0  # Or any default value you prefer
            if 'items' in video_response and video_response['items']:
                like_count = video_response['items'][0]['statistics'].get('likeCount', 0) 
            else:
                like_count = 0  # Or any default value you prefer
            if 'items' in video_response and video_response['items']:
                favorite_count = video_response['items'][0]['statistics'].get('favoriteCount', 0) 
            else:
                favorite_count = 0  # Or any default value you prefer
            if 'items' in video_response and video_response['items']:
                comment_count = video_response['items'][0]['statistics'].get('commentCount', 0)  
            else:
                comment_count = 0  # Or any
            
            videos.append({
                'title': video_title,
                'videoId': video_id,
                'publishedAt': video_published_at,
                'tags': video_tags,
                'viewCount': view_count,
                'likeCount': like_count,
                'favoriteCount': favorite_count,
                'commentCount': comment_count,
                'video_owner_title':video_owner_title
            })

        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break  # Nếu không còn trang kế tiếp thì thoát vòng lặp

    return videos

playlist_id = 'PLgzTt0k8mXzE6H9DDgiY7Pd8pKZteis48'
videos = get_playlist_items(playlist_id)

with open('playlist_data.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Title', 'Video ID', 'Video Owner Title', 'Published At', 'View Count', 'Like Count', 'Favorite Count', 'Comment Count']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for video in videos:
        writer.writerow({
            'Title': video['title'],
            'Video ID': video['videoId'],
            'Video Owner Title': video['video_owner_title'],
            'Published At': video['publishedAt'],
            'View Count': video['viewCount'],
            'Like Count': video['likeCount'],
            'Favorite Count': video['favoriteCount'],
            'Comment Count': video['commentCount']
        })

print("CSV file has been created successfully!")