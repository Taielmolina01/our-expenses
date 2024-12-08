import NavBarTo from './navBarTo';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser } from '@fortawesome/free-solid-svg-icons';
import { GetUser } from '../utils';
import ProfileMenu from './profileMenu/profileMenu';
import PendingInvitesButton from './pendingInvitesButton/PendingInvitesButton';

function NavbarHome() {

    const user = GetUser();

    return (
        <nav className="navbar-home">
            <NavBarTo link={"/home"} />
            <div className="on-right">
                <PendingInvitesButton />
                <FontAwesomeIcon icon={faUser}/>
                {user.name}
                <ProfileMenu />
            </div>
        </nav>
    )
}   

export default NavbarHome;