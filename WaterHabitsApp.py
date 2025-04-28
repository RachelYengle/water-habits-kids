# WATER HABITS FOR KIDS - Unified Streamlit App

import streamlit as st
import pandas as pd
import base64, pathlib
import random
from openai import OpenAI

# ---- CONFIG ----
st.set_page_config(page_title="Water Habits for Kids", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---- LOAD DATA ----
tips_df = pd.read_csv("expanded_tips_data.csv")

# ---- BACKGROUND FIX ----
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---- IMAGE BASE64 ENCODER ----
def img_to_base64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()

# ---- SESSION STATE ----
if 'tips_used' not in st.session_state:
    st.session_state.tips_used = 0
if 'last_tip' not in st.session_state:
    st.session_state.last_tip = ""
if 'tip_history' not in st.session_state:
    st.session_state.tip_history = []
if 'page' not in st.session_state:
    st.session_state.page = "home"

# ---- GLOBAL CARD STYLE ----
st.markdown("""
    <style>
        .feature-card {
            background-color: rgba(255, 255, 255, 0.85);
            color: #003344;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 4px 6px 12px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease;
        }
        .feature-card:hover {
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

# ---- NAV BAR ----
col_logo, col_nav = st.columns([1, 5])

with col_logo:
    st.image("static/Logo.png", width=120)

with col_nav:
    nav_choice = st.columns(3)

    with nav_choice[0]:
        if st.button("🏠 Home", key="home_btn"):
            st.session_state.page = "home"
    with nav_choice[1]:
        if st.button("👨‍🏫 About Us", key="about_btn"):
            st.session_state.page = "about"
    with nav_choice[2]:
        if st.button("💧 Water Goals", key="goals_btn"):
            st.session_state.page = "goals"

# ---- Inject NAVIGATION STYLE ----
st.markdown("""
    <style>
        div.stButton > button {
            background-color: #0a4c86;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            height: 50px;
            width: 100%;
            border: none;
            font-size: 18px;
            transition: background-color 0.3s, transform 0.2s;
        }
        div.stButton > button:hover {
            background-color: #1565c0;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# ---- PAGE SELECTION ----
page = st.session_state.page

# ---- BUBBLE ANIMATION ----
unique_id = random.randint(1, 999999)  # Unique id for each bubble load

# Inject bubble animation and CSS
st.markdown(f"""
    <style>
        .bubble {{
            position: absolute;
            bottom: -50px;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 50%;
            opacity: 0.8;
            animation: bubbleUp 10s forwards;
            z-index: 0;
        }}

        @keyframes bubbleUp {{
            0% {{
                transform: translateY(0) scale(0.8);
                opacity: 0.8;
            }}
            100% {{
                transform: translateY(-1200px) scale(1.5);
                opacity: 0;
            }}
        }}

        .bubble-container {{
            position: fixed;
            width: 100%;
            height: 100%;
            overflow: hidden;
            pointer-events: none;
            top: 0;
            left: 0;
            z-index: 0;
        }}
    </style>

    <div class="bubble-container" id="bubble-{unique_id}">
        <div class="bubble" style="left:5%; width:25px; height:25px;"></div>
        <div class="bubble" style="left:15%; width:30px; height:30px;"></div>
        <div class="bubble" style="left:30%; width:20px; height:20px;"></div>
        <div class="bubble" style="left:45%; width:35px; height:35px;"></div>
        <div class="bubble" style="left:60%; width:22px; height:22px;"></div>
        <div class="bubble" style="left:75%; width:28px; height:28px;"></div>
        <div class="bubble" style="left:85%; width:18px; height:18px;"></div>
        <div class="bubble" style="left:90%; width:25px; height:25px;"></div>
    </div>
""", unsafe_allow_html=True)

# ---- HOME ----
if page == "home":
    set_background("static/Background.jpg")

    st.markdown("<br><h1 style='text-align:center; color:#003344;'>💧 Welcome to Water Habits for Kids</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>💡 Water-Saving Tips</h3>
            <p>Fun, personalized tips for kids to build daily conservation habits.</p>
        """, unsafe_allow_html=True)
        if st.button("Start Tips", key="start_tips"):
            st.session_state.page = "tips"
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>📖 Eco Story + Game</h3>
            <p>Interactive story and comic adventure to save water together!</p>
        """, unsafe_allow_html=True)
        if st.button("Start Story", key="start_story"):
            st.session_state.page = "story"
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
<style>
.bubble {
    position: absolute;
    bottom: -100px;
    border-radius: 50%;
    opacity: 0.8;
    animation: bubbleUp 20s infinite;
    z-index: 0;
}

/* Lighter blue shades for bubbles */
.bubble.light {
    background-color: #cceeff; /* baby blue */
}
.bubble.medium {
    background-color: #aaddff; /* slightly deeper blue */
}
.bubble.dark {
    background-color: #88ccff; /* even a little deeper */
}

/* Infinite floating animation */
@keyframes bubbleUp {
    0% {
        transform: translateY(0) scale(0.8);
        opacity: 0.8;
    }
    50% {
        opacity: 0.5;
    }
    100% {
        transform: translateY(-1500px) scale(1.2);
        opacity: 0;
    }
}

.bubble-container {
    position: fixed;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
    top: 0;
    left: 0;
    z-index: 0;
}
</style>

<div class="bubble-container">
    <div class="bubble light" style="left:5%; width:20px; height:20px; animation-delay: 0s;"></div>
    <div class="bubble medium" style="left:15%; width:35px; height:35px; animation-delay: 5s;"></div>
    <div class="bubble dark" style="left:30%; width:25px; height:25px; animation-delay: 2s;"></div>
    <div class="bubble light" style="left:45%; width:40px; height:40px; animation-delay: 7s;"></div>
    <div class="bubble medium" style="left:60%; width:18px; height:18px; animation-delay: 3s;"></div>
    <div class="bubble dark" style="left:75%; width:30px; height:30px; animation-delay: 6s;"></div>
    <div class="bubble light" style="left:85%; width:22px; height:22px; animation-delay: 4s;"></div>
    <div class="bubble medium" style="left:90%; width:28px; height:28px; animation-delay: 1s;"></div>
</div>
""", unsafe_allow_html=True)

# ---- ABOUT US ----
elif page == "about":
    set_background("static/Background.jpg")

    # Load images
    sjsu_b64 = img_to_base64("static/sjsu_logo.png")
    photo_b64 = img_to_base64("static/Photo4.jpg")

    # ---- Custom Fade-In Styles (ONLY card & images fade, NOT bubbles)
    st.markdown("""
    <style>
        /* Fade-in Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .about-card, .about-image {
            animation: fadeIn 1.5s ease-out;
        }

        .about-card {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            max-width: 1000px;
            margin: 2rem auto;
        }

        .about-text {
            color: black;
            font-size: 18px;
            line-height: 1.6;
        }

        h1, h2, h3 {
            color: black;
        }

        .about-image {
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .about-image-caption {
            text-align: center;
            color: #003344;
            font-weight: bold;
            margin-top: 10px;
            font-size: 18px;
        }

        .about-image:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
<style>
.bubble {
    position: absolute;
    bottom: -100px;
    border-radius: 50%;
    opacity: 0.8;
    animation: bubbleUp 20s infinite;
    z-index: 0;
}

/* Lighter blue shades for bubbles */
.bubble.light {
    background-color: #cceeff; /* baby blue */
}
.bubble.medium {
    background-color: #aaddff; /* slightly deeper blue */
}
.bubble.dark {
    background-color: #88ccff; /* even a little deeper */
}

/* Infinite floating animation */
@keyframes bubbleUp {
    0% {
        transform: translateY(0) scale(0.8);
        opacity: 0.8;
    }
    50% {
        opacity: 0.5;
    }
    100% {
        transform: translateY(-1500px) scale(1.2);
        opacity: 0;
    }
}

.bubble-container {
    position: fixed;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
    top: 0;
    left: 0;
    z-index: 0;
}
</style>

<div class="bubble-container">
    <div class="bubble light" style="left:5%; width:20px; height:20px; animation-delay: 0s;"></div>
    <div class="bubble medium" style="left:15%; width:35px; height:35px; animation-delay: 5s;"></div>
    <div class="bubble dark" style="left:30%; width:25px; height:25px; animation-delay: 2s;"></div>
    <div class="bubble light" style="left:45%; width:40px; height:40px; animation-delay: 7s;"></div>
    <div class="bubble medium" style="left:60%; width:18px; height:18px; animation-delay: 3s;"></div>
    <div class="bubble dark" style="left:75%; width:30px; height:30px; animation-delay: 6s;"></div>
    <div class="bubble light" style="left:85%; width:22px; height:22px; animation-delay: 4s;"></div>
    <div class="bubble medium" style="left:90%; width:28px; height:28px; animation-delay: 1s;"></div>
</div>
""", unsafe_allow_html=True)

    # ---- About Us Header
    st.markdown("<h1 style='text-align:center; color:black;'>👨‍🏫 About Us</h1>", unsafe_allow_html=True)

    # ---- Side-by-side layout for logo and photo
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown(f"""
        <div style="text-align:center;">
            <img src="data:image/png;base64,{sjsu_b64}" class="about-image" style="width:100px;">
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="text-align:center;">
            <img src="data:image/jpeg;base64,{photo_b64}" class="about-image">
            <div class="about-image-caption">
                Front Row (L–R): Andy Nguyen, Bella Le, Gisselle Picho<br>
                Back Row (L–R): Rachel Yengle, Shreya Sobti
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---- Floating Card Text
    st.markdown("""
    <div class="about-card">
    <div class="about-text">

    We’re a team of students from **San José State University** who are passionate about teaching children sustainable water habits through play and interactive storytelling.

    🌍 **Our Mission:**  
    Our mission is to inspire young minds to become lifelong champions of water conservation.  
    We believe that children are not just the leaders of tomorrow — they are powerful change-makers today. Through fun, interactive learning, we aim to nurture a sense of responsibility, creativity, and care for our planet’s most precious resource: water.  
    By making sustainability exciting and accessible, we hope to plant seeds of awareness that grow into a future where every drop counts.

    ✨ **About Water Habits for Kids:**  
    *Water Habits for Kids* is an educational platform created with young learners in mind.  
    Designed for children between the ages of 3–12, it blends playful storytelling, real-world tips, and interactive challenges to make saving water a natural and enjoyable part of everyday life.

    💧 **Fun Fact:**  
    Turning off the tap while brushing your teeth can save up to 8 gallons of water every day!

    🌊 **Why It Matters:**  
    Teaching children about water conservation from an early age is crucial because the habits they form now will shape the future of our planet.  
    Water is one of our most precious resources, yet it's often taken for granted.  
    By helping kids understand the value of every drop, we empower them to make smarter choices that reduce waste, protect ecosystems, and ensure clean water is available for generations to come.

    👉 Thank you for visiting our project — together, let's make every drop count! 🌱

    </div>
    </div>
    """, unsafe_allow_html=True)

# ---- WATER GOALS ----
elif page == "goals":
    set_background("static/Background.jpg")

    # Load images
    yard_img_b64 = img_to_base64("static/Kids_in_Yard.jpg")
    bathroom_img_b64 = img_to_base64("static/Kids_in_Bathroom.jpg")

    # Floating card + image styles (no bubble CSS because it's already injected globally)
    st.markdown("""
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .goals-card, .goal-image {
            animation: fadeIn 1.5s ease-out;
        }

        .goals-card {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            max-width: 1000px;
            margin: 2rem auto;
        }

        .goals-text {
            color: black;
            font-size: 18px;
            line-height: 1.6;
        }

        .goal-image {
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .goal-image:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }

        .goal-image-caption {
            text-align: center;
            color: #003344;
            font-weight: bold;
            margin-top: 10px;
            font-size: 18px;
        }

        h1, h2, h3 {
            color: black;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<style>
.bubble {
    position: absolute;
    bottom: -100px;
    border-radius: 50%;
    opacity: 0.8;
    animation: bubbleUp 20s infinite;
    z-index: 0;
}

/* Lighter blue shades for bubbles */
.bubble.light {
    background-color: #cceeff; /* baby blue */
}
.bubble.medium {
    background-color: #aaddff; /* slightly deeper blue */
}
.bubble.dark {
    background-color: #88ccff; /* even a little deeper */
}

/* Infinite floating animation */
@keyframes bubbleUp {
    0% {
        transform: translateY(0) scale(0.8);
        opacity: 0.8;
    }
    50% {
        opacity: 0.5;
    }
    100% {
        transform: translateY(-1500px) scale(1.2);
        opacity: 0;
    }
}

.bubble-container {
    position: fixed;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
    top: 0;
    left: 0;
    z-index: 0;
}
</style>

<div class="bubble-container">
    <div class="bubble light" style="left:5%; width:20px; height:20px; animation-delay: 0s;"></div>
    <div class="bubble medium" style="left:15%; width:35px; height:35px; animation-delay: 5s;"></div>
    <div class="bubble dark" style="left:30%; width:25px; height:25px; animation-delay: 2s;"></div>
    <div class="bubble light" style="left:45%; width:40px; height:40px; animation-delay: 7s;"></div>
    <div class="bubble medium" style="left:60%; width:18px; height:18px; animation-delay: 3s;"></div>
    <div class="bubble dark" style="left:75%; width:30px; height:30px; animation-delay: 6s;"></div>
    <div class="bubble light" style="left:85%; width:22px; height:22px; animation-delay: 4s;"></div>
    <div class="bubble medium" style="left:90%; width:28px; height:28px; animation-delay: 1s;"></div>
</div>
""", unsafe_allow_html=True)

    # Water-Saving Goals Header
    st.markdown("<h1 style='text-align:center; color:black;'>🌍 Water-Saving Goals</h1>", unsafe_allow_html=True)

    # First Image
    st.markdown(f"""
    <div style="text-align:center;">
        <img src="data:image/jpeg;base64,{yard_img_b64}" class="goal-image">
        <div class="goal-image-caption">Learning Rainwater Collection</div>
    </div>
    """, unsafe_allow_html=True)

    # First Floating Card (Journey, Problem, Solution)
    st.markdown("""
    <div class="goals-card">
    <div class="goals-text">

    ### Our Journey to Building Water Habits for Kids 🌱

    Our team started this project with one simple question:  
    *How can we teach young children the importance of water conservation in a way that truly sticks?*

    We realized that while many resources exist for adults, few tools truly engage children — especially through fun and empowerment.

    ### Understanding the Problem 🚰
    - Kids respond better to **short, achievable actions** they can control.
    - **Positive reinforcement** boosts motivation.
    - **Stories and characters** help emotional connection.

    These insights shaped our goal: an interactive app where kids don't just learn — they **become water heroes**.

    ### Building the Solution 💡
    **Water Habits for Kids** is designed to make small daily conservation habits fun and meaningful.

    </div>
    </div>
    """, unsafe_allow_html=True)

    # Second Image
    st.markdown(f"""
    <div style="text-align:center;">
        <img src="data:image/jpeg;base64,{bathroom_img_b64}" class="goal-image">
        <div class="goal-image-caption">Practicing Water-Saving at Home</div>
    </div>
    """, unsafe_allow_html=True)

    # Second Floating Card (Water Goals Feature + Mission)
    st.markdown("""
    <div class="goals-card">
    <div class="goals-text">

    ### Why We Created Water Goals 🎯
    Setting a goal gives kids ownership and pride in saving water!

    - Children pick one small daily action.
    - They track progress.
    - They celebrate success.

    ### Our Mission 🌎
    To empower young generations to protect water through everyday choices — one small, joyful goal at a time.

    👉 Thank you for being part of the change! 🌱

    </div>
    </div>
    """, unsafe_allow_html=True)

# ---- TIPS PAGE ----
elif page == "tips":
    set_background("static/Background.jpg")

    # Bubble animation already global
    # Only light fade-in for content if needed (optional)

    st.markdown("""
        <style>
        /* Tips page clean style */
        .stApp {
            background-color: #d6f9ff;
        }

        .custom-header, .custom-subheader {
            color: #002244 !important;
        }

        label, .stTextInput>label, .stSlider>label, .stSelectbox>label {
            color: #002244 !important;
            font-weight: bold !important;
        }

        .tip-box, .custom-info, .most-recent {
            background-color: #e0f7fa;
            color: #002244;
            border-radius: 10px;
            padding: 1rem;
            font-weight: bold;
        }

        /* Button styling navy */
        .stButton>button {
            background-color: #0a4c86;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5rem 1.5rem;
        }
        .stButton>button:hover {
            background-color: #083d6d;
        }

        /* Child age slider dark navy text */
        .stSlider>div>div>div>div {
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='custom-header'>💡 Personalized Water-Saving Tip</h2>", unsafe_allow_html=True)

    st.markdown("""
<style>
.bubble {
    position: absolute;
    bottom: -100px;
    border-radius: 50%;
    opacity: 0.8;
    animation: bubbleUp 20s infinite;
    z-index: 0;
}

/* Lighter blue shades for bubbles */
.bubble.light {
    background-color: #cceeff; /* baby blue */
}
.bubble.medium {
    background-color: #aaddff; /* slightly deeper blue */
}
.bubble.dark {
    background-color: #88ccff; /* even a little deeper */
}

/* Infinite floating animation */
@keyframes bubbleUp {
    0% {
        transform: translateY(0) scale(0.8);
        opacity: 0.8;
    }
    50% {
        opacity: 0.5;
    }
    100% {
        transform: translateY(-1500px) scale(1.2);
        opacity: 0;
    }
}

.bubble-container {
    position: fixed;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
    top: 0;
    left: 0;
    z-index: 0;
}
</style>

<div class="bubble-container">
    <div class="bubble light" style="left:5%; width:20px; height:20px; animation-delay: 0s;"></div>
    <div class="bubble medium" style="left:15%; width:35px; height:35px; animation-delay: 5s;"></div>
    <div class="bubble dark" style="left:30%; width:25px; height:25px; animation-delay: 2s;"></div>
    <div class="bubble light" style="left:45%; width:40px; height:40px; animation-delay: 7s;"></div>
    <div class="bubble medium" style="left:60%; width:18px; height:18px; animation-delay: 3s;"></div>
    <div class="bubble dark" style="left:75%; width:30px; height:30px; animation-delay: 6s;"></div>
    <div class="bubble light" style="left:85%; width:22px; height:22px; animation-delay: 4s;"></div>
    <div class="bubble medium" style="left:90%; width:28px; height:28px; animation-delay: 1s;"></div>
</div>
""", unsafe_allow_html=True)

    # Input fields
    child_name = st.text_input("👶 Child's Name")

    child_age = st.slider("🎂 Child's Age", min_value=3, max_value=12, value=6)

    routine = st.selectbox("🛁 Which routine?", ["Brushing Teeth", "Washing Hands", "Showering", "Bath Time", "Other"])

    def get_age_group(age):
        if 3 <= age <= 5:
            return "3–5"
        elif 6 <= age <= 8:
            return "6–8"
        else:
            return "9–12"

    # Generate Tip Button
    if st.button("✨ Generate Tip"):
        if not child_name:
            st.warning("⚠️ Please enter your child's name.")
        else:
            age_group = get_age_group(child_age)
            filtered = tips_df[(tips_df['age_group'] == age_group) & (tips_df['routine'] == routine)]

            if not filtered.empty:
                row = filtered.sample(1).iloc[0]
                base = row['kid_friendly_phrase']
                challenge = row['challenge_idea']
            else:
                base = "Always remember to turn off the water when you can!"
                challenge = "Try to use less water today!"

            prompt = f"Rewrite this for a {child_age}-year-old in a fun way: '{base}'"
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                    temperature=0.9
                )
                final_tip = response.choices[0].message.content
                st.markdown(f"""
                    <div class="tip-box">
                        💡 <strong>{final_tip}</strong><br><br>
                        🎯 <em>Challenge:</em> {challenge}
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.tip_history.append(f"{child_name} ({child_age}) - {final_tip}")
                st.session_state.last_tip = final_tip
                st.session_state.tips_used += 1
            except Exception as e:
                st.error(f"API error: {e}")

    # Tip History & Download
    if st.session_state.tips_used > 0:
        st.markdown("<h3 class='custom-subheader'>📊 Tip Progress</h3>", unsafe_allow_html=True)
        st.write(f"✅ Tips Generated: {st.session_state.tips_used}")
        st.markdown(f"<div class='most-recent'>💡 <strong>Most Recent Tip:</strong> {st.session_state.last_tip}</div>", unsafe_allow_html=True)

        tips_text = "\n".join(st.session_state.tip_history)
        st.download_button("📥 Download All My Tips", tips_text, file_name="water_tips_summary.txt")
    else:
        st.markdown("<div class='custom-info'>📝 No tips yet — generate one above!</div>", unsafe_allow_html=True)

# ---- STORY PAGE ----
elif page == "story":
    set_background("static/Background.jpg")

    # Page styling
    st.markdown("""
    <style>
        .stApp {
            background-color: #d6f4ff;
        }

        h1, h2, h3, h4, .stMarkdown, p {
            color: #002244 !important;
        }

        label, .stTextInput>label, .stSelectbox>label {
            color: #002244 !important;
            font-weight: bold !important;
        }

        /* Buttons navy blue */
        .stButton>button {
            background-color: #0a4c86;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1.5rem;
            border-radius: 10px;
        }

        .stButton>button:hover {
            background-color: #083d6d;
        }

        .stExpanderHeader {
            color: #002244 !important;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<style>
.bubble {
    position: absolute;
    bottom: -100px;
    border-radius: 50%;
    opacity: 0.8;
    animation: bubbleUp 20s infinite;
    z-index: 0;
}

/* Lighter blue shades for bubbles */
.bubble.light {
    background-color: #cceeff; /* baby blue */
}
.bubble.medium {
    background-color: #aaddff; /* slightly deeper blue */
}
.bubble.dark {
    background-color: #88ccff; /* even a little deeper */
}

/* Infinite floating animation */
@keyframes bubbleUp {
    0% {
        transform: translateY(0) scale(0.8);
        opacity: 0.8;
    }
    50% {
        opacity: 0.5;
    }
    100% {
        transform: translateY(-1500px) scale(1.2);
        opacity: 0;
    }
}

.bubble-container {
    position: fixed;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
    top: 0;
    left: 0;
    z-index: 0;
}
</style>

<div class="bubble-container">
    <div class="bubble light" style="left:5%; width:20px; height:20px; animation-delay: 0s;"></div>
    <div class="bubble medium" style="left:15%; width:35px; height:35px; animation-delay: 5s;"></div>
    <div class="bubble dark" style="left:30%; width:25px; height:25px; animation-delay: 2s;"></div>
    <div class="bubble light" style="left:45%; width:40px; height:40px; animation-delay: 7s;"></div>
    <div class="bubble medium" style="left:60%; width:18px; height:18px; animation-delay: 3s;"></div>
    <div class="bubble dark" style="left:75%; width:30px; height:30px; animation-delay: 6s;"></div>
    <div class="bubble light" style="left:85%; width:22px; height:22px; animation-delay: 4s;"></div>
    <div class="bubble medium" style="left:90%; width:28px; height:28px; animation-delay: 1s;"></div>
</div>
""", unsafe_allow_html=True)

    # Story Page Header
    st.header("📖 Eco Story Adventure + Game")

    # Inputs for the story
    hero = st.text_input("🧒 Hero’s Name", placeholder="e.g., Andy")

    setting = st.selectbox("🌍 Choose a Story Setting", ["bathroom", "garden", "school", "beach", "forest"])

    habit = st.selectbox("💧 Water Habit Focus", ["brushing teeth", "watering plants", "taking showers", "fixing leaks"])

    with st.expander("⚙️ Game Settings"):
        theme = st.radio("🎨 Visual Theme", ["Blue Drop", "Nature Kids", "Clean City", "Water Warriors"])
        hint_mode = st.checkbox("💡 Show Helpful Hints", value=True)

    # Theme background
    theme_styles = {
        "Blue Drop": {"background": "#e1f5fe", "button": "#0288d1"},
        "Nature Kids": {"background": "#e8f5e9", "button": "#388e3c"},
        "Clean City": {"background": "#eeeeee", "button": "#616161"},
        "Water Warriors": {"background": "#fbe9e7", "button": "#e64a19"}
    }

    style = theme_styles.get(theme, theme_styles["Blue Drop"])

    # Override background for this theme
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {style["background"]};
        }}
        .stButton>button {{
            background-color: {style["button"]};
            color: white;
            font-weight: bold;
            border-radius: 10px;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Generate Story Button
    if st.button("✨ Generate My Eco Adventure"):
        with st.spinner("Creating your story and game..."):
            story_prompt = (
                f"Write a fun children's story about {hero}, a young eco-hero in the {setting}, "
                f"learning to save water by practicing {habit}. Include a friendly sidekick and end with a water-saving tip."
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative children's storyteller focused on sustainability."},
                    {"role": "user", "content": story_prompt}
                ],
                max_tokens=800,
                temperature=0.8
            )

            story = response.choices[0].message.content.strip()

            # Display Story
            st.subheader("📘 Your Personalized Story")
            st.markdown(f"**{hero}'s Adventure in the {setting.capitalize()}**")
            st.write(story)

            # Game Rules Section
            st.subheader("🎮 Your Water-Saving Game")
            game_rules = {
                "brushing teeth": {
                    "challenge": "🪥 Tap to turn off the faucet while brushing.",
                    "goal": "Save 10 gallons by acting quickly!",
                    "points": "+5 per correct tap, -2 for misses."
                },
                "watering plants": {
                    "challenge": "🌿 Water only dry plants. Skip the ones already wet.",
                    "goal": "Keep your garden healthy and hydrated!",
                    "points": "+10 correct, -5 for overwatering."
                },
                "taking showers": {
                    "challenge": "🚿 Finish your shower in under 2 minutes.",
                    "goal": "Use under 5 gallons total!",
                    "points": "+2 per second saved."
                },
                "fixing leaks": {
                    "challenge": "🔧 Tap leaks before the bucket fills.",
                    "goal": "Fix 10 leaks in time!",
                    "points": "+5 per fix, -3 for missed."
                }
            }

            game = game_rules.get(habit.lower(), {
                "challenge": "💧 Make a smart water-saving choice!",
                "goal": "Reduce waste and become an Eco Hero!",
                "points": "+5 per smart move."
            })

            st.markdown(f"**Challenge:** {game['challenge']}")
            st.markdown(f"**Goal:** {game['goal']}")
            st.markdown(f"**Scoring:** {game['points']}")

            # Helpful Hints
            if hint_mode:
                with st.expander("💡 Tips & Tricks"):
                    st.markdown("""
- Turn off taps while brushing your teeth.  
- Keep showers short and sweet.  
- Fix leaky faucets quickly.  
- Water plants early morning or evening.  
- Use buckets instead of hoses when cleaning.
                    """)

            # Comic Scene Generation
            st.subheader("🎬 Your Eco Adventure Comic")
            comic_prompt = (
                f"You are a comic artist turning this children's story into a 4-6 panel comic. "
                f"Number each panel and describe each scene visually, 1–2 sentences per panel. "
                f"Apply this theme: {theme}. Story:\n{story}"
            )

            comic_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": comic_prompt}]
            )

            scene_text = comic_response.choices[0].message.content.strip()

            import re
            panel_descriptions = re.findall(r'\d\.\s.*?(?=\n\d\.|\Z)', scene_text, re.DOTALL)

            if panel_descriptions:
                for i, panel in enumerate(panel_descriptions, start=1):
                    panel_cleaned = re.sub(r"^\d+\.\s*", "", panel.strip())
                    st.markdown(f"**Panel {i}:** {panel_cleaned}")
            else:
                st.warning("⚠️ Could not parse comic panels. Here is raw text:")
                st.code(scene_text)