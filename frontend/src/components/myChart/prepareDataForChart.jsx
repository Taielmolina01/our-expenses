import { CHART_PALETTE } from "./chartOptions";
import { GetCategoryColor } from "../table/utilsTable";
import { GetUser } from "../../utils";

export function PrepareDataForPieChart(payments) {
    const amountsByPayer = payments.reduce((acc, payment) => {
        acc[payment.payer_name] = (acc[payment.payer_name] || 0) + payment.amount;
        return acc;
    }, {});
  
    return {
        labels: Object.keys(amountsByPayer),
        datasets: [
            {
                label: "Amount Paid",
                data: Object.values(amountsByPayer),
                backgroundColor: CHART_PALETTE,
                hoverOffset: 4,
            },
        ],
    };
  };

export function PreparePaymentsDataByGroup(payments) {
    const amountsByGroup = payments.reduce((acc, payment) => {
        acc[payment.group_name] = (acc[payment.group_name] || 0) + payment.amount;
        return acc;
    }, {});
  
    return {
        labels: Object.keys(amountsByGroup),
        datasets: [
            {
                label: "Amount Paid",
                data: Object.values(amountsByGroup),
                backgroundColor: CHART_PALETTE,
                hoverOffset: 4,
            },
        ],
    };
  };
  
export function PrepareDataforBarplotByCategory(payments) {
  const amountsByCategory = payments.reduce((acc, payment) => {
    acc[payment.category] = (acc[payment.category] || 0) + payment.amount;
    return acc;
  }, {});

  const categories = Object.keys(amountsByCategory);

  return {
    labels: categories,
    datasets: [
      {
        label: "Amount by Category",
        data: Object.values(amountsByCategory),
        backgroundColor: categories.map(GetCategoryColor),
        hoverOffset: 4,
      },
    ],
  };
}
  
export function PrepareDataforBarplotByYear(payments) {
    const amountsByYear = payments.reduce((acc, payment) => {
      const year = new Date(payment.payment_date).getFullYear();
      acc[year] = (acc[year] || 0) + payment.amount; 
      return acc;
    }, {});
  
    return {
      labels: Object.keys(amountsByYear),  
      datasets: [
        {
          label: "Amount Paid by Year",  
          data: Object.values(amountsByYear),  
          backgroundColor: CHART_PALETTE,
          hoverOffset: 4,
        },
      ],
    };
  };
  
export function PrepareDebtsDataForBarplotByGroup(debts) {
  const userDebts = debts.filter(
    (debt) => debt.debt_state === "UNPAID" && debt.debtor_name === GetUser().name
  );

  const amountsByGroup = userDebts.reduce((acc, debt) => {
    console.log(debt)
    acc[debt.group_name] = (acc[debt.group_name] || 0) + debt.calculated_amount;
    return acc;
  }, {});

  const groups = Object.keys(amountsByGroup);

  return {
    labels: groups,
    datasets: [
      {
        label: "Unpaid Debts by Group",
        data: Object.values(amountsByGroup),
        backgroundColor: CHART_PALETTE, 
        hoverOffset: 4,
      },
    ],
  };
}

export function PrepareDataforBarplotByCategoryByGroup(payments) {
  console.log(payments)

  const allCategories = Array.from(new Set(payments.map((p) => p.category)));
  const allGroupIds = Array.from(new Set(payments.map((p) => p.group_id)));
  const allGroupNames = Array.from(new Set(payments.map((p) => p.group_name)));

  const amountsMatrix = allGroupIds.map((group_id) =>
    allCategories.map((category) =>
      payments.filter((p) => p.group_id === group_id && p.category === category).length
    )
  );

  console.log(allGroupNames);  

  const series = allGroupIds.map((group_id, rowIndex) => ({
    name: allGroupNames[rowIndex], 
    data: amountsMatrix[rowIndex].map((amount, colIndex) => ({
      x: allCategories[colIndex],  
      y: amount,  
    })),
  }));

  return {
    categories: allCategories,  
    series, 
  };
}

  
export function PrepareDataforHeatMap(data) {
    const emailToNameMap = {};
    data.forEach(item => {
      emailToNameMap[item.debtor_email] = item.debtor_name;
      emailToNameMap[item.creditor_email] = item.creditor_name;
    });
    
    // Crear un conjunto único de deudores y acreedores
    const uniqueDebtors = [...new Set(data.map(item => item.debtor_email))];
    const uniqueCreditors = [...new Set(data.map(item => item.creditor_email))];
    
    // Crear la serie de datos para cada deudor
    const series = uniqueDebtors.map(debtor => ({
      name: emailToNameMap[debtor], 
      data: uniqueCreditors.map(creditor => {
        // Contar la cantidad de deudas activas (debt_state === "UNPAID")
        const activeDebts = data.filter(d => 
          d.debtor_email === debtor && 
          d.creditor_email === creditor && 
          d.debt_state === "UNPAID"
        );
        return activeDebts.length; // Contar la cantidad de deudas activas
      }),
    }));
    
    return {
      series, 
      categories: uniqueCreditors.map(creditor => emailToNameMap[creditor]),
      xAxisLabel: 'Creditors (by name)',
      yAxisLabel: 'Debtors (by name)', 
    };
}