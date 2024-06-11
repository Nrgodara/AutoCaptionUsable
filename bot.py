import pyrogram
import logging
import os
import asyncio
from config import Config
from pyrogram import Client

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set Pyrogram logging to warning to reduce verbosity
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class autocaption(Client):
    
    def __init__(self):
        super().__init__(
            session_name="Captioner",
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            workers=20,
            plugins=dict(root="plugins")
        )

    async def start_with_retries(self, retries=5, delay=5):
        """Attempt to start the bot with a retry mechanism."""
        for attempt in range(retries):
            try:
                logger.info(f"Attempt {attempt + 1} of {retries} to start the client.")
                await self.start()
                logger.info("Client started successfully.")
                # Handle the bot's tasks
                await self.idle()  # Keep the bot running and listening for events
                break
            except pyrogram.errors.BadMsgNotification as e:
                logger.error(f"BadMsgNotification error: {e}. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)  # Wait for a delay before retrying
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                break  # Break on unexpected errors
        else:
            logger.critical("Failed to start the client after several attempts.")

if __name__ == "__main__":
    client = autocaption()

    # Run the client's start_with_retries method using the event loop
    try:
        asyncio.run(client.start_with_retries())
    except RuntimeError as e:
        logger.error(f"Runtime error occurred: {e}")
