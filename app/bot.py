import datetime

import gspread
from gspread import WorksheetNotFound 
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram.constants import ReactionEmoji

import app.config as config


def authorize_gspread():
    """Authorizes the Google Sheets API using service account credentials."""
    try:
        gc = gspread.service_account_from_dict(config.google_service_creditionals)
        return gc
    except Exception as e:
        print(f"Error authorizing Google Sheets: {e}")
        return None


def get_worksheet(gc):
    """Opens the specified Google Sheet and retrieves the worksheet."""
    try:
        sh = gc.open_by_key(config.sheet_link)

        today = datetime.datetime.now()
        days_offset = today.weekday()  # Get the current weekday
        monday_date = today - datetime.timedelta(days=days_offset)
        sunday_date = monday_date + datetime.timedelta(days=6)  # Week is 7 days


        start_date_str = monday_date.strftime("%Y-%m-%d")
        end_date_str = sunday_date.strftime("%Y-%m-%d")

        worksheet_title = f"{start_date_str} to {end_date_str}"

        try:
            worksheet = sh.worksheet(worksheet_title)  # Check if worksheet exists
            return worksheet
        except WorksheetNotFound:
            # Create worksheet if not found
            worksheet = sh.duplicate_sheet(source_sheet_id=sh.worksheet("default").id, new_sheet_name=worksheet_title)
            #worksheet = sh.add_worksheet(title=worksheet_title, rows=1000, cols=52)
            return worksheet
    except Exception as e:
        print(f"Error opening Google Sheet worksheet: {e}")
        return None
        
def add_user_data(worksheet, chat_id, username, value):
    """Adds user data to the worksheet, handling existing usernames."""
    try:
        username_column = 1  # Column A
        
        # Iterate through the first 80 rows to find the username
        cell = worksheet.find(username, in_column=username_column)
        
        if cell:
            row_number = cell.row
            row_values = worksheet.row_values(row_number)
            lowest_empty_index = next((i for i, val in enumerate(row_values) if val == '' or val is None), None)
            if lowest_empty_index is not None:
                next_column = lowest_empty_index + 1 
            else:
                next_column = len(row_values) + 1
            worksheet.update_cell(row_number, next_column, value)
            print(f"Appended data for existing user {username} (Chat ID: {chat_id})")
        else:
            cell = worksheet.find("", in_column=username_column)
            if cell:
                worksheet.update_cell(cell.row, username_column, username)
                worksheet.update_cell(cell.row, username_column + 1, value)
                print(f"Added new data for user {username} (Chat ID: {chat_id})")
            else:
                print("Worksheet has reached the 80-row limit. No new rows can be added.")
            
    except Exception as e:
        print(f"Error adding data to Google Sheet: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming messages from the Telegram chat."""
    chat_id = update.effective_chat.id
    username = update.message.from_user.username

    value = None
    
    #print(update.message)

    if update.message.text:
        # If the message has text, extract the value directly from the text
        if not update.message.text.strip().isdigit():
            await context.bot.send_message(chat_id=chat_id, text="Please enter a numeric value only.")
            return
        else:
            if len(update.message.text.strip()) > 5:
                await context.bot.send_message(chat_id=chat_id, text="Maximum 5 digit number.")
                return
            else:
                value = update.message.text.strip()
                    

    elif update.message.photo:
        # If the message has multiple photos
        # photos = update.message.photo
        if not update.message.caption:
            await context.bot.send_message(chat_id=chat_id, text="Please send an image with a caption.")
            return
        else:
            if not update.message.caption.strip().isdigit():
                await context.bot.send_message(chat_id=chat_id, text="Please enter a numeric value only.")
                return
            else:
                if update.message.caption.strip().isdigit():
                    if len(update.message.caption.strip()) > 5:
                        await context.bot.send_message(chat_id=chat_id, text="Maximum 5 digit number.")
                        return
                    else:
                        value = update.message.caption.strip()

    # Now, proceed with the extracted value
    gc = authorize_gspread()
    if gc:
        worksheet = get_worksheet(gc)
        if worksheet:
            add_user_data(worksheet, chat_id, username, value)
        else:
            print("Error retrieving worksheet")
    else:
        print("Error authorizing Google Sheets")

    await update.message.set_reaction(reaction=ReactionEmoji.OK_HAND_SIGN)



def main():
    """Initializes and runs the Telegram bot."""
    print("Starting bot...")
    app = ApplicationBuilder().token(config.token).build()
    echo_handler = MessageHandler((filters.TEXT | filters.PHOTO) & (~filters.COMMAND), echo)
    app.add_handler(echo_handler)
    app.run_polling()
    print("Bot stopped.")


if __name__ == "__main__":
    main()
