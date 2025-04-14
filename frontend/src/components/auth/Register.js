import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

const Register = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Formik setup with Yup validation
  const formik = useFormik({
    initialValues: {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
    validationSchema: Yup.object({
      name: Yup.string()
        .required('Name is required'),
      email: Yup.string()
        .email('Invalid email address')
        .required('Email is required'),
      password: Yup.string()
        .min(8, 'Password must be at least 8 characters')
        .required('Password is required'),
      confirmPassword: Yup.string()
        .oneOf([Yup.ref('password'), null], 'Passwords must match')
        .required('Confirm password is required'),
    }),
    onSubmit: async (values) => {
      try {
        setError(null);
        // Register the user with STUDENT role by default
        const response = await axios.post('http://localhost:8000/api/v1/auth/register', {
          name: values.name,
          email: values.email,
          password: values.password,
          role: "STUDENT"  // Must match the exact enum value in the backend
        });
        
        // If registration is successful, redirect to login page
        if (response.status === 200 || response.status === 201) {
          navigate('/', { state: { message: 'Registration successful! You can now log in.' } });
        }
      } catch (err) {
        console.error('Registration error:', err);
        // Handle different types of error responses
        if (err.response?.data?.detail) {
          // If the error is a string
          if (typeof err.response.data.detail === 'string') {
            setError(err.response.data.detail);
          } 
          // If the error is an object or array
          else {
            setError('Registration failed. Please check your information and try again.');
          }
        } else {
          setError('Registration failed. Please try again.');
        }
      }
    },
  });

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">Create Account</h2>
        <h3 className="login-subtitle">Register as a Student</h3>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        <form onSubmit={formik.handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              id="name"
              name="name"
              type="text"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.name}
              className={formik.touched.name && formik.errors.name ? 'error' : ''}
            />
            {formik.touched.name && formik.errors.name ? (
              <div className="error-text">{formik.errors.name}</div>
            ) : null}
          </div>

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

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <div className="password-input-container">
              <input
                id="confirmPassword"
                name="confirmPassword"
                type={showConfirmPassword ? "text" : "password"}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.confirmPassword}
                className={formik.touched.confirmPassword && formik.errors.confirmPassword ? 'error' : ''}
              />
              <button 
                type="button" 
                className="toggle-password-button"
                onClick={toggleConfirmPasswordVisibility}
                aria-label={showConfirmPassword ? "Hide password" : "Show password"}
              >
                <i className={`password-eye ${showConfirmPassword ? "eye-open" : "eye-closed"}`}></i>
              </button>
            </div>
            {formik.touched.confirmPassword && formik.errors.confirmPassword ? (
              <div className="error-text">{formik.errors.confirmPassword}</div>
            ) : null}
          </div>

          <button type="submit" className="login-button" disabled={formik.isSubmitting}>
            {formik.isSubmitting ? 'Registering...' : 'Register'}
          </button>
        </form>

        <div className="login-help">
          <p>Already have an account? <Link to="/">Login</Link></p>
          <p className="login-note">Note: New accounts are created as Student by default</p>
        </div>
      </div>
    </div>
  );
};

export default Register;
