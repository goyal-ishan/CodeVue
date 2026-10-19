import React, { useState, useEffect } from 'react';
import { useAuth } from "../context/AuthContext.jsx";
import { Link , useNavigate} from "react-router-dom";
import { ArrowRight, Mail, Lock, Eye, EyeOff } from 'lucide-react';
import './Login.css';
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";

function Login() {
    const { setUser } = useAuth();
    const navigate = useNavigate();
    const [loginError, setLoginError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [googleError, setGoogleError] = useState('');
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        rememberMe: true,
    });

    const [showPassword, setShowPassword] = useState(false);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;

        setFormData((prev) => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value,
        }));
    };

    
   
const handleGoogleResponse = async (response) => {
    try {
        console.log('Google response:', response);
        setGoogleError('');

        if (response.error || !response.code) {
            throw new Error(
                response.error || 'Google did not return an authorization code'
            );
        }

        console.log('Sending code to backend...');

        const result = await fetch(
            'http://localhost:8080/api/auth/google',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: response.code,
                    agreeToTerms: true
                })
            }
        );

        const data = await result.json();

        console.log('Backend status:', result.status);
        console.log('Backend response:', data);

        if (!result.ok) {
            throw new Error(data.message || 'Google login failed');
        }

        if (!data.accessToken) {
            throw new Error('Backend did not return an access token');
        }

        localStorage.setItem('accessToken', data.accessToken);

        console.log('Navigating to Dashboard...');
        navigate('/dashboard');

    } catch (error) {
        console.error('Google sign-in error:', error);
        setGoogleError(error.message || 'Google sign-in failed');
    }
};


    useEffect(() => {
    const script = document.createElement('script');

    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;

    script.onload = () => {
        console.log('Google script loaded');

        window.googleOAuthClient = window.google.accounts.oauth2.initCodeClient({
            client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
            scope: 'openid email profile',
            ux_mode: 'popup',
            callback: handleGoogleResponse
        });
    };

    document.body.appendChild(script);

    return () => {
        document.body.removeChild(script);
    };
    }, []);


    const handleGoogleSignIn = () => {
        window.googleOAuthClient.requestCode();
    };


    
const handleSubmit = async (e) => {
    e.preventDefault();

    setLoginError('');
    setIsLoading(true);

    try {
        const response = await fetch(
            'http://localhost:8080/api/auth/login',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: formData.email,
                    password: formData.password
                })
            }
        );

        const result = await response.json();

        if (!response.ok) {
            setLoginError(result.message || 'Login failed. Please try again.');
            return;
        }

        if (!result.accessToken) {
            setLoginError('Login succeeded, but no access token was returned.');
            return;
        }

       
        localStorage.setItem('accessToken', result.accessToken);
        localStorage.setItem('userName', result.user.fullName);
        localStorage.setItem('userEmail', result.user.email);
        setUser(result.user);
        navigate('/dashboard');

    } catch (error) {
        console.error('Error while logging in:', error);
        setLoginError('Unable to connect to the server. Please try again.');
    } finally {
        setIsLoading(false);
    }
};


    return (
        <>
        <Header/>
        <div className="login-page-wrapper">

            {/* Background Radial Glow */}
            <div
                className="ambient-radial-glow"
                aria-hidden="true"
            />

            {/* Main Login Card */}
            <div className="login-card">

                {/* Header */}
                <div className="login-card-header">

                    <h1 className="login-title">
                        Welcome Back to
                        <div className="LogoName2">
                            <span className="logo-code2">Code</span>
                            <span className="logo-vue2">Vue</span>
                        </div>
                    </h1>

                    <p className="login-subtitle">
                        Sign in to resume your mock interview preparation.
                    </p>

                </div>

                {/* 1-Click Social Sign-In (Google Only - GitHub removed) */}
                <div className="social-auth-single">

                    <button
                        type="button"
                        className="social-btn-full"
                        onClick={handleGoogleSignIn}
                    >

                        {/* Google Vector Icon */}
                        <svg
                            className="google-icon"
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

                        <span>Continue with Google</span>

                    </button>
                    {googleError && (
    <p style={{ color: '#ef4444', marginTop: '10px' }}>
        {googleError}
    </p>
)}
                </div>

                {/* Divider */}
                <div className="auth-divider">
                    <span>OR CONTINUE WITH EMAIL</span>
                </div>

                {/* Login Form */}
                <form
                    className="login-form"
                    onSubmit={handleSubmit}
                >

                    {/* Email Address */}
                    <div className="form-group">

                        <label
                            className="form-label"
                            htmlFor="email"
                        >
                            Email Address
                        </label>

                        <div className="input-icon-wrapper">

                            <Mail
                                className="input-icon-left"
                                size={16}
                            />

                            <input
                                id="email"
                                name="email"
                                type="email"
                                className="form-input"
                                placeholder="ishan@gmail.com"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />

                        </div>

                    </div>

                    {/* Password */}
                    <div className="form-group">

                        <div className="form-label-row">

                            <label
                                className="form-label"
                                htmlFor="password"
                            >
                                Password
                            </label>

                            <Link to="/forget-password"
                                className="forgot-password-link"
                            >
                                Forgot password?
                            </Link>

                        </div>

                        <div className="input-icon-wrapper">

                            <Lock
                                className="input-icon-left"
                                size={16}
                            />

                            <input
                                id="password"
                                name="password"
                                type={showPassword ? 'text' : 'password'}
                                className="form-input"
                                placeholder="••••••••••••"
                                value={formData.password}
                                onChange={handleChange}
                                required
                            />

                            <button
                                type="button"
                                className="input-action-right"
                                onClick={() =>
                                    setShowPassword(!showPassword)
                                }
                                aria-label={
                                    showPassword
                                        ? 'Hide password'
                                        : 'Show password'
                                }
                            >
                                {showPassword
                                    ? <EyeOff size={16} />
                                    : <Eye size={16} />
                                }
                            </button>

                        </div>

                    </div>

                    {/* Remember Me Checkbox */}
                    <label className="remember-row">

                        <input
                            type="checkbox"
                            name="rememberMe"
                            className="remember-checkbox"
                            checked={formData.rememberMe}
                            onChange={handleChange}
                        />

                        <span className="remember-text">
                            Remember me
                        </span>

                    </label>
                    {loginError && (
                      <p style={{ color: '#ef4444', marginTop: '10px' }}>
                         {loginError}
                     </p>
                    )}
                    {/* Sign In CTA Button */}
                    <button
                        type="submit"
                        className="btn-submit"
                    >
                        
    <span>{isLoading ? 'Signing In...' : 'Sign In'}</span>
    {!isLoading && <ArrowRight size={16} />}
                    </button>

                </form>

                {/* Footer / Registration Link */}
                <div className="login-card-footer">

                    <span>Don't have an account?</span>

                    <a
                        href="/Get Started"
                        className="register-link"
                    >
                        Get Started for free &rarr;
                    </a>

                </div>

            </div>

        </div>
        <Footer/>
        </>
    );
}

export default Login;