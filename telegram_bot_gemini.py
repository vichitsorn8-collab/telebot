import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load environment variables
TELEGRAM_TOKEN = os.getenv("8670658132:AAHWj-_8a0_Hwfi1TKe9OdV2Zs2XHpd5Y3Q")
GOOGLE_API_KEY = os.getenv("AIzaSyB4Ez740aykORmhqPqD-VmcjoJXmICq1D4")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    try:
        # Show "typing" action to user
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get response from Gemini
        response = model.generate_content(user_text)
        bot_response = response.text
        
        # Send response back to Telegram
        await update.message.reply_text(bot_response)
        
    except Exception as e:
        logging.error(f"Error while generating response: {e}")
        await update.message.reply_text("សូមអភ័យទោស មានបញ្ហាបន្តិចបន្តួចក្នុងការបង្កើតចម្លើយ។ សូមព្យាយាមម្តងទៀត! (Sorry, there was a small problem generating a response. Please try again!)")

if __name__ == '__main__':
    if not TELEGRAM_TOKEN or not GOOGLE_API_KEY:
        print("Error: TELEGRAM_BOT_TOKEN or GOOGLE_API_KEY environment variables are not set.")
        exit(1)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is starting...")
    app.run_polling()

