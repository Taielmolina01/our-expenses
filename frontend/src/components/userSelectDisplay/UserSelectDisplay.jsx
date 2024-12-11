import React, { useState, useEffect } from 'react';
import './userSelectDisplay.css';
import Table from '../table/Table';
import SearchBar from '../searchBar/SearchBar';
import LoadingSpinner from '../loadingSpinner/LoadingSpinner';
import SelectFilter from '../selectFilter/SelectFilter';
import UserProfile from '../userProfile/UserProfile';
import GraphicSelects from '../graphicSelects/GraphicSelects';
import { BACK_URL, GetToken, MAX_NAME_LENGTH, TrimField, TypeChart, ViewType } from '../../utils';

function UserSelectDisplay({ user }) {
    const [selectedOption, setSelectedOption] = useState('Profile');
    const [search, setSearch] = useState('');
    const [gropuSearch, setGropuSearch] = useState('');
    const [filteredPayments, setFilteredPayments] = useState([]);
    const [filteredDebts, setFilteredDebts] = useState([]);
    const [payments, setPayments] = useState([]);
    const [debts, setDebts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [paymentCategories, setPaymentCategories] = useState([]);
    const [error, setError] = useState(null);
    const [reload, setReload] = useState(false);
    const [showPasswordForm, setShowPasswordForm] = useState(false);
    const [showUsernameForm, setShowUsernameForm] = useState(false);

    const token = GetToken();

    // Fetch inicial de datos
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);

                // Fetch categorías de pagos
                const categoriesRes = await fetch(`${BACK_URL}/payments/options`, {
                    method: "GET",
                    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
                });
                if (!categoriesRes.ok) throw new Error('Error loading payment categories');
                setPaymentCategories(await categoriesRes.json());

                // Fetch pagos
                const paymentsRes = await fetch(`${BACK_URL}/users/${user.email}/payments/data`, {
                    method: "GET",
                    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
                });
                if (!paymentsRes.ok) throw new Error('Error loading payments');
                setPayments(await paymentsRes.json());

                // Fetch deudas
                const debtsRes = await fetch(`${BACK_URL}/debts/users/${user.email}/data`, {
                    method: "GET",
                    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
                });
                if (!debtsRes.ok) throw new Error('Error loading debts');
                setDebts(await debtsRes.json());
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [reload, token]); // Vuelve a cargar los datos cuando cambia `reload`

    // Filtros para pagos
    useEffect(() => {
        setFilteredPayments(
            payments.filter(payment =>
                payment.description.toLowerCase().includes(search.toLowerCase()) &&
                payment.group_name.toLowerCase().includes(gropuSearch.toLowerCase())
            )
        );
    }, [search, gropuSearch, payments]);

    // Filtros para deudas
    useEffect(() => {
        setFilteredDebts(debts.filter(debt =>
            debt.debt_state.toLowerCase().includes(search.toLowerCase())
        ));
    }, [search, debts]);

    const handleFilterPayments = (field) => {
        if (field === 'Default') {
            setFilteredPayments(payments);
        } else {
            setFilteredPayments(payments.filter(payment => 
                payment.category.toLowerCase().includes(field.toLowerCase())
            ));
        }
    };

    const handleFilterDebts = (field) => {
        if (field === 'Default') {
            setFilteredDebts(debts);
        } else {
            setFilteredDebts(debts.filter(debt => 
                debt.debt_state.toLowerCase() === field.toLowerCase()
            ));
        }
    };

    const settleDebt = async (row) => {
        let debt_state = row.debt_state === 'UNPAID' ? 1 : 0;
        try {
            setLoading(true);
            const res = await fetch(`${BACK_URL}/debts/${row.debt_id}`, {
                method: "PUT",
                headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
                body: JSON.stringify({ state: debt_state }),
            });

            if (!res.ok) throw new Error('Error settling the debt');

            await res.json();

            setReload(!reload); // Fuerza recarga tras liquidar deuda
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleShowPasswordForm = (e) => {
        setShowPasswordForm(e);
    }

    const handleShowUsernameForm = (e) => {
        setShowUsernameForm(e);
    }

    if (loading) {
        return <LoadingSpinner />;
    }

    const profileRows = [
        { name: 'Name', value: user.name, edit: true, handleEdit: handleShowUsernameForm},
        { name: 'Email', value: user.email, edit: false },
        { name: 'Password', value: "********", edit: true, handleEdit: handleShowPasswordForm },
    ];
    const paymentsColumns = [
        { name: 'Group name' }, 
        { name: 'Description' }, 
        { name: 'Payer' }, 
        { name: 'Date' }, 
        { name: 'Category' }, 
        { name: 'Amount' }
    ];
    const debtsColumns = [
        { name: 'Group name' }, 
        { name: 'Payment description' }, 
        { name: 'Debtor' }, 
        { name: 'Creditor' }, 
        { name: 'Amount owed' }, 
        { name: 'Status' }, 
        { name: 'Settle' }
    ];

    return (
        <div className="display-table">
            <div className="display-table-options">
                <button className={`display-table-option ${selectedOption === 'Profile' ? 'active' : ''}`} onClick={() => setSelectedOption('Profile')}>
                    Profile
                </button>
                <button className={`display-table-option ${selectedOption === 'Payments' ? 'active' : ''}`} onClick={() => setSelectedOption('Payments')}>
                    Payments
                </button>
                <button className={`display-table-option ${selectedOption === 'Debts' ? 'active' : ''}`} onClick={() => setSelectedOption('Debts')}>
                    Debts
                </button>
                <button className={`display-table-option ${selectedOption === 'Graphics' ? 'active' : ''}`} onClick={() => setSelectedOption('Graphics')}>
                    Graphics
                </button>
            </div>

            <div className="display-table-content">
                {selectedOption === 'Profile' && (
                    <div className="profile-table-super-container">
                        <UserProfile rows={profileRows}/>
                        {showPasswordForm && <EditPasswordForm onClose={handleShowPasswordForm} user={user} />}
                        {showUsernameForm && <EditUsernameForm onClose={handleShowUsernameForm} user={user} />}
                    </div>
                )}
                {selectedOption === 'Payments' && (
                    <div>
                        <div className="payments-container">
                            <SearchBar placeholder="Search payment..." value={search} onSearch={setSearch} />
                            <SearchBar placeholder="Search group..." value={gropuSearch} onSearch={setGropuSearch} />
                            <SelectFilter fields={paymentCategories} onFilterChange={handleFilterPayments} defaultOption="category" />
                        </div>
                        <div className="payments-user-table-super-container">
                            <Table data={filteredPayments} columns={paymentsColumns} type={TypeChart.PAYMENTS_IN_USER} />
                        </div>
                    </div>
                )}
                {selectedOption === 'Debts' && (
                    <div>
                        <div className="debts-container">
                            <SelectFilter fields={['Unpaid', 'Paid']} onFilterChange={handleFilterDebts} defaultOption="status" />
                        </div>
                        <div className="debts-user-table-super-container">
                            <Table data={filteredDebts} columns={debtsColumns} onRowClick={settleDebt} type={TypeChart.DEBTS_IN_USER}/>
                        </div>
                    </div>
                )}
                {selectedOption === 'Graphics' && (
                    <GraphicSelects view={ViewType.USER_CHARTS} payments={payments} debts={debts}/>
                )}
            </div>
        </div>
    );
}

function EditPasswordForm({ onClose, user }) {
    const [currPassword, setCurrPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [newConfirmPassword, setNewConfirmPassword] = useState('');
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();

        setNewPassword(TrimField(newPassword))

        if (newPassword === '') {
            setError('Password cannot be empty');
            return;
        }

        if (newPassword !== newConfirmPassword) {
            setError("New password and confirmation do not match.");
            setIsLoading(false);
            return;
        }

        setError(null);
        setIsLoading(true);

        try {
            const response = await fetch(`${BACK_URL}/users/${user.email}/updatepass`, {
                method: 'PUT',
                headers: {
                    "Authorization": `Bearer ${GetToken()}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    currentPassword: currPassword,
                    newPassword: newPassword,
                    user: user
                }),
            });

            const result = await response.json();

            if (!response.ok) {
                setError(result.detail || "Wrong password");
            } else {
                setError(null);
                alert("Password changed successfully.");
                onClose(false);
                window.location.reload(); 
            }
        } catch (error) {
            setError("An error occurred. Please try again.");
        } finally {
            setIsLoading(false); 
        }
    };

    return (
        <div className="Modal-overlay">
            <div className="Modal-content">
                <div className="create-payment-container">
                    <h2 className="form-h2">Change password</h2>
                    <form className="create-payment-form" onSubmit={handlePasswordSubmit}>
                        <div className="form-inputs">
                            <label>Current password</label>
                            <input
                                type="password"
                                className="payment-description-input"
                                onChange={(e) => setCurrPassword(e.target.value)}
                                value={currPassword}
                                required
                            />
                            <label>New password</label>
                            <input
                                type="password"
                                className="payment-description-input"
                                onChange={(e) => setNewPassword(e.target.value)}
                                value={newPassword}
                                required
                            />
                            <label>Confirm new password</label>
                            <input
                                type="password"
                                className="payment-description-input"
                                onChange={(e) => setNewConfirmPassword(e.target.value)}
                                value={newConfirmPassword}
                                required
                            />
                            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
                        </div>
                        <div className="overlay-pass-buttons">
                            <button
                                type="submit"
                                className={isLoading ? "btn-disabled" : "submit-button"}
                                disabled={isLoading}
                            >
                                {isLoading ? (
                                    <LoadingSpinner style={{  display: 'inline-block', margin: '0', width: '25px', height: '25px' }} />
                                ) : (
                                    "Submit"
                                )}
                            </button>
                            <button
                                type="button"
                                className="cancel-button"
                                onClick={() => onClose(false)}
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}

function EditUsernameForm({ onClose, user }) {
    const [newUsername, setNewUsername] = useState('');
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleUsernameSubmit = async (e) => {
        e.preventDefault();

        if (newUsername.length > MAX_NAME_LENGTH) {
            setError(`Username must be less than ${MAX_NAME_LENGTH} characters`);
            return;
        }

        setError(null);
        setIsLoading(true);

        try {
            const response = await fetch(`${BACK_URL}/users/${user.email}`, {
                method: "PUT",
                cache: "no-store",
                headers: {
                    "Authorization": `Bearer ${GetToken()}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: newUsername,
                    balance: null
                }),
            });
            const result = await response.json();

            if (!response.ok) {
                setError(result.detail || "Error editing user");
            } else {
                setError(null);
                localStorage.setItem('user', JSON.stringify(result));
                alert("Name changed successfully.");
                onClose(false);
                window.location.reload(); 
            }
        } catch (error) {
            setError("An error occurred. Please try again.");
        } finally {
            setIsLoading(false); 
        }
    };
    

    return (
        <div className="Modal-overlay">
            <div className="Modal-content">
                <div className="create-payment-container">
                    <h2 className="form-h2">Change username</h2>
                    <form className="create-payment-form" onSubmit={handleUsernameSubmit}>
                        <div className="form-inputs">
                            <label>Current name: {user.name}</label>
                            
                            <label>New name</label>
                            <input
                                className="payment-description-input"
                                onChange={(e) => setNewUsername(e.target.value)}
                                value={newUsername}
                                required
                            />
                            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
                        </div>
                        <div className="overlay-pass-buttons">
                            <button
                                type="submit"
                                className={isLoading ? "btn-disabled" : "submit-button"}
                                disabled={isLoading}
                            >
                                {isLoading ? (
                                    <LoadingSpinner style={{  display: 'inline-block', margin: '0', width: '25px', height: '25px' }} />
                                ) : (
                                    "Save"
                                )}
                            </button>
                            <button
                                type="button"
                                className="cancel-button"
                                onClick={() => onClose(false)}
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default UserSelectDisplay;