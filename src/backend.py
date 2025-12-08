from flask import Flask, request, jsonify
from WordleCSP import WordleCSP
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
allWordsLeft = ["allow", "fruit"]

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

# wordleCSP = WordleCSP(variables, domain, constraints)

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
            len(domain[0]) == 1,
            len(domain[1]) == 1,
            len(domain[2]) == 1,
            len(domain[3]) == 1,
            len(domain[4]) == 1,
          }
      return jsonify({"success": True, "allWords": allWordsLeft})
   except Exception as e:
      print("resetting failed", e)
      return jsonify({"success": False})

@app.post("/madeGuess")
def madeGuess():
    # return jsonify({"nextGuesses": allWordsLeft})

    print("zzz")
    try:
      data = request.get_json()
      word = data.get("nextGuess")
      result = data.get("nextGuessResults")

      # return jsonify({"nextGuesses": type(wordleCSP)})
      word = word.lower()
      result = result.upper()
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
   print("allwordsleft:", allWordsLeft[0])
   print("updating")
   print(result)
   print("word:", word)
   temp = allWordsLeft[:]
   print(len(temp))
   print(len(allWordsLeft))

   # currentYellow = ["","","","",""]
   #same idea as the loop above
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
        print(" in g")
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
         print("in b")
         for val in domain:
            if currentLetter.upper() in domain[val]:
              domain[val].remove(currentLetter.upper())
          
#need to account for edge case were there is 1 green and 1 black for a letter in a word
         for w in allWordsLeft:
            if currentLetter.lower() in w:
               #the B letter is in the word
               # instanceofLetter = 0
               # for le in green:
               #    if le == currentLetter:
               #       instanceofLetter+=1

               inyellow = False
               for arr in yellow:
                  if currentLetter.lower() in yellow[arr]:
                     inyellow = True

               if inyellow:
                  #if in yellow, then just remove words with the letter in this index
                  print("in yellow", currentLetter)
                  if w[i] == currentLetter.lower() and w in temp:
                     temp.remove(w)
               # elif currentLetter.lower() in green:
               #    # multiple instances of the letter, where 1 is green and others are B
               #    # if the word has a B letter in that position, remove no matter what
               #    # but if it is not in yellow and is black, but is in green
               #    # remove every word where the greens of the currentletter doesnt match
               #    print("in the green section", currentLetter)
               #    for greenLetters in green:
               #       if greenLetters.lower() == currentLetter.lower() and w[i] != green[i] and w in temp:
               #          temp.remove(w)

               elif w[i] == currentLetter.lower() and w in temp:
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
   for c in constraints:
      if c == False:
         return False
   return True


def onStartup():
   with open("allWords.txt") as f:
      return f.read().splitlines()

if __name__ == "__main__":
    allWordsLeft = onStartup()
    app.run(debug=True)