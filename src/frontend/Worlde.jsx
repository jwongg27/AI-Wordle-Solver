import "./wordle.css";
import React, { useState, useEffect} from 'react'

function solver(){
    const [history, setHistory] = useState({})

    const [bestWord, setBestWord] = useState("ADIEU") //the next best word to use

    const [error, setError] = useState("")
    const [isLoading, setLoading] = useState(false)

    const [nextGuess, setNextGuess] = useState("") //user inputs what word they will guess
    const [nextGuessResults, setResults] = useState("") //after guessing on wordle, user inputs results

    // const [turn, setTurn] = useState(1)

    const validResults = ["G", "Y", "B"]

    const checkIfValid = () =>{
    //     for (r in nextGuessResults){
    //         if (!validResults.includes(r)){
    //             return false;
    //         }
    //     }
    //     const allLetters = /^[A-Za-z]+$/
    //     return allLetters.test(nextGuess)

    }


///
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
        if (result.ok){
            setHistory(previousHistory => ({
                ...previousHistory, nextGuess: nextGuessResults}))

            setBestWord(result.nextGuesses)
            setError("")
            console.log(bestWord)
        } 
    } catch (e){
        setError(e)
        console.error(e)
    }




    /// end of handle submit
}

    return(
        <div>
            <h1 id="rules">
                Rules of AI Wordle Solver

            </h1>

            <div id="nextGuessForm">
                <form onSubmit={handleSubmit}>
                    <div>
                    <label htmlFor="">Next Guess:</label>
                    <input type="text" value={nextGuess} 
                    onChange={(e) => setNextGuess(e.target.value)}/>
                    </div>

                    <div>
                    <label htmlFor="">Results of Guess (G, Y, B):</label>
                    <input type="text" value={nextGuessResults}
                    onChange={(e) => setResults(e.target.value)}/>
                    </div>

                    <button type="submit">Get Next Word</button>
                </form>

            </div>

            <div id="bestWords">
                {error}
            </div>

            <div id="previousGuesses">
                {/* {history.map((h) => (
                    <div>{h}</div>
                ))} */}
            </div>

        </div>
    )


}





export default solver