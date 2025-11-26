-- Accounts table
CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    owner VARCHAR(50) NOT NULL,
    balance DECIMAL(10,2) NOT NULL CHECK (balance >= 0)
);

-- Transactions table
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    account_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
