import streamlit as st

from services.linkedin_scraper import scrape_linkedin_profile
from services.openai_service import generate_bot_response, generate_playbook

# Set the page configuration
st.set_page_config(
    page_title="🎈 Sales Chatbot Demo",
    page_icon="🎈",
    layout="wide",
)


# Initialize session state
def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "sell_description" not in st.session_state:
        st.session_state.sell_description = ""
    if "linkedin_url" not in st.session_state:
        st.session_state.linkedin_url = ""
    if "calendar_link" not in st.session_state:
        st.session_state.calendar_link = ""
    if "playbook" not in st.session_state:
        st.session_state.playbook = None
    if "playbook_generated" not in st.session_state:
        st.session_state.playbook_generated = False
    if "show_playbook" not in st.session_state:
        st.session_state.show_playbook = False
    if "guide_shown" not in st.session_state:
        st.session_state.guide_shown = False
    if "messaging_mode" not in st.session_state:
        st.session_state.messaging_mode = "Lead Initiates Conversation"
    if "bot_initiated" not in st.session_state:
        st.session_state.bot_initiated = False


# Show guide at the beginning
def show_guide():
    if not st.session_state.guide_shown:
        st.markdown(
            """
            ## Welcome to the Sales Chatbot Demo!

            **How to use this app:**

            1. **Configure the Chatbot:**
               - In the sidebar, enter what you are selling and your calendar link.
            2. **Generate a Playbook:**
               - Enter a LinkedIn profile URL (of the lead you want to target).
               - Click on **Generate Playbook** to create a personalized playbook.
            3. **Choose Messaging Mode:**
               - Select whether the bot initiates the conversation or the lead does.
            4. **View and Use the Playbook:**
               - After generating, click on **View Playbook** to see the generated playbook.
               - The playbook will guide the chatbot's conversation with the lead.
            5. **Chat with the Bot:**
               - Use the chat interface to test the chatbot.

            **Note:** This is a demo app. All data is for demonstration purposes only.

            ---
            """
        )
        st.session_state.guide_shown = True


# Sidebar for Configuration Inputs
def sidebar_section():
    st.sidebar.header("🔧 Configure Your Chatbot")

    # Form for inputting what to sell
    with st.sidebar.form("sell_form"):
        st.subheader("Selling Configuration")
        sell_description = st.text_input(
            "What are you selling?",
            placeholder="Describe the product or service...",
            value=st.session_state.sell_description,
        )
        calendar_link = st.text_input(
            "Your Calendar Link",
            placeholder="https://calendly.com/your-link",
            value=st.session_state.calendar_link,
        )
        submit_sell = st.form_submit_button("Save Selling Points")
        if submit_sell:
            st.session_state.sell_description = sell_description
            st.session_state.calendar_link = calendar_link
            st.sidebar.success("Selling points and calendar link saved!")

    st.sidebar.markdown("---")  # Separator

    # Form for LinkedIn URL and Playbook Generation
    with st.sidebar.form("playbook_form"):
        st.subheader("Target LinkedIn Profile")
        linkedin_url = st.text_input(
            "LinkedIn Profile URL",
            placeholder="https://www.linkedin.com/in/username",
            value=st.session_state.linkedin_url,
        )
        submit_playbook = st.form_submit_button("Generate Playbook")
        if submit_playbook:
            if linkedin_url.strip() == "":
                st.sidebar.error("Please enter a valid LinkedIn URL.")
            else:
                st.session_state.linkedin_url = linkedin_url
                # Show loading indicator
                with st.spinner("Generating playbook..."):
                    # Scrape LinkedIn profile
                    scraped_data = scrape_linkedin_profile(linkedin_url)
                    # Generate playbook using OpenAI API
                    playbook = generate_playbook(
                        scraped_data,
                        st.session_state.sell_description,
                        st.session_state.calendar_link,
                    )
                    st.session_state.playbook = playbook
                    st.session_state.playbook_generated = True
                    st.session_state.bot_initiated = False  # Reset bot initiation
                    st.sidebar.success("Playbook generated successfully!")

    # Messaging Mode Selection
    st.sidebar.markdown("---")
    st.sidebar.subheader("📲 Messaging Mode")
    st.sidebar.radio(
        "Choose how the conversation starts:",
        options=["Bot Initiates Conversation", "Lead Initiates Conversation"],
        index=(
            0 if st.session_state.messaging_mode == "Bot Initiates Conversation" else 1
        ),
        key="messaging_mode",
    )


# Display Playbook Modal (simulated with expander)
def display_playbook():
    if st.session_state.playbook_generated:
        # Display the "View Playbook" button in the main area
        if not st.session_state.show_playbook:
            if st.button("📘 View Playbook"):
                st.session_state.show_playbook = True

    if st.session_state.show_playbook and st.session_state.playbook:
        # Simulate modal using st.expander
        with st.expander("📘 View Generated Playbook", expanded=True):
            st.json(st.session_state.playbook)


# Chat Interface
def chat_interface():
    st.header("💬 Chat with Your Sales Bot")

    # Check if playbook is generated before proceeding
    if not st.session_state.playbook_generated:
        st.warning("Please generate a playbook first.")
        return  # Do not display chat interface until playbook is generated

    # If mode is "Bot Initiates Conversation" and bot hasn't initiated yet
    if (
        st.session_state.messaging_mode == "Bot Initiates Conversation"
        and not st.session_state.bot_initiated
    ):
        if st.button("🚀 Initiate First Contact"):
            # Bot initiates conversation using the playbook
            initial_message = f"{st.session_state.playbook['greeting']} {st.session_state.playbook['intro']} {st.session_state.playbook['value_proposition']} {st.session_state.playbook['call_to_action']}"
            st.session_state.messages.append(
                {"role": "assistant", "content": initial_message}
            )
            st.session_state.bot_initiated = True
    elif (
        st.session_state.messaging_mode == "Bot Initiates Conversation"
        and st.session_state.bot_initiated
    ):
        # Bot has already initiated, proceed to chat
        pass

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # Update message history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate bot response using OpenAI API
        bot_response = generate_bot_response(
            st.session_state.messages, st.session_state.playbook
        )

        # Display bot response
        with st.chat_message("assistant"):
            st.write(bot_response)

        # Save bot response
        st.session_state.messages.append({"role": "assistant", "content": bot_response})


# Main App Function
def main():
    initialize_session()
    show_guide()
    sidebar_section()
    display_playbook()
    chat_interface()


if __name__ == "__main__":
    main()
