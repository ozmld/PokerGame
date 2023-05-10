from Run import Run


def __main__():
    poker = Run()
    poker.start()
    while poker.human_is_in_game() and poker.get_players_num() > 1:
        poker.run_subround()
        if poker.get_subround_name() == "showdown":
            poker.delete_zero_balance_players()
            poker.next_round()
        poker.next_subround()
    poker.end_game()


__main__()
