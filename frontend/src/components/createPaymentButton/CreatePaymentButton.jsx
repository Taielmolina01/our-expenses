import React, { useState, useRef, useEffect } from 'react';
import { BACK_URL, GetToken, MAX_NAME_LENGTH, TrimField } from '../../utils';
import './createPaymentButton.css'
import LoadingSpinner from '../loadingSpinner/LoadingSpinner'
import PercentageSlider from '../percentageSlider/PercentageSlider';
import BasickDatePicker from '../datePicker/DatePicker';
import dayjs from 'dayjs';
import { format } from 'date-fns';

function CreatePaymentButton({ users, groupID }) {
    const [isOpen, setIsOpen] = useState(false);
    const [paymentDescription, setpaymentDescription] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [paymentCategorySelected, setPaymentCategorySelected] = useState('');
    const [paymentCategories, setPaymentCategories] = useState([]);
    const [paymentDate, setPaymentDate] = useState(null);
    const [userSelected, setUserSelected] = useState('');
    const [percentagesData, setPercentagesData] = useState([]);
    const hasBeenFetched = useRef(false);
    const [paymentAmount, setPaymentAmount] = useState('');
    const [error, setError] = useState(null);
    const [isChecked, setIsChecked] = useState(false);

    const handleCheckboxChange = (event) => {
      setIsChecked(event.target.checked);
    };

    const token = GetToken();

    const toggleForm = () => {
        setIsOpen(!isOpen);
    };

    useEffect(() => {
        const fetchCategories = async () => {
            
            if (hasBeenFetched.current) return;

            try {
                setIsLoading(true);

                const res = await fetch(`${BACK_URL}/payments/options`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                    cache: "no-store",
                  }); 

                if (!res.ok) {
                    throw new Error('Error loading the payment categories');
                }

                const data = await res.json();
                setPaymentCategories(data);

            } catch (err) {
                setError(err.message);
            } finally {
                setIsLoading(false);
                hasBeenFetched.current = true;
            }
        };

        fetchCategories();
        
    }, []); 

    const handleSubmit = async (e) => {
        e.preventDefault();

        const totalPercentage = Object.values(percentagesData).reduce((a, b) => a + b, 0);

        setpaymentDescription(TrimField(paymentDescription));

        if (!userSelected) {
            setError("You must select a payer");
            return;
        }
    
        if (!paymentDate) {
            setError("You must select a payment date");
            return;
        }

        if (!paymentCategorySelected || paymentCategorySelected === "default") {
            setError("You must choose a category");
            return;
        }

        if (totalPercentage !== 100) {
            setError("The sum of percentages must be 100%");
            return;
        }

        if (paymentDescription.length > MAX_NAME_LENGTH) {
            setError(`Payment description must be less than ${MAX_NAME_LENGTH} characters`);
            return;
        }

        const updatedPercentages = Object.keys(percentagesData).reduce((acc, email) => {
            if (email != 'undefined') {
                acc[email] = percentagesData[email] / 100;
                return acc;
            }
        }, {});
        
        const formattedDate = paymentDate ? format(paymentDate.toDate(), 'yyyy-MM-dd') : '';

        console.log(formattedDate)

        const requestBody = {
            payment: {
                group_id: groupID,
                description: paymentDescription,
                payer_email: userSelected,
                payment_date: formattedDate,
                category: paymentCategories.indexOf(paymentCategorySelected.toLocaleUpperCase()),
                amount: paymentAmount
            },
            percentages: updatedPercentages
        };
        
        try {
            setIsLoading(true);

            const response = await fetch(`${BACK_URL}/payments`, {
                method: 'POST',
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                body: JSON.stringify(requestBody),
                cache: "no-store",
            });

            if (!response.ok) {
                setError('Error creating the payment');
            }

            setpaymentDescription('');
            setError(null);
            toggleForm();
            alert('Success creating the payment!');
            window.location.reload()
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handlePercentagesData = (data) => {
        setPercentagesData(data);
    };

    const handleDateChange = (newValue) => {
        setPaymentDate(newValue); 
    };

    const cancelForm = () => {
        setpaymentDescription('');
        setPaymentCategorySelected('');
        setPaymentDate(null);
        setUserSelected('');
        setPaymentAmount('');
        setError(null);
        setIsOpen(false);
    };

    return (
        <div className="create-payment-super-container">
            <button onClick={toggleForm} className="create-payment-button">
                + Create payment
            </button>

            {isOpen && (
                <div className="Modal-overlay">
                    <div className="Modal-content">
                        <div className="create-payment-container">
                            <h2 className="form-h2">Create payment</h2>
                            <form className="create-payment-form" onSubmit={handleSubmit}>
                                <div className="form-inputs">
                                    <label>Description</label>
                                    <input
                                        type="text"
                                        value={paymentDescription}
                                        onChange={(e) => setpaymentDescription(e.target.value)}
                                        required
                                        className="payment-description-input"
                                    />

                                    <label>Category</label>
                                    <select
                                        value={paymentCategorySelected}
                                        onChange={(e) => setPaymentCategorySelected(e.target.value)}
                                    >
                                        <option value=""></option>
                                        {paymentCategories.map((category, index) => (
                                            <option key={index} value={category.toLowerCase().replace(" ", "")}>
                                                {category.charAt(0).toUpperCase() + category.slice(1).toLowerCase()}
                                            </option>
                                        ))}
                                    </select>

                                    <label>Payer</label>
                                    <select
                                        value={userSelected}
                                        onChange={(e) => setUserSelected(e.target.value)}
                                    >
                                        <option value=""></option>
                                        {users.map((user, index) => (
                                            <option key={index} value={user.user_email}>
                                                {user.user_name}
                                            </option>
                                        ))}
                                    </select>

                                    <label>Date</label>
                                    <BasickDatePicker
                                        value={paymentDate ? dayjs(paymentDate) : null}
                                        onChange={handleDateChange}
                                        required
                                        className="payment-date-input"
                                        lang="en"
                                    />

                                    <label>Amount</label>
                                    <input
                                        type="number"
                                        value={paymentAmount}
                                        onChange={(e) => setPaymentAmount(e.target.value)}
                                        required
                                        className="payment-amount-input"
                                    />

                                    <label>Assign percentages</label>
                                    
                                    <div className="split-section">
                                        <label>
                                            Split equally
                                        </label>

                                        <input
                                            type="checkbox"
                                            checked={isChecked}
                                            onChange={handleCheckboxChange}
                                        />
                                    </div>

                                    <PercentageSlider 
                                        users={users} 
                                        sendDataToParent={handlePercentagesData} 
                                        isDisabled={isChecked}
                                    />

                                    {error && <p style={{ color: 'red' }}>{error}</p>}
                                </div>

                                <button className={isLoading ? 'btn-form-disabled' : 'btn-form'} type="submit" disabled={isLoading}>
                                    {isLoading ? (
                                        <LoadingSpinner style={{ display: 'inline-block', margin: '0', width: '25px', height: '25px' }} />
                                    ) : (
                                        "Create"
                                    )}
                                </button>
                                <button className={isLoading ? 'btn-form-cancel-disabled' : 'btn-form-cancel'} onClick={cancelForm} disabled={isLoading}>
                                    Cancel
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default CreatePaymentButton;
