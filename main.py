from bot import Bot, BotOffense, BotDefense, BotOptimized, BotOptimizedCounterattack
import time
import animations
import os

sleep_time_eval = 1
sleep_time_main = 1
phase = None

# evaluate the guesses
def evaluate(guess, target_bot, guessing_bot):
    global phase
    phase = "evaluate"
    # evaluate the guess and return if it is higher, lower, or a hit
    if guess > target_bot.number:
        animation_display(guess, target_bot, guessing_bot)
        time.sleep(sleep_time_eval)
        return "lower"
    elif guess < target_bot.number:
        animation_display(guess, target_bot, guessing_bot)
        time.sleep(sleep_time_eval)
        return "higher"
    else:  # if it's a hit reduce health, print results, and reset number
        target_bot.health -= 10
        animation_display(guess, target_bot, guessing_bot)

        print(f"{target_bot.name} has been hit.")
        target_bot.number = target_bot.generate_number()
        time.sleep(sleep_time_eval)
        return 0

# adjust the guesses
def adjust_guess(bot, num_eval, guess):
    if num_eval == "higher":
        if not bot.optimized_counterattack:  # if not counterattack bot then adjust lower end
            bot.lower_end = guess + 1
        else:  # if counterattack bot then remove all guesses ruled out
            remove_elements(bot.number_set, 'beginning', bot.last_guess)
    elif num_eval == "lower":  # if not counterattack bot then adjust upper end
        if not bot.optimized_counterattack:
            bot.upper_end = guess - 1
        else:  # if counterattack bot then remove all guesses ruled out
            remove_elements(bot.number_set, 'end', bot.last_guess)
    else:
        bot.reset_bounds()  # reset the possible guesses after a successful hit

# optimized counterattack list edit
def remove_elements(list_name, direction, last_guess):
    index = list_name.index(last_guess)
    # remove beginning elements
    if direction == 'beginning':
        for x in range(index + 1):
            list_name.pop(0)

    # remove ending elements
    if direction == 'end':
        length = len(list_name) - 1
        iterations = length - index
        for x in range(iterations + 1):
            list_name.pop(length)
            length -= 1

# play the turn
def turn(bot):
    global phase
    phase = "guess"
    guess = bot.guess()
    animation_display(guess, bot)
    time.sleep(sleep_time_main)
    return guess

# reset the game
def reset_game():
    bot1.health = 100

# animation display function
def animation_display(guess, bot, guessing_bot=None):
    os.system('cls')
    print(f"{bot1.name}: {bot1.health}     {bot2.name}: {bot2.health}")
    if guess != bot.number:
        print(animations.idle)
    if phase == "guess":
        print(f"{bot.name} guesses {guess} ")
        print("          ")
    elif phase == "evaluate":
        print(f"{guessing_bot.name} guesses {guess} ")
        if guess > bot.number:
            print("Lower")
        elif guess < bot.number:
            print("Higher")
        else:  # if it's a hit reduce health, print results, and reset number
            if bot.name == "Bot 1":
                print(animations.bot2_attack)
                print("")
            else:
                print(animations.bot1_attack)
                print("")


simulation_amount = 100
bot1_wins = 0
bot2_wins = 0

for x in range(simulation_amount):
    bot1 = BotOptimizedCounterattack(name="Bot 1")
    bot2 = BotOptimizedCounterattack(name="Bot 2")
    while bot1.health > 0 and bot2.health > 0:
        # bot 1 turn
        bot1_guess = turn(bot1)  # bot 1 turn
        bot1_eval = evaluate(bot1_guess, bot2, bot1)  # evaluate bot 1's guess
        adjust_guess(bot1, bot1_eval, bot1_guess)  # adjust bot 1's guess
        if bot2.health == 0:
            break

        # bot 2 turn
        bot2_guess = turn(bot2)  # bot 2 turn
        bot2_eval = evaluate(bot2_guess, bot1, bot2)  # evaluate bot 2's guess
        adjust_guess(bot2, bot2_eval, bot2_guess)  # adjust bot 2's guess

    # evaluate winner
    if bot1.health == 0:
        print("Bot 2 wins!")
        bot2_wins += 1
    else:
        print("Bot 1 wins!")
        bot1_wins += 1

print(f"Bot 1 Wins: {bot1_wins} ({bot1_wins / (bot2_wins + bot1_wins)})")
print(f"Bot 2 Wins: {bot2_wins} ({bot2_wins / (bot2_wins + bot1_wins)})")

