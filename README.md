# 🎧 MoodTune AI

MoodTune AI is an AI-powered music recommendation chatbot built using Streamlit, Gemini API, and Spotify API.

The app analyzes the user's mood, genre preference, and prompts to generate personalized song recommendations with playable Spotify embeds.

<img width="1511" height="903" alt="Screenshot 2026-05-12 at 6 21 09 PM" src="https://github.com/user-attachments/assets/22751a7d-7410-46bd-9050-62151b5cf20b" />

---

# ✨ Features

* 🤖 AI Music Recommendation using Gemini
* 🎵 Spotify Embedded Music Player
* 🎧 Mood-based Playlist Generator
* 🎙️ DJ Mode for energetic recommendations
* 🎨 Modern Spotify-inspired UI
* 💬 Chat-style interaction
* 🔥 Trending recommendation section
* 🖼️ Album cover previews
* ⚡ Fast Gemini integration

---

# 🛠️ Tech Stack

* Python
* Streamlit
* Gemini API
* Spotify API
* Spotipy
* Streamlit Lottie
* HTML/CSS

---

# 📦 Installation

## 1. Clone Repository

```bash
git clone https://github.com/AldythNahak/MoodTune_AI.git
cd MoodTune_AI
```

---

## 2. Create Virtual Environment (Optional)

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the root folder.

```env
GEMINI_API_KEY=your_gemini_api_key

SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

---

# 🤖 Gemini API Setup

1. Open Google AI Studio
   https://aistudio.google.com/

2. Create API Key

3. Copy the API key into `.env`

---

# 🎵 Spotify API Setup

1. Open Spotify Developer Dashboard
   https://developer.spotify.com/dashboard

2. Create an App

3. Copy:

* Client ID
* Client Secret

4. Paste into `.env`

No OAuth login required because this project uses Spotify Client Credentials.

---

# ▶️ Run The App

```bash
streamlit run app.py
```

---

# 🎯 Example Prompts

```text
Give me chill songs like wave to earth

Sad songs for midnight drive

Workout EDM playlist

Romantic jazz music

Songs similar to Joji
```

---

# 📂 Project Structure

```text
MoodTune_AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
```

---

# 📌 Requirements

Example `requirements.txt`

```txt
streamlit
google-genai
python-dotenv
requests
spotipy
streamlit-lottie
```

---

# 🚀 Future Improvements

* Spotify OAuth Login
* Playlist Save to Spotify
* Music History Memory
* AI Mood Detection
* Voice Assistant
* Lyrics Integration
* YouTube Music Support

---

# 👨‍💻 Author

Developed by *Aldyth Nahak*
[GitHub](https://github.com/AldythNahak) | [LinkedIn](https://linkedin.com/in/aldythnahak)
---

# 📄 License

This project is for training "Maju Bareng AI for Data Scientists | 9 may | LLM - Based Tools and Gemini API Integration for Data Scientists" Final Project purposes.
