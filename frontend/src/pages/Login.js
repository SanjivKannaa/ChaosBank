import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import Button from '@mui/material/Button';
import axios from 'axios'; 
// import './css/global.css';
import styles from '../css/login.module.css';
import Header from '../components/Header';
import Footer from '../components/Footer';
import QuickLinks from '../components/QuickLinks';


function Login() {
  let navigate = useNavigate();
  const [formData, setFormData] = useState({
    userid: '',
    password: '',
  });

  const [error, setError] = useState('');

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
    setError('       ');
  };

  const signup = async (event) => {
    navigate('/register');
  }

  const handleSubmit = async (event) => {
    event.preventDefault();

    const loginData = {
      username: formData.userid,
      password: formData.password,
    };

    if (loginData["username"]==='' || loginData["password"]===''){
      setError("Please enter all the details");
      return;
    }

    try {
      const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/auth/login`, loginData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Handle different error cases based on response data
      console.log("login successful");
      const jwtToken = response.data.jwt;
      const expirationTime = new Date(Date.now() + 30 * 60 * 1000);
      document.cookie = `token=${jwtToken}; path=/; expires=${expirationTime.toUTCString()}`;
      navigate('/dashboard')
    } catch (error) {
      if (error.response) {
        // Server responded with a status code outside 2xx
        const { status, data } = error.response;

        if (status === 400) {
          setError("Not all fields are valid.");
        } else if (status === 401) {
          setError(data.error === "User not found" ? "User not found" : "Invalid credentials");
        } else {
          setError("Something went wrong.");
        }

        console.log(data);
      } else if (error.request) {
        // Request was made but no response received (Server Down / No Internet)
        setError("Cannot connect to the server. Please check your internet or try again later.");
        console.error("No response from server:", error.request);
      } else {
        // Other errors (Unexpected issues)
        setError("An unexpected error occurred.");
        console.error("Unexpected Error:", error.message);
      }

    }
  };

  return (
    <div>
      <QuickLinks />
      <Header />
      <div className={styles.App}>
        <div className={styles.container}>
          <div className={styles.leftDiv}>
            <p className={styles.logintext}>Login to Your Account</p>
          </div>
          <div className={styles.rightDiv}>
            <form onSubmit={handleSubmit}>
              <label>
                USERNAME:
                <input 
                  placeholder='username'
                  type="text" 
                  name="userid" 
                  value={formData.userid} 
                  onChange={handleChange} 
                />
              </label>
              <label>
                PASSWORD:
                <input 
                  placeholder='Pa$$w0rd'
                  type="password" 
                  name="password" 
                  value={formData.password} 
                  onChange={handleChange} 
                />
              </label>
              <br />
              {error && <label className={styles.error} style={{ color: 'red' }}>{error}</label>}
              <br />
              <Button type="submit" variant="contained">LOGIN</Button>
              <br /><br />
            </form>
            <Button onClick={signup} variant="outlined">New User? Signup</Button>
            <br />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Login;
