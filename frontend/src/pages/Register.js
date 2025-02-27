import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import QuickLinks from "../components/QuickLinks";
import styles from "../css/register.module.css"; // Import CSS module
import axios from "axios";
import { responsiveFontSizes } from "@mui/material";

const Register = () => {
  let navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    profileName: "",
    password: "",
    confirmPassword: "",
    email: "",
    phoneNumber: "",
    securityQuestion1: "",
    securityQuestion2: "",
    securityQuestion3: "",
  });
  const [usernameAvailable, setUsernameAvailable] = useState('1'); // should be set at '' for false

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const checkUsernameAvailability = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    axios
    .get(`${process.env.REACT_APP_BACKEND_URL}/isUsernameAvailable?username=${formData.username}`)
    .then((response) => {
      setUsernameAvailable('1');
      setError('');
      setSuccess('');
      return true;
    })
    .catch((error) => {
      setUsernameAvailable('');
      setError('');
      setSuccess('');
      return false;
    })
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
    setSuccess('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSuccess("");

    const {
      username,
      profileName,
      password,
      confirmPassword,
      email,
      phoneNumber,
      securityQuestion1,
      securityQuestion2,
      securityQuestion3,
    } = formData;
    console.log(formData);

    if (checkUsernameAvailability === false) {
      setError('Username not available')
      return;
    }
    if (!username || !profileName || !password || !confirmPassword || !email || !phoneNumber || !securityQuestion1 || !securityQuestion1 || !securityQuestion2 || !securityQuestion2 || !securityQuestion3 || !securityQuestion3) {
      setError("All fields are required.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    axios
      .post(`${process.env.REACT_APP_BACKEND_URL}/register`, formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response) => {
        console.log(response.data);
        const jwtToken = response.data.jwt;
        const expirationTime = new Date(Date.now() + 30 * 60 * 1000);
        document.cookie = `token=${jwtToken}; path=/; expires=${expirationTime.toUTCString()}`;
        setSuccess('Successfully Registered!! Redirecting to Dashboard...')
      })
      .catch((error) => {
        console.log(error);
        setError(error);
      })
    setTimeout(() => {
      navigate("/dashboard");
    }, 1500);
  };

  return (
    <div className={styles.container}>
      {/* <Header /> */}
      <QuickLinks />
      <div className={styles.registerBox}>
        <h2>Create an Account</h2>
        {error && <div className={styles.error}>{error}</div>}
        {success && <div className={styles.success}>{success}</div>}
        <form onSubmit={handleSubmit}>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            placeholder="Enter username"
            value={formData.username}
            onChange={handleChange}
            className={styles.input}
          />
          <button className={styles.checkUsernameButton} onClick={checkUsernameAvailability}>
            check username Availability
          </button>
          {usernameAvailable && <label className={styles.usernameAvailable}>✅Username Available</label>}
          {!usernameAvailable && <label className={styles.usernameUnavailable}>❌Username Unavailable</label>}
          <label>Profile Name:</label>
          <input
            type="text"
            name="profileName"
            placeholder="Enter profile name"
            value={formData.profileName}
            onChange={handleChange}
            className={styles.input}
          />

          <label>Email:</label>
          <input
            type="email"
            name="email"
            placeholder="Enter email"
            value={formData.email}
            onChange={handleChange}
            className={styles.input}
          />

          <label>Phone Number:</label>
          <input
            type="tel"
            name="phoneNumber"
            placeholder="Enter phone number"
            value={formData.phoneNumber}
            onChange={handleChange}
            className={styles.input}
          />

          <label>Password:</label>
          <input
            type="password"
            name="password"
            placeholder="Enter password"
            value={formData.password}
            onChange={handleChange}
            className={styles.input}
          />

          <label>Confirm Password:</label>
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm password"
            value={formData.confirmPassword}
            onChange={handleChange}
            className={styles.input}
          />

          <label>Security Question 1: What is the name of your first pet?</label>
          <input
            type="text"
            name="securityQuestion1"
            placeholder="Your answer"
            value={formData.securityQuestion1}
            onChange={handleChange}
            className={styles.input}
          />

          <label>Security Question 2: What was the name of your first school?</label>
          <input
            type="text"
            name="securityQuestion2"
            placeholder="Your answer"
            value={formData.securityQuestion2}
            onChange={handleChange}
            className={styles.input}
          />

          <label>Security Question 3: What was the name of your favorite teacher?</label>
          <input
            type="text"
            name="securityQuestion3"
            placeholder="Your answer"
            value={formData.securityQuestion3}
            onChange={handleChange}
            className={styles.input}
          />

          <button type="submit" className={styles.button}>
            Sign Up
          </button>
        </form>
        <p>
          Already have an account? <a href="/login" className={styles.link}>Login</a>
        </p>
      </div>
      <Footer />
    </div>
  );
};

export default Register;
