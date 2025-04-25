# 🤖 Zenith Discord Bot

Zenith is a versatile Discord bot designed for **everyone**. It offers a wide range of commands, from games and artificial intelligence to crypto, weather data, and moderation tools.

## 📦 Setup

1. Clone this repository:

```bash
git clone https://github.com/TheShasec/Zenith.git
cd zenith-bot
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add the necessary keys:

```env
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
WEATHER_API_KEY=your_weather_api
COIN_API_KEY=your_coingecko_key
```

4. Start the bot:

```bash
python bot.py
```

## 📜 Commands

Zenith supports the following commands:

### 🎮 Game Commands
- `/rockpaperscissors [choice]` — Play Rock, Paper, Scissors!
- `/roll_dice [guess]` — Roll the dice and guess the result!
- `/poll [title] [options]` — Create an interactive poll.

### 🧠 Artificial Intelligence
- `/ai [model] [message]` — Chat with ChatGPT or Gemini.

### 🌦️ Information Commands
- `/weather [city]` — Get weather information for a city.
- `/crypto [coin]` — View cryptocurrency data.
- `/currency [base_currency]` — Get currency exchange rates.
- `/wikipedia [query]` — Search on Wikipedia.
- `/translate [text] [language]` — Translate text.
- `/serverinfo` — Display server information.

### ⏰ Utility Commands
- `/remind [time] [unit] [reminder]` — Set a reminder.
- `/help` — Lists all commands.
- `/ping` — Shows the bot's latency.
- `/level` — Displays a user's level and XP information.

### 🛠️ Moderation Commands (Admin)
- `/clear [amount]` — Clear messages.
- `/slowmode [seconds]` — Set slow mode for a channel.
- `/join` — Invite the bot to a voice channel.
- `/leave` — Remove the bot from the voice channel.
- `/play [url]` — Play music from YouTube.
- `/pause` — Pause the music.
- `/resume` — Resume the music.
- `/stop` — Stop the music.

### 🛡️ Auto Listeners
- **Spam Detector**: Analyzes messages sent by users in the server and detects excessive messaging. If a user spams, the bot will automatically send a warning or start a punishment process.

- **Profanity Detector**: Detects the use of offensive language in messages. The bot can warn or apply penalties to the user for using profane words.

## 🛠 Developer Information

### requirements.txt

```txt
discord==2.3.2
dotenv==0.9.9
google==3.0.0
google-genai==1.9.0
googletrans==4.0.2
h2==4.2.0
numpy==2.2.5
openai==1.70.0
pip==25.0.1
PyNaCl==1.5.0
regex==2024.11.6
safetensors==0.5.3
tokenizers==0.21.1
yt-dlp==2025.3.31
```

## 🧠 Contributing

We welcome any contributions! If you'd like to add new commands or improve existing ones, please submit a **pull request**.

---

Zenith - The bot that will help you reach the next level. 🚀

