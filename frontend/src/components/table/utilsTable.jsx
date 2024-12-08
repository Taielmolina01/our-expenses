export function MapStrings(str) {
    switch (str) {
        case 'Username': return 'user_name';
        case 'Name': return 'name';
        case 'Group': return 'group_name';
        case 'Group name': return 'group_name';
        case 'Email': return 'user_email';
        case 'Payer': return 'payer_name';
        case 'Payment name': return 'payment_name';
        case 'Status': return 'debt_state';
        case 'Amount': return 'amount';
        case 'Amount owed': return 'calculated_amount';
        case 'Debtor': return 'debtor_name';
        case 'Creditor': return 'creditor_name';
        case 'Date': return 'payment_date';
        case 'Payment description': return 'payment_description';
        default: return str.toLowerCase();
    }
}

export const FormatDate = (dateString) => {
    const date = new Date(`${dateString}T00:00:00Z`); 
    const year = date.getUTCFullYear();
    const month = date.toLocaleString('en', { month: 'short', timeZone: 'UTC' }).toUpperCase();
    const day = String(date.getUTCDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
};

export const GetCategoryColor = (category) => {
    switch (category.toLowerCase()) {
        case 'food':
            return '#a254e8'; 
        case 'utilities':
            return '#4c42e8'; 
        case 'clothing':
            return '#ff5d40'; 
        case 'healthcare':
            return '#ffcf2a';
        case 'personal':
            return '#ff8e2a';
        case 'education':
            return '#40ffe5';
        case 'gifts':
            return '#ff40f1';
        case 'entertainment':
            return '#3a3dff';
        case 'others':
            return '#25ff75';
        default:
            return '#ffffff'; 
    }
};

export const DecimalFormat = (numero) => {
    const numeroConDecimales = Number(numero).toFixed(2);

    let [parteEntera, parteDecimal] = numeroConDecimales.split(".");

    const expresionMiles = /(\d)(?=(\d{3})+(?!\d))/g;
    parteEntera = parteEntera.replace(expresionMiles, "$1.");

    return `${parteEntera},${parteDecimal}`;
};
