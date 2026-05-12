#author: Aldyth Nahak
#description: A Streamlit app that uses Gemini API to recommend songs based on user's mood and genre preferences. It integrates with Spotify to display album covers and play songs. The app features a chat interface where users can describe their vibe, and the AI responds with song recommendations. It also includes a sidebar for selecting mood, genre, and assistant mode (Normal AI or DJ Mode). The app is styled with custom CSS and includes Lottie animations for a dynamic user experience.
# Note: Remember to set your Gemini API key and Spotify credentials in the .env file before running the app.
# Required environment variables:
# GEMINI_API_KEY=your_gemini_api_key
# SPOTIFY_CLIENT_ID=your_spotify_client_id
# SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
# To run the app, use the command: streamlit run app.py

# ================= IMPORTS =================
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import requests
import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
from streamlit_lottie import st_lottie

# ================= CONFIG =================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

st.set_page_config(
    page_title="MoodTune AI 🎧",
    page_icon="🎵",
    layout="wide"
)

# ================= SAFE MODEL FALLBACK =================
AVAILABLE_MODELS = [
    "gemini-2.5-flash"
]

def generate_ai_response(prompt):
    for model_name in AVAILABLE_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text, model_name
        except Exception:
            continue

    return "⚠️ No available Gemini model found.", None

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
)

# ================= LOTTIE =================
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

music_lottie = load_lottie(
    "https://assets10.lottiefiles.com/packages/lf20_jtbfg2nb.json"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.stApp {
    background-color: #0b0c10;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #12141c;
}

/* Title */
.main-title {
    font-size: 50px;
    font-weight: bold;
    color: white;
}

/* Subtitle */
.subtitle {
    color: #9ca3af;
    margin-bottom: 30px;
}

/* Music cards */
.music-card {
    background: linear-gradient(145deg, #171923, #11131a);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #262a36;
    margin-bottom: 15px;
    transition: 0.3s;
}

.music-card:hover {
    border: 1px solid #1db954;
    transform: scale(1.02);
}

/* Spotify button */
.spotify-btn {
    display: inline-block;
    margin-top: 10px;
    background-color: #1db954;
    color: black;
    padding: 8px 12px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: bold;
}

/* Chat bubble */
.user-msg {
    background-color: #1db954;
    color: black;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.ai-msg {
    background-color: #1f2430;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}
            
iframe {
    border-radius: 16px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="main-title">🎧 MoodTune AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Your Personal AI Music Assistant</div>',
        unsafe_allow_html=True
    )

with col2:
    if music_lottie:
        st_lottie(music_lottie, height=140)

# ================= SIDEBAR =================
st.sidebar.title("🎛️ DJ Controls")

mood = st.sidebar.selectbox(
    "Select Mood",
    ["Chill", "Happy", "Sad", "Workout", "Focus", "Romantic"]
)

genre = st.sidebar.selectbox(
    "Genre",
    ["Any", "Lo-fi", "Pop", "Rock", "Jazz", "EDM", "K-Pop"]
)

mode = st.sidebar.radio(
    "Assistant Mode",
    ["Normal AI", "🎙️ DJ Mode"]
)

# ================= MUSIC CARD =================
def music_card(song, artist):
    try:

        query = f"track:{song} artist:{artist}"

        result = spotify.search(
            q=query,
            type="track",
            limit=1
        )

        tracks = result["tracks"]["items"]

        if not tracks:
            st.warning(f"No Spotify result: {song} - {artist}")
            return

        track = tracks[0]

        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        album_cover = track["album"]["images"][0]["url"]
        track_id = track["id"]

        # Album cover card
        st.markdown( f""" <div class="music-card"> <img src="{album_cover}" width="100%"> <div>🎵 {track_name}</div> <div>👤 {artist_name}</div> </div> """, unsafe_allow_html=True )

        # Spotify embed
        st.components.v1.html(
            f"""
            <iframe
                style="border-radius:12px"
                src="https://open.spotify.com/embed/track/{track_id}"
                width="100%"
                height="152"
                frameBorder="0"
                allowfullscreen=""
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                loading="lazy">
            </iframe>
            """,
            height=170
        )

    except Exception as e:
        st.error(f"Spotify Error: {e}")

# ================= RECOMMENDED =================
st.subheader("🔥 Trending Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    music_card("seasons", "Wave to Earth")

with col2:
    music_card("XXL", "LANY")

with col3:
    music_card("Different Lives", "Fly By Midnight")

# ================= CHAT =================
def parse_songs(text):
    songs = []

    lines = text.strip().splitlines()

    for line in lines:

        # remove numbering
        line = re.sub(r'^\d+\.\s*', '', line)

        # remove bullets
        line = line.replace("•", "").strip()

        # support "by"
        if " - " in line:
            parts = line.split(" - ", 1)

        elif " by " in line.lower():
            parts = re.split(r' by ', line, flags=re.IGNORECASE)

        else:
            continue

        if len(parts) >= 2:
            song = parts[0].strip()
            artist = parts[1].strip()

            songs.append((song, artist))

    return songs

st.subheader("💬 Chat with MoodTune AI")

if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:

    if msg["role"] == "You":
        st.chat_message("user").write(msg["content"])

    else:
        st.chat_message("assistant").write(
            f"🎧 I created a {mood.lower()} {genre.lower()} playlist for you below."
        )

# ================= AI PLAYLIST =================
if "playlist" not in st.session_state:
    st.info(
        "🎵 Describe your mood and MoodTune AI will create your perfect playlist."
    )

if "playlist" in st.session_state:

    st.subheader("🎧 Your AI Playlist")

    playlist = st.session_state["playlist"]

    cols = st.columns(3)

    for idx, (song, artist) in enumerate(playlist):

        with cols[idx % 3]:
            music_card(song, artist)

# ================= MODEL INFO =================

if "last_model" in st.session_state:
    st.caption(
        f"⚡ Powered by {st.session_state['last_model']}"
    )

prompt = st.chat_input("Tell me your vibe...")

if prompt:
    st.session_state.chat.append({
        "role": "You",
        "content": prompt
    })

    system_prompt = f"""
    You are MoodTune AI, an AI music recommendation assistant.

    Current settings: 
        - Mood: {mood} 
        - Genre: {genre} 
        - Mode: {mode}

    TASK:
    Recommend EXACTLY 3 REAL songs available on Spotify.

    IMPORTANT: 
        - If the user mentions an artist, band, or song, prioritize songs from that artist OR songs with very similar vibes. 
        - Match the user's requested mood and genre.

    STRICT OUTPUT RULES: 
        - Return ONLY 3 lines 
        - One song per line 
        - Format MUST be: Song Name - Artist Name 
    
    DO NOT: 
    - add numbering 
    - add bullet points 
    - add explanations 
    - add emojis 
    - add intro/outro text 
    - add markdown

    GOOD EXAMPLE:
    XXL - LANY
    Seasons - Wave to Earth
    Baby - Justin Bieber
    """

    if mode == "🎙️ DJ Mode":
        system_prompt += """

        EXTRA:
        Match energetic radio DJ vibes internally
        while still following strict output format.
        """

    full_prompt = system_prompt + "\nUser: " + prompt

    with st.spinner("🎵 Finding perfect songs..."):
        reply, used_model = generate_ai_response(full_prompt)

    st.write("DEBUG AI RESPONSE:")
    st.code(reply)

    # Save chat
    st.session_state.chat.append({
        "role": "AI",
        "content": reply
    })

    # Parse songs from AI response
    songs = parse_songs(reply)
    # st.write("PARSED SONGS:", songs)

    # Save playlist separately
    st.session_state["playlist"] = songs

    st.session_state["last_model"] = used_model

    st.rerun()