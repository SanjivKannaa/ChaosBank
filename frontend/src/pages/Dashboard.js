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
    transactions: {
      totalCreditThisMonth: "Fetching...",
      totalDebitThisMonth: "Fetching...",
      totalCreditLastMonth: "Fetching...",
      totalDebitLastMonth: "Fetching...",
      totalCreditLast6Months: "Fetching...",
      totalDebitLast6Months: "Fetching...",
      totalCreditThisYear: "Fetching...",
      totalDebitThisYear: "Fetching...",
    },
  });

  useEffect(() => {
    if (getCookie("token")) {
      axios
        .get(`${process.env.REACT_APP_BACKEND_URL}/user/dashboard`, {
          headers: { Authorization: `Bearer ${getCookie("token")}` },
        })
        .then((response) => {
          setUserData({
            username: response.data.username,
            profileName: response.data.profileName,
            phoneNumber: response.data.phoneNumber,
            email: response.data.email,
            balance: response.data.balance,
            transactions: {
              totalCreditThisMonth: response.data.totalCreditThisMonth,
              totalDebitThisMonth: response.data.totalDebitThisMonth,
              totalCreditLastMonth: response.data.totalCreditLastMonth,
              totalDebitLastMonth: response.data.totalDebitLastMonth,
              totalCreditLast6Months: response.data.totalCreditLast6Months,
              totalDebitLast6Months: response.data.totalDebitLast6Months,
              totalCreditThisYear: response.data.totalCreditThisYear,
              totalDebitThisYear: response.data.totalDebitThisYear,
            },
          });
          console.log(response.data);
        })
        .catch(() => {
          setUserData({ ...userData, username: "Error fetching data" });
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
          <h1>Account Number: {userData.username}</h1>
          <h1>Phone Number: {userData.phoneNumber}</h1>
          <h1>Email: {userData.email}</h1>
        </div>
        <div className={styles.div1right}>
          <h1>ACCOUNT BALANCE</h1>
          <p className={styles.balance}>₹ {userData.balance}</p>
        </div>
      </div>
      <div className={styles.div2}>
        <h2>Transaction Summary</h2>
        <table className={styles.transactionTable}>
          <thead>
            <tr>
              <th>Period</th>
              <th>Credit (₹)</th>
              <th>Debit (₹)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>This Month</td>
              <td>{userData.transactions.totalCreditThisMonth}</td>
              <td>{userData.transactions.totalDebitThisMonth}</td>
            </tr>
            <tr>
              <td>Last Month</td>
              <td>{userData.transactions.totalCreditLastMonth}</td>
              <td>{userData.transactions.totalDebitLastMonth}</td>
            </tr>
            <tr>
              <td>Last 6 Months</td>
              <td>{userData.transactions.totalCreditLast6Months}</td>
              <td>{userData.transactions.totalDebitLast6Months}</td>
            </tr>
            <tr>
              <td>This Year</td>
              <td>{userData.transactions.totalCreditThisYear}</td>
              <td>{userData.transactions.totalDebitThisYear}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <Footer />
    </div>
  );
}

export default Dashboard;
