import discord
from discord.ext import commands

# ---------------- CONFIG ----------------
TOKEN = "YOUR_BOT_TOKEN_HERE"          # <-- Replace with your bot token
FREE_ROLE_ID = 123456789012345678      # <-- Replace with your Free role ID (numeric)
INVITE_CODE = "yourinvite"             # <-- Replace with your server invite code
# ---------------------------------------

intents = discord.Intents.default()
intents.members = True  # Needed to detect new members

bot = commands.Bot(command_prefix="!", intents=intents)

# -------- Events --------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and monitoring new members!")

@bot.event
async def on_member_join(member: discord.Member):
    """Automatically assign Free role to members who joined via specific invite."""
    try:
        guild = member.guild
        invites = await guild.invites()

        for invite in invites:
            if invite.code == INVITE_CODE and invite.uses > 0:
                # Assign Free role
                free_role = guild.get_role(FREE_ROLE_ID)
                if free_role:
                    await member.add_roles(free_role, reason="Auto-assigned Free role via invite link")
                    print(f"✅ Assigned Free role to {member}")
                    try:
                        await member.send("✅ You have received the Free role! You can now access the generators.")
                    except:
                        pass
                else:
                    print("❌ Free role not found. Check FREE_ROLE_ID.")
                break

    except Exception as e:
        print(f"Error assigning Free role: {e}")

# Run the bot
bot.run(TOKEN)
