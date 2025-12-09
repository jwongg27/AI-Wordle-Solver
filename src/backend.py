from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback


app = Flask(__name__, static_folder="dist")
CORS(app, origins=["http://localhost:5173"])

g = 0
global green
global yellow
global domain
global variables
global constraints

green = ["", "", "", "", ""]

    #prioritize words with these letters first
yellow = {
        0:[], 
        1:[], 
        2:[],
        3:[],
        4:[]
        }

#all lowercase variables
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
    
constraints = [
      green[0] != "",
      green[1] != "",
      green[2] != "",
      green[3] != "",
      green[4] != "",
    ]


@app.post("/reset")
def resetPost():
   try:
      global green
      global yellow
      global domain
      global variables
      global constraints
      global allWordsLeft

      green = ["", "", "", "", ""]

          #prioritize words with these letters first
      yellow = {
              0:[], 
              1:[], 
              2:[],
              3:[],
              4:[]
              }
      allWordsLeft = onStartup()
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
            green[0] != "",
            green[1] != "",
            green[2] != "",
            green[3] != "",
            green[4] != "",
          }
      return jsonify({"success": True, "allWords": allWordsLeft})
   except Exception as e:
      print("resetting failed", e)
      return jsonify({"success": False})

@app.post("/madeGuess")
def madeGuess():

    try:
      data = request.get_json()
      word = data.get("nextGuess")
      result = data.get("nextGuessResults")
      word = word.lower()
      result = result.upper()

      lowercaseAlphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", 
                            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
      resultLetters = ["G", "Y", "B"]


      word = word.lower()
      result = result.upper()
      if len(word) != 5 or len(result) != 5 or all(l not in lowercaseAlphabet for l in word) or all(r not in resultLetters for r in result):
         return ({"success": False, "error": "Wrong Format"})

      update(word, result)

      nextguess = optimalGuess()

      cons = check()
      print("solved:",cons)

      return jsonify({"nextGuesses": nextguess, "success": True, "solved": cons})
    
    except Exception as e:
       print("error", e)
       traceback.print_exc()
       return jsonify({"error": e})

def update(word, result):
   global allWordsLeft
   global green
   if not allWordsLeft:
      print("no words found")
      return
   word = word.lower()
   result = result.upper()

   #allWordsLeft needs to be kept unchanged atm since it is being looped through
   temp = allWordsLeft[:]

   for i in range(5):
      #deal with cases where there is multiple of the same letter and B comes before G
      currentLetter = word[i]
      currentResult = result[i]
      if currentResult == "G":
         green[i] = currentLetter

      elif currentResult == "Y":
         yellow[i].append(currentLetter)





   for i in range(5):
      currentLetter = word[i]
      currentResult = result[i]

      if currentResult == "G":
        green[i] = currentLetter.lower() #lowercase
        domain[i] = [currentLetter]

        for w in allWordsLeft:
           if w[i] != currentLetter.lower():
              if w in temp:
                 temp.remove(w)


      elif currentResult == "Y":
         
         yellow[i].append(currentLetter)

         if currentLetter.upper() in domain[i]:
          domain[i].remove(currentLetter.upper())

         for w in allWordsLeft:
            if w[i] == currentLetter.lower():
               #remove if current letter has the letter in the yellow position
               if w in temp:
                  temp.remove(w)


            elif currentLetter.lower() not in w:
               if w in temp:
                  temp.remove(w)


      elif currentResult == "B":
         for val in domain:
            if currentLetter.upper() in domain[val] and (currentLetter not in green or all(currentLetter not in yellow[y] for y in yellow)):
              domain[val].remove(currentLetter.upper())
          
#need to account for edge case were there is 1 green and 1 black for a letter in a word
         for w in allWordsLeft:
            if currentLetter.lower() in w:
               inyellow = False
               for arr in yellow:
                  if currentLetter.lower() in yellow[arr]:
                     inyellow = True

               if inyellow:
                  #if in yellow, then just remove words with the letter in this index
                  if w[i] == currentLetter.lower() and w in temp:
                     temp.remove(w)
               elif currentLetter.lower() in green:
                  # multiple instances of the letter, where 1 is green and others are B
                  if w[i] == currentLetter.lower() and w in temp:
                     temp.remove(w)

               elif currentLetter.lower() not in green and w in temp:
                  temp.remove(w)

   print(temp)
   allWordsLeft = temp

def optimalGuess():
   alphabet = [0] * 26
   bestword = ""
   bestwordscore = 0
   for word in allWordsLeft:
      for letter in word:
         alphabet[ord(letter) - ord('a')] += 1

   for word in allWordsLeft:
      score = 0
      for letter in word:
         score += alphabet[ord(letter) - ord('a')]
      if score > bestwordscore:
         bestword = word
         bestwordscore = score
   return bestword


def check():
   return all(g != "" for g in green) and len(allWordsLeft) == 1


def onStartup():
   with open("allWords.txt") as f:
      return f.read().splitlines()

if __name__ == "__main__":
    allWordsLeft = onStartup()
    app.run(debug=True)