# WATER HABITS FOR KIDS - Unified Streamlit App

import streamlit as st
import pandas as pd
import base64, pathlib
import random
from openai import OpenAI

# ---- PRIVACY POLICY GATE (Black Text Version) ----
if 'agreed_to_terms' not in st.session_state:
    st.session_state.agreed_to_terms = False
if 'show_privacy' not in st.session_state:
    st.session_state.show_privacy = False
if 'show_terms' not in st.session_state:
    st.session_state.show_terms = False

if not st.session_state.agreed_to_terms:
    st.markdown("""
    <style>
    .stApp {
        background-color: #d6f4ff;
    }
    h1, h2, h3, h4, p, label, .stMarkdown, .stExpanderHeader, .css-1v0mbdj, .css-1dp5vir {
        color: black !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #0a4c86;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
        width: 100%;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #083d6d;
    }
    .stExpander > summary {
        background-color: #0a4c86 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>🚸 Welcome to Water Habits for Kids</h1>", unsafe_allow_html=True)
    st.markdown("""
    Before using the app, please review and agree to our **Privacy Policy** and **Terms of Service**.
    """)

    if st.button("📜 View Privacy Policy"):
        st.session_state.show_privacy = True

    if st.button("📜 View Terms of Service"):
        st.session_state.show_terms = True

    if st.session_state.show_privacy:
        with st.expander("🔒 Privacy Policy", expanded=True):
            st.write("""
            **Privacy Policy**  
            • We **do not collect** your name, age, or any personal information.  
            • We only track how many water-saving tips or stories you create to improve the app.  
            • Your information stays private and is **never shared** with anyone else.  
            By using this app, you agree to our friendly privacy approach.
            """)
            if st.button("❌ Close Privacy Policy"):
                st.session_state.show_privacy = False
                st.rerun()

    if st.session_state.show_terms:
        with st.expander("📜 Terms of Service", expanded=True):
            st.write("""
            **Terms of Service**  
            • This app is for **educational and fun purposes** only.  
            • Water tips and stories are AI-generated for inspiration, not official advice.  
            • Use this app responsibly.  
            By continuing, you agree to use the app appropriately.
            """)
            if st.button("❌ Close Terms of Service"):
                st.session_state.show_terms = False
                st.rerun()

    agree = st.checkbox("✅ I have read and agree to the Privacy Policy and Terms of Service.")

    if agree:
        if st.button("🚀 Continue to Water Habits App"):
            st.session_state.agreed_to_terms = True
            st.rerun()

    st.stop()

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
/* Main labels (text inputs, selects) */
label, .stTextInput>label, .stSelectbox>label {
    color: #002244 !important;
    font-weight: bold !important;
}

/* Child age slider main label */
.stSlider>label {
    color: #002244 !important;
    font-weight: bold !important;
}

/* Child age slider range numbers ("3" and "12") */
div[data-baseweb="slider"] > div > div > div > div {
    color: black !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)
    
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
/* Fix child age slider numbers */
div[data-baseweb="slider"] > div > div > div > div {
    color: black !important;
    font-weight: bold !important;
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

    # Input fields
    child_name = st.text_input("👶 Child's Name", placeholder="e.g Rachel")

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

    # ---- Corrected NAV BUTTON STYLE for Story Page ----
    st.markdown("""
    <style>
    /* NAV buttons (Home, About Us, Water Goals) */
    div.stButton > button {
        background-color: #0a4c86; /* Navy blue background */
        color: white !important;   /* White text */
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-size: 18px;
        width: 100%;
        height: 50px;
        border: none;
        transition: background-color 0.3s, transform 0.2s;
    }

    /* Force inner text (span) inside buttons to white */
    div.stButton > button > div, div.stButton > button span {
        color: white !important;
        font-weight: bold;
    }

    /* Hover Effect */
    div.stButton > button:hover {
        background-color: #083d6d;
        transform: scale(1.05);
    }

    /* Light Blue Page Background */
    .stApp {
        background-color: #d6f4ff !important;
    }

    /* Floating Card Style */
    .story-card {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin: 2rem auto;
        max-width: 900px;
    }

    /* Navy Blue Expander */
    .stExpander > summary {
        background-color: #0a4c86 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* Fix Floating Card text */
    .story-card, .story-card p, .story-card strong, .story-card h2, .story-card h4 {
        color: #002244 !important; /* dark navy for floating cards */
    }

    /* ALSO fix page main headings */
    h1, h2, h3 {
        color: #002244 !important; /* dark navy for big headers too */
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Story Page CSS ---
    st.markdown("""
    <style>
    /* Button colors */
    div.stButton > button { ... }
    /* Hover */
    div.stButton > button:hover { ... }
    /* Light blue background */
    .stApp { ... }
    /* NEW: Fix floating cards text */
    .story-card, .story-card p, .story-card strong, .story-card h2, .story-card h4 {
        color: #002244 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* Fix label texts like Hero’s Name, Choose a Story, etc. */
    label, .stTextInput>label, .stSelectbox>label, .stSlider>label, .stRadio>label, .stExpander>summary {
        color: #002244 !important; /* dark navy */
        font-weight: bold !important;
    }

    /* Fix radio button options (Blue Drop, Nature Kids, etc.) */
    .stRadio>div>label {
        color: #002244 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---- BUBBLE ANIMATION ----
    unique_id = random.randint(1, 999999)
    st.markdown(f"""
    <style>
    .bubble {{
        position: absolute;
        bottom: -100px;
        border-radius: 50%;
        opacity: 0.8;
        animation: bubbleUp 20s infinite;
        z-index: 0;
    }}

    @keyframes bubbleUp {{
        0% {{
            transform: translateY(0) scale(0.8);
            opacity: 0.8;
        }}
        50% {{
            opacity: 0.5;
        }}
        100% {{
            transform: translateY(-1500px) scale(1.2);
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

    <div class="bubble-container" id="bubbles-{unique_id}">
        <div class="bubble light" style="left:5%; width:20px; height:20px; animation-delay:0s;"></div>
        <div class="bubble medium" style="left:15%; width:35px; height:35px; animation-delay:5s;"></div>
        <div class="bubble dark" style="left:30%; width:25px; height:25px; animation-delay:2s;"></div>
        <div class="bubble light" style="left:45%; width:40px; height:40px; animation-delay:7s;"></div>
        <div class="bubble medium" style="left:60%; width:18px; height:18px; animation-delay:3s;"></div>
        <div class="bubble dark" style="left:75%; width:30px; height:30px; animation-delay:6s;"></div>
        <div class="bubble light" style="left:85%; width:22px; height:22px; animation-delay:4s;"></div>
        <div class="bubble medium" style="left:90%; width:28px; height:28px; animation-delay:1s;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ---- PAGE CONTENT ----
    st.markdown("<h1 style='text-align:center;'>📖 Eco Story Adventure + Game</h1>", unsafe_allow_html=True)

    hero = st.text_input("🧒 Hero’s Name", placeholder="e.g., Andy")
    setting = st.selectbox("🌍 Choose a Story Setting", ["bathroom", "garden", "school", "beach", "forest"])
    habit = st.selectbox("💧 Water Habit Focus", ["brushing teeth", "watering plants", "taking showers", "fixing leaks"])

    theme = "Blue Drop"  # Set default theme automatically
    hint_mode = True     # Set default hints on

    if st.button("✨ Generate My Eco Adventure"):
        with st.spinner("Creating your story and game..."):

            # Generate Story
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

            # Game Rules
            rules = {
                "brushing teeth": {"challenge": "🪥 Tap to turn off faucet.", "goal": "Save 10 gallons!", "points": "+5 per tap, -2 miss."},
                "watering plants": {"challenge": "🌿 Water dry plants only.", "goal": "Healthy garden!", "points": "+10 good, -5 overwater."},
                "taking showers": {"challenge": "🚿 Finish in 2 min.", "goal": "Save 5 gallons!", "points": "+2 per second saved."},
                "fixing leaks": {"challenge": "🔧 Tap leaks fast.", "goal": "Fix 10 leaks!", "points": "+5 fix, -3 miss."}
            }

            game = rules.get(habit.lower(), {
                "challenge": "💧 Make smart water choices!",
                "goal": "Reduce waste!",
                "points": "+5 per action."
            })

            # 📘 Personalized Story
            st.markdown("<h2 style='text-align:center;'>📘 Your Personalized Story</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='story-card'><p>{story}</p></div>", unsafe_allow_html=True)

            # 🎮 Water-Saving Game
            st.markdown("<h2 style='text-align:center;'>🎮 Your Water-Saving Game</h2>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='story-card'>
            <p><strong>Challenge:</strong> {game['challenge']}</p>
            <p><strong>Goal:</strong> {game['goal']}</p>
            <p><strong>Scoring:</strong> {game['points']}</p>
            </div>
            """, unsafe_allow_html=True)

            # 🎬 Eco Comic
            st.markdown("<h2 style='text-align:center;'>🎬 Your Eco Adventure Comic</h2>", unsafe_allow_html=True)

            scene_prompt = (
                f"Create a 4-6 panel comic script from this story. Number panels (1., 2., etc.) and 1-2 sentences each.\n\nStory:\n{story}"
            )

            scene_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": scene_prompt}]
            )

            scene_text = scene_response.choices[0].message.content.strip()

            import re
            panel_descriptions = re.findall(r'\d\.\s.*?(?=\n\d\.|\Z)', scene_text, re.DOTALL)

            if panel_descriptions:
                for i, panel in enumerate(panel_descriptions, start=1):
                    panel_cleaned = re.sub(r"^\d+\.\s*", "", panel.strip())
                    st.markdown(f"""
                    <div class="story-card">
                    <h4>Panel {i}</h4>
                    <p>{panel_cleaned}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.spinner(f"Generating image for Panel {i}..."):
                        try:
                            panel_img_response = client.images.generate(
                                prompt=f"Comic panel about: {panel_cleaned}, visual theme {theme}",
                                n=1,
                                size="512x512"
                            )
                            image_url = panel_img_response.data[0].url
                            st.image(image_url, caption=f"Panel {i}")
                        except Exception:
                            st.warning(f"⚠️ Could not generate image for Panel {i}.")
                            st.text(f"Panel description: {panel_cleaned}")
            else:
                st.warning("⚠️ Comic panels could not be parsed. Here's raw output:")
                st.code(scene_text)