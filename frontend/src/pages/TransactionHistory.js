import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import styles from "../css/transactionHistory.module.css";
import QuickLinks from "../components/QuickLinks";
import axios from "axios";

function TransactionHistory() {
  const navigate = useNavigate();
  const [transactions, setTransactions] = useState([]);
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userId, setUserId] = useState("");

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  };

  useEffect(() => {
    const token = getCookie("token");

    if (!token) {
      navigate("/login");
      return;
    }

    const fetchUserIdAndSummary = async () => {
      try {
        const [userIdRes] = await Promise.all([
          axios.get(`${process.env.REACT_APP_BACKEND_URL}/misc/getUserIdFromUsername`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
          axios.get(`${process.env.REACT_APP_BACKEND_URL}/transaction/summary`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ]);

        setUserId(userIdRes.data.userId);
      } catch (err) {
        setError("Failed to fetch user ID or transaction summary");
      }
    };

    fetchUserIdAndSummary();
    fetchTransactions();
  }, []);

  const fetchTransactions = () => {
    setLoading(true);
    setError(null);

    const token = getCookie("token");

    const requestBody = {
      ...(fromDate && { fromDate }),
      ...(toDate && { toDate }),
    };

    axios
      .post(`${process.env.REACT_APP_BACKEND_URL}/transaction/transactionHistory`, requestBody, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setTransactions(response.data || []);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load transactions.");
        setLoading(false);
      });
  };

  return (
    <div>
      <Header />
      <QuickLinks />
      <div className={styles.div2}>
        <h2>Transaction History</h2>
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
          <>
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
                    <td
                      className={
                        transaction.receiver.includes(userId)
                          ? styles.credit
                          : styles.debit
                      }
                    >
                      ₹{transaction.amount}
                    </td>
                    <td>{transaction.timestamp}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </div>
      <Footer />
    </div>
  );
}

export default TransactionHistory;