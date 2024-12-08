import React, { useState } from 'react';
import './userProfile.css';

function UserProfile({ rows }) {
    const columns = [
        { name: '' },
        { name: '' },
        { name: '' }
    ];

    const gridTemplateColumns = `repeat(${columns.length}, 1fr)`;

    return (
        <div className="table-container">
            <table className="table" style={{ gridTemplateColumns }}>
                <tbody className="table-body">
                    {rows
                        .map((row, index) => (
                            <tr key={index} className={`table-card`}>
                                <>
                                    <>
                                        <td className="table-card-column2" style={{fontWeight: 'bold'}}>
                                            <div className="table-card-subcontainer">
                                                {row.name}
                                            </div>
                                        </td>
                                        <td className="table-card-column2" style={{fontWeight: 'bold'}}>
                                            <div className="table-card-subcontainer">
                                                {row.value}
                                            </div>
                                        </td>
                                    </>
                                </>
                                {row.edit === true ? (
                                    <td className="table-card-column-settle">
                                        <button 
                                            className="settle-button"
                                            onClick={() => {row.handleEdit(true)}}
                                        >
                                            Edit
                                        </button>
                                    </td>
                                ) : (
                                    <td></td>
                                )}
                            </tr>
                        ))}
                </tbody>
            </table>
        </div>
    );
}

export default UserProfile;
