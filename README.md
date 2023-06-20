# TG-Cricket-Football


This code is a Python script that retrieves information about cricket and football matches from sugoi API and provides it to users through a messaging platform. It uses the Pyrogram library for interacting with the messaging platform and the aiohttp library for making HTTP requests to the API.

The code defines a MatchManager class that manages the retrieval and storage of match data. It has methods to fetch matches from the API, get the next set of matches, and reset the match data. The code also includes a function to format the match information into a text string and another function to create inline keyboards for user interaction.

The script defines two instances of the MatchManager class, one for cricket matches and another for football matches. It includes message handlers for the commands "/cricket" and "/football" which fetch the respective match data, format it into a text string, and send it as a reply to the user. It also handles inline keyboard callbacks for retrieving the next set of matches.


> join our Telegram channel <https://t.me/ProjectCodeX>
> where we share these modules along with their complete functionality. Additionally, we showcase fascinating projects for you to explore as well.
