// src/components/SignUp.js
import React, { useState } from "react";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "../firebaseConfig";
import { Link, useNavigate } from "react-router-dom";
import './AuthForm.css';

const SignUp = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSignUp = async (e) => {
        e.preventDefault();
        try {
            await createUserWithEmailAndPassword(auth, email, password);
            navigate("/home");
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <div className="auth-container">
            <form onSubmit={handleSignUp} className="auth-form">
                <h1>Sign Up</h1>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
                <button type="submit">Sign Up</button>
                {error && <p className="auth-error">{error}</p>}
                <p>
                    Already have an account? <Link to="/login">Log In</Link>
                </p>
            </form>
        </div>
    );
};

export default SignUp;
