import './card.css'

function Card({ title, icon, body }) {
    return (
        <div className="card">
            <div className="title-container">
                <i className={icon} aria-hidden="true"></i>
                <h4>
                    {title}
                </h4>
            </div>

            <p className="card-body">
                {body}
            </p>
        </div>
    )
}

export default Card;