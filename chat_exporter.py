import datetime
import io
from typing import List, Optional

from chat_exporter.construct.attachment_handler import (
    AttachmentHandler,
    AttachmentToDiscordChannelHandler,
    AttachmentToLocalFileHostHandler,
    AttachmentToWebhookHandler,
)
from chat_exporter.construct.transcript import Transcript
from chat_exporter.ext.discord_import import discord

__all__ = [
    "quick_export",
    "export",
    "raw_export",
    "AttachmentHandler",
    "AttachmentToLocalFileHostHandler",
    "AttachmentToDiscordChannelHandler",
    "AttachmentToWebhookHandler",
]


async def quick_export(
    channel: discord.TextChannel,
    guild: Optional[discord.Guild] = None,
    bot: Optional[discord.Client] = None,
    raise_exceptions: bool = False,
):

    if guild:
        channel.guild = guild

    transcript = (
        await Transcript(
            channel=channel,
            limit=None,
            messages=None,
            pytz_timezone="UTC",
            military_time=True,
            fancy_times=True,
            before=None,
            after=None,
            bot=bot,
            attachment_handler=None,
            raise_exceptions=raise_exceptions,
        ).export()
    ).html

    if not transcript:
        return

    transcript_embed = discord.Embed(
        description=f"**Transcript Name:** transcript-{channel.name}\n\n", colour=discord.Colour.blurple()
    )

    transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{channel.name}.html")
    return await channel.send(embed=transcript_embed, file=transcript_file)


async def export(
    channel: discord.TextChannel,
    limit: Optional[int] = None,
    tz_info="UTC",
    guild: Optional[discord.Guild] = None,
    bot: Optional[discord.Client] = None,
    military_time: Optional[bool] = True,
    fancy_times: Optional[bool] = True,
    before: Optional[datetime.datetime] = None,
    after: Optional[datetime.datetime] = None,
    attachment_handler: Optional[AttachmentHandler] = None,
    raise_exceptions: bool = False,
):

    if guild:
        channel.guild = guild

    return (
        await Transcript(
            channel=channel,
            limit=limit,
            messages=None,
            pytz_timezone=tz_info,
            military_time=military_time,
            fancy_times=fancy_times,
            before=before,
            after=after,
            bot=bot,
            attachment_handler=attachment_handler,
            raise_exceptions=raise_exceptions,
        ).export()
    ).html


async def raw_export(
    channel: discord.TextChannel,
    messages: List[discord.Message],
    tz_info="UTC",
    guild: Optional[discord.Guild] = None,
    bot: Optional[discord.Client] = None,
    military_time: Optional[bool] = False,
    fancy_times: Optional[bool] = True,
    attachment_handler: Optional[AttachmentHandler] = None,
    raise_exceptions: bool = False,
):

    if guild:
        channel.guild = guild

    return (
        await Transcript(
            channel=channel,
            limit=None,
            messages=messages,
            pytz_timezone=tz_info,
            military_time=military_time,
            fancy_times=fancy_times,
            before=None,
            after=None,
            bot=bot,
            attachment_handler=attachment_handler,
            raise_exceptions=raise_exceptions,
        ).export()
    ).html
