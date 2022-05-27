from typing import List

import alt
import chat
import random

spawns: List[alt.Vector3] = [
    alt.Vector3(-695.1956176757812, 83.94725036621094, 55.85205078125),
    alt.Vector3(-527.6835327148438, -678.7252807617188, 33.6607666015625),
    alt.Vector3(200.6637420654297, -935.2879028320312, 30.6783447265625),
    alt.Vector3(897.7318725585938, -1054.6944580078125, 32.818359375),
    alt.Vector3(363.1516418457031, -2123.156005859375, 16.052734375),
    alt.Vector3(-265.3582458496094, -1898.0703125, 27.7464599609375),
]

spawn_models: List[str] = ["u_m_y_mani", "csb_mweather", "hc_driver", "mp_m_weapexp_01"]

weapons: List[str] = [
    "dagger",
    "bat",
    "bottle",
    "crowbar",
    "flashlight",
    "golfclub",
    "hammer",
    "hatchet",
    "knuckle",
    "knife",
    "machete",
    "switchblade",
    "nightstick",
    "wrench",
    "battleaxe",
    "poolcue",
    "stone_hatchet",
    "pistol",
    "pistol_mk2",
    "combatpistol",
    "appistol",
    "stungun",
    "pistol50",
    "snspistol",
    "snspistol_mk2",
    "heavypistol",
    "vintagepistol",
    "flaregun",
    "marksmanpistol",
    "revolver",
    "revolver_mk2",
    "doubleaction",
    "raypistol",
    "microsmg",
    "smg",
    "smg_mk2",
    "assaultsmg",
    "combatpdw",
    "machinepistol",
    "minismg",
    "raycarbine",
    "pumpshotgun",
    "pumpshotgun_mk2",
    "sawnoffshotgun",
    "assaultshotgun",
    "bullpupshotgun",
    "musket",
    "heavyshotgun",
    "dbshotgun",
    "autoshotgun",
    "assaultrifle",
    "assaultrifle_mk2",
    "carbinerifle",
    "carbinerifle_mk2",
    "advancedrifle",
    "specialcarbine",
    "specialcarbine_mk2",
    "bullpuprifle",
    "bullpuprifle_mk2",
    "compactrifle",
    "mg",
    "combatmg",
    "combatmg_mk2",
    "gusenberg",
    "sniperrifle",
    "heavysniper",
    "heavysniper_mk2",
    "marksmanrifle",
    "marksmanrifle_mk2",
    "rpg",
    "grenadelauncher",
    "grenadelauncher_smoke",
    "minigun",
    "firework",
    "railgun",
    "hominglauncher",
    "compactlauncher",
    "rayminigun",
    "grenade",
    "bzgas",
    "smokegrenade",
    "flare",
    "molotov",
    "stickybomb",
    "proxmine",
    "snowball",
    "pipebomb",
    "ball",
]


@alt.event(alt.Event.PlayerConnect)
def player_connect(player: alt.Player) -> None:
    if "admin" in player.name:
        player.kick()
        return

    # alt.hash is here because MyPy currently doesn't really like
    # properties which have different setter and getter types
    # Should get fixed soon
    player.model = alt.hash(random.choice(spawn_models))
    player.set_meta("vehicles", [])
    spawn = random.choice(spawns)
    player.spawn(spawn)
    player.emit("freeroam:spawned")
    player.emit("freeroam:Interiors")

    def send_welcome_message() -> None:
        if player and player.valid:
            player_count = len(alt.Player.all)
            chat.broadcast(
                f"{{1cacd4}}{player.name} {{ffffff}}has {{00ff00}}joined {{ffffff}}the Server... "
                f"({player_count} players online)"
            )
            chat.send(
                player,
                f"{{80eb34}}Press {{34dfeb}}T {{80eb34}}and type "
                f"{{34dfeb}}/help {{80eb34}}to see all available commands..",
            )

    alt.timer(send_welcome_message, 1000)


@alt.event(alt.Event.PlayerDeath)
def player_death(player: alt.Player, killer: alt.Entity, _: str) -> None:
    spawn = random.choice(spawns)
    player.emit("freeroam:switchInOutPlayer", True, 0, 2)

    def player_death_timeout() -> None:
        if player and player.valid:
            player.spawn(spawn)
            player.emit("freeroam:switchInOutPlayer", True)
            player.clear_blood_damage()

    alt.timer(player_death_timeout, 3000)

    if killer and isinstance(killer, alt.Player):
        alt.log(f"{killer.name} gave {player.name} the rest!")
        send_notification_to_all_player(
            f"~r~<C>{killer.name}</C> ~s~killed ~b~<C>{player.name}</C>"
        )
    elif isinstance(killer, alt.Player):
        alt.log(f"{killer.name} died!")
        send_notification_to_all_player(f"~s~Suicide ~b~<C>{player.name}</C>")


def send_notification_to_player(
    player: alt.Player,
    message: str,
    text_color: int = 0,
    bg_color: int = 2,
    blink: bool = False,
) -> None:
    player.emit("freeroam:sendNotification", text_color, bg_color, message, blink)


def send_notification_to_all_player(
    message: str,
    text_color: int = 0,
    bg_color: int = 2,
    blink: bool = False,
) -> None:
    alt.emit_all_clients(
        "freeroam:sendNotification", text_color, bg_color, message, blink
    )


@alt.event(alt.Event.PlayerDisconnect)
def player_disconnect(player: alt.Player, reason: str) -> None:
    player_count = len(alt.Player.all)
    chat.broadcast(
        f"{{1cacd4}}{player.name} {{ffffff}}has {{ff0000}}left {{ffffff}}the Server.. ({player_count} players online)"
    )
    for vehicle in player.get_meta("vehicles"):
        if vehicle:
            vehicle.destroy()

    player.delete_meta("vehicles")
    alt.log(f"{player.name} has leaved the server because of {reason}")


# ================================================== Commands Begin ==================================================


def help_command(player: alt.Player, args: List[str]) -> None:
    chat.send(player, "{ff0000}========== {eb4034}HELP {ff0000} ==========")
    chat.send(
        player, "{ff0000}= {34abeb}/veh {40eb34}(model)   {ffffff} Spawn a Vehicle"
    )
    chat.send(
        player,
        "{ff0000}= {34abeb}/tp {40eb34}(targetPlayer)   {ffffff} Teleport to Player",
    )
    chat.send(
        player,
        "{ff0000}= {34abeb}/model {40eb34}(modelName)   {ffffff} Change Player Model",
    )
    chat.send(
        player,
        "{ff0000}= {34abeb}/weapon {40eb34}(weaponName)   {ffffff} Get specified weapon",
    )
    chat.send(player, "{ff0000}= {34abeb}/weapons    {ffffff} Get all weapons")
    chat.send(player, "{ff0000} ========================")


def veh_command(player: alt.Player, args: List[str]) -> None:
    if not args:
        chat.send(player, "Usage: /veh (vehicleModel)")
        return
    try:
        vehicle = alt.Vehicle(
            args[0], player.pos.x, player.pos.y, player.pos.z, 0, 0, 0
        )
        player_vehicles: List[alt.Vehicle] = player.get_meta("vehicles")
        if len(player_vehicles) >= 3:
            to_destroy = player_vehicles.pop()
            if to_destroy:
                to_destroy.destroy()
        player_vehicles.insert(0, vehicle)
        player.set_meta("vehicles", player_vehicles)
    except RuntimeError as e:
        chat.send(
            player,
            f"{{ff0000}} Vehicle Model {{ff9500}}{args[0]} {{ff0000}}does not exist...",
        )
        alt.log(e)


def pos_command(player: alt.Player, args: List[str]) -> None:
    alt.log(f"Position: {player.pos.x}, {player.pos.y} {player.pos.z}")
    chat.send(player, f"Position: {player.pos.x}, {player.pos.y} {player.pos.z}")


def tp_command(player: alt.Player, args: List[str]) -> None:
    if not args:
        chat.send(player, "Usage: /tp (target player)")
        return
    found_players = list(filter(lambda p: p.name == args[0], alt.Player.all))
    if found_players:
        player.pos = found_players[0].pos
        chat.send(
            player, f"You got teleported to {{1cacd4}}{found_players[0].name}{{ffffff}}"
        )
    else:
        chat.send(
            player, f"{{ff0000}} Player {{ff9500}}{args[0]} {{ff0000}}not found..."
        )


def model_command(player: alt.Player, args: List[str]) -> None:
    if not args:
        chat.send(player, "Usage: /model (modelName)")
        return
    player.model = alt.hash(args[0])


def weapon_command(player: alt.Player, args: List[str]) -> None:
    if not args:
        chat.send(player, "Usage: /weapon (modelName)")
        return
    player.give_weapon(alt.hash("weapon_" + args[0]), 500, True)


def weapons_command(player: alt.Player, args: List[str]) -> None:
    for weapon in weapons:
        player.give_weapon(alt.hash("weapon_" + weapon), 500, True)


chat.register_cmd("help", help_command)
chat.register_cmd("veh", veh_command)
chat.register_cmd("pos", pos_command)
chat.register_cmd("tp", tp_command)
chat.register_cmd("model", model_command)
chat.register_cmd("weapon", weapon_command)
chat.register_cmd("weapons", weapons_command)

# ================================================== Commands End ==================================================
