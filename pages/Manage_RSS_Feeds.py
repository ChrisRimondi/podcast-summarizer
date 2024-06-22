import streamlit as st
from db import init_db, add_feed, remove_feed, get_feeds

#import os

# Initialize database
init_db()

st.title("Podcast Manager")

# RSS Feed Management
st.header("Manage RSS Feeds")
feed_url = st.text_input("RSS Feed URL")
friendly_name = st.text_input("Podcast Name")
if st.button("Add Feed"):
    add_feed(feed_url, friendly_name)
    st.success("Feed added successfully")

feeds = get_feeds()
feed_ids = [feed[0] for feed in feeds]
feed_urls = [feed[1] for feed in feeds]
friendly_names = [feed[2] for feed in feeds]

feed_selection = st.selectbox("Select Feed to Remove", feed_ids)
                              #, format_func=lambda x: friendly_names[x-1])
if st.button("Remove Feed"):
    remove_feed(feed_selection)
    st.success("Feed removed successfully")