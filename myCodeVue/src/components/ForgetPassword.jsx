import React, { useState } from 'react';
import {Link, useNavigate} from "react-router-dom";
import { Mail, ArrowLeft, ArrowRight, AlertCircle, CheckCircle2, KeyRound } from 'lucide-react';

import './ForgetPassword.css';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            setError('');
            setMessage('');
            setIsLoading(true);

            const response = await fetch(
                'http://localhost:8080/api/auth/forgot-password',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email })
                }
            );

            const result = await response.json();

            if (!response.ok) {
                setError(result.message || 'Something went wrong');
                setIsLoading(false);
                return;
            }

            setMessage(result.message || 'OTP sent successfully to your email');
            console.log('OTP sent successfully');
            
            setTimeout(()=>{
               navigate('/verify-otp',{
                state:{email}
               });
            },1000);

        } catch (err) {
            setError('Error while connecting to the server');
            console.log('Error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="forgot-password-page-wrapper">

            <div className="ambient-radial-glow" aria-hidden="true" />

            <div className="forgot-password-card">

                <div className="card-header">


                    <h1 className="forgot-password-title">
                        Reset your <span className="highlight-text">password</span>
                    </h1>

                    <p className="forgot-password-subtitle">
                        Enter your registered email to receive an OTP.
                    </p>

                </div>

                <form className="forgot-password-form" onSubmit={handleSubmit}>

                    <div className="form-group">

                        <div className="input-icon-wrapper">

                            <Mail className="input-icon" size={16} />

                            <input
                                id="email"
                                type="email"
                                className="form-input"
                                placeholder="Enter your email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />

                        </div>

                    </div>

                    {error && (
                        <div className="status-banner error" role="alert">
                            <AlertCircle className="status-icon" size={16} />
                            <span>{error}</span>
                        </div>
                    )}

                    {message && (
                        <div className="status-banner success" role="status">
                            <CheckCircle2 className="status-icon" size={16} />
                            <span>{message}</span>
                        </div>
                    )}

                    <button
                        type="submit"
                        className="btn-submit"
                        disabled={isLoading}
                    >
                        <span>
                            {isLoading ? 'Sending...' : 'Send OTP'}
                        </span>

                        <ArrowRight size={16} />
                    </button>

                </form>

                <div className="forgot-password-footer">

                    <Link to="/login" className="back-to-login-link">
                        <ArrowLeft className="back-arrow" size={14} />
                        <span>Back to Log in</span>
                    </Link>

                </div>

            </div>

        </div>
    );
};

export default ForgotPassword;