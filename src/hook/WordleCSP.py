class WordleCSP:

    variables = {1, 2, 3, 4, 5}
    domain = {
        1: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        2: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        3: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        4: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        5: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]}
    
    constraints = {
        len(domain[1]) == 1,
        len(domain[2]) == 1,
        len(domain[3]) == 1,
        len(domain[4]) == 1,
        len(domain[5]) == 1
    }



    green = []

    #prioritize words with these letters first
    yellow = {}

    allWordsLeft = []

    def __init__(self, var, domain, constraint):
        self.variable = var
        self.domain = domain
        self.constraint = constraint
        self.solution = None


    
    #guess: a list of tuples, containing the guessed letter, and the result (G, Y, W)
    def update(self, guess):
        for i in range(len(guess)):
            g = guess[i]
            letter, result = g[0], g[1]
            if result == "G":
                self.green[i] = letter
                self.domain[i+1] = [].append(letter)
            elif result == "Y":
                #add into the yellow dictionary as well


                self.domain[i+1].pop(letter)
            elif result == "W":
                for val in self.domain:
                    self.domain[val].pop(letter)

            
    def wordFound(self):
        for i in self.domain:
            if len(self.domain[i]) != 1:
                return False
        return True
    
    def possibleWord(self, word):
        for i in range(len(word)):
            letter = word[i]
            if letter in self.domain[i+1]:
                next
            else:
                return False
        return True
            

    def nextPossibleWords(self):
        temp = []
        for word in self.allWordsLeft:
            if (self.possibleWord(self, word)):
                temp.append(word)
        return temp
    
    def optimalGuesses(self):
