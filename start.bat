start python -m kalaha server -H 127.0.0.1 -p 20202 -tt 60

@REM start python -m kalaha client -H 127.0.0.1 -p 20202 -ap -apd 10 -md 2
@REM start python -m kalaha client -H 127.0.0.1 -p 20202 -ap -apd 10 -ab -md 6

@REM Player with higher md with ab vs Player with lower md with no ab
@REM start python -m kalaha client -H 127.0.0.1 -p 20202 -ap -apd 0 -ab -md 2
@REM start python -m kalaha client -H 127.0.0.1 -p 20202 -ap -apd 0 -md 6

@REM Alpha-beta pruning disabled, player with higher minimax depth wins or ties
start python -m kalaha client -H 127.0.0.1 -p 20202 -ap -apd 5 -ab -md 2
start python -m kalaha client -H 127.0.0.1 -p 20202 -ap -apd 5 -ab -md 4

@REM Alpha-beta pruning disabled, one player uses iterative deepening
@REM start python -m kalaha client -H 127.0.0.1 -p 20202 -ap -apd 0 -ab -md 4 -id
@REM start python -m kalaha client -H 127.0.0.1 -p 20202 -ap -apd 0 -ab -md 2
