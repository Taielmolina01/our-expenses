import { useState } from 'react';

function PasswordInput({ label, name, password, SetPassword}) {

    const [showPassword, setShowPassword] = useState(false);

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    return (
        <>
            <label>{label}</label>
            <div style={{ position: 'relative', width: 'fit-content' }}>
                <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    name={name}
                    style={{ paddingRight: '30px' }}
                />
                <button
                    type="button"
                    onClick={togglePasswordVisibility}
                    style={{
                        position: 'absolute',
                        right: '5px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        border: 'none',
                        background: 'none',
                        cursor: 'pointer',
                    }}
                >
                    {showPassword ? 
                        <i className="fa-solid fa-eye-slash" style={{ color: 'black'}}/>
                        :
                        <i className="fa-solid fa-eye" style={{ color: 'black'}}/>
                    }
                </button>
            </div>
        </>

    )
}

export default PasswordInput;