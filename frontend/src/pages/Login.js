import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import Button from '@mui/material/Button';
import axios from 'axios'; 
import './css/global.css';
import './css/login.css';

function Login() {
  let navigate = useNavigate();
  const [formData, setFormData] = useState({
    userid: '',
    password: '',
  });

  const [error, setError] = useState(''); // State to store the error message

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
    setError(''); // Reset error message when the user types
  };

  const signup = async (event) => {
    navigate('/register');
  }

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent page reload

    const loginData = {
      username: formData.userid,
      password: formData.password,
    };

    if (loginData["username"]==='' || loginData["password"]===''){
      setError("Please enter the details");
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/login', loginData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Handle different error cases based on response data
      if (response.data.error === "Wrong Password") {
        setError('Incorrect password. Please try again.');
      } else if (response.data.error === "User Not Found") {
        setError('User not found. Please check your username.');
      } else {
        // Successful login
        console.log('Login Successful:', response.data);
        // Handle success (e.g., redirect to dashboard or set user state)
        navigate('/dashboard')
      }
    } catch (error) {
      setError('Something went wrong. Please try again later.');
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <div className="left-div">
          <p className="logintext">Login to Your Account</p>
        </div>
        <div className="right-div">
          <form onSubmit={handleSubmit}>
            <label>
              ACCOUNT NUMBER:
              <input 
                placeholder='000000001'
                type="text" 
                name="userid" 
                value={formData.userid} 
                onChange={handleChange} 
              />
            </label>
            <label>
              PASSWORD:
              <input 
                placeholder='P@55wo0d'
                type="password" 
                name="password" 
                value={formData.password} 
                onChange={handleChange} 
              />
            </label>
            <a href="/forgotPassword">Forgot password?</a>
            <br />
            {error && <label className="error" style={{ color: 'red' }}>{error}</label>}
            <br />
            <Button type="submit" variant="contained">LOGIN</Button>
            <br /><br />
          </form>
          <Button onClick={signup} variant="outlined">New User? Signup</Button>
          <br />
        </div>
      </div>
    </div>
  );
}

export default Login;
