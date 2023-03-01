import instaloader
import pandas as pd
#creating an instance of instaLoader
bot = instaloader.Instaloader()
bot.login(user="flick_chiri", passwd="R3m3mb3rm3$")
#loading a profile from an instagram handle 
profile = instaloader.Profile.from_username(bot.context, 'tappi_app')
posts = profile.get_posts()
#iterating through the list and getting all the posts from it 
for index, post in enumerate(posts, 1):
    bot.download_post(post, target=f"{profile.username}_{index}")
