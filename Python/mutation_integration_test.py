from Python.player import Player

myPlayer = Player([[0, 0, 0]])

for i in range(10):
    print(i)
    myPlayer.randomly_mutate_strategy()
    print(myPlayer.strategy)
