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
  const [userName, setUserName] = useState("");
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
        .get(
          `${process.env.REACT_APP_BACKEND_URL}/misc/getUserIdFromUsername`,
          {
            headers: { Authorization: `Bearer ${getCookie("token")}` },
          }
        )
        .then((response) => {
          setUserId(response.data.userId);
        })
        .catch(() => {
          setUserId("");
        });
    }

    if (getCookie("token")) {
      axios
        .get(
          `${process.env.REACT_APP_BACKEND_URL}/misc/getUsername`,
          {
            headers: { Authorization: `Bearer ${getCookie("token")}` },
          }
        )
        .then((response) => {
          setUserName(response.data.username);
        })
        .catch(() => {
          setUserName("");
        }
      );
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
      requestBody = {
        ...(fromDate && { fromDate }),
        ...(toDate && { toDate }),
      };
    } else {
      apiEndpoint = `${process.env.REACT_APP_BACKEND_URL}/transaction/lastXTransactions`;
      requestBody = { limit: lastX };
    }

    axios
      .post(apiEndpoint, requestBody, {
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

  useEffect(() => {
    fetchTransactions();
  }, []);

  const totalCredit = transactions.reduce(
    (acc, transaction) =>
      transaction.receiver.includes(userId) ? acc + transaction.amount : acc,
    0
  );

  const totalDebit = transactions.reduce(
    (acc, transaction) =>
      transaction.sender.includes(userId) ? acc + transaction.amount : acc,
    0
  );

  return (
    <div>
      <Header />
      <QuickLinks />
      <div
        style={{
          padding: "30px",
          maxWidth: "900px",
          margin: "auto",
          backgroundColor: "#f9f9f9",
          borderRadius: "10px",
          boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
          textAlign: "center",
        }}
      >
        <h2 style={{ marginBottom: "20px", color: "#333", fontSize: "24px" }}>
          Transaction Summary
        </h2>

        {/* Filter Section */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "15px",
            alignItems: "center",
          }}
        >
          <div>
            <label style={{ fontWeight: "bold", marginRight: "10px" }}>
              Filter By:
            </label>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              style={{
                padding: "8px",
                borderRadius: "5px",
                border: "1px solid #ccc",
                cursor: "pointer",
                backgroundColor: "#fff",
              }}
            >
              <option value="date">Date Range</option>
              <option value="lastX">Last X Transactions</option>
            </select>
          </div>

          {filterType === "date" ? (
            <div>
              <input
                type="date"
                value={fromDate}
                onChange={(e) => setFromDate(e.target.value)}
                style={{
                  padding: "8px",
                  borderRadius: "5px",
                  border: "1px solid #ccc",
                  marginRight: "10px",
                }}
              />
              <input
                type="date"
                value={toDate}
                onChange={(e) => setToDate(e.target.value)}
                style={{
                  padding: "8px",
                  borderRadius: "5px",
                  border: "1px solid #ccc",
                }}
              />
            </div>
          ) : (
            <div>
              <input
                type="number"
                value={lastX}
                onChange={(e) => setLastX(e.target.value)}
                min="1"
                style={{
                  padding: "8px",
                  borderRadius: "5px",
                  border: "1px solid #ccc",
                  width: "60px",
                }}
              />
              <span style={{ marginLeft: "10px" }}>transactions</span>
            </div>
          )}

          <button
            onClick={fetchTransactions}
            style={{
              backgroundColor: "#007bff",
              color: "#fff",
              padding: "10px 15px",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              fontSize: "16px",
              marginTop: "10px",
              transition: "0.3s",
            }}
            onMouseOver={(e) => (e.target.style.backgroundColor = "#0056b3")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "#007bff")}
          >
            Fetch Transactions
          </button>
        </div>

        {/* Transactions Table */}
        {loading ? (
          <p style={{ marginTop: "20px", fontSize: "18px" }}>
            Loading transactions...
          </p>
        ) : error ? (
          <p style={{ marginTop: "20px", color: "red", fontSize: "18px" }}>
            {error}
          </p>
        ) : transactions.length === 0 ? (
          <p style={{ marginTop: "20px", fontSize: "18px" }}>
            No transactions found.
          </p>
        ) : (
          <>
            <table
              style={{
                width: "100%",
                marginTop: "20px",
                borderCollapse: "collapse",
                borderRadius: "10px",
                overflow: "hidden",
              }}
            >
              <thead>
                <tr
                  style={{
                    backgroundColor: "#007bff",
                    color: "#fff",
                    textAlign: "left",
                  }}
                >
                  <th style={{ padding: "10px" }}>Transaction ID</th>
                  <th style={{ padding: "10px" }}>Sender</th>
                  <th style={{ padding: "10px" }}>Receiver</th>
                  <th style={{ padding: "10px" }}>Amount (₹)</th>
                  <th style={{ padding: "10px" }}>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((transaction, index) => {
                  const isCredit = transaction.receiver === userName;
                  return (
                    <tr
                      key={transaction.transaction_id}
                      style={{
                        backgroundColor: index % 2 ? "#f2f2f2" : "#fff",
                      }}
                    >
                      <td style={{ padding: "10px" }}>
                        {transaction.transaction_id}
                      </td>
                      <td style={{ padding: "10px" }}>{transaction.sender}</td>
                      <td style={{ padding: "10px" }}>
                        {transaction.receiver}
                      </td>
                      <td
                        style={{
                          padding: "10px",
                          fontWeight: "bold",
                          color: isCredit ? "green" : "red",
                        }}
                      >
                        {isCredit ? "+" : "-"}₹{transaction.amount}
                      </td>
                      <td style={{ padding: "10px" }}>
                        {transaction.timestamp}
                      </td>
                    </tr>
                  );
                })}
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