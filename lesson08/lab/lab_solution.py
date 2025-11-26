import time

# ===================================================================
# PART 1: RELATIONAL MODEL (Students add 3 lines)
# ===================================================================

def relational_model():
    """Relational approach - data in separate tables"""
    
    # Pre-built data structures (no student coding needed)
    users = {
        1: {"name": "Alice", "email": "alice@example.com"},
        2: {"name": "Bob", "email": "bob@example.com"},
        3: {"name": "Charlie", "email": "charlie@example.com"}
    }
    
    posts = [
        {"user_id": 1, "content": "Hello world!"},
        {"user_id": 2, "content": "Nice photo!"},
        {"user_id": 1, "content": "Learning Python!"}
    ]
    
    friendships = [
        {"user1_id": 1, "user2_id": 2},  # Alice-Bob
        {"user1_id": 1, "user2_id": 3}   # Alice-Charlie
    ]
    
    print("=== RELATIONAL MODEL ===")
    
    # TASK: Get all posts by Alice (user_id = 1)
    alice_posts = [p["content"] for p in posts if p["user_id"] == 1]

    print(f"Alice's posts: {len(alice_posts)}")
    
    # TASK: Find Alice's friends
    friend_ids = [
        f["user2_id"] for f in friendships if f["user1_id"] == 1
    ]
    alice_friends = [users[f]["name"] for f in friend_ids]

    print(f"Alice's friends: {alice_friends}")
    return alice_posts, alice_friends

# ===================================================================
# PART 2: DOCUMENT MODEL (Students add 3 lines)
# ===================================================================

def document_model():
    """Document approach - nested data in user documents"""
    
    users = {
        "alice": {
            "name": "Alice",
            "email": "alice@example.com",
            "posts": [
                {"content": "Hello world!"},
                {"content": "Learning Python!"}
            ],
            "friends": [
                {"name": "Bob", "email": "bob@example.com"},
                {"name": "Charlie", "email": "charlie@example.com"}
            ]
        },
        "bob": {
            "name": "Bob",
            "email": "bob@example.com",
            "posts": [{"content": "Nice photo!"}],
            "friends": [{"name": "Alice", "email": "alice@example.com"}]
        },
        "charlie": {
            "name": "Charlie",
            "email": "charlie@example.com",
            "posts": [],
            "friends": [{"name": "Alice", "email": "alice@example.com"}]
        }
    }
    
    print("\n=== DOCUMENT MODEL ===")
    
    # TASK: Get Alice's posts
    alice_posts = users["alice"]["posts"]

    print(f"Alice's posts: {len(alice_posts) if alice_posts else 0}")
    
    # TASK: Get Alice's friend names
    alice_friends = [f["name"] for f in users["alice"]["friends"]]

    print(f"Alice's friends: {alice_friends}")
    return alice_posts, alice_friends


# ===================================================================
# PART 3: GRAPH MODEL (Students add 4 lines)
# ===================================================================

def graph_model():
    """Graph approach - connections between nodes"""
    
    nodes = {
        "alice": {"name": "Alice", "email": "alice@example.com"},
        "bob": {"name": "Bob", "email": "bob@example.com"},
        "charlie": {"name": "Charlie", "email": "charlie@example.com"}
    }
    
    connections = {
        "alice": ["bob", "charlie"],
        "bob": ["alice"],
        "charlie": ["alice"]
    }
    
    posts = {
        "alice": ["Hello world!", "Learning Python!"],
        "bob": ["Nice photo!"],
        "charlie": []
    }
    
    print("\n=== GRAPH MODEL ===")
    
    # TASK: Get Alice's posts
    alice_posts = posts["alice"]

    print(f"Alice's posts: {len(alice_posts)}")
    
    # TASK: Find mutual friends between Alice and Bob
    alice_connections = set(connections["alice"])
    bob_connections = set(connections["bob"])
    mutual_friends = list(alice_connections & bob_connections)

    print(f"Mutual friends of Alice and Bob: {mutual_friends}")
    return alice_posts, mutual_friends


# ===================================================================
# COMPARISON RUNNER
# ===================================================================

def compare_models():
    print("DATA MODEL COMPARISON LAB")
    print("=" * 50)
    
    start_time = time.time()
    rel_posts, rel_friends = relational_model()
    rel_time = time.time() - start_time
    
    start_time = time.time()
    doc_posts, doc_friends = document_model()
    doc_time = time.time() - start_time
    
    start_time = time.time()
    graph_posts, graph_mutual = graph_model() 
    graph_time = time.time() - start_time
    
    print(f"\n" + "=" * 50)
    print("SUMMARY COMPARISON")
    print("=" * 50)
    print(f"{'Model':<12} {'Code Lines':<12} {'Query Time':<12} {'Best For'}")
    print("-" * 55)
    print(f"{'Relational':<12} {'Medium':<12} {rel_time*1000:.1f}ms{'':<7} {'Complex queries'}")
    print(f"{'Document':<12} {'Simple':<12} {doc_time*1000:.1f}ms{'':<7} {'Nested data'}")
    print(f"{'Graph':<12} {'Medium':<12} {graph_time*1000:.1f}ms{'':<7} {'Relationships'}")


def show_reflection_questions():
    questions = [
        "\nREFLECTION QUESTIONS:",
        "1. Which model required the least code to get Alice's posts?",
        "2. Which model made finding friends easiest?", 
        "3. Which model would be best for a social media app? Why?",
        "4. Which model would be best for a banking system? Why?",
        "5. What happens if you want to add a new field like 'age' to users?"
    ]
    
    for q in questions:
        print(q)


if __name__ == "__main__":
    compare_models()
    show_reflection_questions()
