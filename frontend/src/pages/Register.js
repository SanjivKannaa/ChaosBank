import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import QuickLinks from "../components/QuickLinks";
import styles from "../css/register.module.css";
import axios from "axios";

const Register = () => {
  let navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    profileName: "",
    password: "",
    email: "",
    phoneNumber: "",
    date_of_birth: "",
    address: {
      door_plot_no: "",
      street_name_1: "",
      street_name_2: "",
      city: "",
      state: "",
      country: "",
      pin: "",
    },
    mobile_number: "",
    aadhar_number: "",
    pan_number: "",
    balance: 0, // Initialize with a default balance, possibly 0
  });

  const [usernameAvailable, setUsernameAvailable] = useState(true); // Initialize as true for initial state
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // --- Input Validation Functions ---
  const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const isValidPhoneNumber = (phoneNumber) => {
    return /^\d{10}$/.test(phoneNumber); // Simple 10-digit check
  };

  const isValidAadharNumber = (aadhar) => {
    return /^\d{12}$/.test(aadhar); // 12-digit Aadhar
  };
  
  const isValidPanNumber = (pan) => {
    return /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test(pan);  //PAN Number regex
  }
  const isValidPinCode = (pin) => {
    return /^\d{6}$/.test(pin);
  }

  // --- Check Username Availability ---
  const checkUsernameAvailability = async () => { // Make this function async
    if (!formData.username) {
      setUsernameAvailable(true); // If empty, consider it "available" (to avoid immediate error)
      return; // Early return to avoid unnecessary API call
    }

    try {
      const response = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}/misc/isUsernameAvailable?username=${formData.username}`
      );
      setUsernameAvailable(true);
      setError(""); // Clear previous errors
    } catch (error) {
      setUsernameAvailable(false);
      setError("Username is not available."); // Specific error message
    }
  };

  // --- Handle Change ---  Handles nested address object
  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name.startsWith("address.")) {
        const addressField = name.split(".")[1];
        setFormData(prevFormData => ({
            ...prevFormData,
            address: {
                ...prevFormData.address,
                [addressField]: value
            }
        }));
    } else {
      setFormData({ ...formData, [name]: value });
    }
    setError(""); // Clear error on any change
    setSuccess("");
  };

  const handleBlur = () => { //for on leaving username input field
    checkUsernameAvailability();
  };

  // --- Handle Submit ---
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSuccess("");

    // --- Comprehensive Validation ---
    if (!formData.username || !formData.profileName || !formData.password || !formData.email ||
        !formData.phoneNumber || !formData.date_of_birth || !formData.mobile_number ||
        !formData.aadhar_number || !formData.pan_number) {
      setError("All fields are required.");
      return;
    }

    // Validate nested address fields
    const address = formData.address;
    if (!address.door_plot_no || !address.street_name_1 || !address.city ||
        !address.state || !address.country || !address.pin) {
        setError("All address fields are required.");
        return;
    }

    if (!usernameAvailable) {
      setError("Username is not available.");
      return;
    }

    if (!isValidEmail(formData.email)) {
      setError("Invalid email format.");
      return;
    }

    if (!isValidPhoneNumber(formData.phoneNumber)) {
      setError("Invalid phone number.  Must be 10 digits.");
      return;
    }

    if(!isValidAadharNumber(formData.aadhar_number)){
        setError("Invalid Aadhar number. Must be 12 digits");
        return;
    }

    if(!isValidPanNumber(formData.pan_number)){
        setError("Invalid PAN number");
        return;
    }

    if(!isValidPinCode(address.pin)){
        setError("Invalid PIN code. Must be 6 digits");
        return;
    }
    
    //Strong Password Validation
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/;
      if (!passwordRegex.test(formData.password)) {
        setError(
          "Password must be at least 8 characters and include at least one uppercase letter, one lowercase letter, one digit, and one special character."
        );
        return;
      }


    // --- API Call ---
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/auth/register`,
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log(response.data);
      const jwtToken = response.data.jwt;
      const expirationTime = new Date(Date.now() + 30 * 60 * 1000);  // 30 min expiration
      document.cookie = `token=${jwtToken}; path=/; expires=${expirationTime.toUTCString()}`;
      setSuccess("Successfully Registered! Redirecting to Dashboard...");
      setTimeout(() => {
        navigate("/dashboard");
      }, 1500); // Redirect after 1.5 seconds

    } catch (error) {
      console.error("Registration error:", error);
       if (error.response && error.response.data && error.response.data.error) {
          setError(error.response.data.error);  // Show backend error message
        }
      else{
        setError("An error occurred during registration."); // Generic error
      }
    }
  };

  return (
    <div className={styles.container}>
      <Header />
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
            onBlur={handleBlur}  // Check availability on blur
            className={styles.input}
          />
           {usernameAvailable ? (
            <label className={styles.usernameAvailable}>✅ Username Available</label>
          ) : (
            <label className={styles.usernameUnavailable}>❌ Username Unavailable</label>
          )}

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

        <label>Date of Birth:</label>
            <input
                type="date"
                name="date_of_birth"
                value={formData.date_of_birth}
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


        <label>Mobile Number:</label>
            <input
                type="tel"
                name="mobile_number"
                placeholder="Enter mobile number"
                value={formData.mobile_number}
                onChange={handleChange}
                className={styles.input}
            />

            <label>Aadhar Number:</label>
            <input
                type="text"
                name="aadhar_number"
                placeholder="Enter Aadhar number"
                value={formData.aadhar_number}
                onChange={handleChange}
                className={styles.input}
            />

            <label>PAN Number:</label>
            <input
                type="text"
                name="pan_number"
                placeholder="Enter PAN number"
                value={formData.pan_number}
                onChange={handleChange}
                className={styles.input}
            />

        <h3>Address</h3>
            <label>Door/Plot No:</label>
            <input
                type="text"
                name="address.door_plot_no"
                placeholder="Enter door/plot number"
                value={formData.address.door_plot_no}
                onChange={handleChange}
                className={styles.input}
            />

            <label>Street Name 1:</label>
            <input
                type="text"
                name="address.street_name_1"
                placeholder="Enter street name 1"
                value={formData.address.street_name_1}
                onChange={handleChange}
                className={styles.input}
            />

            <label>Street Name 2:</label>
            <input
                type="text"
                name="address.street_name_2"
                placeholder="Enter street name 2"
                value={formData.address.street_name_2}
                onChange={handleChange}
                className={styles.input}
            />
            <label>City:</label>
            <input
                type="text"
                name="address.city"
                placeholder="Enter City"
                value={formData.address.city}
                onChange={handleChange}
                className={styles.input}
           />
           <label>State</label>
            <input
                type="text"
                name="address.state"
                placeholder="Enter State"
                value={formData.address.state}
                onChange={handleChange}
                className={styles.input}
           />

            <label>Country:</label>
            <input
                type="text"
                name="address.country"
                placeholder="Enter country"
                value={formData.address.country}
                onChange={handleChange}
                className={styles.input}
            />

            <label>PIN Code:</label>
            <input
                type="text"
                name="address.pin"
                placeholder="Enter PIN code"
                value={formData.address.pin}
                onChange={handleChange}
                className={styles.input}
            />

          <button type="submit" className={styles.button}>
            Sign Up
          </button>
        </form>
        <p>
          Already have an account? <a href="/login" className={styles.link}>
            Login
          </a>
        </p>
      </div>
      <Footer />
    </div>
  );
};

export default Register;
