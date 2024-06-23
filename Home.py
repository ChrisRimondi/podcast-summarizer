import streamlit as st
from db import init_db, get_feeds, add_episode, get_episodes, update_episode_transcription, update_episode_summary
from utils import fetch_feed_episodes, download_episode, convert_mp3_to_wav
from transcribe import transcribe_audio_locally
from summarize import summarize_transcription
#import os

# Initialize database
init_db()

st.title("Podcast Manager")


feeds = get_feeds()
feed_ids = [feed[0] for feed in feeds]
feed_urls = [feed[1] for feed in feeds]
friendly_names = [feed[2] for feed in feeds]
ids_urls = [(feed[0], feed[1]) for feed in feeds]


# List Episodes
st.header("Episodes")
selected_feed_id = st.selectbox("Select Feed to List Episodes", feed_ids, format_func=lambda x: friendly_names[x-1])

if selected_feed_id:
    episodes = get_episodes(selected_feed_id, 5)
    if not episodes:
        # Fetch episodes from the feed and store them in the database if they don't exist
        feed_url = dict(ids_urls)[selected_feed_id]
        feed_episodes = fetch_feed_episodes(feed_url)
        for title, link, published, enclosures_href in feed_episodes:
            add_episode(selected_feed_id, title, link, published, enclosures_href)
        episodes = get_episodes(selected_feed_id, 5)
    
    # Debug: Print all episodes fetched
    #st.write("All Episodes:", episodes)
    
    # Sort episodes by published date and select the last 5
    episodes = sorted(episodes, key=lambda x: x[4], reverse=True)[:5]
    
    # Debug: Print the selected last 5 episodes
    #st.write("Last 5 Episodes:", episodes)
    
    for episode in episodes:
        episode_id, feed_id, title, link, published, transcription, summary, enclosures_href = episode
        st.subheader(title)
        st.write(f"Published: {published}")
        st.write(f"[Link to Episode]({link})")

        if transcription:
            with st.expander("Show Transcript"):
                st.text_area(transcription)
        else:
            if st.button(f"Transcribe Episode {episode_id}"):
                mp3_path = f"data/podcasts/episode_{episode_id}.mp3"
                wav_path = f"data/podcasts/episode_{episode_id}.wav"
                download_episode(enclosures_href, mp3_path)
                convert_mp3_to_wav(mp3_path, wav_path)
                transcription = transcribe_audio_locally(wav_path)
                update_episode_transcription(episode_id, transcription.strip())
                st.success("Transcription completed")
                # Refresh the page to show the transcription
                st.experimental_rerun()

        if summary:
            with st.expander("Show Summary"):
                st.markdown(summary.replace('\\n', '\n'))
        else:
            if transcription and st.button(f"Summarize Episode {episode_id}"):
                summary = summarize_transcription(transcription)
                update_episode_summary(episode_id, summary.strip())
                st.success("Summarization completed")
                # Refresh the page to show the summary
                st.experimental_rerun()



