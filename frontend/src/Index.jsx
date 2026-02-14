import React, { useState, useEffect} from 'react'
import './styles.css'

function Index () {

    const [emailContent, setEmailContent] = useState()
    const [loading, setLoading] = useState(false)
    const [mailResult, setMailResult] = useState(null)
    const [error, setError] = useState(null)

    async function handleSubmit(e) {

        setLoading(true)
        setMailResult(null)

        e.preventDefault()
        try {
            const mailForm = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                headers: {
                    'content-type': 'application/json'
                },
                body: JSON.stringify({email: emailContent})
            })

            if (mailForm.ok) {
                const data = await mailForm.json()
                console.log(data)
                setMailResult(data)
                console.log(mailResult)
            } else {
                setMailResult(null)
                const errorData = await mailForm.json()
                setError(errorData.detail)
            }
        } catch {
            setError("500 Internal Server Error")
        } finally {
            setLoading(false)
        }

    }

    const statusClass = mailResult?.status === 'spam'
        ? 'bg-spam'
        : mailResult?.status === 'mail'
        ? 'bg-mail'
        : 'bg-default'

    return (
        
        <>
            
            <div className={`container ${statusClass}`}>
                <h1 className='main-title'>Spam Detecor</h1>
                {mailResult ? (
                    <div className='result-container'>
                        <div>
                            <h1>This is a {mailResult.status}</h1>
                        </div>
                        <div>
                            <ul>
                                <li>Status: {mailResult.status}</li>
                                <li>Score: {mailResult.score}</li>
                                <li>Conclusion: {mailResult.prediction}</li>
                            </ul>
                        </div>
                        <div>
                            <button onClick={() => setMailResult(null)}>New prediction</button>
                        </div>
                    </div>
                ) : (
                    <div>
                        <form className='form-container' onSubmit={handleSubmit}>
                            <p>Please copy a mail into the text area. Mail must be under 5000 characters</p>
                            <textarea className='textarea' value={emailContent} onChange={(e) => setEmailContent(e.target.value)}></textarea>
                            <button type='submit' disabled={loading || !emailContent || emailContent.length > 5000}>Predict</button>
                        </form>
                    </div>
                )}
                {error ? (
                    <p>{error}</p>
                ) : null }
            </div>  
        </>
    )
}

export default Index;