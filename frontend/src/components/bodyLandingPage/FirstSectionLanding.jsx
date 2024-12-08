import './firstSectionLanding.css'
import { Link } from 'react-router-dom';
import logo from '../../assets/logo.png'

function FirstSectionLanding() {

    return (
        <section className='not-signed-background container-first-section'>
            <div className="subcontainer-first-section">
                <p className="animated-title">
                    See your expenses easier than ever!
                </p>
                <p className="text-body">
                    Welcome to the ultimate solution for managing shared expenses! Our app is perfect for couples, friends, and travelers who want to split costs effortlessly. Track balances, organize payments, and settle debts with ease.
                    
                    <br />
                    
                    Designed to save time and avoid conflicts, it’s the smarter way to manage group finances. Join now and simplify your financial collaborations!
                </p>
                <Link to="/sign-up" className="link-landing">
                    <button className="sign-in button-landing">
                        Start now!
                    </button>
                </Link>
            </div>
            <img src={logo}/>
        </section>
    )
}

export default FirstSectionLanding