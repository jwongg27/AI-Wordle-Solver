class WordleCSP:
    g = 0
    green = []

    #prioritize words with these letters first
    yellow = {
        0:[], 
        1:[], 
        2:[],
        3:[],
        4:[]
        }

    allWordsLeft = []

    variables = {0,1,2,3,4}
    domain = {
        0: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        1: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        2: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        3: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        4: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]}
    
    constraints = {
    }





    def __init__(self, var, domain, constraint):
        self.variable = var
        self.domain = domain
        self.constraint = constraint


    
    #guess: a list of tuples, containing the guessed letter, and the result (G, Y, B)
    def update(self, guess):
        return

        for i in range(5):
            letter, result = guess[0], guess[1]
            if result == "G":
                self.green[i] = letter
                self.domain[i] = [].append(letter)
            elif result == "Y":
                #add into the yellow dictionary as well
                self.yellow[i].append(letter)

                self.domain[i].pop(letter)
                for word in self.allWordsLeft:
                    if word[i] == letter:
                        self.allWordsLeft.remove(word)
                    elif letter not in word:
                        self.allWordsLeft.remove(word)

            elif result == "B":
                for val in self.domain:
                    self.domain[val].pop(letter)

                for word in self.allWordsLeft:
                    if letter in word:
                        self.allWordsLeft.remove(word)
        return

            
    def wordFound(self):
        for i in self.domain:
            if len(self.domain[i]) != 1:
                return False
        return True
    
    def possibleWord(self, word):
        for i in range(len(word)):
            letter = word[i]
            if letter in self.domain[i]:
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
        #using this array to find the most common letters
        alphabet = [0] * 26
        bestword = ""
        bestwordscore = 0
        for word in self.allWordsLeft:
            for letter in word:
                alphabet[ord(letter) - ord('a')] += 1

        for word in self.allWordsLeft:
            score = 0
            for letter in word:
                score += alphabet[ord(letter) - ord('a')]
            if score > bestwordscore:
                bestword = word
        return bestword