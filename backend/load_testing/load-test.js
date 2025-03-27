import http from 'k6/http';
import { check, sleep } from 'k6';
import { uuidv4 } from './k6-utils.js';

export let options = {
    vus: 10, // Number of virtual users
    duration: '15m', // Test duration
};

function generateRandomPhoneNumber() {
    return Math.floor(1000000000 + Math.random() * 9000000000).toString();
}

function generateAddress() {
    return {
        door_plot_no: "123",
        street_name_1: "Main Street",
        street_name_2: "Apt 456",
        city: "Pune",
        state: "Maharashtra",
        country: "India",
        pin: generateRandomPinCode()
    };
}

function generateRandomAadhar() {
    return Math.floor(100000000000 + Math.random() * 900000000000).toString();
}

function generateRandomPan() {
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const digits = '0123456789';
    return (
        Array.from({ length: 5 }, () => letters[Math.floor(Math.random() * letters.length)]).join('') +
        Array.from({ length: 4 }, () => digits[Math.floor(Math.random() * digits.length)]).join('') +
        letters[Math.floor(Math.random() * letters.length)]
    );
}

function generateRandomPinCode() {
    return Math.floor(100000 + Math.random() * 900000).toString();
}

export default function () {
    let username = `load_test_user_${uuidv4()}`;
    let password = 'TestTest@1234';

    // Register user
    let registerPayload = JSON.stringify({
        username: username,
        profileName: username,
        password: password,
        email: `${username}@mail.com`,
        phoneNumber: generateRandomPhoneNumber(),
        date_of_birth: "1995-05-15",
        aadhar_number: generateRandomAadhar(),
        pan_number: generateRandomPan(),
        address: generateAddress()
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

    // Deposit
    let depositPayload = JSON.stringify({
      amount: 5000  // Deposit 5000 units
    });
    let depositRes = http.post('http://api.chaosbank.sanjivkannaa.tech/transaction/deposit', depositPayload, {
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` }
    });
    check(depositRes, { 'deposit successful': (res) => res.status === 200 });

    // Withdraw
    let withdrawPayload = JSON.stringify({
      amount: 2000  // Withdraw 2000 units
    });
    let withdrawRes = http.post('http://api.chaosbank.sanjivkannaa.tech/transaction/withdraw', withdrawPayload, {
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` }
    });
    check(withdrawRes, { 'withdrawal successful': (res) => res.status === 200 });

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
