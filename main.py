import discord
from discord.ext import commands

TOKEN = "MTUyODE3MzYxMTk2NDMwMTMxMg.GxZHJm.QeDUpbGsr8APmoAKqjs95bTed2K5SJihRFbH5k"

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

bot = commands.Bot(intents=intents)


class TicketView(discord.ui.View):
    @discord.ui.button(label=" Create Ticket", style=discord.ButtonStyle.green)
    async def create_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites=overwrites
        )

        await channel.send(f" Welcome {interaction.user.mention}! Staff will assist you shortly.")
        await interaction.response.send_message(
            f" Ticket created: {channel.mention}",
            ephemeral=True
        )


@bot.slash_command(description="Send the ticket panel")
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    embed = discord.Embed(
        title=" Support Tickets",
        description="Click the button below to create a support ticket.",
        color=discord.Color.blue()
    )

    await ctx.respond(embed=embed, view=TicketView())


@bot.event
async def on_ready():
    print(f" Logged in as {bot.user}")


bot.run(TOKEN)