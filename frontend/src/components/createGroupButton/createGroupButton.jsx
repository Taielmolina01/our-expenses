import { useState } from 'react';
import Modal from '../modal/modal'; 
import { BACK_URL, GetToken, MAX_NAME_LENGTH, TrimField } from '../../utils';
import './groupButton.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faXmark } from '@fortawesome/free-solid-svg-icons';

function CreateGroupButton() {
    const [isOpen, setIsOpen] = useState(false);
    const [groupName, setGroupName] = useState('');
    const [error, setError] = useState(null);

    const token = GetToken();

    const toggleForm = () => {
        setIsOpen(!isOpen);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (groupName.length > MAX_NAME_LENGTH) {
            setError(`group name must be less than ${MAX_NAME_LENGTH} characters`);
            return;
        }

        try {
            const response = await fetch(`${BACK_URL}/groups`, {
                method: 'POST',
                headers: {
                    "Authorization": `Bearer ${token}`,
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Origin": "*",
                },
                body: JSON.stringify({
                    name: groupName.trim()
                }),
                cache: "no-store",
            });

            result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail);
            }

            setGroupName('');
            toggleForm();
            alert('Success creating group!');
            window.location.reload()
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="button-and-more-container">
            <button onClick={toggleForm} className="create-group">
                + Create group
            </button>

            <Modal isOpen={isOpen} onClose={toggleForm}>
                <form onSubmit={handleSubmit}>
                    <div className="btn-close-container">
                        <label>
                            Group name:
                        </label>
                        <button
                            type="button"
                            onClick={toggleForm}
                            className="btn-close"
                        >
                            <FontAwesomeIcon icon={faXmark}/>
                        </button>
                    </div>
                        <input
                                type="text"
                                value={groupName}
                                onChange={(e) => setGroupName(e.target.value)}
                                required
                                className="group-name-input"
                            />
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                    <div className="buttons-container">
                        <button type="submit" className="btn">Create</button>
                        <button type="button" onClick={toggleForm} className="btn-cancel">Cancel</button>
                    </div>
                </form>
            </Modal>
        </div>
    );
}

export default CreateGroupButton;