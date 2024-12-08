import BodyGroup from '../components/bodyGroup/BodyGroup';
import NavbarHome from '../components/navbarHome'
import Footer from '../components/footer'
import { useParams } from 'react-router-dom';


function Group() {
    const { groupID, groupName } = useParams();

    return ( 
        <div className="app-container">
            <NavbarHome />
            <BodyGroup className="body-container" groupID={groupID} groupName={groupName}/>
            <Footer />
        </div>
    )
}

export default Group;