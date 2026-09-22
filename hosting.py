import os
import subprocess
import logging
import json
import asyncio
import sys
import time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# --- CONFIGURATION ---
BOT_TOKEN = "8908273209:AAEMwD_4yMitWA6o0NS_9JALWbadKRNsHOk"
OWNER_ID = 8595016465
USERS_FILE = "allowed_users.json"

# --- LOGGING ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- GLOBAL VARIABLES ---
current_directory = os.getcwd()
allowed_users = set()
# Format: { "script_path": process_object }
running_scripts = {}

# --- USER MANAGEMENT FUNCTIONS ---
def load_users():
    global allowed_users
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                data = json.load(f)
                allowed_users = set(data)
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            allowed_users = set()
    else:
        allowed_users = set()

def save_users():
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(list(allowed_users), f)
    except Exception as e:
        logger.error(f"Error saving users: {e}")

def is_authorized(user_id):
    return user_id == OWNER_ID or user_id in allowed_users

# --- BOT COMMAND HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not is_authorized(user.id):
        await update.message.reply_text("⛔ **Access Denied!**")
        return

    welcome_msg = (
        f"💻 **Integrated Multi-Bot Controller**\n"
        f"📂 Path: `{current_directory}`\n\n"
        f"**Multi-Script Control:**\n"
        f"• `/host <file>` - Start a script in background\n"
        f"• `/stop <file>` - Stop a background script\n"
        f"• `/status` - List all running scripts\n\n"
        f"**User Management (Owner Only):**\n"
        f"• `/adduser <id>`\n"
        f"• `/removeuser <id>`\n"
        f"• `/users`\n\n"
        f"**Commands:**\n"
        f"• `/help` - Help Menu\n"
        f"• Type any CMD command"
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id): return
    help_text = """
🤖 **Integrated Help Menu**

**🚀 Multi-Script Hosting:**
• `/host <filename.py>` : Start a python script.
• `/stop <filename.py>` : Stop a script.
• `/status` : View running scripts.

**🔐 User Management:**
• `/adduser <id>` | `/removeuser <id>` | `/users`

**📂 File & System:**
• `dir`, `cd`, `mkdir`, `pip install`, etc.
• `/download <file>`
• Attach file for upload.
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    try:
        new_id = int(context.args[0])
        allowed_users.add(new_id)
        save_users()
        await update.message.reply_text(f"✅ User `{new_id}` added.")
    except: pass

async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != OWNER_ID: return
    if not context.args: return
    try:
        target_id = int(context.args[0])
        if target_id in allowed_users:
            allowed_users.remove(target_id)
            save_users()
            await update.message.reply_text(f"🗑️ User `{target_id}` removed.")
    except: pass

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id): return
    msg = f"👑 **Owner:** `{OWNER_ID}`\n👥 **Allowed:**\n" + "\n".join([f"• `{u}`" for u in allowed_users])
    await update.message.reply_text(msg, parse_mode='Markdown')

# --- SCRIPT MANAGEMENT ---
async def host_script(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("Usage: `/host <filename.py>`")
        return
    
    script_name = context.args[0]
    script_path = os.path.join(current_directory, script_name)
    
    if not os.path.exists(script_path):
        await update.message.reply_text(f"❌ File `{script_name}` not found.")
        return
    
    if script_name in running_scripts:
        await update.message.reply_text(f"⚠️ `{script_name}` is already running.")
        return

    try:
        process = subprocess.Popen([sys.executable, script_path])
        running_scripts[script_name] = process
        await update.message.reply_text(f"🚀 Started `{script_name}` in background (PID: {process.pid})")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to start: {e}")

async def stop_script(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("Usage: `/stop <filename.py>`")
        return
    
    script_name = context.args[0]
    if script_name not in running_scripts:
        await update.message.reply_text(f"❌ `{script_name}` is not running.")
        return

    proc = running_scripts[script_name]
    proc.terminate()
    del running_scripts[script_name]
    await update.message.reply_text(f"🛑 Stopped `{script_name}`.")

async def status_scripts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id): return
    
    # Clean up dead processes first
    for name, proc in list(running_scripts.items()):
        if proc.poll() is not None:
            del running_scripts[name]
            
    if not running_scripts:
        await update.message.reply_text("ℹ️ No background scripts are currently running.")
        return
    
    msg = "🚀 **Running Scripts:**\n"
    for name, proc in running_scripts.items():
        msg += f"• `{name}` (PID: {proc.pid})\n"
    await update.message.reply_text(msg, parse_mode='Markdown')

# --- SYSTEM COMMANDS ---
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_directory
    if not is_authorized(update.effective_user.id): return
    command = update.message.text.strip()
    
    if command.lower().startswith("cd "):
        target = command[3:].strip()
        new_path = os.path.abspath(os.path.join(current_directory, target))
        if os.path.isdir(new_path):
            current_directory = new_path
            os.chdir(current_directory)
            await update.message.reply_text(f"📂 Path: `{current_directory}`")
        else:
            await update.message.reply_text("❌ Not found.")
        return

    msg = await update.message.reply_text("⏳ Processing...")
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=current_directory
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() or stderr.decode().strip() or "✅ Completed."
        if len(output) > 4000: output = output[:4000] + "\n...(truncated)"
        await msg.edit_text(f"📄 **Output:**\n```\n{output}\n```", parse_mode='Markdown')
    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id): return
    doc = update.message.document
    file = await context.bot.get_file(doc.file_id)
    await file.download_to_drive(os.path.join(current_directory, doc.file_name))
    await update.message.reply_text(f"✅ Uploaded: `{doc.file_name}`")

async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id): return
    if not context.args: return
    file_path = os.path.join(current_directory, context.args[0])
    if os.path.isfile(file_path):
        await update.message.reply_document(document=open(file_path, 'rb'))
    else:
        await update.message.reply_text("❌ Not found.")

# --- MAIN RUNNER ---
def run_bot():
    load_users()
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Script management commands
    app.add_handler(CommandHandler("host", host_script))
    app.add_handler(CommandHandler("stop", stop_script))
    app.add_handler(CommandHandler("status", status_scripts))
    
    # Base commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("adduser", add_user))
    app.add_handler(CommandHandler("removeuser", remove_user))
    app.add_handler(CommandHandler("users", list_users))
    app.add_handler(CommandHandler("download", download_file))
    
    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_command))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    print("Integrated Multi-Bot Controller is running...")
    app.run_polling()

if __name__ == '__main__':
    run_bot()
