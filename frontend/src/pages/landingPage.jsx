import BodyLandingPage from "../components/bodyLandingPage/BodyLandingPage";
import FooterLandingPage from "../components/footerLanding/FooterLandingPage";
import NavbarLandingPage from "../components/navbarLandingPage";

function LandingPage() {
    return ( 
        <div className="app-container">
            <NavbarLandingPage />
            <BodyLandingPage className="body-container" />
            <FooterLandingPage />
        </div>
    )
}

export default LandingPage;