import random

# Simulate two participant databases
participants = {
    "DB1": {"accounts": {"A": 1000}},
    "DB2": {"accounts": {"B": 500}}
}

# Each participant can prepare a transaction
def prepare_transaction(participant, transaction):
    print(f"{participant} preparing transaction...")
    # Simulate a check: fail if not enough funds
    account_id = transaction["account_id"]
    change = transaction["change"]
    if participant == "DB1" and account_id == "A" and participants[participant]["accounts"][account_id] + change < 0:
        print(f"{participant} votes NO!")
        return False
    print(f"{participant} votes YES")
    return True

# Each participant applies the transaction
def commit_transaction(participant, transaction):
    account_id = transaction["account_id"]
    change = transaction["change"]
    participants[participant]["accounts"][account_id] += change
    print(f"{participant} committed transaction!")

# Coordinator for 2PC
def two_phase_commit(transactions):
    # Phase 1: Prepare
    votes = []
    for participant, tx in transactions.items():
        vote = prepare_transaction(participant, tx)
        votes.append(vote)

    # Phase 2: Commit or Abort
    if all(votes):
        print("All participants voted YES → committing transaction...")
        for participant, tx in transactions.items():
            commit_transaction(participant, tx)
        print("Transaction committed across all participants!\n")
    else:
        print("At least one participant voted NO → aborting transaction.")
        print("No changes applied.\n")

# --- Example 1: Successful distributed transaction ---
transactions1 = {
    "DB1": {"account_id": "A", "change": -300},
    "DB2": {"account_id": "B", "change": 300}
}

two_phase_commit(transactions1)

# --- Example 2: Failing distributed transaction ---
transactions2 = {
    "DB1": {"account_id": "A", "change": -2000},  # Not enough funds
    "DB2": {"account_id": "B", "change": 2000}
}

two_phase_commit(transactions2)

print("Final DB states:", participants)
