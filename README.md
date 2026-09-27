# Chatlog

> A meticulously crafted, dynamic transcript generator for Discord.

**Chatlog** is a premium Python library designed to take Discord chat histories and render them into beautiful, static HTML files. Built with modern styling and responsive design principles, these transcripts perfectly mimic the native Discord client experience while remaining entirely self-contained. 

Whether you are logging moderation actions, archiving server history, or saving memorable conversations, Chatlog delivers a highly polished, enterprise-grade output.

---

## Why Choose Chatlog?

- **Native UI Replication:** Accurately replicates the Discord interface down to the smallest detail. This includes seamless support for dark mode, native markdown formatting, complex embeds, and media attachments.
- **Dynamic Timezone Resolution:** Gone are the days of static UTC timestamps. Chatlog's engine automatically resolves and formats timestamps dynamically based on the local system time of the user viewing the HTML file.
- **Anonymized & Secure:** Chatlog generates completely standalone and cleanly scrubbed HTML. There are no external tracking scripts, telemetry, or hardcoded author credits.
- **Zero-Dependency Architecture:** The output is compiled into a single, self-contained HTML file. No external CSS or JS dependencies are required for distribution.

---

## Installation

Install the package seamlessly via PyPI using `pip`:

```bash
pip install chatlog
```

---

## Core Usage

Chatlog provides two primary methods for generating transcripts: the standard `export()` function and the granular `raw_export()` function.

### 1. Standard Export (`chatlog.export`)

The `export` function is the simplest way to generate a transcript. You provide the channel, and the library handles the underlying history fetching automatically.

#### Parameters:
- `channel` *(discord.TextChannel)*: The Discord channel to export.
- `limit` *(int, optional)*: The maximum number of messages to fetch. Defaults to `None` (fetches all messages).
- `bot` *(discord.Client, optional)*: Your bot instance, used to resolve internal references (like emojis).
- `tz_info` *(str, optional)*: The fallback timezone. Defaults to `"UTC"`.
- `military_time` *(bool, optional)*: If `True`, renders fallback timestamps in 24-hour format. Defaults to `True`.

#### Implementation Example:

Below is a complete, production-ready implementation utilizing the `export` function within a standard Discord bot environment.

```python
import io
import discord
import chatlog

class Montage(discord.Client):
    async def on_message(self, message: discord.Message):

        if message.author == self.user:
            return

        if message.content.startswith('!export'):

            transcript = await chatlog.export(
                message.channel,
                limit=100,
                bot=self
            )
            
            if transcript:
                transcript_file = discord.File(
                    io.BytesIO(transcript.encode()),
                    filename=f"transcript-{message.channel.name}.html"
                )
                await message.channel.send(file=transcript_file)

client = Montage()
client.run('TOKEN')
```

### 2. Advanced Export (`chatlog.raw_export`)

If your application requires granular control over exactly which messages are exported (e.g., filtering out specific users, or only logging messages that contain attachments), you can utilize `raw_export`. This bypasses the internal history fetcher and requires you to provide the exact list of messages yourself.

#### Parameters:
- `channel` *(discord.TextChannel)*: The context channel for the transcript.
- `messages` *(List[discord.Message])*: The explicit list of message objects to render.
- `bot` *(discord.Client, optional)*: Your bot instance.

#### Implementation Example:

```python

messages = [message async for message in channel.history(limit=50)]

transcript = await chatlog.raw_export(
    channel,
    messages=messages,
    bot=client
)
```

---

## Technical Requirements

To ensure full compatibility, your environment must meet the following prerequisites:
- **Python:** 3.8 or higher
- **Dependencies:** `discord.py >= 2.0.0`, `pytz`

---

## Acknowledgements

Special thanks to the original developer of `chat_exporter` for creating the foundational code that made this project possible.
