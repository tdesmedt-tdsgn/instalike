import time
from datetime import datetime, timedelta
import random
from instagram_private_api import Client, ClientCompatPatch
from instagram_private_api.errors import ClientError


username = ''
password = ''
target_users = ['target_user1', 'target_user2', 'target_user3']
processed_media_file = 'processed_media.txt'
processed_stories_file = 'processed_stories.txt'

def login_to_instagram(username, password):
    return Client(username, password)

def get_user_id(api, username):
    return api.username_info(username)['user']['pk']

def get_media_ids(api, user_id, max_items=50):
    max_id = None
    media_ids = []

    ten_days_ago = datetime.utcnow() - timedelta(days=10)

    while True:
        user_feed = api.user_feed(user_id, max_id=max_id)
        for item in user_feed['items']:
            timestamp = datetime.utcfromtimestamp(item['taken_at']).replace(microsecond=0)
            if timestamp >= ten_days_ago:
                media_ids.append(item['id'])
            else:
                # If we've gone back more than 10 days, break out of the loop
                break

        if len(media_ids) >= max_items or not user_feed.get('more_available'):
            break
        max_id = user_feed['next_max_id']

    return media_ids

def read_processed_ids(filename):
    try: 
        with open(filename, 'r') as f:
            processed_ids = f.read().splitlines()
    except FileNotFoundError:
        processed_ids = []

    return set(processed_ids)

def write_processed_id(filename, media_id):
    with open(filename, 'a') as f:
        f.write(f"{media_id}\n")

def like_and_share_media(api, media_ids, processed_media_file):
    processed_ids = read_processed_ids(processed_media_file)

    for media_id in media_ids:
        if media_id not in processed_ids:
            api.post_like(media_id)
            # api.post_media_share('story', media_id)
            print(f"Liked and shared media ID: {media_id}")
            write_processed_id(processed_media_file, media_id)
            time.sleep(random.randint(5, 12))

def get_story_items(api, user_id):
    reels_tray = api.reels_tray()
    user_reel = None

    for reel in reels_tray['tray']:
        if reel['user']['pk'] == user_id:
            user_reel = reel
            break

    if user_reel:
        user_story_feed = api.user_story_feed(user_id)
        return [story for story in user_story_feed['reel']['items'] if (datetime.utcnow() - datetime.utcfromtimestamp(story['taken_at'])).total_seconds() < 86400]
    else:
        print("No stories found.")
        return []


def like_and_share_stories(api, story_items, processed_stories_file):
    processed_ids = read_processed_ids(processed_stories_file)
    for story in story_items:
        story_id = story['id']
        if story_id not in processed_ids:
            try:
                api.post_like(story_id)
            except ClientError as e:
                print(f"Error liking story ID {story_id}: {e}")
                continue

            try:
                api.post_share('reel', story_id, 'story')
            except ClientError as e:
                print(f"Error sharing story ID {story_id}: {e}")
                continue

            print(f"Liked and shared story ID: {story_id}")
            write_processed_id(processed_stories_file, story_id)
            time.sleep(random.randint(5, 12))



def process_target_users(api, target_users, processed_media_file, processed_stories_file):
    for target_user in target_users:
        target_user_id = get_user_id(api, target_user)
        media_ids = get_media_ids(api, target_user_id)
        like_and_share_media(api, media_ids, processed_media_file)
        story_items = get_story_items(api, target_user_id)
        like_and_share_stories(api, story_items, processed_stories_file)

if __name__ == '__main__':
    api = login_to_instagram(username, password)
    process_target_users(api, target_users, processed_media_file, processed_stories_file)
