# Immutable approach - create new data instead of modifying
def process_transactions(account_balance, transactions):	
    def apply_transaction(balance, transaction):
        if transaction['type']=='withdraw':
            return max(0, balance - transaction['amount'])
        else: # deposit
            return balance + transaction['amount']

    # Pure function - no side effects
    from functools import reduce
    # Reduce passes the accumulator as the first argument (balance)
    # and each transaction as the second argument
    final_balance = reduce(apply_transaction, transactions, account_balance)
    return final_balance

# Usage - original data never changes 

initial_balance = 1000
transactions = [
	{'type':'withdraw','amount':200},
	{'type':'deposit','amount':100},
	{'type':'withdraw','amount':50}]

new_balance = process_transactions(initial_balance,transactions)
print(f"Original:{initial_balance}, New:{new_balance}")
# initial_balance is still 1000 - immutable!

'''
You could also write:

```
def apply_transaction(balance, transaction):
    b = balance * -1 if transaction['type'] == "withdraw" else balance
    return max(0, balance + b)
```

This would make it clearer that the reducer is only doing one thing and moves the logic to a central place. In fact most FPs don't have return statements.

'''