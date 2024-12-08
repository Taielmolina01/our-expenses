import { useState } from "react";
import './graphicSelects.css'
import MyChart from "../myChart/MyChart";
import { ViewType} from '../../utils'

function GraphicSelects( { view , payments, debts } ) {

    const graphicFields = ["Payments", "Unpaid debts"]
    const [selectedEntity, setSelectedEntity] = useState("Default");
    const [selectedGraphic, setSelectedGraphic] = useState("");

    const handleChangeSelectEntity = (event) => {
        setSelectedEntity(event.target.value);
        setSelectedGraphic(""); 
    };

    const handleChangeSelectGraphic = (event) => {
        setSelectedGraphic(event.target.value)
    };

    const groupChartsByEntity = {
        "Payments": {
            "Amount by payer": "Pie", 
            "Amount by category": "Bar", 
            "Amount by year": "Bar", 
        },
        "Unpaid debts": {
            "Debtor vs Creditor": "Heatmap"
        }
    }

    const userChartsByEntity = {
        "Payments": {
            "Categories by groups": "Heatmap",
            "Amount by groups": "Bar",
        },
        "Unpaid debts": {
            "Amount owed by groups": "Bar",
        }
    }

    const chartsByEntity = view === ViewType.USER_CHARTS ? userChartsByEntity : groupChartsByEntity;

    return (
        <>
            <div className="selects-container">
                <select 
                    onChange={handleChangeSelectEntity}
                    className={`select-filter ${selectedEntity !== "Default" ? "default-unselected" : ""}`}
                >
                    <option value="">
                        Select an option
                    </option>
                    {graphicFields.map((field) => (
                        <option key={field} value={field}>
                            {field}
                        </option>
                    ))}
                </select>
                <select
                    onChange={handleChangeSelectGraphic}
                    className={`select-filter ${selectedEntity !== "Default" ? "default-unselected" : ""}`}
                    disabled={selectedEntity === "Default" || !selectedEntity} 
                >
                    <option value="">
                        {(selectedEntity === "Default" || !selectedEntity) ? "First select an option" : "Now select a type of graphic"}
                    </option>
                    {selectedEntity && chartsByEntity[selectedEntity] &&
                    Object.keys(chartsByEntity[selectedEntity]).map((chartKey) => (
                        <option key={chartKey} value={chartKey}>
                            {chartKey}
                        </option>
                    ))}
                </select>
            </div>
                {selectedEntity && selectedGraphic && (
                    <div className="graphic-container">
                        <MyChart 
                            view={view}
                            charts={chartsByEntity}
                            entity={selectedEntity}
                            graphic={selectedGraphic} 
                            data={selectedEntity === "Payments" ? payments : debts} 
                        />
                    </div>
                )}
        </>
    )
}

export default GraphicSelects;