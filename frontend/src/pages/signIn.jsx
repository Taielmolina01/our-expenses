import Footer from "../components/footer";
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import NavbarSign from "../components/navbarSign";
import { HandleSignIn} from "../utils"
import { useUser } from '../userContext';
import LoadingSpinner from '../components/loadingSpinner/LoadingSpinner'
import PasswordInput from "../components/PasswordInput";

function SignIn() {

    const { setUser } = useUser();
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [password, setPassword] = useState('');
    const navigate = useNavigate()


    const labelPassword = "Password";
    const namePassword = "password";

    const handleSubmit = async (e) => {
        e.preventDefault();

        setError(null);

        const formData = new FormData(e.currentTarget);
        const email = formData.get('email');
        const password = formData.get('password');

        await HandleSignIn(email, password, setIsLoading, setError, setUser, navigate);
    }

    return (
        <div className="app-container">
            <NavbarSign />
            <div className="form-container">
                <form onSubmit={handleSubmit}>
                    <h2>Sign in</h2>
                    <label>Email</label>
                    <input 
                        type="email"
                        name="email"
                        required
                    />
                    <PasswordInput 
                        label={labelPassword}
                        name={namePassword}
                        password={password}
                        setPassword={setPassword}
                    />
                    {error && <p style={{ color: 'red', maxWidth: '255px', textAlign: 'center' }}>{error}</p>}
                    <button  className={isLoading ? 'btn-disabled' : 'btn'}  type="submit" disabled={isLoading}>
                        {isLoading ? <LoadingSpinner style={{ display: 'inline-block', 
                                                                margin: '0',
                                                                width: '25px',
                                                                height: '25px' }}/> 
                                                                : "Sign in"}
                    </button>
                    <p>
                        Still not a user?{" "}
                        <Link to="/sign-up" style={{ color: 'green', textDecoration: 'underline' }}>
                            Sign up
                        </Link>
                    </p>
                </form>
            </div>
            <Footer />
        </div>
    )
}

export default SignIn;