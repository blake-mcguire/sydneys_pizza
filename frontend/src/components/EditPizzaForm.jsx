// eslint-disable-next-line no-unused-vars
import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function EditPizzaForm({ pizza, onCancel, onPizzaUpdated }) {
    const [name, setName] = useState(pizza.name);
    const [availableToppings, setAvailableToppings] = useState([]);
    const [selectedToppings, setSelectedToppings] = useState(pizza.toppings.map((topping) => topping.topping_id));
    const [error, setError] = useState(''); // State to store error messages

    useEffect(() => {
        const fetchToppings = async () => {
            try {
                const response = await axios.get(`${API_URL}/toppings`);
                setAvailableToppings(response.data);
            } catch (error) {
                console.error("Error fetching toppings:", error);
            }
        };
        fetchToppings();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const toppings = selectedToppings.map((id) => ({ topping_id: id }));
            await axios.put(`${API_URL}/pizzas/${pizza.pizza_id}`, { name, toppings });
            setError(''); // Clear error on successful submission
            onPizzaUpdated(); 
        } catch (error) {
            if (error.response && error.response.status === 400) {
                setError(error.response.data.error || "An error occurred. Please try again."); // Display error message
            } else {
                console.error("Error updating pizza:", error);
            }
        }
    };

    const handleToppingChange = (e) => {
        const { value, checked } = e.target;
        setSelectedToppings((prev) =>
            checked ? [...prev, parseInt(value)] : prev.filter((id) => id !== parseInt(value))
        );
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Enter Pizza Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
            </div>
            <div className="form-group">
                <h4>Select Toppings</h4>
                {availableToppings.length > 0 ? (
                    availableToppings.map((topping) => (
                        <div key={topping.topping_id} className="form-check">
                            <input
                                type="checkbox"
                                className="form-check-input"
                                value={topping.topping_id}
                                onChange={handleToppingChange}
                                checked={selectedToppings.includes(topping.topping_id)}
                            />
                            <label className="form-check-label">{topping.name}</label>
                        </div>
                    ))
                ) : (
                    <p>Loading toppings...</p>
                )}
            </div>
            {error && <p className="text-danger">{error}</p>}
            <button type="submit" className="btn btn-primary">Update Pizza</button>
            <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
        </form>
    );
}

EditPizzaForm.propTypes = {
    pizza: PropTypes.shape({
        pizza_id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        toppings: PropTypes.arrayOf(
            PropTypes.shape({
                topping_id: PropTypes.number.isRequired,
                name: PropTypes.string.isRequired,
            })
        ).isRequired,
    }).isRequired,
    onCancel: PropTypes.func.isRequired,
    onPizzaUpdated: PropTypes.func.isRequired,
};

export default EditPizzaForm;