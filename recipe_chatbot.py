import streamlit as st
import random
import time
import json
st.set_page_config(page_title="Recipe Bot 🍳", layout="wide")

# recipes = {
#     "pasta": ["Spaghetti Carbonara", "Penne Arrabiata", "Fettuccine Alfredo"],
#     "chicken": ["Grilled Chicken", "Chicken Curry", "Chicken Stir Fry"],
#     "egg": ["Omelette", "Egg Curry", "Scrambled Eggs"],
#     "rice": ["Fried Rice", "Rice Pulao", "Vegetable Biryani"],
#     "veg": ["Veg Stir Fry", "Vegetable Soup", "Salad"]
# }
with open("recipe.json", "r") as f:
    recipes = json.load(f)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    if "current_msg" not in st.session_state:
        st.session_state.current_msg = ""

# --- CSS for WhatsApp-style chat ---
st.markdown("""
<style>
.chat-card {
    max-width: 400px;
    width: 90%;
    margin: auto;
    margin-top: 40px;
    border: 1px solid #ccc;
    border-radius: 15px;
    background-color: #f8f9fa;
    display: flex;
    flex-direction: column;
    height: 70vh;
    overflow: hidden;
}
.chat-header {
    font-weight: bold;
    font-size: 20px;
    padding: 15px;
    background-color: #075E54;
    color: white;
    text-align: center;
    border-radius: 15px 15px 0 0;
}
.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
}
.bubble-user {
    background-color:#25D366; 
    color:white; 
    padding:10px; 
    border-radius:15px 15px 0 15px; 
    text-align:right; 
    margin:5px 0; 
    max-width:70%; 
    float:right; 
    clear:both;
    word-wrap: break-word;
}
.bubble-bot {
    background-color:#ECE5DD; 
    color:black; 
    padding:10px; 
    border-radius:15px 15px 15px 0; 
    text-align:left; 
    margin:5px 0; 
    max-width:70%; 
    float:left; 
    clear:both;
    word-wrap: break-word;
}
input[type=text] {
    flex: 1;
    padding: 10px 15px;
    border-radius: 25px;
    border: 1px solid #ccc;
}
.send-arrow {
    background-color: #25D366;
    border: none;
    color: white;
    font-size: 20px;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    margin-left: 10px;
    cursor: pointer;
}
.typing {
    color: gray;
    font-style: italic;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Chat Card ---
with st.container():
    st.markdown('<div class="chat-header">Recipe Bot 🍳</div>', unsafe_allow_html=True)
    messages_placeholder = st.empty()
    typing_placeholder = st.empty()

    def display_messages():
        with messages_placeholder.container():
            st.markdown('<div class="chat-messages" id="messages">', unsafe_allow_html=True)
            for sender, msg in st.session_state.chat_history:
                if sender == "user":
                    st.markdown(f'<div class="bubble-user">{msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bubble-bot">{msg}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        # scroll to bottom
        st.markdown("""
            <script>
            var chatBox = document.getElementById('messages');
            if(chatBox){ chatBox.scrollTop = chatBox.scrollHeight; }
            </script>
        """, unsafe_allow_html=True)


    # def send_message():
    #     msg = st.session_state.user_input.strip()
    #     if msg:
    #         st.session_state.current_msg = msg
    #         st.session_state.chat_history.append(("user", msg))
    #         st.session_state.user_input = ""
    #         display_messages()
    #
    #         typing_placeholder.markdown('<div class="typing">Bot is typing...</div>', unsafe_allow_html=True)
    #         time.sleep(1)
    #         typing_placeholder.empty()
    #
    #         matched_category = next((k for k in recipes if k in msg.lower()), None)
    #         bot_response = random.choice(
    #             recipes[matched_category]) if matched_category else "Sorry, no recipes found 😅"
    #         st.session_state.chat_history.append(("bot", bot_response))
    #         display_messages()
    def send_message():
        msg = st.session_state.user_input.strip()
        if msg:
            st.session_state.current_msg = msg
            st.session_state.chat_history.append(("user", msg))
            st.session_state.user_input = ""  # clear input
            display_messages()

            typing_placeholder.markdown('<div class="typing">Bot is typing...</div>', unsafe_allow_html=True)
            time.sleep(1)
            typing_placeholder.empty()

            matched_category = next((k for k in recipes if k in msg.lower()), None)
            bot_response = random.choice(
                recipes[matched_category]) if matched_category else "Sorry, no recipes found 😅"
            st.session_state.chat_history.append(("bot", bot_response))
            display_messages()

    display_messages()

    # --- Input bar ---
    input_col1, input_col2 = st.columns([0.85, 0.15])

    with input_col1:
        st.text_input(
            "Ingredient input",
            placeholder="Enter your ingredient, AI will suggest recipe instructions",
            key="user_input",
            label_visibility="hidden",
            # triggers when user presses Enter
        )

    with input_col2:
        st.button("➡️", key="arrow_send", on_click=send_message)
st.markdown('</div>', unsafe_allow_html=True)
# Clear chat
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.current_msg = ""
    st.experimental_rerun()
