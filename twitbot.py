import tweepy
import time
import configparser

config = configparser.ConfigParser()
config.read('twitbot.cfg')

api_key = config['KEYS']['api_key']
api_secret_key = config['KEYS']['api_secret_key']
access_token = config['TOKENS']['access_token']
access_token_secret = config['TOKENS']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


user = api.me()


def update_profile_pic(filename):
    """
    Update profile image
    """
    api.update_profile_image(filename)


def update_background_image(path_to_image):
    """
    Update profile background image
    """
    api.update_profile_banner('',path_to_image)


def send_dm(receipient_username, message):
    receipient_id = api.get_user(receipient_username).id
    # Send direct message
    api.send_direct_message(receipient_id,message)


def follow_list(list_people_to_follow):
    for person in list_people_to_follow:
        api.create_friendship(person)

def follow_followers():
    """
    Follow everyone that is following you
    """
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
        print ("Followed everyone that is following " + user.name)


# # Retweet or like tweets based on a keyword.
def retweet_keyword(word, number_of_tweets):
    for tweet in tweepy.Cursor(api.search, word).items(number_of_tweets):
        try:
            tweet.retweet()
            print('Retweeted the tweet')
         
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


def like_keyword(word, number_of_tweets):
    for tweet in tweepy.Cursor(api.search, word).items(number_of_tweets):
        try:
            tweet.favorite()
            print('Liked the tweet')
         
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


def get_user_info():
    user = api.me()
    print (user.name)
    print (user.screen_name)
    return user

def other_user_info(username):
    print (api.get_user(username))
    # print (api.followers(user.id))


def follow_after_follow():
    """
    Checks every 1 hour for new followers and follows them.
    """
    user = get_user_info()
    while True:
        old_number_of_followers = user.followers_count
        time.sleep(3600)
        new_number_of_followers = user.followers_count
        num_new_followers = new_number_of_followers - old_number_of_followers
        list_of_followers = tweepy.Cursor(api.followers).items().reverse()

        for i in range(len(new_number_of_followers)):
            list_of_followers[i].follow()
        
        

if __name__ == "__main__":
    follow_after_follow()