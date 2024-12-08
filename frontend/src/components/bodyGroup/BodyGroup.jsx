import CreatePaymentButton from '../createPaymentButton/CreatePaymentButton';
import React, { useState, useEffect, useRef } from 'react';
import { BACK_URL, GetToken } from '../../utils';
import LoadingSpinner from '../loadingSpinner/LoadingSpinner' 
import './bodyGroup.css'
import InviteUserButton from '../inviteUsersButton/InviteUserButton';
import SelectDisplay from '../selectDisplay/SelectDisplay';

function BodyGroup({ groupName, groupID }) {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const hasBeenFetched = useRef(false);

    const token = GetToken();

    useEffect(() => {
        if (hasBeenFetched.current) return;

        const fetchBalanceUsers = async () => {
            try {
                setLoading(true);
                const res = await fetch(`${BACK_URL}/groups/${groupID}/users/data`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                }); 

                if (!res.ok) {
                    throw new Error("Error loading the group's users");
                }

                const data = await res.json();

                setUsers(data);

            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchBalanceUsers();
    }, [groupID, token]);


    if (error) {
        return (
            <div className="body-container">
                <p>Error: {error}</p>;
            </div>
        )
    } 

    return (
        <section className="body-container">
            <div className="body-title">
                <InviteUserButton groupID={groupID}/>
                <h3>
                    {groupName}
                </h3>
                <CreatePaymentButton users={users} groupID={groupID}/>
            </div>
            <div className="display-container">
                {loading ? (
                    <LoadingSpinner/>
                ) : (
                    <SelectDisplay groupID={groupID}/>
                )}
            </div>
        </section>
    )
}

export default BodyGroup;