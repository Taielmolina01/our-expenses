import React, { useState } from 'react';
import { BACK_URL, GetToken, GetUser, TrimField } from '../../utils'
import './inviteUserButton.css'

function InviteUserButton({ groupID }) {
    const [isOpen, setIsOpen] = useState(false);
    const [userEmail, setUserEmail] = useState('');
    const [error, setError] = useState(null);

    const user = GetUser();

    const toggleForm = () => {
        setIsOpen(!isOpen);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const sendDateString = new Date().toISOString().split('T')[0]; 
        const expireDate = new Date();
        expireDate.setDate(expireDate.getDate() + 7);
        const expireDateString = expireDate.toISOString().split('T')[0]; 
        setUserEmail(TrimField(userEmail));

        const requestBody = {
            "invitator_email": user.email,
            "guest_email": userEmail,
            "group_id": groupID,
            "send_date": sendDateString,
            "expire_date": expireDateString
        };
        
        try {
            const response = await fetch(`${BACK_URL}/invitations`, {
                method: 'POST',
                headers: {
                    "Authorization": `Bearer ${GetToken()}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestBody),
                cache: "no-store",
            });
            
            let result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail);
            }

            setUserEmail('');
            setError(null);
            toggleForm();
            alert("Success inviting your friend!")
        } catch (err) {
            setError(err.message);
        }
    };

    const cancelForm = () => {
        setUserEmail('');
        setError(null);
        toggleForm();
    };

    return (
        <div className="container">

            <button onClick={toggleForm} className="invite-user-button">
                + Invite a friend
            </button>

            {isOpen && (
                <div className="Modal-overlay">
                    <div className="Modal-content">
                        <div className="create-user-invitation-container">
                            <h2 className="form-h2">Invite user</h2>
                            <form onSubmit={handleSubmit}>
                                <div className="form-inputs">
                                    <label>
                                        Friend email
                                    </label>
                                    <input
                                        type="email"
                                        value={userEmail}
                                        onChange={(e) => {
                                            setError('')
                                            setUserEmail(e.target.value)}
                                        }
                                        required
                                        className="user-email-input"
                                    />
                                    {error && <p style={{ color: 'red' }}>{error}</p>} {}
                                </div>
                                <button type="submit" className="btn-form">Invite</button>
                                <button type="button" onClick={cancelForm} className="btn-form-cancel">Cancel</button>
                            </form>
                        </div>
                    </div>
                </div>
            )}

        </div>
    )
}

export default InviteUserButton