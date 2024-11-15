
import { useState } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Component to add a new topping
function AddToppingForm({ onToppingAdded }) {
    const [name, setName] = useState(''); 
    const [error, setError] = useState(''); 

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent the default form submission behavior/reloading
        if (!name.trim()) {
            setError('Topping name cannot be empty.');
            return;
        }
        try {
            // Send POST request to add new topping
            await axios.post(`${API_URL}/toppings`, { name });
            setName(''); 
            setError(''); 
            onToppingAdded(); // Trigger the parent callback to refresh the topping list
        } catch (error) {
            if (error.response) {
                setError(`Error: ${error.response.status} ${error.response.statusText} - ${error.response.data?.error || "An error occurred."}`);
            } else if (error.request) {
                setError("Error: No response received from the server.");
            } else {
                setError(`Error: ${error.message}`);
            }
        }
    };

    return (
        <form onSubmit={handleSubmit} className="mb-3">
            <div className="form-group">
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="form-control"
                    placeholder="Enter topping name"
                />
                {error && <div className="alert alert-danger mt-2">{error}</div>}
            </div>
            <button type="submit" className="btn btn-primary">Add Topping</button>
        </form>
    );
}

AddToppingForm.propTypes = {
    onToppingAdded: PropTypes.func.isRequired,
};

export default AddToppingForm;