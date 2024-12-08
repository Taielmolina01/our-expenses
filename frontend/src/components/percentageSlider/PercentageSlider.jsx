import React, { useState, useEffect } from 'react';
import './percentageSlider.css'

function PercentageForm({ users, sendDataToParent, isDisabled }) {
    const [percentages, setPercentages] = useState(
        users.reduce((acc, user) => {
            acc[user.user_email] = 0;
            return acc;
        }, {})
    );

    useEffect(() => {
        if (isDisabled) {
            const equalShare = 100 / users.length;
            let updatedPercentages = users.reduce((acc, user) => {
                acc[user.user_email] = equalShare;
                return acc;
            }, {});

            // Ajustar el último valor para que el total sea 100
            const totalAssigned = Object.values(updatedPercentages).reduce((a, b) => a + b, 0);
            if (totalAssigned < 100 && totalAssigned > 99) {
                const difference = 100 - totalAssigned;
                const lastUser = users[users.length - 1];
                updatedPercentages[lastUser.user_email] += difference;
            }

            setPercentages(updatedPercentages);
            sendDataToParent(updatedPercentages);
        }
    }, [isDisabled, users, sendDataToParent]);
    
    const handleChange = (id, value) => {
        let parsedValue = parseFloat(value) || 0;
        parsedValue = parseFloat(parsedValue.toFixed(2));
        const updatedPercentages = { ...percentages, [id]: parsedValue };
        setPercentages(updatedPercentages);
        sendDataToParent(updatedPercentages);
    };
    
    return (
        <div className="div-container">
            {users.map((user) => (
                <div className="user-div" key={user.user_email}>
                    <label>{user.user_name}</label>
                    <input
                        type="number"
                        value={percentages[user.user_email]?.toFixed(2)} 
                        onChange={(e) => handleChange(user.user_email, e.target.value)} 
                        min="0"
                        max="100"
                        step="0.1"
                        disabled={isDisabled}
                    />
                </div>
            ))}
            <p>Total porcentaje asignado: {Object.values(percentages).reduce((a, b) => a + b, 0).toFixed(2)}%</p>
        </div>
    );
}

export default PercentageForm;