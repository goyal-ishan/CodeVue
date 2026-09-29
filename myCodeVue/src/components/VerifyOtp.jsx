import React, { useEffect, useState } from 'react';
import {
    Mail,
    ArrowLeft,
    ArrowRight,
    AlertCircle,
    CheckCircle2,
    KeyRound
} from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';
import './VerifyOtp.css';

const VerifyOtp = () => {

    const location = useLocation();
    const navigate = useNavigate();

    const email=location.state?.email;
    const [otp, setOtp] = useState('');
    
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const [timeLeft, setTimeLeft] = useState(5 * 60);

    useEffect(()=>{
        if(!email)
        {
            navigate('/forget-password', {replace:true});
        }
    },[email,navigate]);
    useEffect(() => {

        if (timeLeft <= 0) {
            return;
        }

        const timer = setInterval(() => {
            setTimeLeft((prevTime) => prevTime - 1);
        }, 1000);

        return () => clearInterval(timer);

    }, [timeLeft]);


    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;

    const formattedTime =
        `${minutes}:${seconds.toString().padStart(2, '0')}`;


    const handleSubmit = async (e) => {

        e.preventDefault();

        setError('');
        setMessage('');

        if (timeLeft <= 0) {
            setError('OTP has expired. Please request a new OTP.');
            return;
        }

        try {

            setIsLoading(true);

            const response = await fetch(
                'http://localhost:8080/api/auth/verify-otp',
                {
                    method: 'POST',

                    headers: {
                        'Content-Type': 'application/json'
                    },

                    body: JSON.stringify({
                        email,
                        otp
                    })
                }
            );

            const result = await response.json();

            if (!response.ok) {
                setError(result.message || 'Invalid OTP');
                return;
            }

            setMessage(
                result.message || 'OTP verified successfully'
            );

            setTimeout(() => {
                navigate('/reset-password',{
                    state:{
                        email,
                        otpVerified:true
                    }
                });
            },1000);

        } catch (error) {

            setError('Error while connecting to the server');

            console.log('Error:', error);

        } finally {

            setIsLoading(false);

        }
    };


    return (
        <div className="otp-page-wrapper">

            <div
                className="ambient-radial-glow"
                aria-hidden="true"
            />

            <div className="otp-card">

                <div className="card-header">


                    <h1 className="otp-title">
                        Verify your{' '}
                        <span className="highlight-text">
                            OTP
                        </span>
                    </h1>

                    <p className="otp-subtitle">
                        Enter the 6-digit OTP sent to your registered email.
                    </p>

                </div>


                <form
                    className="otp-form"
                    onSubmit={handleSubmit}
                >

                    <div className="form-group">


                        <input
                            id="otp"
                            type="text"
                            className="otp-input"
                            placeholder="Enter 6-digit OTP"
                            value={otp}
                            onChange={(e) =>
                                setOtp(e.target.value)
                            }
                            maxLength={6}
                            inputMode="numeric"
                            required
                        />

                    </div>


              

                    <div className="otp-timer">

                        {timeLeft > 0 ? (
                            <>
                                OTP expires in{' '}
                                <span>
                                    {formattedTime}
                                </span>
                            </>
                        ) : (
                            <span>
                                OTP has expired
                            </span>
                        )}

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
                        disabled={isLoading || timeLeft <= 0}
                    >

                        <span>
                            {isLoading
                                ? 'Verifying...'
                                : timeLeft <= 0
                                    ? 'OTP Expired'
                                    : 'Verify OTP'}
                        </span>

                        <ArrowRight size={16} />

                    </button>

                </form>


                <div className="otp-footer">

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

export default VerifyOtp;