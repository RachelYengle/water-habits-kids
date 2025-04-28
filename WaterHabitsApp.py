# WATER HABITS FOR KIDS - Unified Streamlit App

import streamlit as st
import pandas as pd
import base64, pathlib
import re
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

# ---- BASE64 IMAGE LOADER ----
def img_to_base64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()

# ---- SESSION STATE ----
if 'tips_used' not in st.session_state:
    st.session_state.tips_used = 0
if "page" not in st.session_state:
    st.session_state.page = "home"
if 'last_tip' not in st.session_state:
    st.session_state.last_tip = ""
if 'tip_history' not in st.session_state:
    st.session_state.tip_history = []

# ---- PAGE SELECTION ----
page = st.session_state.page

# ---- GLOBAL NAVBAR STYLE ----
st.markdown("""
    <style>
        .topnav {
            background-color: #cceeff;
            padding: 10px 30px;
            border-radius: 0 0 15px 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
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
        .nav-btn {
            background: none;
            border: none;
            color: #004466;
            font-size: 18px;
            font-weight: bold;
            margin: 0 15px;
            cursor: pointer;
        }
        .nav-btn:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# ---- NAV BAR ----
col_logo, col_nav = st.columns([1, 5])

with col_logo:
    st.image("static/Logo.png", width=120)

with col_nav:
    selected_tab = st.selectbox(
        "",
        ("🏠 Home", "👨‍🏫 About Us", "💧 Water Goals"),
        index=["home", "about", "goals"].index(st.session_state.get("page", "home")),
        key="main_nav"
    )

# Map selected tab to correct page key
page_map = {
    "🏠 Home": "home",
    "👨‍🏫 About Us": "about",
    "💧 Water Goals": "goals"
}
st.session_state.page = page_map[selected_tab]
page = st.session_state.page

# ---- HOME ----
if page == "home":
    set_background("static/Background.jpg")

    # Bubble CSS and Animation (for Home page too)
    st.markdown("""
        <style>
            /* Bubble Animation */
            .bubble {
                position: absolute;
                bottom: -50px;
                border-radius: 50%;
                opacity: 0.8;
                animation: bubbleUp 9s forwards;
                z-index: 0;
            }

            @keyframes bubbleUp {
                0% {
                    transform: translateY(0) scale(0.8);
                    opacity: 0.9;
                }
                100% {
                    transform: translateY(-1200px) scale(1.5);
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
    """, unsafe_allow_html=True)

    # Bubble Colors (NEW! 🌈)
    st.markdown("""
    <div class="bubble-container">
        <div class="bubble" style="left:5%; width:25px; height:25px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:15%; width:30px; height:30px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:30%; width:20px; height:20px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:45%; width:35px; height:35px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:60%; width:22px; height:22px; background-color:rgba(240,248,255,0.9);"></div>
        <div class="bubble" style="left:75%; width:28px; height:28px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:85%; width:18px; height:18px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:90%; width:25px; height:25px; background-color:rgba(173,216,230,0.9);"></div>
    </div>
    """, unsafe_allow_html=True)

    # Welcome text and two feature cards
    st.markdown("<br><h1 style='text-align:center; color:#003344;'>💧 Welcome to Water Habits for Kids</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>💡 Water-Saving Tips</h3>
            <p>Fun, personalized tips for kids to build daily conservation habits.</p>
        """, unsafe_allow_html=True)
        if st.button("Start Tips", key="start_tips"):
            st.query_params["page"] = "tips"
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>📖 Eco Story + Game</h3>
            <p>Interactive story and comic adventure to save water together!</p>
        """, unsafe_allow_html=True)
        if st.button("Start Story", key="start_story"):
            st.query_params["page"] = "story"
        st.markdown("</div>", unsafe_allow_html=True)

# ---- ABOUT US ----
elif page == "about":
    set_background("static/Background.jpg")

    # Load images
    sjsu_b64 = img_to_base64("static/sjsu_logo.png")
    photo_b64 = img_to_base64("static/Photo4.jpg")

    # Bubble Animation CSS
    st.markdown("""
    <style>
        /* Fade-in Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Floating Card Styling */
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

        /* Bubble Animation */
        .bubble {
            position: absolute;
            bottom: -50px;
            border-radius: 50%;
            opacity: 0.8;
            animation: bubbleUp 9s forwards;
            z-index: 0;
        }

        @keyframes bubbleUp {
            0% {
                transform: translateY(0) scale(0.8);
                opacity: 0.9;
            }
            100% {
                transform: translateY(-1200px) scale(1.5);
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
    """, unsafe_allow_html=True)

    # Floating Colorful Bubbles
    st.markdown("""
    <div class="bubble-container">
        <div class="bubble" style="left:5%; width:25px; height:25px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:15%; width:30px; height:30px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:30%; width:20px; height:20px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:45%; width:35px; height:35px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:60%; width:22px; height:22px; background-color:rgba(240,248,255,0.9);"></div>
        <div class="bubble" style="left:75%; width:28px; height:28px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:85%; width:18px; height:18px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:90%; width:25px; height:25px; background-color:rgba(173,216,230,0.9);"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Floating Back to Top Button
    st.markdown("""
    <style>
    .back-to-top {
        position: fixed;
        bottom: 40px;
        right: 30px;
        background-color: #007acc;
        color: white;
        padding: 10px 15px;
        border-radius: 50px;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        z-index: 9999;
        transition: background-color 0.3s ease;
    }
    .back-to-top:hover {
        background-color: #005f99;
    }
    </style>

    <a href="#" class="back-to-top">↑</a>
    """, unsafe_allow_html=True)

    # About Us Header
    st.markdown("<h1 style='text-align:center; color:black;'>👨‍🏫 About Us</h1>", unsafe_allow_html=True)

    # Logo and Team Photo side-by-side
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

    # Floating Card with Text
    st.markdown("""
    <div class="about-card">
    <div class="about-text">

    We’re a team of students from **San José State University** who are passionate about teaching children sustainable water habits through play and interactive storytelling.

    🌍 **Our Mission:**  
    Our mission is to inspire young minds to become lifelong champions of water conservation.  
    We believe that children are not just the leaders of tomorrow — they are powerful change-makers today.  
    Through fun, interactive learning, we aim to nurture a sense of responsibility, creativity, and care for our planet’s most precious resource: water.  
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

    # Bubble Animation CSS
    st.markdown("""
    <style>
        /* Fade-in Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Floating Card Styling */
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

        h1, h2, h3 {
            color: black;
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

        /* Bubble Animation */
        .bubble {
            position: absolute;
            bottom: -50px;
            border-radius: 50%;
            opacity: 0.8;
            animation: bubbleUp 9s forwards;
            z-index: 0;
        }

        @keyframes bubbleUp {
            0% {
                transform: translateY(0) scale(0.8);
                opacity: 0.9;
            }
            100% {
                transform: translateY(-1200px) scale(1.5);
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
    """, unsafe_allow_html=True)

    # Floating Colorful Bubbles
    st.markdown("""
    <div class="bubble-container">
        <div class="bubble" style="left:5%; width:25px; height:25px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:15%; width:30px; height:30px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:30%; width:20px; height:20px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:45%; width:35px; height:35px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:60%; width:22px; height:22px; background-color:rgba(240,248,255,0.9);"></div>
        <div class="bubble" style="left:75%; width:28px; height:28px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:85%; width:18px; height:18px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:90%; width:25px; height:25px; background-color:rgba(173,216,230,0.9);"></div>
    </div>
    """, unsafe_allow_html=True)

    # Floating Back to Top Button
    st.markdown("""
    <style>
    .back-to-top {
        position: fixed;
        bottom: 40px;
        right: 30px;
        background-color: #007acc;
        color: white;
        padding: 10px 15px;
        border-radius: 50px;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        z-index: 9999;
        transition: background-color 0.3s ease;
    }
    .back-to-top:hover {
        background-color: #005f99;
    }
    </style>

    <a href="#" class="back-to-top">↑</a>
    """, unsafe_allow_html=True)

    # Page Header
    st.markdown("<h1 style='text-align:center; color:black;'>🌍 Water-Saving Goals</h1>", unsafe_allow_html=True)

    # First Image (Kids in Yard)
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
    
    As we explored this question, we realized that while there were many resources for adults, there were very few tools designed specifically for kids — especially tools that made saving water feel **fun**, **personal**, and **empowering**.  
    We saw an opportunity to create something new: an interactive experience where kids could learn through storytelling, games, and real-life action.

    ### Understanding the Problem 🚰
    We spent time researching environmental education methods, behavior-change psychology, and how children best develop daily habits.  
    Key insights included:
    - Kids respond better to **short, simple actions** they can control.
    - **Positive reinforcement** and visual progress tracking (like badges and pledges) increase motivation.
    - Stories and characters help children **relate emotionally** to causes like water conservation.
    
    These findings shaped our goal: to build an app that doesn’t just tell kids about water — it **invites them to become water heroes** through everyday choices.

    ### Building the Solution 💡
    We developed **Water Habits for Kids** to make water-saving easy, engaging, and meaningful.  
    Every part of the app — from personalized tips, to eco-stories, to visual games — was designed with one idea in mind:  
    **Small habits today build responsible citizens tomorrow.**

    </div>
    </div>
    """, unsafe_allow_html=True)

    # Second Image (Kids in Bathroom)
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
    As we refined our app, we realized that **setting a goal** gives children a sense of ownership over their habits.  
    A child who pledges to "Turn off the tap while brushing" for a week feels proud of their commitment and is more likely to carry the habit forward.

    That’s why we built the **Water Goals** feature:
    - To help children **choose one simple action**.
    - To **track their progress** over days and weeks.
    - To **celebrate success** and reinforce positive behavior.
    
    Every pledge made is a small promise — but together, these promises ripple outward to create a lasting impact on families, communities, and the planet.

    ### Our Mission 🌎
    Our mission is to empower young generations to protect water through everyday action — starting with one small, achievable goal at a time.
    
    We believe that when children understand they can make a difference, they grow up knowing their actions matter.  
    And with millions of small heroes around the world, the future of water can be brighter for all.

    </div>
    </div>
    """, unsafe_allow_html=True)

# ---- TIPS PAGE ----
elif page == "tips":
    set_background("static/Background.jpg")

    # Bubble Animation CSS
    st.markdown("""
    <style>
        /* Bubble Animation */
        .bubble {
            position: absolute;
            bottom: -50px;
            border-radius: 50%;
            opacity: 0.8;
            animation: bubbleUp 9s forwards;
            z-index: 0;
        }

        @keyframes bubbleUp {
            0% {
                transform: translateY(0) scale(0.8);
                opacity: 0.9;
            }
            100% {
                transform: translateY(-1200px) scale(1.5);
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

        /* Style for all text labels */
        .stSlider > div[data-baseweb="slider"] > div > div {
            color: black !important;
            font-weight: bold !important;
        }

        .stTextInput label, .stSelectbox label {
            color: black !important;
            font-weight: bold !important;
        }

        .tip-box, .custom-info, .most-recent {
            background-color: #e0f7fa;
            color: #002244;
            border-radius: 10px;
            padding: 1rem;
            font-weight: bold;
        }

        .stDownloadButton > button, .stButton > button {
            background-color: #007acc;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }

        .stButton > button:hover {
            background-color: #005f99;
        }
    </style>
    """, unsafe_allow_html=True)

    # Floating Colorful Bubbles
    st.markdown("""
    <div class="bubble-container">
        <div class="bubble" style="left:5%; width:25px; height:25px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:15%; width:30px; height:30px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:30%; width:20px; height:20px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:45%; width:35px; height:35px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:60%; width:22px; height:22px; background-color:rgba(240,248,255,0.9);"></div>
        <div class="bubble" style="left:75%; width:28px; height:28px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:85%; width:18px; height:18px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:90%; width:25px; height:25px; background-color:rgba(173,216,230,0.9);"></div>
    </div>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h2 style='text-align:center; color:black;'>💡 Personalized Water-Saving Tip</h2>", unsafe_allow_html=True)

    # Input fields
    child_name = st.text_input("👶 Child's Name")
    child_age = st.slider("🎂 Child's Age", 3, 12, 6)
    routine = st.selectbox("🛁 Which routine?", ["Brushing Teeth", "Washing Hands", "Showering", "Bath Time", "Other"])

    # Function for Age Group
    def get_age_group(age):
        if 3 <= age <= 5:
            return "3–5"
        elif 6 <= age <= 8:
            return "6–8"
        else:
            return "9–12"

    # Generate Tip Button
    if st.button("Generate Tip"):
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

    # Tip History / Progress
    if st.session_state.tips_used > 0:
        st.markdown("<h3 style='text-align:center; color:black;'>📊 Tip Progress</h3>", unsafe_allow_html=True)
        st.write(f"✅ Tips Generated: {st.session_state.tips_used}")
        st.markdown(f"<div class='most-recent'>💡 <strong>Most Recent Tip:</strong> {st.session_state.last_tip}</div>", unsafe_allow_html=True)
        tips_text = "\n".join(st.session_state.tip_history)
        st.download_button("📥 Download All My Tips", tips_text, file_name="water_tips_summary.txt")
    else:
        st.markdown("<div class='custom-info'>📝 No tips yet — generate one above!</div>", unsafe_allow_html=True)

# ---- STORY PAGE ----
elif page == "story":
    set_background("static/Background.jpg")

    # Bubble Animation CSS
    st.markdown("""
    <style>
        /* Bubble Animation */
        .bubble {
            position: absolute;
            bottom: -50px;
            border-radius: 50%;
            opacity: 0.8;
            animation: bubbleUp 9s forwards;
            z-index: 0;
        }

        @keyframes bubbleUp {
            0% {
                transform: translateY(0) scale(0.8);
                opacity: 0.9;
            }
            100% {
                transform: translateY(-1200px) scale(1.5);
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

        /* General Text Styling */
        h1, h2, h3, h4, label, p, .stMarkdown {
            color: black !important;
            font-weight: bold;
        }

        .stButton>button {
            background-color: #007acc;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1.5rem;
            border-radius: 10px;
        }

        .stButton>button:hover {
            background-color: #005f99;
        }
    </style>
    """, unsafe_allow_html=True)

    # Floating Colorful Bubbles
    st.markdown("""
    <div class="bubble-container">
        <div class="bubble" style="left:5%; width:25px; height:25px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:15%; width:30px; height:30px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:30%; width:20px; height:20px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:45%; width:35px; height:35px; background-color:rgba(173,216,230,0.9);"></div>
        <div class="bubble" style="left:60%; width:22px; height:22px; background-color:rgba(240,248,255,0.9);"></div>
        <div class="bubble" style="left:75%; width:28px; height:28px; background-color:rgba(224,255,255,0.9);"></div>
        <div class="bubble" style="left:85%; width:18px; height:18px; background-color:rgba(255,255,255,0.9);"></div>
        <div class="bubble" style="left:90%; width:25px; height:25px; background-color:rgba(173,216,230,0.9);"></div>
    </div>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 style='text-align:center;'>📖 Eco Story Adventure + Game</h1>", unsafe_allow_html=True)

    # Inputs
    hero = st.text_input("🧒 Hero’s Name", placeholder="e.g., Andy")
    setting = st.selectbox("🌍 Choose a Story Setting", ["bathroom", "garden", "school", "beach", "forest"])
    habit = st.selectbox("💧 Water Habit Focus", ["brushing teeth", "watering plants", "taking showers", "fixing leaks"])

    # Settings
    with st.expander("⚙️ Game Settings"):
        theme = st.radio("🎨 Visual Theme", ["Blue Drop", "Nature Kids", "Clean City", "Water Warriors"])
        hint_mode = st.checkbox("💡 Show Helpful Hints", value=True)

    # Theme color map
    theme_styles = {
        "Blue Drop": {"background": "#e1f5fe", "button": "#0288d1"},
        "Nature Kids": {"background": "#e8f5e9", "button": "#388e3c"},
        "Clean City": {"background": "#eeeeee", "button": "#616161"},
        "Water Warriors": {"background": "#fbe9e7", "button": "#e64a19"}
    }
    style = theme_styles.get(theme, theme_styles["Blue Drop"])

    # Button to Generate
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

            # Game Challenges
            rules = {
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

            game = rules.get(habit.lower(), {
                "challenge": "💧 Make a smart water-saving choice!",
                "goal": "Reduce waste and become an Eco Hero!",
                "points": "+5 per smart move."
            })

            # Display Story
            st.subheader("📘 Your Personalized Story")
            st.markdown(f"**{hero}'s Adventure in the {setting.capitalize()}**")
            st.write(story)

            # Display Game
            st.subheader("🎮 Your Water-Saving Game")
            st.markdown(f"**Challenge:** {game['challenge']}")
            st.markdown(f"**Goal:** {game['goal']}")
            st.markdown(f"**Scoring:** {game['points']}")

            if hint_mode:
                with st.expander("💡 Tips & Tricks"):
                    st.markdown("""
                    - Turn off taps while brushing your teeth.  
                    - Keep showers short and sweet.  
                    - Fix leaky faucets right away.  
                    - Water plants early or late to reduce evaporation.  
                    - Use buckets instead of hoses when cleaning.
                    """)

            # Comic Panels Generation
            st.subheader("🎬 Your Eco Adventure Comic")
            scene_prompt = (
                f"You are a comic artist turning this children's story into a 4 to 6 panel comic. "
                f"For each panel, number them clearly (1. 2. 3...), and describe the scene visually in 1–2 sentences. "
                f"Make sure each panel has a new line and starts with a number. Incorporate this theme into the scene visuals: '{theme}'.\n\n"
                f"Story:\n{story}"
            )

            with st.spinner("Breaking the story into comic scenes..."):
                scene_response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": scene_prompt}]
                )
                scene_text = scene_response.choices[0].message.content.strip()

            import re
            panel_descriptions = re.findall(r'\d\.\s.*?(?=\n\d\.|\Z)', scene_text, re.DOTALL)[:6]

            if panel_descriptions:
                for i, panel in enumerate(panel_descriptions, start=1):
                    panel_cleaned = re.sub(r"^\d+\.\s*", "", panel.strip())
                    st.markdown(f"**Panel {i}:** {panel_cleaned}")
                    with st.spinner(f"Generating image for Panel {i}..."):
                        try:
                            panel_img_response = client.images.generate(
                                prompt=f"Comic panel in theme of '{theme}': {panel_cleaned}",
                                n=1,
                                size="512x512"
                            )
                            image_url = panel_img_response.data[0].url
                            st.image(image_url, caption=f"Panel {i}")
                        except Exception:
                            st.warning(f"⚠️ Could not load image for Panel {i}.")
                            st.text(f"Panel description: {panel_cleaned}")
            else:
                st.warning("⚠️ GPT did not return clearly numbered scenes.")
                st.markdown("Here is the raw output from GPT:")
                st.code(scene_text)