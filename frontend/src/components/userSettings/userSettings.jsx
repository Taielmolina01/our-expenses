/* eslint-disable react/prop-types */
import  { useState, useEffect } from 'react';
import {   EditUser, GetUser } from '../../utils';
import '../createPaymentButton/createPaymentButton.css'
import LoadingSpinner from '../loadingSpinner/LoadingSpinner'

function EditUserSettings({ toggleSettings, setUserName }) {
    const [userN, setUserN] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);


    useEffect(() => {
        const user = GetUser();
        setUserN(user.name);
    },[]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            setIsLoading(true);
            await EditUser(setIsLoading, setError, userN)
            setUserName(userN);
            toggleSettings(false);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
                <div className="Modal-overlay">
                    <div className="Modal-content">
                        <div className="create-payment-container">
                            <h2 className="form-h2">User Settings</h2>
                            <form className="create-payment-form" onSubmit={handleSubmit}>
                                <div className="form-inputs">
                                    <label>Name</label>
                                    <input
                                        type="text"
                                        value={userN}
                                        onChange={(e) => setUserN(e.target.value)}
                                        required
                                        className="payment-description-input"
                                    />

                                    {error && <p style={{ color: 'red' }}>{error}</p>}
                                </div>

                                <button className={isLoading ? 'btn-form-disabled' : 'btn-form'} type="submit" disabled={isLoading} onClick={handleSubmit}>
                                    {isLoading ? (
                                        <LoadingSpinner style={{ display: 'inline-block', margin: '0', width: '25px', height: '25px' }} />
                                    ) : (
                                        "Update Settings"
                                    )}
                                </button>
                                <button className={isLoading ? 'btn-form-cancel-disabled' : 'btn-form-cancel'} onClick={() => toggleSettings(false)} disabled={isLoading}>
                                    Cancel
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
        </div>
    );
}

export { EditUserSettings };