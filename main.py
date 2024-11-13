import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True  # Enable content intents to read messages

# Create bot instance with commands.Bot to support both text and slash commands
client = commands.Bot(command_prefix="!", intents=intents)

# Global lists to store data (mocking a database for simplicity)
profiles = {}
cowork_rooms = []
projects = []
challenges = []
meetups = []

# Event when bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}!')

    try:
        await client.tree.sync()  # Sync global commands
        print("Global slash commands synced successfully.")
    except Exception as e:
        print(f"Error syncing global commands: {e}")

# Handle responses based on text message content
@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:  # Avoid bot responding to itself
        return

    content = message.content.lower()

    # Define responses for different keywords and commands
    if 'hello' in content or 'hi' in content:
        await message.channel.send(f"Hello {message.author.name}! Welcome to the Soul Society for remote workers. How can I help you today?")

    elif 'network' in content:
        await message.channel.send("Looking to network? You can use /setprofile to set up your skills and interests. "
                                   "Once that's done, try /findconnections to discover people with similar interests.")

    elif 'mentor' in content or 'mentorship' in content:
        await message.channel.send("Mentorship is key to growth! Let us know what skills you're looking to develop, "
                                   "and we’ll connect you with potential mentors. Try /findmentor to start.")

    elif 'team' in content or 'project' in content:
        await message.channel.send("Looking for teammates? Use /findteam [skill] to discover people with the skills you need for your project.")

    elif 'cowork' in content or 'coworking' in content:
        await message.channel.send("Join a virtual coworking room to boost your productivity! Use /joincowork to join a room "
                                   "and get in the zone with other remote workers. View current rooms with /listcoworkrooms.")

    elif 'challenge' in content:
        await message.channel.send("Interested in a new challenge? Use /startchallenge [details] to initiate a group challenge, "
                                   "or join an existing one with /listchallenges to collaborate and learn with others!")

    elif 'meetup' in content:
        await message.channel.send("Plan a virtual meet-up to connect with others! Use /schedulemeetup [date] [time] to organize one, "
                                   "or join an upcoming one with /listmeetups.")

    elif 'productivity' in content:
        await message.channel.send("Here are some productivity tips:\n"
                                   "- Take regular breaks to avoid burnout.\n"
                                   "- Use a Pomodoro timer to stay focused.\n"
                                   "- Collaborate with others in a virtual coworking room using /joincowork.")

    elif 'tool' in content or 'resources' in content:
        await message.channel.send("Looking for resources? Here are some tools for remote work:\n"
                                   "- Trello for project management\n"
                                   "- Slack for team communication\n"
                                   "- Notion for organizing notes and tasks\n"
                                   "- Focusmate for virtual coworking\n"
                                   "Use /resources for a full list.")

    elif 'feedback' in content:
        await message.channel.send("We value your feedback! Please let us know what features you’d like to see or any improvements you suggest. "
                                   "You can send feedback via /sendfeedback [your feedback].")

    elif 'help' in content or content.startswith('/help'):
        await message.channel.send("Here are some things I can help you with:\n"
                                   "- /setprofile [details]: Set up your profile with skills and interests.\n"
                                   "- /findconnections: Find people with similar interests.\n"
                                   "- /findmentor: Get matched with a mentor.\n"
                                   "- /findteam [skill]: Find teammates with a specific skill.\n"
                                   "- /joincowork: Join a virtual coworking room.\n"
                                   "- /startchallenge [details]: Start a group challenge.\n"
                                   "- /schedulemeetup [details]: Schedule a virtual meet-up.\n"
                                   "- /resources: Get a list of productivity tools.\n"
                                   "- /sendfeedback [feedback]: Send us your feedback.\n"
                                   "Let me know if you have any questions!")

    else:
        await message.channel.send(f"Hi there, {message.author.name}! I'm here to support our remote worker community. "
                                   "Here are some things you can try:\n"
                                   "- Networking and mentorship\n"
                                   "- Joining a team\n"
                                   "- Participating in challenges\n"
                                   "- Virtual coworking\n"
                                   "Type /help for a list of commands.")

# Slash commands to interact globally
@client.tree.command(name="hello", description="Greet the user")
async def hello(interaction: discord.Interaction):
    # You only need to send the response once
    await interaction.response.send_message(f"Hello, {interaction.user.name}!")


# Make sure this dictionary is declared somewhere at the top of your bot code
# profiles = {}

# @client.tree.command(name="setprofile", description="Set up your profile with skills and interests")
# async def set_profile(interaction: discord.Interaction, skills: str, interests: str):
#     # Validate if both skills and interests are provided
#     if len(skills) < 1 or len(interests) < 1:
#         # Send an error message and return early if validation fails
#         await interaction.response.send_message("Please provide both skills and interests to set up your profile.")
#         return
    
#     # Save the profile for the user in the profiles dictionary
#     profiles[interaction.user.name] = {'skills': skills, 'interests': interests}
    
#     # Acknowledge and confirm the profile setup with skills and interests
#     await interaction.response.send_message(f"Profile set for {interaction.user.name}!\nSkills: {skills}\nInterests: {interests}")

profiles = {}

@client.tree.command(name="setprofile", description="Set up your profile with skills and interests")
async def set_profile(interaction: discord.Interaction, skills: str, interests: str):
    # Validate if both skills and interests are provided
    if len(skills) < 1 or len(interests) < 1:
        # Send an error message and return early if validation fails
        await interaction.response.send_message("Please provide both skills and interests to set up your profile.")
        return
    
    # Save the profile for the user in the profiles dictionary
    profiles[interaction.user.name] = {'skills': skills, 'interests': interests}
    
    # Acknowledge and confirm the profile setup with skills and interests
    await interaction.response.send_message(f"Profile set for {interaction.user.name}!\nSkills: {skills}\nInterests: {interests}")

9



@client.tree.command(name="findconnections", description="Find people with similar interests")
async def find_connections(interaction: discord.Interaction):
    user_profile = profiles.get(interaction.user.name)
    if not user_profile:
        await interaction.response.send_message("Please set up your profile first using /setprofile.")
        return

    similar_connections = []
    for name, profile in profiles.items():
        if profile['interests'] == user_profile['interests'] and name != interaction.user.name:
            similar_connections.append(name)

    if similar_connections:
        await interaction.response.send_message(f"People with similar interests: {', '.join(similar_connections)}")
    else:
        await interaction.response.send_message("No connections found. Try adjusting your profile or wait for more users to join.")

# @client.tree.command(name="coworking", description="Create a virtual coworking room")
# async def create_coworking_channel(interaction: discord.Interaction, room_name: str):
#     guild = interaction.guild

#     # Format the channel name to ensure no odd characters or spaces interfere
#     formatted_room_name = f"coworking-{room_name}".lower()  # Ensure case insensitivity

#     # Check if a voice room with the same name already exists (across all users)
#     existing_room = discord.utils.get(guild.voice_channels, name=formatted_room_name)

#     if existing_room:
#         # If the room already exists, notify the user and exit the function
#         await interaction.response.send_message(f"A coworking room named '{formatted_room_name}' already exists.")
#         return

#     # Defer the response so the interaction doesn't timeout while the room is being created
#     await interaction.response.defer()

#     # Create a voice channel (which supports both voice and video)
#     channel = await guild.create_voice_channel(formatted_room_name)

#     # Now send a message after the creation is completed
#     await interaction.followup.send(f"Your virtual coworking room (voice & video) '{channel.name}' has been created!")

#     # Send a welcome message in the newly created voice channel
#     await channel.send(f"Welcome to your coworking room, {interaction.user.name}! You can now start collaborating and working together via voice/video.")

# @client.tree.command(name="coworking", description="Create a virtual coworking room")
# async def create_coworking_channel(interaction: discord.Interaction, room_name: str):
#     guild = interaction.guild

#     # Format the channel name to ensure no odd characters or spaces interfere
#     formatted_room_name = f"coworking-{room_name}".lower()  # Ensure case insensitivity

#     # Check if a voice room with the same name already exists (across all users)
#     existing_room = discord.utils.get(guild.voice_channels, name=formatted_room_name)

#     if existing_room:
#         # If the room already exists, notify the user and exit the function
#         await interaction.response.send_message(f"A coworking room named '{formatted_room_name}' already exists.")
#         return

#     # Defer the response so the interaction doesn't timeout while the room is being created
#     await interaction.response.defer()

#     # Create a voice channel (which supports both voice and video)
#     channel = await guild.create_voice_channel(formatted_room_name)

#     # Now send a message after the creation is completed
#     await interaction.followup.send(f"Your virtual coworking room (voice & video) '{channel.name}' has been created!")

#     # Send a welcome message in the newly created voice channel
#     await channel.send(f"Welcome to your coworking room, {interaction.user.name}! You can now start collaborating and working together via voice/video.")

#     # Redirect the user to the newly created voice channel
#     await interaction.user.move_to(channel)

@client.tree.command(name="coworking", description="Create a virtual coworking room")
async def create_coworking_channel(interaction: discord.Interaction, room_name: str):
    guild = interaction.guild

    # Format the channel name to ensure no odd characters or spaces interfere
    formatted_room_name = f"coworking-{room_name}".lower()  # Ensure case insensitivity

    # Check if a voice room with the same name already exists (across all users)
    existing_room = discord.utils.get(guild.voice_channels, name=formatted_room_name)

    if existing_room:
        # If the room already exists, notify the user and exit the function
        await interaction.response.send_message(f"A coworking room named '{formatted_room_name}' already exists.")
        return

    # Defer the response so the interaction doesn't timeout while the room is being created
    await interaction.response.defer()

    # Create a voice channel (which supports both voice and video)
    channel = await guild.create_voice_channel(formatted_room_name)

    # Now send a message after the creation is completed
    await interaction.followup.send(f"Your virtual coworking room (voice & video) '{channel.name}' has been created!")

    # Send a welcome message in the newly created voice channel
    await channel.send(f"Welcome to your coworking room, {interaction.user.name}! You can now start collaborating and working together via voice/video.")

    # Attempt to move the user to the newly created voice channel
    try:
        await interaction.user.move_to(channel)
        await interaction.followup.send(f"{interaction.user.name} has been moved to the coworking room!")
    except discord.errors.HTTPException as e:
        # Handle any issues (e.g., user not in a voice channel, missing permissions)
        await interaction.followup.send(f"Unable to move {interaction.user.name} to the coworking room. They may need to join a voice channel manually.")


@client.tree.command(name="listcoworkrooms", description="List all virtual coworking rooms")
async def list_cowork_rooms(interaction: discord.Interaction):
    rooms = [room.name for room in interaction.guild.text_channels if "coworking" in room.name]
    if rooms:
        await interaction.response.send_message(f"Current coworking rooms: {', '.join(rooms)}")
    else:
        await interaction.response.send_message("No active coworking rooms yet. Create one using /coworking.")


@client.tree.command(name="startchallenge", description="Start a group challenge")
async def start_challenge(interaction: discord.Interaction, details: str):
    if not details:
        await interaction.response.send_message("Please provide details for the challenge.")
        return

    challenges.append(details)
    await interaction.response.send_message(f"Challenge started: {details}. Join others to collaborate and improve!")


@client.tree.command(name="listchallenges", description="List all ongoing challenges")
async def list_challenges(interaction: discord.Interaction):
    if challenges:
        await interaction.response.send_message(f"Current challenges: {', '.join(challenges)}")
    else:
        await interaction.response.send_message("No active challenges yet. Start one using /startchallenge.")

@client.tree.command(name="schedulemeetup", description="Schedule a meetup")
async def schedule_meetup(interaction: discord.Interaction, date: str, time: str):
    # Defer the response to avoid timeout, especially for longer operations
    await interaction.response.defer()

    # Code to handle scheduling (perhaps saving the meetup details to a database or variable)
    meetup_details = f"Meet-up scheduled for {date} at {time}."
    
    # Use followup to send a message after deferring the response
    await interaction.followup.send(meetup_details)



@client.tree.command(name="listmeetups", description="List upcoming meetups")
async def list_meetups(interaction: discord.Interaction):
    # Check if there are any meetups in the list
    if meetups:
        # Format the list with each meeting on a new line
        formatted_meetups = "\n".join([f"- {meetup}" for meetup in meetups])
        await interaction.response.send_message(f"Upcoming meetups:\n{formatted_meetups}")
    else:
        await interaction.response.send_message("No upcoming meetups yet. Schedule one using /schedulemeetup.")


@client.tree.command(name="resources", description="List productivity tools and resources")
async def resources(interaction: discord.Interaction):
    await interaction.response.send_message(
        """
        *Remote Work Tools & Resources:*
        - Trello: Project management tool for organizing tasks and projects.
        - Slack: Team communication for real-time collaboration.
        - Notion: An all-in-one workspace for your notes, tasks, and wikis.
        - Focusmate: Virtual coworking tool to stay focused and productive.
        - Zoom: Video conferencing for virtual meetups and team calls.
        - Asana: Task and project management tool to keep you organized.
        """
    )


@client.tree.command(name="sendfeedback", description="Send feedback about the bot")
async def send_feedback(interaction: discord.Interaction, feedback: str):
    if not feedback:
        await interaction.response.send_message("Please provide feedback.")
        return

    # Print to console for review (could be saved to a file or database)
    print(f"Feedback from {interaction.user.name}: {feedback}")
    await interaction.response.send_message("Thank you for your feedback! We appreciate it and will consider it for future improvements.")


@client.tree.command(name="features", description="Display all available features")
async def features(interaction: discord.Interaction):
    await interaction.response.send_message(
        """
        *Available Features:*
        
        - /setprofile [details]: Set up your profile with skills and interests.
        - /findconnections: Find people with similar interests.
        - /findmentor: Get matched with a mentor.
        - /findteam [skill]: Find teammates with a specific skill.
        - /coworking: Create a virtual coworking room.
        - /listcoworkrooms: List all virtual coworking rooms.
        - /startchallenge [details]: Start a group challenge.
        - /listchallenges: List all ongoing challenges.
        - /schedulemeetup [date] [time]: Schedule a virtual meet-up.
        - /listmeetups: List upcoming meetups.
        - /resources: Get a list of productivity tools.
        - /sendfeedback [feedback]: Send us your feedback.
        """
    )


# Run the bot
client.run(TOKEN)