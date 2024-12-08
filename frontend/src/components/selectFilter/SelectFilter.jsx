import React, { useState } from 'react';
import './selectFilter.css';

function SelectFilter({ fields, onFilterChange, defaultOption }) {
    const [selectedField, setSelectedField] = useState("Default");

    const handleFieldChange = (e) => {
        const field = e.target.value;
        setSelectedField(field);
        onFilterChange(field);
    };

    function Capitalize(s) {
        if (!s) return ''; // Manejo de valores no válidos
        return s[0].toUpperCase() + s.slice(1);
      };

    return (
        <div className="select-filter-container">
            <select
                value={selectedField}
                onChange={handleFieldChange}
                className={`select-filter ${selectedField !== "Default" ? "default-unselected" : ""}`}
            >
                <option value="Default">Filter {defaultOption}...</option>
                {fields.map((category, index) => (
                    <option key={index} value={category.toLowerCase().replace(" ", "")}>
                        {category[0].toUpperCase() + category.slice(1).toLowerCase()}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default SelectFilter;
