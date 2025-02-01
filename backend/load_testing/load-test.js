import http from 'k6/http';
import { check } from 'k6';

const baseUrl = 'http://localhost:5000';
let registeredUsers = {}; // Object to store registered usernames
let loggedInUsers = new Set(); // Set to store logged-in usernames (avoids duplicates)
let successfulTransactions = 0;

export const options = {
  stages: [
    { duration: '20s', target: 1, vus: { iterations: 1 } },
    { duration: '1m', target: 10, vus: { iterations: 1 } },
    { duration: '20s', target: 1, vus: { iterations: 1 } },
  ],
};

// Function to register a new user
function registerUser(username) {
  const registerData = {
    username,
    password: "load_test_pass",
    balance: "1000",
  };

  const registerResponse = http.post(
    `${baseUrl}/register`,
    JSON.stringify(registerData),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(registerResponse.status, { 'register success': (r) => r === 200 });

  registeredUsers[username] = true;
}

// Function to login a registered user
function loginUser(username) {
  const loginData = {
    username,
    password: "load_test_pass",
  };

  const loginResponse = http.post(
    `${baseUrl}/login`,
    JSON.stringify(loginData),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(loginResponse.status, { 'login success': (r) => r === 200 });

  // Extract and store cookie from login response (assuming parseCookies exists)
  const loginCookies = loginResponse.headers['Set-Cookie'];
  if (loginCookies) {
    loggedInUsers.add(username);
    return parseCookies(loginCookies);
  } else {
    return null;
  }
}

// Function to perform a transfer with stored cookies
function performTransfer(cookies) {
  const transferData = {
    "receiver": "0000000001",
    "amount": "100",
  };
  const transferResponse = http.post(
    `${baseUrl}/transfer`,
    JSON.stringify(transferData),
    { headers: { 'Content-Type': 'application/json' }, cookies }
  );

  check(transferResponse.status, { 'transfer success': (r) => r === 200 });
  successfulTransactions++;
}

export default function () {
  const username = `test_1_user_${++userNumber || 1}`;
  // Registration Phase
  if (!registeredUsers[username]) {
    registerUser(username);
  }

  // Login Phase
  const loginCookies = loginUser(username);
  if (loginCookies) {
    // Transfer Phase
    performTransfer(loginCookies);
  } else {
    console.warn(`Failed to login user: ${username}`); // Handle login failure (optional)
  }
}

function parseCookies(cookieString) {
  // Implement parsing logic to extract cookie key-value pairs
  // You can use existing libraries or a simple split/trim approach
  const cookiePairs = cookieString.split(';').map(pair => pair.trim().split('='));
  const cookiesObj = {};
  for (const [key, value] of cookiePairs) {
    cookiesObj[key] = value;
  }
  return cookiesObj;
}

let userNumber = 0;

// export function teardown() {
//   console.log(`--- Test Results ---`);
//   console.log(`Number of Users Created: ${registeredUsers.length}`);
//   console.log(`Number of Users Logged In: ${loggedInUsers.size}`);
//   console.log(`Number of Successful Transactions: successfulTransactions`);
//   console.log(`List of Registered Usernames:`);
//   console.log(registeredUsers);
//   console.log(`List of Logged-In Usernames:`);
//   console.log(loggedInUsers);
// }