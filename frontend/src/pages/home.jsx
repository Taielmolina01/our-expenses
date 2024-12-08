import NavbarHome from "../components/navbarHome";
import BodyHome from "../components/bodyHome"
import Footer from "../components/footer";
import { useUser } from '../userContext.jsx';


function Home() {

    const { user } = useUser();
    
    return (
        <div className ="app-container">
            <NavbarHome currentUser={user}/>
            <BodyHome className="body-container" currentUser={user}/>
            <Footer />
        </div>
    )
}

export default Home;