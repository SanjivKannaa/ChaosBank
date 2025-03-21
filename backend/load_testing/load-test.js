import http from 'k6/http';
import { check, sleep } from 'k6';
import { uuidv4 } from './k6-utils.js';

export let options = {
    vus: 10, // Number of virtual users
    duration: '15m', // Test duration
};

export default function () {
    let username = `load_test_user_${uuidv4()}`;
    let password = 'Test@1234';

    // Register user
    let registerPayload = JSON.stringify({
        username: username,
        profileName: username,
        password: password,
        email: username+"@mail.com",
        phoneNumber: Math.floor(1000000000 + Math.random() * 9000000000).toString(),
        securityQuestion1: "test",
        securityQuestion2: "test",
        securityQuestion3: "test"
    });
    let registerRes = http.post('http://api.chaosbank.sanjivkannaa.tech/auth/register', registerPayload, {
        headers: { 'Content-Type': 'application/json' }
    });
    check(registerRes, { 'registered successfully': (res) => res.status === 201 });

    // Login user
    let loginPayload = JSON.stringify({
      username: username,
      password: password
    });
    let loginRes = http.post('http://api.chaosbank.sanjivkannaa.tech/auth/login', loginPayload, {
        headers: { 'Content-Type': 'application/json' }
    });
    check(loginRes, { 'logged in successfully': (res) => res.status === 200 });

    let authToken = loginRes.json('jwt');

    // Access dashboard
    let dashboardRes = http.get('http://api.chaosbank.sanjivkannaa.tech/user/dashboard', {
        headers: { Authorization: `Bearer ${authToken}` }
    });
    check(dashboardRes, { 'dashboard loaded': (res) => res.status === 200 });

    // Perform fund transfer
    let transferPayload = JSON.stringify({
      receiverId: '1',
      amount: 100
    });
    let transferRes = http.post('http://api.chaosbank.sanjivkannaa.tech/transaction/transfer', transferPayload, {
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` }
    });
    check(transferRes, { 'funds transferred': (res) => res.status === 200 });

    // Check transaction history
    let historyPayload = JSON.stringify({
      fromDate: "",
      toDate: "",
    });
    let historyRes = http.post('http://api.chaosbank.sanjivkannaa.tech/transaction/transactionHistory', historyPayload, {
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` }
    });
    check(historyRes, { 'transaction history fetched': (res) => res.status === 200 });

    sleep(1);
}
