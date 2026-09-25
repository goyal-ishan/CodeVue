import React, { useState } from 'react';
import { ArrowRight, Code2 } from 'lucide-react';
import './GetStarted.css';
import Header from '../components/Header.jsx';

function GetStarted() {
    const [formData, setFormData] = useState({
        fullName: '',
        email: '',
        password: '',
        agreeToTerms: false
    });
    const [error, setError]=useState();
    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;

        setFormData((prev) => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };
    
    
    async function onSubmit(data){
        try{
            setError('');
            const response=await fetch('http://localhost:8080/api/auth/register',
                {
                     method: 'POST',
                     headers: {
                        'Content-type': 'application/json'
                     },
                     body: JSON.stringify(data)
                });
            const result=await response.json();
            if(!response.ok)
            {  
               setError(result.message || 'Registration failed! Please try again');
               console.log('Registration failed!', result.message);
               return;
            }

            console.log('Registered Successfully');

        }catch(error){
            setError('Error while connecting to the server');
            console.log('Error while registering: ', error);
        }
    }
    return (
        <>
        <Header/>
        <div className="register-page-wrapper">

            {/* Background Radial Glow */}
            <div
                className="ambient-radial-glow"
                aria-hidden="true"
            />

            {/* Main Registration Card */}
            <div className="register-card">

                {/* Header */}
                <div className="register-card-header">

                    <div className="card-badge">
                        <Code2 size={12} />
                        <span>GET STARTED</span>
                    </div>

                    <h1 className="register-title">
                        Create your CodeVue account
                    </h1>

                    <p className="register-subtitle">
                        Start practicing AI mock interviews in minutes.
                        No credit card required.
                    </p>

                </div>

                {/* 1-Click Social Sign-Up */}
                <div className="social-auth-grid">

                    <button
                        type="button"
                        className="social-btn"
                        onClick={() => console.log('Google Auth')}
                    >
                        {/* Google SVG Icon */}
                        <svg
                            className="social-icon"
                            viewBox="0 0 24 24"
                        >
                            <path
                                fill="#EA4335"
                                d="M12 5c1.6 0 3 .6 4.1 1.7l3.1-3.1C17.3 1.8 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.4 9 5 12 5z"
                            />

                            <path
                                fill="#4285F4"
                                d="M23.5 12.3c0-.8-.1-1.7-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5.1 3.7-8.8z"
                            />

                            <path
                                fill="#FBBC05"
                                d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.8s.2-2.1.4-2.8L1.9 6.3C.7 8.7 0 10.3 0 12s.7 3.3 1.9 5.7l3.7-2.9z"
                            />

                            <path
                                fill="#34A853"
                                d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2-6.4-4.8L1.9 16.4C3.7 20.4 7.5 23 12 23z"
                            />
                        </svg>

                        <span>Google</span>
                    </button>

                </div>

                {/* Divider */}
                <div className="auth-divider">
                    <span>OR CONTINUE WITH EMAIL</span>
                </div>

                {/* Registration Form */}
                <form
                    className="register-form"
                    onSubmit={(e)=>{
                        e.preventDefault();
                        onSubmit(formData);
                    }
                    }
                >

                    {/* Full Name */}
                    <div className="form-group">
                        <label
                            className="form-label"
                            htmlFor="fullName"
                        >
                            Full Name
                        </label>

                        <input
                            id="fullName"
                            name="fullName"
                            type="text"
                            className="form-input"
                            placeholder="e.g. Ishan Goyal"
                            value={formData.fullName}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    {/* Email Address */}
                    <div className="form-group">
                        <label
                            className="form-label"
                            htmlFor="email"
                        >
                            Email
                        </label>

                        <input
                            id="email"
                            name="email"
                            type="email"
                            className="form-input"
                            placeholder="Ishan@example.com"
                            value={formData.email}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    {/* Password */}
                    <div className="form-group">
                        <label
                            className="form-label"
                            htmlFor="password"
                        >
                            Password
                        </label>

                        <input
                            id="password"
                            name="password"
                            type="password"
                            className="form-input"
                            placeholder="••••••••••••"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            minLength={8}
                        />
                    </div>

                    {/* Terms & Conditions Checkbox */}
                    <label className="terms-row">

                        <input
                            type="checkbox"
                            name="agreeToTerms"
                            className="terms-checkbox"
                            checked={formData.agreeToTerms}
                            onChange={handleChange}
                            required
                        />

                        <span className="terms-text">
                            I agree to the{' '}
                            <a
                                href="#terms"
                                className="terms-link"
                            >
                                Terms of Service
                            </a>{' '}
                            and{' '}
                            <a
                                href="#privacy"
                                className="terms-link"
                            >
                                Privacy Policy
                            </a>
                            .
                        </span>

                    </label>
                    {
                        error && (
                            <p className='error-message'>*{error}</p>
                        )
                    }
                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="btn-submit"
                    >
                        <span>Create Account</span>
                        <ArrowRight size={16} />
                    </button>

                </form>

                {/* Footer / Login Link */}
                <div className="register-card-footer">
                    <span>Already have an account?</span>

                    <a
                        href="/login"
                        className="login-link"
                    >
                        Log in
                    </a>
                </div>

            </div>
        </div>
        </>
    );
}

export default GetStarted;