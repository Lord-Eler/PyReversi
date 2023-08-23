import multiprocessing as mp
import pickle
from game import Board
from random import choice
from ai import AI

def AIGame(exploreConstant1,exploreConstant2,iterations=200):
        board = Board()
        turn = choice([True,False])
        ai1 = AI(turn,'mcts')
        ai2 = AI(not turn,'mcts')
        while not board.checkFinished():
            moves = board.validMoves()
            if moves == []:
                board.changeTurn()
                continue
            diskToPlay = None
            if board.getTurn() == turn:
                diskToPlay = ai1.monteCarlo(board,iterations,exploreConstant1)
            else:
                diskToPlay = ai2.monteCarlo(board,iterations,exploreConstant2)
            board.update(diskToPlay[0],diskToPlay[1],moves)
            board.changeTurn()
        
        board.count()
        if board.count1 == board.count2:
            return 0
        elif board.count1 < board.count2:
            return 2
        else:
            return 1

def AITournament(a,games,inf,sup,wins,total):
    exploreConstant = a/10
    results = []
    totalTemp = []
    for b in range(inf,sup):
        if a == b:
            results.append(-2)
            totalTemp.append(-2)
            continue
        exploreConstant2 = b/10
        results.append(0)
        totalTemp.append(0)
        for game in range(games):
            try:
                result = AIGame(exploreConstant,exploreConstant2)
                if result == 0:
                    results[b-inf] += 1/2
                elif result == 1:
                    results[b-inf] += 1
                elif result == 2:
                    results[b-inf] += 0
                totalTemp[b-inf] += 1
            except:
                errors.value += 1
        print(f'Process {a} at {round(100*(b-inf)/(sup-inf),2)} %')
    for b in range(inf,sup):
        wins[(a-inf)*(sup-inf)+b-inf] = results[b-inf]
        total[(a-inf)*(sup-inf)+b-inf] = totalTemp[b-inf]

if __name__ == '__main__':
    games = 20
    inf = 5
    sup = 20
    errors = mp.Value('i',0)
    processes = []
    wins = mp.Array('d',(sup-inf)**2)
    total = mp.Array('d',(sup-inf)**2)
    for a in range(inf,sup):
        process = mp.Process(target=AITournament,args=(a,games,inf,sup,wins,total))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    resultsWins = list(wins)
    resultsTotal = list(total)
    with open('results3.pickle','wb') as file:
        pickle.dump(resultsWins,file)
    with open('total3.pickle','wb') as file:
        pickle.dump(resultsTotal,file)
    print(errors.value)