from Python.player import Player

myPlayer = Player([[0, 0, 0]])

for i in range(10):
    print(i)
    myPlayer.randomlyMutateStrategy()
    print(myPlayer.strategy)
