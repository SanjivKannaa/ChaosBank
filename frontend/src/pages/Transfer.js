import { useNavigate } from "react-router-dom";
import { useState } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import styles from "../css/transfer.module.css";
import QuickLinks from "../components/QuickLinks";
import axios from "axios";
import Swal from "sweetalert2";

function Transfer() {
  const navigate = useNavigate();
  const [receiverId, setReceiverId] = useState("");
  const [amount, setAmount] = useState("");

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  };

  const handleTransfer = async (e) => {
    e.preventDefault();

    if (!receiverId || !amount || amount <= 0) {
      Swal.fire({
        title: "Error",
        text: "Please enter a valid receiverId and amount.",
        icon: "error",
        confirmButtonColor: "#d33",
      });
      return;
    }

    const token = getCookie("token");
    if (!token) {
      navigate("/login");
      return;
    }

    try {
      const response = await axios.get(
        `http://localhost:5000/getProfileNameFromUserId?userId=${receiverId}`
      );
      const receiverName = response.data.profileName;

      const confirmTransfer = await Swal.fire({
        title: "Confirm Transfer",
        text: `Transfer ₹${amount} to ${receiverName} (UserID: ${receiverId})?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, Transfer",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#28a745",
        cancelButtonColor: "#d33",
      });

      if (!confirmTransfer.isConfirmed) return;

      await axios.post(
        "http://localhost:5000/transfer",
        { receiverId, amount },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      Swal.fire({
        title: "Success!",
        text: "Transfer successful!",
        icon: "success",
        confirmButtonColor: "#28a745",
      });

      setReceiverId("");
      setAmount("");
    } catch (error) {
      if (error.response?.status === 404) {
        Swal.fire({
          title: "Error",
          text: "Account Not Found",
          icon: "error",
          confirmButtonColor: "#d33",
        });
      } else {
        Swal.fire({
          title: "Error",
          text: error.response?.data?.error || "Transfer failed. Please try again.",
          icon: "error",
          confirmButtonColor: "#d33",
        });
      }
    }
  };

  return (
    <div>
      <Header />
      <QuickLinks />
      <div className={styles.div1}></div>
      <div className={styles.div2}>
        <h2>Transfer Money</h2>
        <form className={styles.transferForm} onSubmit={handleTransfer}>
          <label>ReceiverId Username:</label>
          <input
            type="text"
            value={receiverId}
            onChange={(e) => setReceiverId(e.target.value)}
            placeholder="Enter receiverId's username"
            required
          />

          <label>Amount (₹):</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Enter amount"
            required
          />

          <button type="submit" className={styles.transferButton}>
            Transfer
          </button>
        </form>
      </div>
      <div className={styles.div1}></div>
      <Footer />
    </div>
  );
}

export default Transfer;
