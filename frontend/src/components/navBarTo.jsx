import { Link } from 'react-router-dom';

function NavBarTo( { link } ) {
    return (
        <div className="enterprise-name">
                <Link to={link}>
                    <span>
                        OurExpenses
                    </span>
                </Link>
        </div>
    )
}

export default NavBarTo;