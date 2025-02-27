import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import styles from "../css/dashboard.module.css";
import QuickLinks from "../components/QuickLinks";
import axios from "axios";

function TransactionHistory() {
  const navigate = useNavigate();
  const [transactions, setTransactions] = useState([]);
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  };

  const fetchTransactions = () => {
    setLoading(true);
    setError(null);
    const token = getCookie("token");

    if (!token) {
      navigate("/login");
      return;
    }

    const requestBody = {
      ...(fromDate && { fromDate }),
      ...(toDate && { toDate }),
    };

    axios
      .post("http://localhost:5000/transactionHistory", requestBody, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setTransactions(response.data || []);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching transactions:", error);
        setError("Failed to load transactions.");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  return (
    <div>
      <Header />
      <QuickLinks />
      <div className={styles.div2}>
        <h2>Transaction Summary</h2>

        {/* Date Filters */}
        <div className={styles.filterContainer}>
          <div className={styles.filterInputs}>
            <label>From:</label>
            <input
              type="date"
              value={fromDate}
              onChange={(e) => setFromDate(e.target.value)}
            />
            <label>To:</label>
            <input
              type="date"
              value={toDate}
              onChange={(e) => setToDate(e.target.value)}
            />
          </div>
          <button className={styles.filterButton} onClick={fetchTransactions}>
            Filter
          </button>
        </div>

        {loading ? (
          <p>Loading transactions...</p>
        ) : error ? (
          <p className={styles.error}>{error}</p>
        ) : transactions.length === 0 ? (
          <p>No transactions found.</p>
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
              {transactions.map((transaction) => (
                <tr key={transaction.transaction_id}>
                  <td>{transaction.transaction_id}</td>
                  <td>{transaction.sender}</td>
                  <td>{transaction.receiver}</td>
                  <td>{transaction.amount}</td>
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

export default TransactionHistory;
