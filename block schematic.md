# Block Schematic

## Modules

1. Profile Creation
2. Edit Profile
3. Deposit
4. Withdrawal
5. Transfer
6. Last 'x' Transactions
7. Transaction history for given period

## 1. Create Profile

- Prompt template
  - Username (string(15))
  - Date-of-birth (dd-mm-yyyy)
  - Address
    - Door/plot no. (string(5))
    - street name (string(15))
    - area (string(15))
    - city (predefined options)
    - state (predefined options)
    - country (predefined options)
    - pin (6 digit number)
  - Mobile number (country code, 10 digit number)
  - Aadhar number (12 digits)
  - PAN number (string(10))
- Verify user Identity
  - Get proof of DOB (pdf/png/jpeg/jpg)
  - Get proof of address (pdf/png/jpeg/jpg)
  - Get proof of Aadhar (pdf/png/jpeg/jpg)
  - Get proof of PAN (pdf/png/jpeg/jpg)
  - Mobile number verification
    - send OTP to given mobile number
    - receive OTP from user
    - if sent OTP is same as received OTP accept, else reject
- Create entry for user in Database and create account number
- Send notification (Sms/email) to user with account number, etc

## 2. Edit Profile

## 3. Deposit

## 4. Withdrawal

## 5. Transfer

- Prompt Template
  - Sender Account Number (automatically detected)
  - Receiver Account Number (int)
  - Amount (int)
- Confirm Receiver
  - Retrieve information of receiver account details (username) and get confirmation user
- Validate Transaction
  - check if the amount is > 0
  - check if the sender has sufficient balance
  - check if the receiver is a valid profile
- Perform transaction
  - Make database entry to transactions table
- Display transaction result (success/failure) to user

## 6. Last 'x' Transactions

- Get the value of x from user (hardcoded buttons/variable x)
- Retrieve data from Database
- Display the result to user

## 7. Transaction for given period

- Get the value of fromDate and toDate from user
- Retrieve data from Database
- Display the result to user
