import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
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
  const [filterType, setFilterType] = useState("date");
  const [lastX, setLastX] = useState(10);

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  };

  useEffect(() => {
    if (getCookie("token")) {
      axios
        .get(`${process.env.REACT_APP_BACKEND_URL}/misc/getUserIdFromUsername`, {
          headers: { Authorization: `Bearer ${getCookie("token")}` },
        })
        .then((response) => {
          setUserId(response.data.userId);
        })
        .catch(() => {
          setUserId("");
        });
    }
  }, []);

  const fetchTransactions = () => {
    setLoading(true);
    setError(null);
    const token = getCookie("token");

    if (!token) {
      navigate("/login");
      return;
    }

    let requestBody = {};
    let apiEndpoint = `${process.env.REACT_APP_BACKEND_URL}/transaction/transactionHistory`;

    if (filterType === "date") {
      requestBody = { ...(fromDate && { fromDate }), ...(toDate && { toDate }) };
    } else {
      apiEndpoint = `${process.env.REACT_APP_BACKEND_URL}/transaction/lastTransactions`;
      requestBody = { limit: lastX };
    }

    axios
      .post(apiEndpoint, requestBody, {
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
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

  useEffect(() => {
    fetchTransactions();
  }, []); //  fetchTransactions only once initially. Subsequent fetches are triggered by the button.

  const totalCredit = transactions.reduce(
    (acc, transaction) => (transaction.receiver.includes(userId) ? acc + transaction.amount : acc),
    0
  );

  const totalDebit = transactions.reduce(
    (acc, transaction) => (transaction.sender.includes(userId) ? acc + transaction.amount : acc),
    0
  );

  return (
    <div style={{ fontFamily: 'Arial, sans-serif' }}>
      <Header />
      <QuickLinks />
      <div
        style={{
          padding: "30px",
          maxWidth: "900px",
          margin: "auto",
          backgroundColor: "#f5f5f5", // Light grey background
          borderRadius: "10px",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          textAlign: "center",
        }}
      >
        <h2 style={{ marginBottom: "20px", color: "#333", fontSize: "28px", fontWeight: '600' }}>Transaction Summary</h2>

        {/* Filter Section */}
        <div style={{ display: "flex", flexDirection: "column", gap: "15px", alignItems: "center" }}>
          <div style={{marginBottom: '10px'}}>
            <label style={{ fontWeight: "bold", marginRight: "10px", fontSize: '16px'}}>Filter By:</label>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              style={{
                padding: "10px",
                borderRadius: "5px",
                border: "1px solid #ccc",
                cursor: "pointer",
                backgroundColor: "#fff",
                fontSize: '16px',
              }}
            >
              <option value="date">Date Range</option>
              <option value="lastX">Last X Transactions</option>
            </select>
          </div>

          {filterType === "date" ? (
            <div style={{ display: 'flex', gap: '10px', marginBottom: '15px'}}>
              <input
                type="date"
                value={fromDate}
                onChange={(e) => setFromDate(e.target.value)}
                style={{
                  padding: "10px",
                  borderRadius: "5px",
                  border: "1px solid #ccc",
                  fontSize: '16px',
                }}
              />
              <input
                type="date"
                value={toDate}
                onChange={(e) => setToDate(e.target.value)}
                style={{
                  padding: "10px",
                  borderRadius: "5px",
                  border: "1px solid #ccc",
                  fontSize: '16px',
                }}
              />
            </div>
          ) : (
            <div style={{marginBottom: '15px'}}>
              <input
                type="number"
                value={lastX}
                onChange={(e) => setLastX(parseInt(e.target.value, 10) || 10)}  // Ensure it's a number
                min="1"
                style={{
                  padding: "10px",
                  borderRadius: "5px",
                  border: "1px solid #ccc",
                  width: "60px",
                  fontSize: '16px',
                  marginRight: '8px'
                }}
              />
              <span style={{ fontSize: '16px' }}>transactions</span>
            </div>
          )}

          <button
            onClick={fetchTransactions}
            style={{
              backgroundColor: "#4CAF50", // Green color
              color: "#fff",
              padding: "12px 20px",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              fontSize: "18px",
              transition: "background-color 0.3s ease",
            }}
            onMouseOver={(e) => (e.target.style.backgroundColor = "#45a049")} // Darker green on hover
            onMouseOut={(e) => (e.target.style.backgroundColor = "#4CAF50")}
          >
            Fetch Transactions
          </button>
        </div>


        {/* Transactions Table */}
        {loading ? (
          <p style={{ marginTop: "20px", fontSize: "18px" }}>Loading transactions...</p>
        ) : error ? (
          <p style={{ marginTop: "20px", color: "red", fontSize: "18px" }}>{error}</p>
        ) : transactions.length === 0 ? (
          <p style={{ marginTop: "20px", fontSize: "18px" }}>No transactions found.</p>
        ) : (
          <>
            <div style={{ overflowX: 'auto' }}>
              <table
                style={{
                  width: "100%",
                  marginTop: "20px",
                  borderCollapse: "collapse",
                  borderRadius: "10px",
                  overflow: "hidden", // Ensures the border-radius applies to the table
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                }}
              >
                <thead>
                  <tr style={{ backgroundColor: "#3498db", color: "#fff", textAlign: "left" }}> {/* Blue header */}
                    <th style={{ padding: "12px 15px", fontSize: '16px' }}>Transaction ID</th>
                    <th style={{ padding: "12px 15px", fontSize: '16px' }}>Sender</th>
                    <th style={{ padding: "12px 15px", fontSize: '16px' }}>Receiver</th>
                    <th style={{ padding: "12px 15px", fontSize: '16px' }}>Amount (₹)</th>
                    <th style={{ padding: "12px 15px", fontSize: '16px' }}>Timestamp</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map((transaction, index) => (
                    <tr key={transaction.transaction_id} style={{ backgroundColor: index % 2 ? "#f9f9f9" : "#fff" }}>
                      <td style={{ padding: "12px 15px", fontSize: '16px' }}>{transaction.transaction_id}</td>
                      <td style={{ padding: "12px 15px", fontSize: '16px' }}>{transaction.sender}</td>
                      <td style={{ padding: "12px 15px", fontSize: '16px' }}>{transaction.receiver}</td>
                      <td style={{ padding: "12px 15px", fontWeight: "bold", fontSize: '16px', color: transaction.receiver.includes(userId) ? "green" : "red" }}>
                        ₹{transaction.amount}
                      </td>
                      <td style={{ padding: "12px 15px", fontSize: '16px' }}>{transaction.timestamp}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Total Summary */}
            <div style={{ marginTop: "20px", fontSize: "18px", fontWeight: "bold" , display: "flex", justifyContent: "space-between"}}>
              <p style={{color: 'green'}}>Total Credit: ₹{totalCredit.toFixed(2)}</p>
              <p style={{color: 'red'}}>Total Debit: ₹{totalDebit.toFixed(2)}</p>
            </div>
          </>
        )}
      </div>
      <Footer />
    </div>
  );
}

export default TransactionHistory;
