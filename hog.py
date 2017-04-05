"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.


    >>> counted_dice = make_test_dice(4, 1, 2, 6)
    >>> roll_dice(3, counted_dice)
    1
    >>> roll_dice(1, counted_dice)  # Make sure you call dice exactly num_rolls times!
    6
    """

    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    count = 0
    diceSum = 0
    oneRolled = False
    while count < num_rolls:
        currentRoll = dice()
        # Pig Out
        if currentRoll == 1:
            oneRolled = True
        diceSum += currentRoll
        count += 1
    if oneRolled == True:
        return 1
    else:
        return diceSum
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    >>> free_bacon(42)
    5
    >>> free_bacon(57)
    8
    >>> free_bacon(7)
    8
    >>> free_bacon(0)
    1

    """
    # BEGIN PROBLEM 2
    return 1 + max( (opponent_score%10), (opponent_score//10) )
    # END PROBLEM 2

# Write your prime functions here!

def is_prime(integer):
    """
    >>> is_prime(47)
    True
    >>> is_prime(49)
    False
    >>> is_prime(51)
    False
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True

    """
    if integer == 1:
        return False
    else:
        for n in range(2,integer):
            if integer % n == 0:
                return False
        return True


def next_prime(integer):
    while(1):
        integer += 1
        if is_prime(integer):
            return integer



def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    >>> take_turn(2, 0, make_test_dice(4, 6, 1))
    10
    >>> take_turn(3, 0, make_test_dice(4, 6, 1))
    1
    >>> take_turn(0, 35)
    6
    >>> take_turn(0, 7)
    8
    >>> take_turn(0, 0)
    1
    >>> take_turn(1, 0, make_test_dice(3))
    5

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if num_rolls == 0:
        diceRoll = free_bacon(opponent_score)
    else:
        diceRoll = roll_dice(num_rolls, dice)
    # Hogtimus Prime
    if is_prime(diceRoll):
        return next_prime(diceRoll)
    else:
        return diceRoll
    # END PROBLEM 2

# Hog Wild
def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).

    >>> select_dice(4, 24) == four_sided
    True
    >>> select_dice(16, 64) == four_sided
    False
    >>> select_dice(0, 0) == four_sided
    True
    >>> select_dice(50, 80) == four_sided
    False

    """
    # BEGIN PROBLEM 3
    if (score+opponent_score)%7 == 0:
        return four_sided
    else:
        return six_sided
    # END PROBLEM 3

#Hog Tied
def max_dice(score, opponent_score):
    """Return the maximum number of dice the current player can roll. The
    current player can roll at most 10 dice unless the sum of SCORE and
    OPPONENT_SCORE ends in a 7, in which case the player can roll at most 1.

    >>> max_dice(7, 10)
    1
    >>> max_dice(10, 7)
    1
    >>> max_dice(23, 44)
    1
    >>> max_dice(35, 35)
    10

    """
    # BEGIN PROBLEM 3
    if (score+opponent_score)%10 == 7:
        return 1
    else:
        return 10
    # END PROBLEM 3

# Swine Swap
def is_swap(score):
    """Returns whether the SCORE contains only one unique digit, such as 22.
    >>> is_swap(19)
    False
    >>> is_swap(44)
    True
    >>> is_swap(2) # Single digits have one unique digit
    True
    >>> is_swap(100)
    False
    >>> is_swap(111)
    True
    """
    # BEGIN PROBLEM 4
    if score//10 == 0:
        return True
    else:
        onesDigit = score % 10
        currentScore = score//10
        while currentScore != 0:
            if(currentScore%10 != onesDigit):
                return False
            currentScore //= 10
        return True

    # END PROBLEM 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> import hog
    >>> hog.four_sided = hog.make_test_dice(1)
    >>> hog.six_sided = hog.make_test_dice(3)
    >>> always = hog.always_roll
    >>> # Play function stops at goal
    >>> s0, s1 = hog.play(always(5), always(3), score0=91, score1=10)
    >>> s0
    106
    >>> s1 # answer to this is 10
    10
    >>> # Goal score is not hardwired
    >>> s0, s1 = hog.play(always(5), always(5), goal=10)
    >>> s0
    0
    >>> s1
    16
    >>> # Swine swap applies to 3 digit scores
    >>> s0, s1 = hog.play(always(5), always(3), score0=96, score1=10)
    >>> s0
    10
    >>> s1
    111

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    maxDice = 0
    selectedDice = None
    # each strategy function should be called once per turn
    while score0 < goal and score1 < goal:
        # figure out max number of dice current player is allowed to roll
        maxDice = max_dice(score0, score1)
        # select dice for current player (four-sided or six-sided
        selectedDice = select_dice(score0, score1)
        # roll dice
        if player == 0:
            score0 += take_turn( min( maxDice, strategy0(score0, score1) ), score1, selectedDice )
            if is_swap(score0):
                score0, score1 = score1, score0
        elif player == 1:
            score1 += take_turn( min( maxDice, strategy1(score1, score0) ), score0, selectedDice )
            if is_swap(score1):
                score0, score1 = score1, score0
        # switch current player
        player = other(player)
        # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """

    @check_strategy
    def strategy(score, opponent_score):
        return n

    return strategy

def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid strategy
    output. All strategy outputs must be non-negative integers less than or
    equal to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'

def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the 
    strategy returns a valid input. Use `check_strategy_roll` to raise 
    an error with a helpful message if the strategy returns an invalid 
    output.

    >>> always_roll_5 = always_roll(5)
    >>> # Be specific about the error type (AssertionError, rather than Error)
    >>> always_roll_5 == check_strategy(always_roll_5)
    True
    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> fail_15_20 == check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_15_20(score, opponent_score):
    ...     if score == 15 and opponent_score == 20:
    ...         return 100
    ...     return 5
    >>> fail_15_20 == check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned 100 (invalid number of rolls)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> fail_102_115 == check_strategy(fail_102_115)
    True
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    # call strategy for all valid inputs
    validRange = range(0, goal)
    for x in validRange:
        for y in validRange:
            check_strategy_roll(x, y, strategy(x, y))
    # END PROBLEM 6
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> averaged_roll_dice = make_averaged(roll_dice, 1000)
    >>> # Average of calling roll_dice 1000 times
    >>> averaged_roll_dice(2, dice)
    6.0
    """
    # BEGIN PROBLEM 7
    def averageFN(*args):
        i = 0
        sumFN = 0
        while i < num_samples:
            sumFN += fn(*args)
            i += 1
        return sumFN/num_samples

    return averageFN
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    """
    averageScores = {
        '1': make_averaged(roll_dice, num_samples)(1, dice),
        '2': make_averaged(roll_dice, num_samples)(2, dice),
        '3': make_averaged(roll_dice, num_samples)(3, dice),
        '4': make_averaged(roll_dice, num_samples)(4, dice),
        '5': make_averaged(roll_dice, num_samples)(5, dice),
        '6': make_averaged(roll_dice, num_samples)(6, dice),
        '7': make_averaged(roll_dice, num_samples)(7, dice),
        '8': make_averaged(roll_dice, num_samples)(8, dice),
        '9': make_averaged(roll_dice, num_samples)(9, dice),
        '10': make_averaged(roll_dice, num_samples)(10, dice)
    }
    """
    averageScores = {}
    i = 1
    while i < 11:
        averageScores[str(i)] = make_averaged(roll_dice, num_samples)(i, dice)
        i += 1

    maxValue = averageScores[ max(averageScores, key=lambda x: averageScores[x]) ]
    # max returns some key associated with the max value (there may be more than one such key)
    # from Python 3.5.2 documentation:
    # "If multiple items are maximal, the function returns [the key associated with]
    #  the first one encountered."
    # remember: you don't know anything about the order in which dictionaries are checked
    keys = []
    for key in averageScores:
        if averageScores[key] == maxValue:
            keys += [key]

    return int( min(keys) )


    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

@check_strategy
def bacon_strategy(score, opponent_score, margin=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.

    >>> bacon_strategy(0, 0, margin=8, num_rolls=5)
    5
    >>> bacon_strategy(70, 50, margin=8, num_rolls=5)
    5
    >>> bacon_strategy(50, 70, margin=8, num_rolls=5)
    0

    """
    # BEGIN PROBLEM 9
    if take_turn(0, opponent_score, select_dice(score, opponent_score)) >= margin:
        return 0
    else:
        return num_rolls  # Replace this statement
    # END PROBLEM 9


@check_strategy
def swap_strategy(score, opponent_score, margin=5, num_rolls=6):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points and doesn't trigger a
    swap. Otherwise, it rolls NUM_ROLLS.
    >>> swap_strategy(23, 60, 5, 6)
    0
    >>> swap_strategy(38, 54, 10, 6) # beneficial swap
    0
    """
    # BEGIN PROBLEM 10
    turnScore = take_turn(0, opponent_score, select_dice(score, opponent_score))
    scoreTotal = score + turnScore
    if ( scoreTotal < opponent_score and is_swap(scoreTotal) ) \
            or ( turnScore >= margin and not is_swap(scoreTotal) ):
        return 0
    else:
        return num_rolls
    # END PROBLEM 10



@check_strategy
def final_strategy(score, opponent_score, margin=7, num_rolls=8):
    """
    Prevent swap if winning
    try to force a beneficial swap at all costs
    sometimes trigger "hog tied" for opponent
    make num_rolls less when "hog wild"
    (change defaults values for margin and num_rolls)

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 10

    turnScore = take_turn(0, opponent_score, select_dice(score, opponent_score))
    scoreTotal = score + turnScore
    if (scoreTotal < opponent_score and is_swap(scoreTotal)) \
            or (turnScore >= margin and not is_swap(scoreTotal)) \
            or select_dice(score, opponent_score) is four_sided and not is_swap(scoreTotal) \
            or (score+opponent_score)%7 == 0 and not is_swap(scoreTotal) \
            or (scoreTotal+opponent_score)%10 == 7 and not is_swap(scoreTotal):
        return 0
    else:
        return num_rolls
    # END PROBLEM 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()