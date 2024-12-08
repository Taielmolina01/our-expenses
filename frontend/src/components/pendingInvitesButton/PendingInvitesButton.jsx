import React, { useState, useEffect } from 'react';
import { BACK_URL, GetToken, GetUser, AcceptInvitation, RejectInvitation } from '../../utils';
import './pendingInvitesButton.css';

function PendingInvitesButton() {
    const [isOpen, setIsOpen] = useState(false);
    const [error, setError] = useState(null);
    const [requests, setRequests] = useState([]);
    const [enableRenderRequests, setEnableRenderRequests] = useState(false);

    const user = GetUser();
    const token = GetToken();

    useEffect(() => {
        const fetchUserInvitations = async () => {
            try {
                const response = await fetch(`${BACK_URL}/invitations/${user.email}/data`, {
                    method: 'GET',
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                    cache: "no-store",
                });
                const data = await response.json();
                if (data) {
                    setRequests(data);
                }
    
                if (!response.ok) {
                    throw new Error('Error fetching invitations');
                }
                setError(null);
            } catch (err) {
                setError(err.message);
            } 
        };

        fetchUserInvitations();
    }, []);

    const toggleForm = () => {
        setIsOpen(true);
    };

    const disableForm = () => {
        setIsOpen(false);
    };

    const handleAccept = async (invitationId) => {
        try {
            await AcceptInvitation(invitationId);
            window.location.reload();
        } catch (err) {
            setError(err.message);
        }
    };

    const handleReject = async (invitationId) => {
        try {
            await RejectInvitation(invitationId);
            window.location.reload();
        } catch (err) {
            setError(err.message);
        }
    };

    const hasPendingInvitations = requests.length > 0; 

    return (
        <div>
            <button 
                onClick={toggleForm} 
                className={`pending-invites-button ${hasPendingInvitations ? 'pending' : ''}`}
                disabled={!hasPendingInvitations}
            >
                Pending invites
            </button>

            {isOpen && (
                <div className="Modal-overlay">
                    <div className="Modal-content">
                        <div className="pending-invites-container">
                            <h2 className="form-h2">Pending Invites</h2>
                            <div style={{ padding: "20px" }}>
                                {requests.map((request) => (
                                    <div className="pending-invite"
                                        key={request.invitation_id}>
                                        <div>
                                            <h3>{request.group_name}</h3>
                                            <p>Invited by {request.invitator_name}</p>
                                        </div>
                                        <div>
                                            <button 
                                                className="btn-accept" 
                                                onClick={() => handleAccept(request.invitation_id)}
                                                >
                                                Accept
                                            </button>
                                            <button
                                                className="btn-reject"
                                                onClick={() => handleReject(request.invitation_id)}
                                                >
                                                Reject
                                            </button>
                                        </div>
                                    </div>
                                ))}
                                <div style={{ display: "flex", justifyContent: "center" }}>
                                    <button type="button" onClick={disableForm} className="btn-cancel">Close</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default PendingInvitesButton;
