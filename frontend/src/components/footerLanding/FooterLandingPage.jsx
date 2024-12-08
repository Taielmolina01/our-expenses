import MemberItem from "../memberItem";

function FooterLandingPage() {
    const members = {
        "Batemarco, Joaquín": "https://github.com/BA73C0",
        "Molina, Taiel": "https://github.com/Taielmolina01",
        "Puglisi, Agustín": "https://github.com/agusspuglisi",
        "Schulc, Mariana": "https://github.com/marian1908",
        "Taibo, Nazareno": "https://github.com/PMNaza"
    }
    
    const linkRepoFront = "https://github.com/Taielmolina01/frontend-our-expenses";
    const linkDocumentation = "https://drive.google.com/drive/folders/1uFdO6GChyodO61MmLpd-53IefFHcBNiT?usp=sharing";

    return (
        <footer className="footer-landing">
            <div className="about-us">
                <h2>
                    OurExpenses
                </h2>
                <div>
                    <p>
                        We are the group number 2 of the course Turri in the subject Management and Development of Software Projects at FIUBA.
                    </p>
                    <h3>
                        Members
                    </h3>
                    <ul>
                        {Object.keys(members).map((memberName) => (
                            <MemberItem 
                            key={memberName}
                            name={memberName} 
                            link={members[memberName]} />
                        ))}
                    </ul>
                </div>
            </div>
            <div className="help">
                <h2>
                    Help
                </h2>
                <div>
                    <a 
                        href={linkRepoFront}
                        className="footer-link"
                        target="_blank"
                    >
                        Code
                    </a>
                    <a
                        href={linkDocumentation}
                        className="footer-link"
                        target="_blank"
                    >
                        Documentation
                    </a>
                </div>
            </div>
            <div className="company">

            </div>
        </footer>    
    ) 
}

export default FooterLandingPage;