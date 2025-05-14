import React, { useState, useEffect } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Login.css';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, error: authError, currentUser } = useAuth();
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  // Check for success message in location state (e.g., after registration)
  useEffect(() => {
    if (location.state?.message) {
      setSuccessMessage(location.state.message);
      // Clear the location state after reading the message
      window.history.replaceState({}, document.title);
    }
  }, [location]);

  // Redirect if user is already logged in
  useEffect(() => {
    if (currentUser) {
      console.log('User is logged in, redirecting to dashboard');
      navigate('/dashboard');
    }
  }, [currentUser, navigate]);

  // Formik setup with Yup validation
  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
    },
    validationSchema: Yup.object({
      email: Yup.string()
        .email('Invalid email address')
        .required('Email is required'),
      password: Yup.string()
        .required('Password is required'),
    }),
    onSubmit: async (values) => {
      if (isLoggingIn) return; // Prevent multiple submissions
      
      try {
        setIsLoggingIn(true);
        setError(null);
        setSuccessMessage(null);
        
        console.log('Attempting to log in with:', values.email);
        await login(values.email, values.password);
        
        // If login is successful, we'll be redirected by the useEffect above
        console.log('Login successful');
      } catch (err) {
        console.error('Login error:', err);
        setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
      } finally {
        setIsLoggingIn(false);
      }
    },
  });

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">Exam Planning System</h2>
        <h3 className="login-subtitle">Login</h3>
        
        {successMessage && (
          <div className="success-message">
            {successMessage}
          </div>
        )}
        
        {(error || authError) && (
          <div className="error-message">
            {error || authError}
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

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="password-input-container">
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.password}
                className={formik.touched.password && formik.errors.password ? 'error' : ''}
              />
              <button 
                type="button" 
                className="toggle-password-button"
                onClick={togglePasswordVisibility}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                <i className={`password-eye ${showPassword ? "eye-open" : "eye-closed"}`}></i>
              </button>
            </div>
            {formik.touched.password && formik.errors.password ? (
              <div className="error-text">{formik.errors.password}</div>
            ) : null}
          </div>

          <div className="forgot-password">
            <Link to="/forgot-password">Forgot Password?</Link>
          </div>

          <button type="submit" className="login-button" disabled={formik.isSubmitting}>
            {formik.isSubmitting ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="login-help">
          <p>Don't have an account? <Link to="/register">Create Account</Link></p>
          <p className="login-note">New accounts are created as Student by default</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
