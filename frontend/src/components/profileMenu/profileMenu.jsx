import { useState } from "react";
import { GetUser, LogOut } from "../../utils"
import { useNavigate } from 'react-router-dom';
import LoadingSpinner from '../loadingSpinner/LoadingSpinner';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEllipsis } from "@fortawesome/free-solid-svg-icons";
import './profileMenu.css'

function ProfileMenu() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const user = GetUser();

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    const logout = async () => {
        setIsLoading(true);
        await LogOut(setIsLoading, setError, navigate);
    };

    const showSettings = () => {
        setIsMenuOpen(false);
        navigate(`/users/${user.email}`)
    };

    const changeTheme = () => {
        document.documentElement.classList.toggle('light-mode');
        localStorage.setItem('theme', document.documentElement.classList.contains('light-mode') ? 'light' : 'dark');
        window.location.reload();
        setIsMenuOpen(false);
    }

    if (isLoading) {
        <LoadingSpinner />
    }

    return (
        <div>
            <div style={{ position: 'relative', display: 'inline-block' }}>
                <button onClick={toggleMenu} className="menu-button">
                    <FontAwesomeIcon icon={faEllipsis} />
                </button>

                {isMenuOpen && (
                    <div className="menu-dropdown">
                        <button onClick={showSettings} className="menu-item">My profile</button>
                        <button onClick={changeTheme} className="menu-item">Change theme</button>
                        <button onClick={logout} className="menu-item">Logout</button>
                    </div>
                )}
            </div>
        </div>
    );
}


export default ProfileMenu;