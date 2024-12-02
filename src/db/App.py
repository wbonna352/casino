import os
from time import sleep
from random import randint
from base import session
from models import Player
from games import play_range_roulette, play_straight_roulette


email: str = os.getenv("USER_EMAIL")
player: Player = Player.query.filter(Player.email == email).first()

if __name__ == '__main__':

    while player.account_balance >= 1:
        stake = max(player.account_balance * randint(5, 50) / 100, 1)
        game = play_range_roulette(player.id, stake)
        session.add(game)
        session.commit()
        sleep(randint(1, 120))
