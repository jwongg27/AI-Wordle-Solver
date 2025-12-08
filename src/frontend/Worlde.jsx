import "./wordle.css";
import React, { useState, useEffect} from 'react'

function Solver(){
    const [history, setHistory] = useState([])

    const [bestWord, setBestWord] = useState("ADIEU") //the next best word to use

    const [error, setError] = useState("")
    const [isLoading, setLoading] = useState(false)

    const [nextGuess, setNextGuess] = useState("") //user inputs what word they will guess
    const [nextGuessResults, setResults] = useState("") //after guessing on wordle, user inputs results

    // const [turn, setTurn] = useState(1)

    const validResults = ["G", "Y", "B"]

    const checkIfValid = () =>{
        // for (let r of nextGuessResults){
        //     if (!validResults.includes(r)){
        //         return false;
        //     }
        // }
        // const allLetters = [] //needs to have all lower and uppercase letters
        // for (let l of nextGuess){

        // }

    }


/// 
    const resetGame = async (e) => {
        try {
            const response = await fetch ("http://127.0.0.1:5000/reset", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
            })
        
        setHistory([])
        setBestWord("ADIEU")
        setNextGuess("")
        setResults("")
        setError("")
        } catch (e) {
            console.error(e)
        }
    }
    const handleSubmit = async (e) =>{
        e.preventDefault()

    // if (!checkIfValid()){
    //     setError("Please change the inputs to what the rules specify")
    // }

        let payload = {nextGuess, nextGuessResults}
        try{
            const response = await fetch ("http://127.0.0.1:5000/madeGuess", {
                method: "POST",
                headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
            })

            const result = await response.json()
            console.log(result.nextGuesses)
            if (result.success){
                setHistory(previousHistory => [
                    ...previousHistory,
                    { word: nextGuess, result: nextGuessResults}
                ])

                setBestWord(result.nextGuesses)
                setNextGuess("")
                setResults("")
                setError("")
                console.log("success")
            } 
        } catch (e){
            setError(e)
            console.error(e)
        }
    




    /// end of handle submit
}

    return(
        <div className="solver-container">
            <h1 id="rules">
                Wordle Solver

            </h1>

            <div id="nextGuessForm" className="form-container">
                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                    <label htmlFor="">Next Guess:</label>
                    <input id = "guessInput" type="text" value={nextGuess} maxLength={5} placeholder="APPLE" 
                    onChange={(e) => setNextGuess(e.target.value.toUpperCase())}/>
                    </div>

                    <div className="input-group">
                    <label htmlFor="">Results of Guess (G, Y, B):</label>
                    <input id = "resultInput" type="text" value={nextGuessResults} maxLength={5} placeholder="GBYBG"
                    onChange={(e) => setResults(e.target.value.toUpperCase())}/>
                    </div>
                <div className="button-container">
                    <button type="submit" className="submit-btn">Get Next Word</button>
                    <button onClick={resetGame} type="button" className="reset-btn">Reset</button>
                </div>
                </form>

            </div>

            <div id="bestWords" className="suggestion-box">
                {error}
                <div className="suggestion-label">Recommended Guess:</div>
                <div className="the-word">{bestWord}</div>
            
            </div>

            <div id="previousGuesses" className="history-container">
                <h3>History:</h3>
                <div className="history-list">
                    {history.map((h, index) => (
                        <div key={index} className="history-row">
                            <span className="turn-number">
                            <div className="word-grid">
                                {h.word.split('').map((letter, i) => (
                                    <span key={i} className={'tile ${h.result[i]}'}>
                                        {letter}
                                    </span>
                                ))}
                            </div>
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
                
    


}






export default Solver