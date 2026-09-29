import React, { useState, useEffect} from 'react';
import {
    LockKeyhole,
    ArrowLeft,
    ArrowRight,
    AlertCircle,
    CheckCircle2,
    KeyRound
} from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ResetPassword.css';

const ResetPassword = () => {

    const location = useLocation();
    const navigate = useNavigate();

    const email = location.state?.email;
    const otpVerified= location.state?.otpVerified;
    useEffect(() => {
        if (!email || !otpVerified) {
            navigate('/forget-password', { replace: true });
        }
    }, [email, otpVerified, navigate]);
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            setError('');
            setMessage('');

            if (newPassword !== confirmPassword) {
                setError('Passwords do not match');
                return;
            }

            setIsLoading(true);

            const response = await fetch(
                'http://localhost:8080/api/auth/reset-pass',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email,
                        newPassword
                    })
                }
            );

            const result = await response.json();

            if (!response.ok) {
                setError(result.message || 'Unable to reset password');
                return;
            }

            setMessage(
                result.message || 'Password reset successfully'
            );

            setTimeout(() => {
                navigate('/login');
            }, 1000);

        } catch (error) {
            setError('Error while connecting to the server');
            console.log('Error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="reset-password-page-wrapper">

            <div
                className="ambient-radial-glow"
                aria-hidden="true"
            />

            <div className="reset-password-card">

                <div className="card-header">


                    <h1 className="reset-password-title">
                        Create a new{' '}
                        <span className="highlight-text">
                            password
                        </span>
                    </h1>

                    <p className="reset-password-subtitle">
                        Enter your new password below.
                    </p>

                </div>


                <form
                    className="reset-password-form"
                    onSubmit={handleSubmit}
                >

                    <div className="form-group">

                        <div className="input-icon-wrapper">

                            <LockKeyhole
                                className="input-icon"
                                size={16}
                            />

                            <input
                                id="newPassword"
                                type="password"
                                className="form-input"
                                placeholder="Enter new password"
                                value={newPassword}
                                onChange={(e) =>
                                    setNewPassword(e.target.value)
                                }
                                minLength={8}
                                required
                            />

                        </div>

                    </div>


                    <div className="form-group">

                        <div className="input-icon-wrapper">

                            <LockKeyhole
                                className="input-icon"
                                size={16}
                            />

                            <input
                                id="confirmPassword"
                                type="password"
                                className="form-input"
                                placeholder="Confirm new password"
                                value={confirmPassword}
                                onChange={(e) =>
                                    setConfirmPassword(e.target.value)
                                }
                                minLength={8}
                                required
                            />

                        </div>

                    </div>


                    {error && (
                        <div
                            className="status-banner error"
                            role="alert"
                        >
                            <AlertCircle
                                className="status-icon"
                                size={16}
                            />

                            <span>{error}</span>
                        </div>
                    )}


                    {message && (
                        <div
                            className="status-banner success"
                            role="status"
                        >
                            <CheckCircle2
                                className="status-icon"
                                size={16}
                            />

                            <span>{message}</span>
                        </div>
                    )}


                    <button
                        type="submit"
                        className="btn-submit"
                        disabled={isLoading}
                    >

                        <span>
                            {isLoading
                                ? 'Resetting...'
                                : 'Reset Password'}
                        </span>

                        <ArrowRight size={16} />

                    </button>

                </form>


                <div className="reset-password-footer">

                    <button
                        type="button"
                        className="back-to-login-link"
                        onClick={() => navigate('/login')}
                    >

                        <ArrowLeft
                            className="back-arrow"
                            size={14}
                        />

                        <span>Back to Log in</span>

                    </button>

                </div>

            </div>

        </div>
    );
};

export default ResetPassword;