import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import styles from "../css/dashboard.module.css";
import QuickLinks from "../components/QuickLinks";
import axios from "axios";

function Dashboard() {
  const navigate = useNavigate();

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  };

  const [userData, setUserData] = useState({
    username: "Fetching...",
    profileName: "Fetching...",
    phoneNumber: "Fetching...",
    email: "Fetching...",
    balance: "Fetching...",
    accountNumber: "Fetching...",
    transactions: [],
  });

  useEffect(() => {
    if (getCookie("token")) {
      axios
        .get(`${process.env.REACT_APP_BACKEND_URL}/user/dashboard`, {
          headers: { Authorization: `Bearer ${getCookie("token")}` },
        })
        .then((response) => {
          setUserData((prevData) => ({
            ...prevData,
            username: response.data.username,
            profileName: response.data.profileName,
            phoneNumber: response.data.phoneNumber,
            email: response.data.email,
            balance: response.data.balance,
            accountNumber: "RB" + String(response.data.accountNumber).padStart(7, "0"),
          }));
        })
        .catch(() => {
          setUserData({ ...userData, username: "Error fetching data" });
        });

      axios
        .get(`${process.env.REACT_APP_BACKEND_URL}/transaction/lastTenTransactions`, {
          headers: { Authorization: `Bearer ${getCookie("token")}` },
        })
        .then((response) => {
          console.log(response.data);
          setUserData((prevData) => ({ ...prevData, transactions: response.data || [] }));
        })
        .catch(() => {
          setUserData((prevData) => ({ ...prevData, transactions: [] }));
        });
    } else {
      navigate("/login");
    }
  }, []);

  return (
    <div>
      <Header />
      <QuickLinks />
      <div className={styles.div1}>
        <div className={styles.div1left}>
          <h1>Profile Name: {userData.profileName}</h1>
          <h1>Account Number: {userData.accountNumber}</h1>
          <h1>Phone Number: {userData.phoneNumber}</h1>
          <h1>Email: {userData.email}</h1>
        </div>
        <div className={styles.div1right}>
          <h1>ACCOUNT BALANCE</h1>
          <p className={styles.balance}>₹ {userData.balance}</p>
        </div>
      </div>

      <div className={styles.div2}>
        <h2>Recent Transactions</h2>
        {userData.transactions.length === 0 ? (
          <p>No recent transactions found.</p>
        ) : (
          <table className={styles.transactionTable}>
            <thead>
              <tr>
                <th>Transaction ID</th>
                <th>Sender</th>
                <th>Receiver</th>
                <th>Amount (₹)</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {userData.transactions.map((transaction) => (
                <tr key={transaction.transId}>
                  <td>{transaction.transId}</td>
                  <td>{transaction.sender}</td>
                  <td>{transaction.receiver}</td>
                  <td>₹{transaction.amount}</td>
                  <td>{transaction.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <Footer />
    </div>
  );
}

export default Dashboard;