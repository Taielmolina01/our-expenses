import Footer from "../components/footer";
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import NavbarSign from "../components/navbarSign";
import { BACK_URL, HandleSignIn } from "../utils"
import { useUser } from '../userContext.jsx';
import LoadingSpinner from "../components/loadingSpinner/LoadingSpinner.jsx";
import PasswordInput from "../components/PasswordInput.jsx";

function SignUp() {

    const { setUser } = useUser();
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate()

    const [passwordEntry, setPasswordEntry] = useState('');
    const [confirmPasswordEntry, setConfirmPasswordEntry] = useState('');
    const labelPassword = "Create a password";
    const labelConfirmPassword = "Confirm your password";
    const namePassword = "password";
    const nameConfirmPassword = "confirmPassword";

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData(e.currentTarget);

        const password = formData.get(namePassword);

        if (password !== formData.get(nameConfirmPassword)) {
            setError('Passwords do not match');
            return;
        }
        
        const json = {};

        json["email"] = formData.get('email');
        json["name"] = formData.get('name');
        json["password"] = password;

        const email = json["email"];
    
        let res;

        try {
            setIsLoading(true)
            res = await fetch(`${BACK_URL}/users`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(json),
                cache: "no-store",
            });
      
            const data = await res.json();

            if (!res.ok) {
                setError(`${JSON.stringify(data.detail)}`)
            } else {
                await HandleSignIn(email, password, setIsLoading, setError, setUser, navigate);
                navigate("/home"); 
            }
        } catch (e) {
            setError("Connection error: " + e);
            return;
        } finally {
            setIsLoading(false)
        }
    }   

    return (
        <div className="app-container">
            <NavbarSign />
            <div className="form-container">
                <form onSubmit={handleSubmit}>
                    <h2>Sign up</h2>
                    <label>Enter your name</label>
                    <input 
                        type="string"
                        name="name"
                        required
                    />
                    <label>Enter your email</label>
                    <input 
                        type="email"
                        name="email"
                        required
                    />
                    <PasswordInput
                        name={namePassword}
                        label={labelPassword}
                        password={passwordEntry}
                        setPassword={setPasswordEntry}
                    />
                    <PasswordInput 
                        name={nameConfirmPassword}
                        label={labelConfirmPassword}
                        password={confirmPasswordEntry}
                        setPassword={setConfirmPasswordEntry}
                    />
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                    <button  className={isLoading ? 'btn-disabled' : 'btn'}  type="submit" disabled={isLoading}>
                        {isLoading ? <LoadingSpinner style={{ display: 'inline-block', 
                                                                    margin: '0',
                                                                    width: '25px',
                                                                    height: '25px' }}/> 
                                                                    : "Sign up"}                    
                    </button>
                    <p>
                        Already a user?{" "}
                        <Link to="/sign-in" style={{ color: 'green', textDecoration: 'underline' }}>
                            Sign in
                        </Link>
                    </p>
                </form>
            </div>
            <Footer></Footer>
        </div>
    )
}

export default SignUp;