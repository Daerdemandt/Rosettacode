#!/usr/bin/env python3

import curses
from random import randrange, choice

letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))

field_height, field_width = 4, 4
game_field = []
score, highscore = 0, 0
help_string1 = '(W)Up (S)Down (A)Left (D)Right\n'
help_string2 = '     (R)Restart (Q)Exit\n'

def reset_game():
	global game_field
	global score
	global highscore
	if score > highscore:
		highscore = score
	score = 0
	game_field = [[0 for i in range(field_width)] for j in range(field_height)]

def get_user_action(keyboard):    
	char = "N"
	while char not in actions_dict:    
		char = keyboard.getch()
	return actions_dict[char]

def draw(screen):
	screen.clear()
	def draw_hor_separator():
		top = '┌' + ('┬──────' * field_width + '┐')[1:] + '\n'
		mid = '├' + ('┼──────' * field_width + '┤')[1:] + '\n'
		bot = '└' + ('┴──────' * field_width + '┘')[1:] + '\n'
		if not hasattr(draw_hor_separator, "counter"):
			draw_hor_separator.counter = 0
			current = top
		else:
			current = bot if draw_hor_separator.counter == field_height else mid
		screen.addstr(current)
		draw_hor_separator.counter += 1

	def draw_row(row):
		string = ''.join('│{: ^5} '.format(num) for num in row) + '│\n'
		screen.addstr(string)

	screen.addstr('SCORE: ' + str(score) + '\n')
	if 0 != highscore:
		screen.addstr('HGHSCORE: ' + str(highscore) + '\n')
	for row in game_field:
		draw_hor_separator()
		draw_row(row)
	draw_hor_separator()
	screen.addstr(' '*10 + 'GAME OVER' if is_gameover() else help_string1)
	screen.addstr(help_string2)

def left_or_right_is_possible(field):
	if any(0 in row for row in field):
		return True
	merge_in_rows = [[row[i] == row[i + 1] for i in range(len(row) - 1)] for row in field if len(row) > 1]
	return any(any(row) for row in merge_in_rows)

def transpose(field):
	return [list(row) for row in zip(*field)]

def up_or_down_is_possible(field):
	return left_or_right_is_possible(transpose(field))

def is_possible(action):
	assert action in ['Up', 'Left', 'Down', 'Right']
	if action in ['Left', 'Right']:
		return left_or_right_is_possible(game_field)
	else:
		return up_or_down_is_possible(game_field)

def is_gameover():
	global highscore
	highscore = not any((left_or_right_is_possible(game_field), up_or_down_is_possible(game_field)))
	return not any((left_or_right_is_possible(game_field), up_or_down_is_possible(game_field)))

def is_2048():
	return False

def move(direction):
	def move_row_left(row):
		def tighten(row):
			new_row = [i for i in row if i != 0]
			new_row += [0 for i in range(len(row) - len(new_row))]
			assert len(new_row) == len(row)
			return new_row

		def merge(row):
			global score
			pair = False
			new_row = []
			for i in range(len(row)):
				if pair:
					new_row.append(2 * row[i])
					score += row[i]
					pair = False
				else:
					if i + 1 < len(row) and row[i] == row[i + 1]:
						pair = True
						new_row.append(0)
					else:
						new_row.append(row[i])
			assert len(new_row) == len(row)
			return new_row
		return tighten(merge(tighten(row)))

	def move_left():
		global game_field
		game_field = [move_row_left(row) for row in game_field]

	def invert():
		global game_field
		game_field = [row[::-1] for row in game_field]

	def move_right():
		invert()
		move_left()
		invert()

	def move_up():
		global game_field
		game_field = transpose(game_field)
		move_left()
		game_field = transpose(game_field)

	def move_down():
		global game_field
		game_field = transpose(game_field)
		move_right()
		game_field = transpose(game_field)
		
	d = dict(zip(actions, [move_up, move_left, move_down, move_right]))
	d[direction]()			

def spawn():
	global game_field
	new_element = 4 if randrange(100) > 89 else 2
	(i,j) = choice([(i,j) for i in range(field_width) for j in range(field_height) if game_field[i][j] == 0])	
	game_field[i][j] = new_element

def init():
	global game_field
	global score
	global highscore
	if score > highscore:
		highscore = score
	score = 0
	game_field = [[0 for i in range(field_width)] for j in range(field_height)]
	

def main(stdscr):
	pass
		

curses.wrapper(main)
