import os
import praw
import requests
import re
from bs4 import BeautifulSoup


# Initialize the Reddit client with your credentials
reddit = praw.Reddit(
    client_id="MNpGEycmgxVtqZ6gMbnERA",
    client_secret="Rr1qkfuiXY51Kknn73U2iMgNvlzi-w",
    password="74UKi-eP5ncA$35",
    username="hkiawiki-bot",
    user_agent="HKIA Wiki Bot v1.0 (by /u/hkiawiki-bot)",
)

# Access a subreddit
subreddit = reddit.subreddit("HelloKittyIsland")  # Correctly access the subreddit
print(subreddit)

# Known URLs for commonly searched terms
wiki_urls = { 
            "tophat gudetama": "https://hellokittyislandadventure.wiki.gg/wiki/Tophat_Gudetama",
            "gudetama": "https://hellokittyislandadventure.wiki.gg/wiki/Gudetama",
            "dandelily": "https://hellokittyislandadventure.wiki.gg/wiki/Dandelily",
            "events": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "event": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "visitor cabin": "https://hellokittyislandadventure.wiki.gg/wiki/Visitor_Cabins",
            "visitor cabins": "https://hellokittyislandadventure.wiki.gg/wiki/Visitor_Cabins",
            "cabin": "https://hellokittyislandadventure.wiki.gg/wiki/Visitor_Cabins",
            "cabin": "https://hellokittyislandadventure.wiki.gg/wiki/Island_Visitors",
            "cabins": "https://hellokittyislandadventure.wiki.gg/wiki/Visitor_Cabins",
            "city town": "https://hellokittyislandadventure.wiki.gg/wiki/City_Town",
            "city": "https://hellokittyislandadventure.wiki.gg/wiki/City_Town",
            "hello kitty": "https://hellokittyislandadventure.wiki.gg/wiki/Hello_Kitty",
            "giant seed": "https://hellokittyislandadventure.wiki.gg/wiki/Giant_Seed",
            "giant seeds": "https://hellokittyislandadventure.wiki.gg/wiki/Giant_Seed",
            "big seed": "https://hellokittyislandadventure.wiki.gg/wiki/Giant_Seed",
            "seed": "https://hellokittyislandadventure.wiki.gg/wiki/Giant_Seed",
            "kuromi": "https://hellokittyislandadventure.wiki.gg/wiki/Kuromi",
            "my melody": "https://hellokittyislandadventure.wiki.gg/wiki/My_Melody",
            "tag": "https://hellokittyislandadventure.wiki.gg/wiki/Tags",
            "tags": "https://hellokittyislandadventure.wiki.gg/wiki/Tags",
            "icon": "https://hellokittyislandadventure.wiki.gg/wiki/Tags",
            "likes": "https://hellokittyislandadventure.wiki.gg/wiki/Tags",
            "icons": "https://hellokittyislandadventure.wiki.gg/wiki/Tags",
            "flower": "https://hellokittyislandadventure.wiki.gg/wiki/Flowers",
            "flowers": "https://hellokittyislandadventure.wiki.gg/wiki/Flowers",
            "keroppi": "https://hellokittyislandadventure.wiki.gg/wiki/Keroppi",
            "hangyodon": "https://hellokittyislandadventure.wiki.gg/wiki/hangyodon",
            "wish me mell": "https://hellokittyislandadventure.wiki.gg/wiki/Wish_me_mell",
            "my sweet piano": "https://hellokittyislandadventure.wiki.gg/wiki/My_Sweet_Piano",
            "usahana": "https://hellokittyislandadventure.wiki.gg/wiki/Usahana",
            "pekkle": "https://hellokittyislandadventure.wiki.gg/wiki/Pekkle",
            "pompompurin": "https://hellokittyislandadventure.wiki.gg/wiki/Pompompurin",
            "pompom": "https://hellokittyislandadventure.wiki.gg/wiki/Pompompurin",
            "fish": "https://hellokittyislandadventure.wiki.gg/wiki/Fish",
            "critter": "https://hellokittyislandadventure.wiki.gg/wiki/Critters",
            "critters": "https://hellokittyislandadventure.wiki.gg/wiki/Critters",
            "bug": "https://hellokittyislandadventure.wiki.gg/wiki/Critters",
            "bugs": "https://hellokittyislandadventure.wiki.gg/wiki/Critters",
            "puzzle": "https://hellokittyislandadventure.wiki.gg/wiki/Puzzles",
            "puzzles": "https://hellokittyislandadventure.wiki.gg/wiki/Puzzles",
            "pochacco": "https://hellokittyislandadventure.wiki.gg/wiki/Pochacco",
            "retsuko": "https://hellokittyislandadventure.wiki.gg/wiki/Retsuko",
            "big challenges": "https://hellokittyislandadventure.wiki.gg/wiki/Big_Challenges",
            "tophat": "https://hellokittyislandadventure.wiki.gg/wiki/TOPHAT",
            "chococat": "https://hellokittyislandadventure.wiki.gg/wiki/Chococat",
            "quest": "https://hellokittyislandadventure.wiki.gg/wiki/Quests",
            "quests": "https://hellokittyislandadventure.wiki.gg/wiki/Quests",
            "visitor": "https://hellokittyislandadventure.wiki.gg/wiki/Island_Vistors",
            "visitors": "https://hellokittyislandadventure.wiki.gg/wiki/Island_Vistors",
            "sewer": "https://hellokittyislandadventure.wiki.gg/wiki/Sewers",
            "sewers": "https://hellokittyislandadventure.wiki.gg/wiki/Sewers",
            "seaside resort": "https://hellokittyislandadventure.wiki.gg/wiki/Seaside_Resort",
            "resort": "https://hellokittyislandadventure.wiki.gg/wiki/Seaside_Resort",
            "spooky swamp": "https://hellokittyislandadventure.wiki.gg/wiki/Spooky_Swamp",
            "swamp": "https://hellokittyislandadventure.wiki.gg/wiki/Spooky_Swamp",
            "rainbow reef": "https://hellokittyislandadventure.wiki.gg/wiki/Rainbow_Reef",
            "reef": "https://hellokittyislandadventure.wiki.gg/wiki/Rainbow_Reef",
            "gemstone mountain": "https://hellokittyislandadventure.wiki.gg/wiki/Gemstone_Mountain",
            "ruins": "https://hellokittyislandadventure.wiki.gg/wiki/Red_Hot_Ruins",
            "red hot ruins": "https://hellokittyislandadventure.wiki.gg/wiki/Red_Hot_Ruins",
            "mount hothead": "https://hellokittyislandadventure.wiki.gg/wiki/Mount_Hothead",
            "merry meadow": "https://hellokittyislandadventure.wiki.gg/wiki/Merry_Meadows",
            "merry meadows": "https://hellokittyislandadventure.wiki.gg/wiki/Merry_Meadows",
            "meadow": "https://hellokittyislandadventure.wiki.gg/wiki/Merry_Meadows",
            "meadows": "https://hellokittyislandadventure.wiki.gg/wiki/Merry_Meadows",
            "greenhouse": "https://hellokittyislandadventure.wiki.gg/wiki/Greenhouse",
            "multiplayer": "https://hellokittyislandadventure.wiki.gg/wiki/Multiplayer",
            "friendship bead": "https://hellokittyislandadventure.wiki.gg/wiki/Multiplayer",
            "friendship beads": "https://hellokittyislandadventure.wiki.gg/wiki/Multiplayer",
            "bead": "https://hellokittyislandadventure.wiki.gg/wiki/Multiplayer",
            "beads": "https://hellokittyislandadventure.wiki.gg/wiki/Multiplayer",
            "glowbal": "https://hellokittyislandadventure.wiki.gg/wiki/Glowbal",
            "petunia": "https://hellokittyislandadventure.wiki.gg/wiki/Petunia",
            "bellbutton": "https://hellokittyislandadventure.wiki.gg/wiki/Bellbutton",
            "penstemum": "https://hellokittyislandadventure.wiki.gg/wiki/Penstemum",
            "tulias": "https://hellokittyislandadventure.wiki.gg/wiki/Tulias",
            "hibiscus": "https://hellokittyislandadventure.wiki.gg/wiki/Hibiscus",
            "ghostgleam": "https://hellokittyislandadventure.wiki.gg/wiki/Ghostgleam",
            "thistle": "https://hellokittyislandadventure.wiki.gg/wiki/Thistle",
            "heavy nettle": "https://hellokittyislandadventure.wiki.gg/wiki/Heavy_Nettle",
            "anemone": "https://hellokittyislandadventure.wiki.gg/wiki/Anemone",
            "dreampuff": "https://hellokittyislandadventure.wiki.gg/wiki/Dreampuff",
            "marigold": "https://hellokittyislandadventure.wiki.gg/wiki/Marigold",
            "eggwort": "https://hellokittyislandadventure.wiki.gg/wiki/Eggwort",
            "bowblossom": "https://hellokittyislandadventure.wiki.gg/wiki/Bowblossom",
            "poinsettia": "https://hellokittyislandadventure.wiki.gg/wiki/Poinsettia",
            "cloud island": "https://hellokittyislandadventure.wiki.gg/wiki/Cloud_Island",
            "cloud islands": "https://hellokittyislandadventure.wiki.gg/wiki/Cloud_Island",
            "gift flowers": "https://hellokittyislandadventure.wiki.gg/wiki/Gift_Flowers",
            "pink flowers": "https://hellokittyislandadventure.wiki.gg/wiki/Gift_Flowers",
            "blue flowers": "https://hellokittyislandadventure.wiki.gg/wiki/Rainfall_Flowers",
            "rain flowers": "https://hellokittyislandadventure.wiki.gg/wiki/Rainfall_Flowers",
            "rainfall flowers": "https://hellokittyislandadventure.wiki.gg/wiki/Rainfall_Flowers",
            "creation station": "https://hellokittyislandadventure.wiki.gg/wiki/Creation_Station",
            "clothing": "https://hellokittyislandadventure.wiki.gg/wiki/Clothing",
            "clothes": "https://hellokittyislandadventure.wiki.gg/wiki/Clothing",
            "furniture": "https://hellokittyislandadventure.wiki.gg/wiki/Furniture",
            "craft": "https://hellokittyislandadventure.wiki.gg/wiki/Crafting_Table",
            "crafting": "https://hellokittyislandadventure.wiki.gg/wiki/Crafting_Table",
            "crafting table": "https://hellokittyislandadventure.wiki.gg/wiki/Crafting_Table",
            "crafting plans": "https://hellokittyislandadventure.wiki.gg/wiki/Crafting_Table",
            "plans": "https://hellokittyislandadventure.wiki.gg/wiki/Crafting_Table",
            "instructions": "https://hellokittyislandadventure.wiki.gg/wiki/Creation_Station",
            "instruction": "https://hellokittyislandadventure.wiki.gg/wiki/Creation_Station",
            "crafting plan": "https://hellokittyislandadventure.wiki.gg/wiki/Crafting_Table",
            "plans": "https://hellokittyislandadventure.wiki.gg/wiki/Crafting_Table",
            "materials": "https://hellokittyislandadventure.wiki.gg/wiki/Materials",
            "material": "https://hellokittyislandadventure.wiki.gg/wiki/Materials",
            "candle": "https://hellokittyislandadventure.wiki.gg/wiki/Candles_(All)",
            "candles": "https://hellokittyislandadventure.wiki.gg/wiki/Candles_(All)",
            "oven": "https://hellokittyislandadventure.wiki.gg/wiki/Oven",
            "potion": "https://hellokittyislandadventure.wiki.gg/wiki/Cauldron",
            "potions": "https://hellokittyislandadventure.wiki.gg/wiki/Cauldron",
            "cauldron": "https://hellokittyislandadventure.wiki.gg/wiki/Cauldron",
            "espresso machine": "https://hellokittyislandadventure.wiki.gg/wiki/Espresso_Machine",
            "drink machine": "https://hellokittyislandadventure.wiki.gg/wiki/Espresso_Machine",
            "soda machine": "https://hellokittyislandadventure.wiki.gg/wiki/Soda_Machine",
            "soda": "https://hellokittyislandadventure.wiki.gg/wiki/Soda_Machine",
            "sodas": "https://hellokittyislandadventure.wiki.gg/wiki/Soda_Machine",
            "dessert machine": "https://hellokittyislandadventure.wiki.gg/wiki/Dessert_Machine",
            "desserts": "https://hellokittyislandadventure.wiki.gg/wiki/Dessert_Machine",
            "ice cream": "https://hellokittyislandadventure.wiki.gg/wiki/Dessert_Machine",
            "icecream": "https://hellokittyislandadventure.wiki.gg/wiki/Dessert_Machine",
            "pudding": "https://hellokittyislandadventure.wiki.gg/wiki/Dessert_Machine",
            "shake": "https://hellokittyislandadventure.wiki.gg/wiki/Dessert_Machine",
            "shakes": "https://hellokittyislandadventure.wiki.gg/wiki/Dessert_Machine",
            "pizza": "https://hellokittyislandadventure.wiki.gg/wiki/Pizza_Oven",
            "pizzas": "https://hellokittyislandadventure.wiki.gg/wiki/Pizza_Oven",
            "pizza oven": "https://hellokittyislandadventure.wiki.gg/wiki/Pizza_Oven",
            "candy cloud machine": "https://hellokittyislandadventure.wiki.gg/wiki/Candy_Cloud_Machine",
            "clouds": "https://hellokittyislandadventure.wiki.gg/wiki/Candy_Cloud_Machine",
            "cottoncandy": "https://hellokittyislandadventure.wiki.gg/wiki/Candy_Cloud_Machine",
            "cotton candy": "https://hellokittyislandadventure.wiki.gg/wiki/Candy_Cloud_Machine",
            "egg pan station": "https://hellokittyislandadventure.wiki.gg/wiki/Egg_Pan_Station",
            "egg pan": "https://hellokittyislandadventure.wiki.gg/wiki/Egg_Pan_Station",
            "omelet": "https://hellokittyislandadventure.wiki.gg/wiki/Egg_Pan_Station",
            "crepe": "https://hellokittyislandadventure.wiki.gg/wiki/Egg_Pan_Station",
            "crepes": "https://hellokittyislandadventure.wiki.gg/wiki/Egg_Pan_Station",
            "omelets": "https://hellokittyislandadventure.wiki.gg/wiki/Egg_Pan_Station",
            "omelette": "https://hellokittyislandadventure.wiki.gg/wiki/Egg_Pan_Station",
            "omelettes": "https://hellokittyislandadventure.wiki.gg/wiki/Egg_Pan_Station",
            "egg": "https://hellokittyislandadventure.wiki.gg/wiki/Egg",
            "photo op": "https://hellokittyislandadventure.wiki.gg/wiki/Photo_Ops",
            "photo ops": "https://hellokittyislandadventure.wiki.gg/wiki/Photo_Ops",
            "courses": "https://hellokittyislandadventure.wiki.gg/wiki/Challenge_Courses",
            "challenge courses": "https://hellokittyislandadventure.wiki.gg/wiki/Challenge_Courses",
            "fwish": "https://hellokittyislandadventure.wiki.gg/wiki/Fwishing_Well",
            "fwishing well": "https://hellokittyislandadventure.wiki.gg/wiki/Fwishing_Well",
            "rain": "https://hellokittyislandadventure.wiki.gg/wiki/Weather",
            "steam": "https://hellokittyislandadventure.wiki.gg/wiki/Weather",
            "starfall": "https://hellokittyislandadventure.wiki.gg/wiki/Weather",
            "stars": "https://hellokittyislandadventure.wiki.gg/wiki/Weather",
            "achievement": "https://hellokittyislandadventure.wiki.gg/wiki/Achievements",
            "achievements": "https://hellokittyislandadventure.wiki.gg/wiki/Achievements",
            "collection": "https://hellokittyislandadventure.wiki.gg/wiki/Collections",
            "collections": "https://hellokittyislandadventure.wiki.gg/wiki/Collections",
            "mini game": "https://hellokittyislandadventure.wiki.gg/wiki/Mini_Games",
            "mini games": "https://hellokittyislandadventure.wiki.gg/wiki/Mini_Games",
            "mini-game": "https://hellokittyislandadventure.wiki.gg/wiki/Mini_Games",
            "mini-games": "https://hellokittyislandadventure.wiki.gg/wiki/Mini_Games",
            "game": "https://hellokittyislandadventure.wiki.gg/wiki/Mini_Games",
            "hat": "https://hellokittyislandadventure.wiki.gg/wiki/Hats",
            "hats": "https://hellokittyislandadventure.wiki.gg/wiki/Hats",
            "shirt": "https://hellokittyislandadventure.wiki.gg/wiki/Shirts",
            "shirts": "https://hellokittyislandadventure.wiki.gg/wiki/Shirts",
            "jacket": "https://hellokittyislandadventure.wiki.gg/wiki/Shirts",
            "jackets": "https://hellokittyislandadventure.wiki.gg/wiki/Shirts",
            "dresses": "https://hellokittyislandadventure.wiki.gg/wiki/Outfits",
            "dress": "https://hellokittyislandadventure.wiki.gg/wiki/Outfits",
            "outfits": "https://hellokittyislandadventure.wiki.gg/wiki/Outfits",
            "pants": "https://hellokittyislandadventure.wiki.gg/wiki/Pants",
            "skirts": "https://hellokittyislandadventure.wiki.gg/wiki/Pants",
            "skirt": "https://hellokittyislandadventure.wiki.gg/wiki/Pants",
            "glasses": "https://hellokittyislandadventure.wiki.gg/wiki/Face_Accessories",
            "backpack": "https://hellokittyislandadventure.wiki.gg/wiki/Back_Accessories",
            "backpacks": "https://hellokittyislandadventure.wiki.gg/wiki/Back_Accessories",
            "badtz": "https://hellokittyislandadventure.wiki.gg/wiki/Badtz-maru",
            "cinnamoroll": "https://hellokittyislandadventure.wiki.gg/wiki/Cinnamoroll",
            "tuxedosam": "https://hellokittyislandadventure.wiki.gg/wiki/Tuxedosam",
            "kiki": "https://hellokittyislandadventure.wiki.gg/wiki/Kiki",
            "lala": "https://hellokittyislandadventure.wiki.gg/wiki/Lala",
            "month of meh": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "meh": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "give and gather": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "give & gather": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "holiday gift": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "jam jamboree": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "jam": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "cds": "https://hellokittyislandadventure.wiki.gg/wiki/Music_Discs",
            "cd": "https://hellokittyislandadventure.wiki.gg/wiki/Music_Discs",
            "music disc": "https://hellokittyislandadventure.wiki.gg/wiki/Music_Discs",
            "music discs": "https://hellokittyislandadventure.wiki.gg/wiki/Music_Discs",
            "disc": "https://hellokittyislandadventure.wiki.gg/wiki/Music_Discs",
            "discs": "https://hellokittyislandadventure.wiki.gg/wiki/Music_Discs",
            "50th": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "jubilee": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "lantern": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "haven": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "days of plenty": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "sea": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "parade": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "sunshine": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "festival": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "celebration": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "colorblaze": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "springtime": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "frenzy": "https://hellokittyislandadventure.wiki.gg/wiki/Events",
            "nul": "https://hellokittyislandadventure.wiki.gg/wiki/Nuls",
            "nuls": "https://hellokittyislandadventure.wiki.gg/wiki/Nuls",
            "abilities": "https://hellokittyislandadventure.wiki.gg/wiki/Companion_Abilities",
            "ability": "https://hellokittyislandadventure.wiki.gg/wiki/Companion_Abilities",
            "companion abilities": "https://hellokittyislandadventure.wiki.gg/wiki/Companion_Abilities",
            "companion": "https://hellokittyislandadventure.wiki.gg/wiki/Companion_Abilities",
            "island spirit": "https://hellokittyislandadventure.wiki.gg/wiki/Island_Spirit",
            "spirit": "https://hellokittyislandadventure.wiki.gg/wiki/Spirit_Hearts",
            "spirit heart": "https://hellokittyislandadventure.wiki.gg/wiki/Spirit_Hearts",
            "spirit hearts": "https://hellokittyislandadventure.wiki.gg/wiki/Spirit_Hearts",
            "best friend": "https://hellokittyislandadventure.wiki.gg/wiki/Best_Friends",
            "comic": "https://hellokittyislandadventure.wiki.gg/wiki/Comic_Books",
            "comics": "https://hellokittyislandadventure.wiki.gg/wiki/Comic_Books",
            "comic book": "https://hellokittyislandadventure.wiki.gg/wiki/Comic_Books",
            "comic books": "https://hellokittyislandadventure.wiki.gg/wiki/Comic_Books",
            "complete set": "https://hellokittyislandadventure.wiki.gg/wiki/Complete_Set_(Comics)",
            "complete sets": "https://hellokittyislandadventure.wiki.gg/wiki/Complete_Set_(Comics)",

            }

# Define the default homepage URL
default_wiki_url = "https://hellokittyislandadventure.wiki.gg"

# Function to search the wiki for relevant pages
def search_wiki(query):
    query = query.lower()  # Convert query to lowercase for case-insensitive matching
    if query in wiki_urls:
        return [wiki_urls[query]]
    else:
        return [default_wiki_url]

# Function to extract relevant keywords from post text
def extract_keywords(post_title, post_body):
    keywords = []
    combined_text = f"{post_title} {post_body}".lower()  # Convert combined text to lowercase
    
    for term in wiki_urls:
        if re.search(r'\b' + re.escape(term) + r'\b', combined_text, re.IGNORECASE):
            keywords.append(term)
    
    return keywords

# Function to check if the bot has already replied to a post
def has_bot_replied(post, bot_username):
    post.comments.replace_more(limit=0)
    for comment in post.comments.list():
        if comment.author and comment.author.name == bot_username:
            return True
    return False

import time

# Rate limit to 30 requests per minute (i.e., 2 requests per 5 seconds)
RATE_LIMIT = 2  # Requests per 5 seconds
SLEEP_TIME = 5 / RATE_LIMIT  # Adjust sleep time accordingly

# Function to process posts and search wiki
def process_posts():
    keywords = ["how", "help", "what", "where", "tag", "icon", "?", "why", "location"]
    for post in subreddit.new(limit=25):
        print(f"Checking post: {post.title}")
        if has_bot_replied(post, "hkiawiki-bot"):
            print(f"The bot has already replied to this post. No action taken.")
            continue

        title = post.title.lower()
        if any(keyword in title for keyword in keywords):
            print(f"Processing post: {post.title}")
            
            keywords_found = extract_keywords(post.title, post.selftext)
            if keywords_found:
                print(f"Keywords found: {', '.join(keywords_found)}")
                unique_links = set()

                for keyword in keywords_found:
                    wiki_links = search_wiki(keyword)
                    unique_links.update(wiki_links)
                
                unique_links = list(unique_links)
                if default_wiki_url in unique_links and len(unique_links) > 1:
                    unique_links.remove(default_wiki_url)

                if unique_links:
                    reply_message = "Hi there, it's HKIA Wiki Bot! Here are some links that might help you:\n\n"
                    reply_message += "\n".join(f"- [{url.split('/')[-1].replace('_', ' ')}]({url})" for url in unique_links)
                    reply_message += "\n\nIf you need more information, feel free to check out the [Hello Kitty Island Adventure Wiki]({}).".format(default_wiki_url)
                    reply_message += "\n\n^*Note:* ^*I* ^*want* ^*to* ^*identify* ^*users* ^*who* ^*might* ^*need* ^*my* ^*help,* ^*sorry* ^*if* ^*I* ^*got* ^*confused* ^*(^*I'm* ^*just* ^*a* ^*lil* ^*robot* ^*<3^*)*!"
                    print(f"Replying to post: {reply_message}")
                    print(f"Found relevant links: {unique_links}")
                    # Uncomment the line below to enable replying
                    #post.reply(reply_message)
                    time.sleep(SLEEP_TIME)  # Add a delay to avoid exceeding rate limits

                else:
                    reply_message = "Hi there, it's HKIA Wiki Bot! I couldn't find a specific link for your query, but you can explore more on the [Hello Kitty Island Adventure Wiki]({}).".format(default_wiki_url)
                    reply_message += "\n\n^*Note:* ^*I* ^*want* ^*to* ^*identify* ^*users* ^*who* ^*might* ^*need* ^*my* ^*help,* ^*sorry* ^*if* ^*I* ^*got* ^*confused* ^*(^*I'm* ^*just* ^*a* ^*lil* ^*robot* ^*<3^*)*!"
                    print(f"Replying to post: {reply_message}")
                    print(f"Redirecting to homepage: {default_wiki_url}")
                    # Uncomment the line below to enable replying
                    #post.reply(reply_message)
                    time.sleep(SLEEP_TIME)  # Add a delay to avoid exceeding rate limits

            else:
                reply_message = "Hi there, it's HKIA Wiki Bot! I couldn't find a specific link for your query, but you can explore more on the [Hello Kitty Island Adventure Wiki]({}).".format(default_wiki_url)
                reply_message += "\n\n^*Note:* ^*I* ^*want* ^*to* ^*identify* ^*users* ^*who* ^*might* ^*need* ^*my* ^*help,* ^*sorry* ^*if* ^*I* ^*got* ^*confused* ^*(^*I'm* ^*just* ^*a* ^*lil* ^*robot* ^*<3^*)*!"
                print(f"Replying to post: {reply_message}")
                print(f"Redirecting to homepage: {default_wiki_url}")
                # Uncomment the line below to enable replying
                #post.reply(reply_message)
                time.sleep(SLEEP_TIME)  # Add a delay to avoid exceeding rate limits

        else:
            print(f"Post does not contain the required keywords. No action taken.")

if __name__ == "__main__":
    process_posts()
