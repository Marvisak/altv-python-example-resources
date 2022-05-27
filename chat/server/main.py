import alt

from typing import Dict, Callable, List
from html import escape

cmd_handlers: Dict[str, Callable[[alt.Player, List[str]], None]] = {}
muted_players: List[alt.Player] = []


def invoke_cmd(player: alt.Player, cmd: str, args: List[str]) -> None:
    cmd = cmd.lower()
    try:
        callback = cmd_handlers[cmd]
    except KeyError:
        send(player, f"{{FF0000}} Unknown command /{cmd}")
        return

    callback(player, args)


@alt.client_event("chat:message")
def chat_message(player: alt.Player, msg: str) -> None:
    msg = msg.strip()
    if msg and msg[0] == "/":
        msg = msg[1:]
        if msg:
            alt.log(f"[chat:cmd] {player.name}: /{msg}")

            args = msg.split(" ")
            cmd = args.pop(0)

            invoke_cmd(player, cmd, args)

    elif player in muted_players:
        send(player, f"{{FF0000}} You are currently muted.")

    elif msg:
        alt.log(f"[chat:msg] {player.name}: {msg}")
        alt.emit_all_clients("chat:message", player.name, escape(msg))


def send(player: alt.Player, msg: str) -> None:
    player.emit("chat:message", None, msg)


def broadcast(msg: str) -> None:
    alt.emit_all_clients("chat:message", None, msg)


def register_cmd(cmd: str, callback: Callable[[alt.Player, List[str]], None]) -> None:
    cmd = cmd.lower()
    if cmd_handlers.get(cmd):
        alt.log_error(f"Failed to register command /{cmd}, already registered")
    else:
        cmd_handlers[cmd] = callback


def mute_player(player: alt.Player, mute: bool) -> None:
    if mute and player in muted_players:
        muted_players.append(player)
    elif not mute:
        muted_players.remove(player)


@alt.custom_event("sendChatMessage")
def send_chat_message(player: alt.Player, msg: str) -> None:
    alt.log_warning("Usage of chat events is deprecated use export functions instead")
    send(player, msg)


@alt.custom_event("broadcastMessage")
def broadcast_event(msg: str) -> None:
    alt.log_warning("Usage of chat events is deprecated use export functions instead")
    broadcast(msg)


alt.export("send", send)
alt.export("broadcast", broadcast)
alt.export("register_cmd", register_cmd)
alt.export("mute_player", mute_player)
