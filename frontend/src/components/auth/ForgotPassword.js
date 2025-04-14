import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

const ForgotPassword = () => {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState(null);

  // Formik setup with Yup validation
  const formik = useFormik({
    initialValues: {
      email: '',
    },
    validationSchema: Yup.object({
      email: Yup.string()
        .email('Invalid email address')
        .required('Email is required'),
    }),
    onSubmit: async (values) => {
      try {
        setError(null);
        // Since we don't have a real email service set up yet, we'll simulate a successful submission
        // In a production environment, this would call a real API endpoint that sends emails
        // await axios.post('http://localhost:8000/api/v1/auth/reset-password-request', { email: values.email });
        
        // For now, just simulate success
        setTimeout(() => {
          setIsSubmitted(true);
        }, 1000);
      } catch (err) {
        // Even if the email doesn't exist, we don't want to reveal that for security reasons
        // So we'll still show a success message
        setIsSubmitted(true);
      }
    },
  });

  if (isSubmitted) {
    return (
      <div className="login-container">
        <div className="login-card">
          <h2 className="login-title">Password Reset</h2>
          <div className="success-message">
            <p>If an account exists with the email {formik.values.email}, you will receive password reset instructions.</p>
            <p><strong>Note:</strong> Email sending is not yet implemented in this development environment. In a production environment, you would receive an email with reset instructions.</p>
          </div>
          <div className="login-help">
            <p><Link to="/">Return to Login</Link></p>
            <p><Link to="/test-login">Use Test Login</Link> (for development purposes)</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">Forgot Password</h2>
        <h3 className="login-subtitle">Enter your email to reset your password</h3>
        
        <div className="info-message">
          <p><strong>Development Note:</strong> Email sending is not yet implemented. This is a simulation of the password reset flow.</p>
        </div>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        <form onSubmit={formik.handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.email}
              className={formik.touched.email && formik.errors.email ? 'error' : ''}
            />
            {formik.touched.email && formik.errors.email ? (
              <div className="error-text">{formik.errors.email}</div>
            ) : null}
          </div>

          <button type="submit" className="login-button" disabled={formik.isSubmitting}>
            {formik.isSubmitting ? 'Submitting...' : 'Reset Password'}
          </button>
        </form>

        <div className="login-help">
          <p>Remember your password? <Link to="/">Back to Login</Link></p>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
