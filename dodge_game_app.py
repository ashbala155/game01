# dodge_game_app.py
import streamlit as st
from PIL import Image, ImageDraw
import random
import time

# ====== Settings ======
WIDTH, HEIGHT = 300, 400
PLAYER_SIZE = 30
BLOCK_SIZE = 30
BLOCK_SPEED = 10
REFRESH_RATE = 0.3

# ====== Session State ======
if "player_x" not in st.session_state:
    st.session_state.player_x = WIDTH // 2 - PLAYER_SIZE // 2
if "blocks" not in st.session_state:
    st.session_state.blocks = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# ====== Functions ======
def reset_game():
    st.session_state.player_x = WIDTH // 2 - PLAYER_SIZE // 2
    st.session_state.blocks = []
    st.session_state.score = 0
    st.session_state.game_over = False

def update_game():
    if random.randint(0, 10) > 7:
        st.session_state.blocks.append([random.randint(0, WIDTH - BLOCK_SIZE), 0])
    for block in st.session_state.blocks:
        block[1] += BLOCK_SPEED
    for block in st.session_state.blocks:
        if (st.session_state.player_x < block[0] + BLOCK_SIZE and
            st.session_state.player_x + PLAYER_SIZE > block[0] and
            HEIGHT - PLAYER_SIZE < block[1] + BLOCK_SIZE):
            st.session_state.game_over = True
    st.session_state.blocks = [b for b in st.session_state.blocks if b[1] < HEIGHT]
    st.session_state.score += 1

def draw_game():
    img = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([st.session_state.player_x, HEIGHT - PLAYER_SIZE,
                    st.session_state.player_x + PLAYER_SIZE, HEIGHT], fill="blue")
    for block in st.session_state.blocks:
        draw.rectangle([block[0], block[1], block[0] + BLOCK_SIZE, block[1] + BLOCK_SIZE], fill="red")
    return img

# ====== Streamlit Layout ======
st.set_page_config(page_title="Dodge the Blocks", page_icon="🚀")
st.title("🚀 Dodge the Falling Blocks")

# Movement buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("←") and not st.session_state.game_over:
        st.session_state.player_x = max(0, st.session_state.player_x - 20)
with col3:
    if st.button("→") and not st.session_state.game_over:
        st.session_state.player_x = min(WIDTH - PLAYER_SIZE, st.session_state.player_x + 20)

# Update game
if not st.session_state.game_over:
    update_game()

# Draw game
st.image(draw_game(), use_column_width=False)

# Score and Game Over
st.write(f"Score: {st.session_state.score}")
if st.session_state.game_over:
    st.write("**Game Over!**")
    if st.button("Restart Game"):
        reset_game()

# Auto-refresh for animation
if not st.session_state.game_over:
    time.sleep(REFRESH_RATE)
    st.experimental_rerun()
