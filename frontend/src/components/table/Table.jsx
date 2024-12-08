import React from 'react';
import './table.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser } from '@fortawesome/free-solid-svg-icons';

import { TypeChart } from '../../utils';
import { GetUser } from '../../utils';
import { MapStrings, FormatDate, GetCategoryColor, DecimalFormat } from './utilsTable';


function messageNoPaymentsOrDebts(type) {
    let message = '';
    switch (type) {
        case TypeChart.DEBTS_IN_GROUP:
            message = "No debts registered in group";
            break;
        case TypeChart.DEBTS_IN_USER:
            message = "No debts registered with you as debtor or creditor"
            break;
        case TypeChart.PAYMENTS_IN_GROUP:
            message = "No payments registered in group";
            break;
        case TypeChart.PAYMENTS_IN_USER:
            message = "No payments registered with you as payer";
            break;
        default:
            message = "No data available";
    }
    return message;
}

function Table({ data, columns, onRowClick, redirect, type}) {
    const gridTemplateColumns = `repeat(${columns.length}, 1fr)`;

    return (
        <div className="table-container">
            {data.length === 0 ? (
                <p style={{margin: "auto", textAlign: 'center'}}>{messageNoPaymentsOrDebts(type)}</p>
            ) : (
            <table className="table" style={{ gridTemplateColumns }}>
                <thead className="table-head">
                    <tr className="column-names">
                        {columns.map((col, index) => (
                            <th key={index}>
                                {col.name !== "Settle" ? ( 
                                    col.name
                                ) : (
                                    ""
                                )}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody className="table-body">
                    {data.map((row, index) => (
                        <tr 
                            className={`table-card ${redirect ? 'pointer-cursor' : ''}`}
                            key={index} 
                            onClick={redirect ? () => onRowClick(row) : null}
                        >
                            {columns.map((col, i) => (
                                <td key={i} className={`${col.name === "Settle" ? 'table-card-column-settle' : 'table-card-column'}`}>
                                    {col.name === "Balance" ? (
                                        <div className="table-card-subcontainer">
                                            <div className={row.balance < 0 ? 'balance-positive' : 'balance-negative'}>
                                                {DecimalFormat(row[MapStrings(col.name)])}
                                            </div>
                                        </div>
                                    ) : col.name === "Username" ? (
                                        <div className="table-card-subcontainer">
                                            <div className="icon">
                                                <FontAwesomeIcon icon={faUser} />
                                                {row[MapStrings(col.name)]}
                                            </div>
                                        </div>
                                    ) : col.name === "Category" ? (
                                        <div className="table-card-subcontainer" style={{ color: GetCategoryColor(row[MapStrings(col.name)]), fontWeight: 'bolder' }}>
                                            {row[MapStrings(col.name)].charAt(0).toUpperCase() + row[MapStrings(col.name)].slice(1).toLowerCase()}
                                        </div>
                                    ) : col.name === "Status" ? (
                                        <div className="table-card-subcontainer">
                                            <div className={row.debt_state === "PAID" ? 'balance-negative' : 'balance-positive'}>
                                            {row[MapStrings(col.name)].charAt(0).toUpperCase() + row[MapStrings(col.name)].slice(1).toLowerCase()}
                                            </div>
                                        </div>
                                    ) : col.name === "Settle" ? (
                                        <button 
                                            className="settle-button"
                                            onClick={() => onRowClick(row)}
                                            >
                                            {row.debt_state === "UNPAID" ? "Settle debt" : "Unsettle debt"}
                                        </button>
                                    ) : col.name === "Date" ? (
                                        <div className="table-card-subcontainer">
                                            {FormatDate(row[MapStrings(col.name)])}
                                        </div>
                                    ) : col.name === "Amount" || col.name === "Amount owed" ? (
                                        <div className="table-card-subcontainer">
                                            {DecimalFormat(row[MapStrings(col.name)])}
                                        </div>
                                    ) : (col.name === "Payer" || col.name === "Debtor" || col.name === "Creditor") && row[MapStrings(col.name)] === GetUser().name ? (
                                        <div className="table-card-subcontainer">
                                        {row[MapStrings(col.name)]} (me)
                                    </div>
                                    ) : (
                                        <div className="table-card-subcontainer">
                                            {row[MapStrings(col.name)]}
                                        </div>
                                    )}
                            </td>
                            ))}
                        </tr>
                    ))}
                    {(type === TypeChart.PAYMENTS_IN_GROUP || type === TypeChart.PAYMENTS_IN_USER) && (
                        <tr className="table-card total-row">
                            {columns.map((col, i) => (
                                <td key={i} className="table-card-column">
                                    {col.name === "Amount" ? (
                                        <div className="table-card-subcontainer">
                                            <strong>
                                                {DecimalFormat(data.reduce((sum, row) => sum + (row[MapStrings(col.name)] || 0), 0))}
                                            </strong>
                                        </div>
                                    ) : (
                                        i === 0 && <div className="table-card-subcontainer"><strong>Total expended amount</strong></div>
                                    )}
                                </td>
                            ))}
                        </tr>
                    )}
                    {(type === TypeChart.DEBTS_IN_GROUP) && (
                        <tr className="table-card total-row">
                        {columns.map((col, i) => (
                            <td key={i} className="table-card-column">
                                {col.name === "Amount owed" ? (
                                    <div className="table-card-subcontainer">
                                        <strong>
                                            {DecimalFormat(
                                                data.reduce((sum, row) => {
                                                    return row.debt_state === "UNPAID"
                                                        ? sum + (row[MapStrings(col.name)] || 0)
                                                        : sum;
                                                }, 0)
                                            )}
                                        </strong>
                                    </div>
                                ) : (
                                    i === 0 && (
                                        <div className="table-card-subcontainer">
                                            <strong>Total unpaid debts's amount</strong>
                                        </div>
                                    )
                                )}
                            </td>
                        ))}
                        </tr>
                    )}
                    {(type === TypeChart.DEBTS_IN_USER) && (
                    <>
                        <tr className="table-card total-row">
                            {columns.map((col, i) => (
                                <td key={i} className="table-card-column">
                                    {col.name === "Amount owed" ? (
                                        <div className="table-card-subcontainer">
                                            <strong>
                                                {(() => {
                                                    const totalOwedToMe = data.reduce((sum, row) => {
                                                        if (row.debt_state === "UNPAID" && row[MapStrings("Creditor")] === GetUser().name) {
                                                            return sum + (row[MapStrings(col.name)] || 0);
                                                        }
                                                        return sum;
                                                    }, 0);
                                                    return <strong>{DecimalFormat(totalOwedToMe)}</strong>;
                                                })()}
                                            </strong>
                                        </div>
                                    ) : (
                                        i === 0 && (
                                            <div className="table-card-subcontainer">
                                                <strong>Total owed to me</strong>
                                            </div>
                                        )
                                    )}
                                </td>
                            ))}
                        </tr>
                        <tr className="table-card total-row">
                            {columns.map((col, i) => (
                                <td key={i} className="table-card-column" style={{ border: "none" }}>
                                {col.name === "Amount owed" ? (
                                        <div className="table-card-subcontainer">
                                            <strong>
                                                {(() => {
                                                    const totalIOwe = data.reduce((sum, row) => {
                                                        if (row.debt_state === "UNPAID" && row[MapStrings("Creditor")] !== GetUser().name) {
                                                            return sum + (row[MapStrings(col.name)] || 0);
                                                        }
                                                        return sum;
                                                    }, 0);
                                                    return <strong>{DecimalFormat(totalIOwe)}</strong>;
                                                })()}
                                            </strong>
                                        </div>
                                    ) : (
                                        i === 0 && (
                                            <div className="table-card-subcontainer">
                                                <strong>Total I owe</strong>
                                            </div>
                                        )
                                    )}
                                </td>
                            ))}
                        </tr>
                    </>
                    )}
                </tbody>
            </table>
            )}
        </div>
    );
}

export default Table;
