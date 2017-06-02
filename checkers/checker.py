'''
Ali Suleiman
start 6/8/2015 5:56 6:10

This program is a commandline checkers game.
The main intent of this program is to provide A checkers Al
That uses the minimax Algorithm to make descissions.

Special considerations:
	Jump chains are considered a single move as they are completed in a single turn.
	The minimax cursion function must be called inside a helper function that returns the move, using
	Portable checkers format standard

The input, Enter the location of the peice you wish to  (1-32) and select location 
you would like to go to (1-32)

If time allows, I will add a few more graphical features

░░▓▓░░▓▓░░▓▓░░▓▓
▓▓░░▓▓░░▓▓░░▓▓░░
░░▓▓░░▓▓░░▓▓░░▓▓
▓▓░░▓▓░░▓▓░░▓▓░░
░░▓▓░░▓▓░░▓▓░░▓▓
▓▓░░▓▓░░▓▓░░▓▓░░
░░▓▓░░▓▓░░▓▓░░▓▓

'''






'''
Board

 1▓▓ 2▓▓ 3▓▓ 4▓▓
▓▓ 5▓▓ 6▓▓ 7▓▓ 8
 9▓▓10▓▓11▓▓12▓▓
▓▓13▓▓14▓▓15▓▓16
17▓▓18▓▓19▓▓20▓▓
▓▓21▓▓22▓▓23▓▓24
25▓▓26▓▓27▓▓28▓▓
▓▓29▓▓30▓▓31▓▓32

'''
import subprocess
import time

board = [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
board3 = [-9,0,0,0,1,1,0,2,0,0,0,0,0,1,0,0,-2,0,0,0,0,-1,0,0,0,0,-1,0,0,0,0,0,0]
BKing = -2
BMan = -1
WKing = 2
WMan = 1
EmptySquare = 0

WManSprite = ["","",""]
BManSprite = ["","",""]
WKingSprite = ["","",""]
BKingSprite = ["","",""]
emptySprite = ["","",""]



'''
Code for Loading the sprites
'''

def loadSprite(filename):
	sprite = []
	f = open(filename,"r")
	for line in f:
		sprite.append(line.replace('"',"").replace(" \n",""))
	return sprite

WManSprite = loadSprite("whiteman.txt")
BManSprite = loadSprite("blackman.txt")
WKingSprite = loadSprite("whiteking.txt")
BKingSprite = loadSprite("BlackKing.txt")
emptySprite = loadSprite("blankspace.txt")

template = open("template_2.txt","r").read()

spriteDictionary = {-2:BKingSprite,-1:BManSprite ,1:WManSprite,2:WKingSprite,0:emptySprite,-9:["","",""]}

def printBoard(board):
	pass
	# count = 0
	# t1 = template
	# for i in board:
	# 	sprite1 = spriteDictionary[i]
	# 	##print len(sprite1[0])
	# 	t1 = t1.replace("{" +str(count)  + "a}", sprite1[0][:6])
	# 	t1 = t1.replace("{" +str(count)  + "b}", sprite1[1][:6])
	# 	t1 = t1.replace("{" +str(count)  + "c}", sprite1[2][:6])
	# 	count = count + 1
	# #print t1

def pB(board):
	count = 0
	t1 = template
	for i in board:
		sprite1 = spriteDictionary[i]
		##print len(sprite1[0])
		t1 = t1.replace("{" +str(count)  + "a}", sprite1[0][:6])
		t1 = t1.replace("{" +str(count)  + "b}", sprite1[1][:6])
		t1 = t1.replace("{" +str(count)  + "c}", sprite1[2][:6])
		count = count + 1
	print t1


def setupBoard():
	pass


'''
End of "Loading the sprites"
'''

'''
************************************************************
Opening moves dictionary
based on:
http://www.usacheckers.com/checkersinanutshell.php
'''
openingMove = '11-15'
# openingCounterMoves = {'11-15':'23-19', 
# 				'9-14': '22-18',
# 				'11-16':'22-18',
# 				'10-15':'21-17',
# 				'10-14':'24-19',
# 				'12-16':'24-20',
# 				'9-13':'22-18'
# 				}
openingCounterMoves = {'22-18':'10-14', 
				'24-19': '11-15',
				'22-17':'11-15',
				'23-18':'12-16',
				'23-19':'9-14',
				'21-17':'9-13',
				'24-20':'11-15'
				}

'''
*********************************************************
'''

'''
'***AI Functions***'
'''

"""
TODO HARD CODE SPACE Relations
"""



#Primitive Functions
def isOddRow(pos):
	return (((pos-1)/4)%2) == 1

def isEvenRow(pos):
	return (((pos-1)/4)%2) == 0

def isLeftEnd(pos):
	return pos%4 == 1

def isRightEnd(pos):
	return pos%4 == 0

def isOnBottomRow(pos):
	return pos >28

def isOnTopRow(pos):
	return pos < 5

def downLeft(pos):
	if (isLeftEnd(pos) and isOddRow(pos) or isOnBottomRow(pos)):
		return "NOP"
	if isEvenRow(pos):
		return pos + 4
	if isOddRow(pos):
		return pos + 3
	else:
		print "Unhandled Case!!"

def downRight(pos):
	if (isRightEnd(pos) and isEvenRow(pos) or isOnBottomRow(pos)):
		return "NOP"
	if isEvenRow(pos):
		return pos + 5
	if isOddRow(pos):
		return pos + 4


def upLeft(pos):
	if (isLeftEnd(pos) and isOddRow(pos) or isOnTopRow(pos)):
		return "NOP"
	if isEvenRow(pos):
		return pos - 4
	if isOddRow(pos):
		return pos - 5

def upRight(pos):
	if (isRightEnd(pos) and isEvenRow(pos) or isOnTopRow(pos)):
		return "NOP"
	if isEvenRow(pos):
		return pos - 3
	if isOddRow(pos):
		return pos - 4


def jumpUpRight(pos,b1):
	target = upRight(pos)
	if target =="NOP":
		return "NOP"
	des = upRight(upRight(pos))
	## print "des:" + str(des)
	## print "target:" + str(target)
	if des == "NOP":
		return "NOP"
	if b1[des] == 0 and (((b1[target] == -1 or b1[target] == -2) and b1[pos]>0) or((b1[target] == 1 or b1[target] == 2) and b1[pos]<0) ):
		return des
	else:
		return "NOP"

def jumpUpLeft(pos,b1):
	target = upLeft(pos)
	if target =="NOP":
		return "NOP"
	des = upLeft(upLeft(pos)) # This isnt safe passing NOP and triggering an error
	## print "des:" + str(des)
	## print "target:" + str(target)
	if des == "NOP":
		return "NOP"
	if b1[des] == 0 and (((b1[target] == -1 or b1[target] == -2) and b1[pos]>0) or((b1[target] == 1 or b1[target] == 2) and b1[pos]<0) ):
		return des
	else:
		return "NOP"

def jumpDownRight(pos,b1):
	target = downRight(pos)
	if target =="NOP":
		return "NOP"	
	des = downRight(downRight(pos))
	if des == "NOP":
		return "NOP"
	if b1[des] == 0 and (((b1[target] == -1 or b1[target] == -2) and b1[pos]>0) or((b1[target] == 1 or b1[target] == 2) and b1[pos]<0) ):
		return des
	else:
		return "NOP"	

def jumpDownLeft(pos,b1):
	target = downLeft(pos)
	if target =="NOP":
		return "NOP"
	des = downLeft(downLeft(pos))
	if des == "NOP":
		return "NOP"
	if b1[des] == 0 and (((b1[target] == -1 or b1[target] == -2) and b1[pos]>0) or((b1[target] == 1 or b1[target] == 2) and b1[pos]<0) ):
		return des
	else:
		return "NOP"

def checkForJumps(board,pos):
	global jumps
	jumps = []
	b1 = board[:]
	square = b1[pos]
	if square == BKing or square == WKing:
		directions = [jumpDownLeft,jumpDownRight,jumpUpLeft,jumpUpRight]
	if square == WMan:
		directions = [jumpDownLeft,jumpDownRight]
	if square == BMan:
		directions = [jumpUpLeft,jumpUpRight]
	checkForJumpsHelper(directions,b1,pos,str(pos))
	#print jumps
	return jumps 


def checkForJumpsHelper(directions,b1,pos,path):
	global jumps
	#b1 = board
	##print "pos is:" +str(pos)
	#printBoard(b1)
	jumpAvailableFlag = False
	for direction in directions:
		##print "pos"+ str(pos)+" NOP?" + str(direction(pos,b1))
		if direction(pos,b1) != "NOP":
			##print "checking: " + str(pos)
			nextpos = direction(pos,b1)
			##print "next pos: " + str(nextpos)
			b1[nextpos]=b1[pos]
			#printBoard(b1)
			#time.sleep(1)
			checkForJumpsHelper(directions,b1,nextpos, path+"x"+str(nextpos))
			b1[nextpos] = 0
			jumpAvailableFlag = True
			#paths.append(path)
	if not jumpAvailableFlag:
		if "x" in path:
			#print path
			jumps.append(path)
			#print jumps
			return jumps

def checkForSlidesHelper(directions,board,pos):
	slides = []
	for direction in directions:
		if direction(pos) is not "NOP":
			if board[direction(pos)] == 0:
				#print str(pos) + "-" + str(direction(pos))
				slides.append(str(pos) + "-" + str(direction(pos)))
	return slides


def checkForSlides(board,pos):
	square = board[pos]
	directions = []
	if square == BKing or square == WKing:
		directions = [downLeft, downRight, upLeft, upRight]
	if square == WMan:
		directions = [downLeft, downRight]
	if square == BMan:
		directions = [upLeft, upRight]
	return checkForSlidesHelper(directions,board,pos)

def listAvailableMoves(board,player):
	moves = []
	jumpsFlag = False
	if player > 0:
		for place in range(1,33):
			if board[place] > 0:
				if checkForJumps(board,place) != []:
					jumpsFlag = True
					moves = moves + checkForJumps(board,place)
		if jumpsFlag == False:
			for place in range(1,33):
				if board[place] > 0:
					moves = moves + checkForSlides(board,place)
	if player < 0:
		for place in range(1,33):
			if board[place] < 0:
				if checkForJumps(board,place) != []:
					jumpsFlag = True
					moves = moves + checkForJumps(board,place)
		if jumpsFlag == False:
			for place in range(1,33):
				if board[place] < 0:
					moves = moves + checkForSlides(board,place)
	return moves

def listAvailableMoves1(board,player):
	moves = []
	jumpsFlag = False
	if player > 0:
		for place in range(1,33):
			if board[place] > 0:
				if checkForJumps(board,place) != []:
					jumpsFlag = True
				if jumpsFlag == False:
					moves = moves + checkForSlides(board,place)
				else:
					moves = moves + checkForJumps(board,place)
	if player < 0:
		for place in range(1,33):
			if board[place] < 0:
				if checkForJumps(board,place) != []:
					jumpsFlag = True
				if jumpsFlag == False:
					moves = moves + checkForSlides(board,place)
				else:
					moves = moves + checkForJumps(board,place)
	return moves

def min(a,b):
	if a[1]>b[1]:
		return b
	else:
		return a

def max(a,b):
	if a[1]>b[1]:
		return a
	else:
		return b


'''
miniMax 
'''
def miniMax(node,depth,maxPlayer,whosMove):
	pass

'''
Return a node that represents the best move, that maximizes 
Computer Player, and Minimized Humun player
'''
def bestMove(node,depth,whosMove): #maxPlayer is assume
	pass


class Node:
	def __init__(self, ):
		#Position Prior to move
		self.parent = ""

		#String that describes move
		#Jump: "29x22x15"
		#Move: "29 26"
		self.Move = ""

		#Resulting Board State
		#board = [-9,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,]
		self.Result = ""

		#Sum of values of board
		self.Value = 0

class sprite:
	def __init__(self,a,b,c):
		this.a =a
		this.b =b
		this.c =c

# f = open("WhiteKing.txt","w+").read().replace('"','').split("/n")
# Bking = sprite(f[0],f[1],f[2])

# f = open("BlackKing.txt","w+").read().replace('"','').split("/n")
# Wking = sprite(f[0],f[1],f[2])

# f = open("Whiteman.txt").read().replace('"','').split("/n")
# Wman = sprite(f[0],f[1],f[2])

# f = open("blackman.txt").read().replace('"','').split("/n")
# Bman = sprite(f[0],f[1],f[2])

'''
'***User Input Related Functions***
'''
def isLegalMove(moveString,board):
	start = moveString.split(" ")
	if move in listMovesForPosition(board,position):
		return True
	else:
		return False
'''

'''
def listMovesForPosition(Board,position):
	square = Node.Result[position];
	moves = []
	pass

def move(position,to,board):
	peice = board[position]
	board[position] = 0
	board [to] = peice
	sum(board)
	printBoard(board)

def performMove(mv,board):
	if "-" in mv:
		pos,des = mv.split("-")
		pos = int(pos)
		des = int(des)
		move(pos,des,board)
	if "x" in mv:
		mvlist = mv.split("x")
		#print mvlist
		pos = mvlist[0]
		for i in range(0,len(mvlist)-1):
			mvlist[i] = int(mvlist[i])
			mvlist[i+1] = int(mvlist[i+1])
			delta = mvlist[i] - mvlist[i+1]
			if delta == 9:
				board[upLeft(mvlist[i])] = 0
			if delta == 7:
				#upright
				board[upRight(mvlist[i])] = 0
			if delta == -7:
				#downleft
				board[downLeft(mvlist[i])] = 0
			if delta == -9:
				board[downRight(mvlist[i])] = 0
			move(mvlist[i],mvlist[i+1],board)
			#time.sleep(1)
	for space in range(1,5):
		if board[space] == -1:
			board[space] = -2
	for space in range(29,33):
		if board[space] == 1:
			board[space] = 2
			#printBoard(board)
			#time.sleep(1)

def performMoveReal(mv,board):
	if "-" in mv:
		pos,des = mv.split("-")
		pos = int(pos)
		des = int(des)
		move(pos,des,board)
	if "x" in mv:
		mvlist = mv.split("x")
		#print mvlist
		pos = mvlist[0]
		for i in range(0,len(mvlist)-1):
			mvlist[i] = int(mvlist[i])
			mvlist[i+1] = int(mvlist[i+1])
			delta = mvlist[i] - mvlist[i+1]
			if delta == 9:
				board[upLeft(mvlist[i])] = 0
			if delta == 7:
				#upright
				board[upRight(mvlist[i])] = 0
			if delta == -7:
				#downleft
				board[downLeft(mvlist[i])] = 0
			if delta == -9:
				board[downRight(mvlist[i])] = 0
			move(mvlist[i],mvlist[i+1],board)
			pB(board)
			time.sleep(1)
	for space in range(1,5):
		if board[space] == -1:
			board[space] = -2
	for space in range(29,33):
		if board[space] == 1:
			board[space] = 2
			#printBoard(board)
			time.sleep(1)


def minimaxHelper(board, depth, maximizingPlayer,mv):
	performMove(mv,board)
	if depth == 0:
		sumval = sum(board)
		#printBoard(board)
		return [mv,sumval]
	if maximizingPlayer:
		bestValue = ["NOP",-1000]
		moves = listAvailableMoves(board,1)
		for mv in moves:
			val = minimaxHelper(board[:], depth - 1, False, mv)
			bestValue = max(bestValue, val)
			#time.sleep(1)
			#printBoard(board)
			#time.sleep(1)
		return bestValue
	else:
		bestValue = ["NOP",1000]
		moves = listAvailableMoves(board,-1)
		for mv in moves:
			val = minimaxHelper(board[:], depth - 1, True, mv)
			bestValue = min(bestValue, val)
		return bestValue

def minimax(board, depth, maximizingPlayer,mv):
	performMove(mv,board)
	if depth == 0:
		sumval = sum(board)
		#printBoard(board)
		return [mv,sumval]
	if maximizingPlayer:
		bestValue = ["NOP",-1000]
		moves = listAvailableMoves(board,1)
		# if len(moves) == 1:
		# 	return [moves[0],1]
		for mv in moves:
			val = minimaxHelper(board[:], depth - 1, False, mv)
			val[0]=mv
			#print mv + " val: " +str(val[1])
			bestValue = max(bestValue, val)
		#	time.sleep(1)
		#	printBoard(board)
		#	time.sleep(1)
		return bestValue
	else:
		bestValue = ["NOP",1000]
		moves = listAvailableMoves(board,-1)
		for mv in moves:
			val = minimaxHelper(board[:], depth - 1, True, mv)
			val[0] = mv
			bestValue = min(bestValue, val)
		return bestValue

def computerMove(board,plies):
	if listAvailableMoves(board,1) == []:
		print "Game Over, You win!"
	res = minimax(board, plies, True, "0+0")[0]
	performMoveReal(res,board)
	#print res
	pB(board)

def computerMoveB(board,plies):
	res = minimax(board, plies, False, "0+0")[0]
	performMove(res,board)
	#print res
	pB(board)


def main():
	subprocess.call("setup.bat")
	cmd = ""
	global board
	openingMv = True
	valid_difficulty = [1,2,3,4]
	difficulty = int(raw_input("Please enter your difficulty level (1-4):"))

	while (difficulty not in valid_difficulty):
		print "That is not a valid difficult, please enter (1,2,3,or 4) \n"
		difficulty = int(raw_input("Please enter your difficulty level(1-4):"))
	plies = difficulty * 2
	pB(board)
	print "Enter your next move(EX: 22 17):"
	prompt = ""
	while cmd != "q":
		cmd = str(raw_input(prompt))
		prompt = "\nEnter your next move:"
		if cmd == "r":
			board = [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
			difficulty = int(raw_input("Please enter your difficulty level (1-4):"))
			while (difficulty not in valid_difficulty):
				print "That is not a valid difficult, please enter (1,2,3,or 4) \n"
				difficulty = int(raw_input("Please enter your difficulty level(1-4):"))
			plies = difficulty * 2
			pB(board)
			continue
		if cmd == "c":
			computerMoveB(board,plies)
		if cmd == "p":
			pB(board)
			continue
		if cmd == "h":
			print "The following moves are available:"
			for i in listAvailableMoves(board,-1):
				print i
			raw_input("Press Enter to continue...")
			pB(board)
			continue
		allowed = listAvailableMoves(board,-1)
		if "x" in allowed[0]:
			cmd = cmd.replace(" ","x")
		if "-" in allowed[0]:
			cmd = cmd.replace(" ","-")
		if allowed == []:
			"Game Over, you lose."
			cmd = "r"
			continue
		if cmd in allowed:
			performMove(cmd,board)
			time.sleep(1)
			pB(board)
		else:
			if "x" in allowed[0]:
				print "You have jumps available, you must jump, \nEnter 'h' for a list of allowed \n moves."
				raw_input("Press Enter to continue...")
				pB(board)
				continue
			#time.sleep(1)
			continue
		if openingMv:
			print openingCounterMoves[cmd]
			performMoveReal(openingCounterMoves[cmd],board)
			time.sleep(1)
			pB(board)
			openingMv = False
		else:
			if difficulty < 2:
				time.sleep(1)
			if listAvailableMoves(board,1) == []:
				print "You Win!!!"
				cmd ="r"
				continue
			computerMove(board,plies)


if __name__ == '__main__':
	main()