from typing import List
import alt
import chat

# list of voice ranges in meter
range_list = [5, 10, 20]

# index of default range
default_range = 1

channel_short: alt.VoiceChannel
channel_medium: alt.VoiceChannel
channel_long: alt.VoiceChannel

try:
    channel_short = alt.VoiceChannel(True, range_list[0])
    channel_medium = alt.VoiceChannel(True, range_list[1])
    channel_long = alt.VoiceChannel(True, range_list[2])
except RuntimeError as e:
    alt.log_warning(
        "The alt:V voice chat is not enabled and this resource will cease to work. To enable it, "
        'specify the "voice" entry in the server config.'
    )


def change_voice_channel(index: int, player: alt.Player) -> None:
    channel_short.mute_player(player)
    channel_medium.mute_player(player)
    channel_long.mute_player(player)

    if index == 0:
        channel_short.unmute_player(player)
    elif index == 1:
        channel_medium.unmute_player(player)
    elif index == 2:
        channel_long.unmute_player(player)

    chat.send(
        player,
        f"{{80eb34}}Voice Distance changed to {{34dfeb}} {range_list[index]} {{80eb34}}m.",
    )


@alt.event(alt.Event.PlayerConnect)
def player_connect(player: alt.Player) -> None:
    channel_short.add_player(player)
    channel_medium.add_player(player)
    channel_long.add_player(player)

    chat.send(
        player,
        f"{{80eb34}}Press {{34dfeb}}T {{80eb34}}and type {{34dfeb}}/voice {{80eb34}}to see all "
        f"available voice commands.",
    )

    player.set_meta("voice:rangeIndex", default_range)
    change_voice_channel(default_range, player)


@alt.client_event("voice:rangeChanged")
def voice_range_changed(player: alt.Player) -> None:
    index = player.get_meta("voice:rangeIndex")
    index += 1

    if index >= len(range_list):
        index = 0

    change_voice_channel(index, player)
    player.set_meta("voice:rangeIndex", index)


# ================================================== Commands Begin ==================================================


def voice_command(player: alt.Player, args: List[str]) -> None:
    if not args or args[0] == "help":
        chat.send(player, "{ff0000}========== {eb4034}VOICE HELP{ff0000} ==========")
        chat.send(player, "{ff0000}= {34abeb}/voice help {ffffff} - Shows this help.")
        chat.send(
            player,
            '{ff0000}= {ffffff}You can change your voice distance with the Key "F1"',
        )
        chat.send(
            player,
            "{ff0000}= {ffffff}You need to set your microphone as Default Communication Device under Windows.",
        )
        chat.send(
            player,
            "{ff0000}= {ffffff}You can change to PushToTalk in the Mainmenu of alt:V.",
        )
        chat.send(
            player,
            "{ff0000}= {ffffff}You need to activate the Voice Chat in GTA Settings.",
        )
        chat.send(player, "{ff0000} ========================")


chat.register_cmd("voice", voice_command)

# ================================================== Commands End ==================================================
