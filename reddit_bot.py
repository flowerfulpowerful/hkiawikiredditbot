import os
import praw
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ['hkiawiki-bot']
PASSWORD = os.environ['REDDIT_PASSWORD']
CLIENT_ID = os.environ['MNpGEycmgxVtqZ6gMbnERA']
CLIENT_SECRET = os.environ['Rr1qkfuiXY51Kknn73U2iMgNvlzi-w']

# Initialize PRAW with custom User-Agent.
if DEBUG:
    print("Username/pass: " + USERNAME, PASSWORD)
    print("Client ID/pass: " + CLIENT_ID, CLIENT_SECRET)
    print("Authenticating...")
r = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    password=PASSWORD,
    user_agent=BOTNAME,
    username=USERNAME
)
if DEBUG:
    print("Authenticated as: " + format(r.user.me()))

# Keywords to search for in post titles
KEYWORDS = ["how", "help", "what", "where", "tag", "location"]

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent=REDDIT_USER_AGENT
)

# Wiki search function
def search_wiki(query):
    search_url = f"https://hellokittyislandadventure.wiki.gg/wiki/Special:Search?query={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Parse search results
    results = soup.select(".mw-search-result-heading a")
    if results:
        return "https://hellokittyislandadventure.wiki.gg" + results[0]["href"]
    return None

def main():
    subreddit = reddit.subreddit("HelloKittyIsland")
    
    for post in subreddit.new(limit=10):  # Fetch the 10 newest posts
        title = post.title.lower()
        
        # Check if the title contains any of the keywords
        if any(keyword in title for keyword in KEYWORDS):
            # Combine title and post content for the query
            query = title + " " + post.selftext
            relevant_page = search_wiki(query)
            
            if relevant_page:
                reply_text = f"I found something that might help: [Check this wiki page!]({relevant_page})"
                post.reply(reply_text)
                print(f"Replied to post: {post.title}")

if __name__ == "__main__":
    main()
