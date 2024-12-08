import React, { useState, useEffect, useRef } from 'react';
import { BACK_URL, GetUser, GetToken } from '../../utils';
import LoadingSpinner from '../loadingSpinner/LoadingSpinner' 
import '../bodyGroup/bodyGroup.css'
import UserSelectDisplay from '../userSelectDisplay/UserSelectDisplay';

function BodyUser( {currentUser}) {
    const [profile, setProfile] = useState([]);
    const [payments, setPayments] = useState([]);
    const [debts, setDebts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const hasBeenFetched = useRef(false);

    const token = GetToken();
    const user = GetUser();
    
    useEffect(() => {
        if (hasBeenFetched.current) return;

        const fetchUserProfile = async () => {
            try {
                setLoading(true);
                const res = await fetch(`${BACK_URL}/users/${user.email}`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                  });

                if (!res.ok) {
                    throw new Error("Error loading the user's profile");
                }

                const data = await res.json();

                setProfile(data);

            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUserProfile();
    }, []);
    
    if (loading) {
        return (
            <div className="body-container">
                <LoadingSpinner />
            </div>
        )
    }

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
                <h3>
                    {currentUser ? `${user.name}` : `${user.name}`}
                </h3>
            </div>
            <div>
                {loading ? (
                    <LoadingSpinner/>
                ) : (
                    <UserSelectDisplay user={profile}/>
                )}
            </div>
        </section>
    )
}

export default BodyUser;