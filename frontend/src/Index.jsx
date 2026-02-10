import React, { useState, useEffect} from 'react'

function Index () {

    const [emailContent, setEmailContent] = useState()
    const [loading, setLoading] = useState(false)
    const [mailResult, setMailResult] = useState(null)
    const [error, setError] = useState(null)

    async function handleSubmit(e) {

        setLoading(true)
        setMailResult(null)

        try {
            e.preventDefault()
            const mailForm = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                headers: {
                    'content-type': 'application/json'
                },
                body: JSON.stringify({email: emailContent})
            })

            if (mailForm.ok) {
                const data = await mailForm.json()
                setMailResult(data)
            } else {
                setError("Sorry, something happened")
            }
        } catch {
            setError("Couldn't connect to the server")
        } finally {
            setLoading(false)
        }


    }

    return (
        
        <>
            <form onSubmit={handleSubmit}>
                <textarea value={emailContent} onChange={(e) => setEmailContent(e.target.value)}></textarea>
                <button type='submit'>Predict</button>
            </form>
            {mailResult ? (
                <ul>
                    <li>Status: {mailResult.status}</li>
                    <li>Score: {mailResult.score}</li>
                    <li>Conclusion: {mailResult.prediction}</li>
                </ul>
            ) : (
                <p>Please copy a mail into the text area.</p>
            )}
        </>
    )
}

export default Index;