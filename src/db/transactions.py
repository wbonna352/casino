from db.models import Player


def get_player_by_email(email: str) -> Player:
    return Player.query.filter(Player.email == email).first()


def is_player_exists(email: str) -> bool:
    return bool(get_player_by_email(email))


def get_player(player_id: int) -> Player:
    player = Player.query.filter(Player.id == player_id).first()
    assert player is not None, "Player not exists"
    return player
