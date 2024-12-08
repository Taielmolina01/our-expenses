import React, { useState, useEffect } from 'react';
import './selectDisplay.css';
import Table from '../table/Table';
import SearchBar from '../searchBar/SearchBar';
import LoadingSpinner from '../loadingSpinner/LoadingSpinner';
import SelectFilter from '../selectFilter/SelectFilter';
import GraphicSelects from '../graphicSelects/GraphicSelects';
import { BACK_URL, GetToken, TypeChart, ViewType } from '../../utils';

function SelectDisplay({ groupID }) {
    const [selectedOption, setSelectedOption] = useState('Users');
    const [search, setSearch] = useState('');
    const [userSearch, setUserSearch] = useState('');
    const [filteredPayments, setFilteredPayments] = useState([]);
    const [filteredUsers, setFilteredUsers] = useState([]);
    const [filteredDebts, setFilteredDebts] = useState([]);
    const [users, setUsers] = useState([]);
    const [payments, setPayments] = useState([]);
    const [debts, setDebts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [paymentCategories, setPaymentCategories] = useState([]);
    const [error, setError] = useState(null);
    const [reload, setReload] = useState(false);

    const token = GetToken();

    // Fetch inicial de datos
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);

                // Fetch usuarios
                const usersRes = await fetch(`${BACK_URL}/groups/${groupID}/users/data`, {
                    method: "GET",
                    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
                });
                if (!usersRes.ok) throw new Error('Error loading users');
                setUsers(await usersRes.json());

                // Fetch categorías de pagos
                const categoriesRes = await fetch(`${BACK_URL}/payments/options`, {
                    method: "GET",
                    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
                });
                if (!categoriesRes.ok) throw new Error('Error loading payment categories');
                setPaymentCategories(await categoriesRes.json());

                // Fetch pagos
                const paymentsRes = await fetch(`${BACK_URL}/groups/${groupID}/payments/data`, {
                    method: "GET",
                    headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
                });
                if (!paymentsRes.ok) throw new Error('Error loading payments');
                setPayments(await paymentsRes.json());

                // Fetch deudas
                const debtsRes = await fetch(`${BACK_URL}/debts/groups/${groupID}/data`, {
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
    }, [groupID, reload, token]); // Vuelve a cargar los datos cuando cambia `reload`

    // Filtros para usuarios
    useEffect(() => {
        setFilteredUsers(users.filter(user => 
            user.user_name.toLowerCase().includes(userSearch.toLowerCase())
        ));
    }, [userSearch, users]);

    // Filtros para pagos
    useEffect(() => {
        setFilteredPayments(
            payments.filter(payment =>
                payment.description.toLowerCase().includes(search.toLowerCase()) &&
                payment.payer_name.toLowerCase().includes(userSearch.toLowerCase())
            )
        );
    }, [search, userSearch, payments]);

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

    if (loading) {
        return <LoadingSpinner />;
    }

    const usersColumns = [
        { name: 'Username' }, 
        { name: 'Balance' }
    ];
    const paymentsColumns = [
        { name: 'Description' }, 
        { name: 'Payer' }, 
        { name: 'Date' }, 
        { name: 'Category' }, 
        { name: 'Amount' }
    ];
    const debtsColumns = [
        { name: 'Payment description' }, // dejar el ' ' para que no se confunda con 'Description' de payments
        { name: 'Debtor' }, 
        { name: 'Creditor' }, 
        { name: 'Amount owed' }, 
        { name: 'Status' }, 
        { name: 'Settle' }
    ];

    return (
        <div className="display-table">
            <div className="display-table-options">
                <button className={`display-table-option ${selectedOption === 'Users' ? 'active' : ''}`} onClick={() => setSelectedOption('Users')}>
                    Users
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
                {selectedOption === 'Users' && (
                    <div>
                        <SearchBar placeholder="Search user..." value={userSearch} onSearch={setUserSearch} />
                        <div className="users-table-super-container"> {/* 45% */}
                            <Table data={filteredUsers} columns={usersColumns} />
                        </div>
                    </div>
                )}
                {selectedOption === 'Payments' && (
                    <div>
                        <div className="payments-container">
                            <SearchBar placeholder="Search payment..." value={search} onSearch={setSearch} />
                            <SearchBar placeholder="Search user..." value={userSearch} onSearch={setUserSearch} />
                            <SelectFilter fields={paymentCategories} onFilterChange={handleFilterPayments} defaultOption="category" />
                        </div>
                        <div className="payments-table-super-container"> {/* 60% */}
                            <Table data={filteredPayments} columns={paymentsColumns} type={TypeChart.PAYMENTS_IN_GROUP}/>
                        </div>
                    </div>
                )}
                {selectedOption === 'Debts' && (
                    <div>
                        <div className="debts-container">
                            <SelectFilter fields={['Unpaid', 'Paid']} onFilterChange={handleFilterDebts} defaultOption="status" />
                        </div>
                        <div className="debts-table-super-container"> {/* 70% */}
                            <Table data={filteredDebts} columns={debtsColumns} onRowClick={settleDebt} type={TypeChart.DEBTS_IN_GROUP}/>
                        </div>
                    </div>
                )}
                {selectedOption === 'Graphics' && (
                    <GraphicSelects view={ViewType.GROUP_CHARTS} payments={payments} debts={debts}/>
                )}
            </div>
        </div>
    );
}

export default SelectDisplay;