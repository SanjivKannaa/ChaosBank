import { useNavigate } from "react-router-dom";
import { useState } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import styles from "../css/transfer.module.css";
import QuickLinks from "../components/QuickLinks";
import axios from "axios";
import Swal from "sweetalert2";


function Deposit() {
  const navigate = useNavigate();
  const [amount, setAmount] = useState("");

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  };

  const handleTransfer = async (e) => {
    e.preventDefault();

    if (!amount || amount <= 0) {
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
      const confirmTransfer = await Swal.fire({
        title: "Confirm Transfer",
        text: `Deposit ₹${amount} to Account?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes, Transfer",
        cancelButtonText: "Cancel",
        confirmButtonColor: "#28a745",
        cancelButtonColor: "#d33",
      });

      if (!confirmTransfer.isConfirmed) return;

      await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/transaction/deposit`,
        { amount },
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
        <h2>Deposit Money</h2>
        <form className={styles.transferForm} onSubmit={handleTransfer}>
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

export default Deposit;
