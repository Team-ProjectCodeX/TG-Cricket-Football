# SOURCE https://github.com/Team-ProjectCodeX
# CREATED BY https://t.me/O_okarma
# API BY https://www.github.com/SOME-1HING
# PROVIDED BY https://t.me/ProjectCodeX


import aiohttp
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from REPO import app

# API URLs
CRICKET_API_URL = "https://sugoi-api.vercel.app/cricket"
FOOTBALL_API_URL = "https://sugoi-api.vercel.app/football"

# Create a shared session for making HTTP requests
session = aiohttp.ClientSession()


class MatchManager:
    def __init__(self, api_url):
        self.api_url = api_url
        self.matches = []
        self.match_count = 0

    async def fetch_matches(self):
        async with session.get(self.api_url) as response:
            self.matches = await response.json()

    def get_next_matches(self, count):
        next_matches = self.matches[self.match_count : self.match_count + count]
        self.match_count += count
        return next_matches

    def reset_matches(self):
        self.matches = []
        self.match_count = 0


def get_match_text(match, sport):
    match_text = f"{'🏏' if sport == 'cricket' else '⚽️'} **{match['title']}**\n\n"
    match_text += f"🗓 **Date:** {match['date']}\n"
    match_text += f"🏆 **Team 1:** {match['team1']}\n"
    match_text += f"🏆 **Team 2:** {match['team2']}\n"
    match_text += f"🏟️ **Venue:** {match['venue']}"
    return match_text


def create_inline_keyboard(sport):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                f"Next {sport.capitalize()} Match ➡️",
                callback_data=f"next_{sport}_match",
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


cricket_manager = MatchManager(CRICKET_API_URL)
football_manager = MatchManager(FOOTBALL_API_URL)


@app.on_message(filters.command("cricket"))
async def get_cricket_matches(client, message):
    try:
        cricket_manager.reset_matches()
        await cricket_manager.fetch_matches()

        if not cricket_manager.matches:
            await message.reply("No cricket matches found.")
            return

        next_matches = cricket_manager.get_next_matches(1)
        match = next_matches[0]

        match_text = get_match_text(match, "cricket")
        reply_markup = create_inline_keyboard("cricket")

        await message.reply_text(
            match_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN
        )

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@app.on_message(filters.command("football"))
async def get_football_matches(client, message):
    try:
        football_manager.reset_matches()
        await football_manager.fetch_matches()

        if not football_manager.matches:
            await message.reply("No football matches found.")
            return

        next_matches = football_manager.get_next_matches(1)
        match = next_matches[0]

        match_text = get_match_text(match, "football")
        reply_markup = create_inline_keyboard("football")

        await message.reply_text(
            match_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN
        )

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@app.on_callback_query(filters.regex(r"^next_(cricket|football)_match$"))
async def show_next_match(_, callback_query):
    try:
        sport = callback_query.matches[0].group(1)
        manager = cricket_manager if sport == "cricket" else football_manager

        if not manager.matches:
            await callback_query.answer(f"No more {sport} matches available.")
            return

        next_matches = manager.get_next_matches(3)

        if not next_matches:
            await callback_query.answer(f"No more {sport} matches available.")
            return

        match_text = ""
        for match in next_matches:
            match_text += get_match_text(match, sport) + "\n\n"

        reply_markup = create_inline_keyboard(sport)

        await callback_query.message.edit_text(
            match_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        await callback_query.answer()

    except Exception as e:
        await callback_query.message.reply_text(f"An error occurred: {str(e)}")
