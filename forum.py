import streamlit as st
from datetime import datetime
import json
import os
st.set_page_config(page_title="Maternal Nutritional Planner", page_icon="🍎", layout="wide")

DATA_FILE = "forum_data.json"

def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_posts(posts):
    with open(DATA_FILE, "w") as file:
        json.dump(posts, file, indent=4)

if "posts" not in st.session_state:
    st.session_state.posts = []

def add_post(title, content):
    post = {
        "title": title,
        "content": content,
        "comments": [],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.posts.append(post)

def add_comment(post_index, comment):
    st.session_state.posts[post_index]["comments"].append({
        "comment": comment,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

st.title("Check out the questions people have asked")

tab1, tab2 = st.tabs(["📋 Discussion Forum", "➕ Create Post!!"])

with tab1:
    st.header("Here's what is on people's minds")
    if not st.session_state.posts:
        st.info("Want to ask something on your mind? ")
        st.info("Why not put your thought on the forum!!!")
        st.info("And no one will know who posted it : )")

        search_query = st.text_input("Want to check if your query is already present")

        if search_query.strip():
            filtered_posts = [
                post for post in st.session_state.posts
                if search_query.lower() in post["title"].lower()
            ]
            if not filtered_posts:
                st.warning("Looks like no one has posted on this, why don't you be the first?")
                st.info("Head over to the Create Post tab")
        else:
            filtered_posts = st.session_state.posts
    else:
        for idx, post in enumerate(st.session_state.posts):
            st.subheader(post["title"])
            st.write(f"*{post['content']}*")
            st.caption(f"Posted on: {post['timestamp']}")
            
            with st.expander("View Responses 💬 "):
                if not post["comments"]:
                    st.info("No Responses yet! Can you help with this query")
                for comment in post["comments"]:
                    st.write(f"**-** {comment['comment']} (*{comment['timestamp']}*)")
            
                comment_input = st.text_input(f"Respond? ", key=f"comment_{idx}")
                if st.button("Post Response", key=f"comment_btn_{idx}"):
                    if comment_input.strip():
                        add_comment(idx, comment_input)
                        st.success("Your response has been added")
                        st.rerun()

with tab2:
    st.header("Why not Create a post on your thought?")
    post_title = st.text_input("Give your thought a title")
    post_content = st.text_area("Thoughts have no boundaries, Feel free to express yourself")

    if st.button("Post"):
        if post_title.strip() and post_content.strip():
            add_post(post_title, post_content)
            st.success("Your thought has been posted")
            st.rerun()
        else:
            st.error("Please enter both title and thought for the post.")
