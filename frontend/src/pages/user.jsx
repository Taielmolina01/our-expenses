import BodyUser from '../components/bodyUser/BodyUser';
import NavbarHome from '../components/navbarHome';
import Footer from '../components/footer';
import { useUser } from '../userContext.jsx';

function User() {

    const { user } = useUser();

    return ( 
        <div className="app-container">
            <NavbarHome />
            <BodyUser className="body-container" currentUser={user}/>
            <Footer />
        </div>
    )
}

export default User;