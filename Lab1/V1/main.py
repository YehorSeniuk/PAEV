import random
from crypto import generate_rsa_keys, vote, count_votes

candidates = ['Кандидат_А', 'Кандидат_Б', 'Кандидат_В', 'Кандидат_Г']

cvk_pub_key, cvk_priv_key = generate_rsa_keys()

voters = {}
for i in range(128):
    voters[f'voter_{i + 1}'] = generate_rsa_keys()

registered_voters = set(voters.keys())

voted = set()

votes = []
for voter in voters.keys():
    candidate = random.choice(candidates)
    pub_key_voter, priv_key_voter = voters[voter]

    encrypted_vote, signature, key = vote(voter, candidate, cvk_priv_key, cvk_pub_key, registered_voters, voted)

    votes.append((encrypted_vote, signature, key))

results = count_votes(votes, cvk_priv_key, cvk_pub_key, candidates)

print("Результати голосування:")
for candidate, count in results.items():
    print(f"{candidate}: {count} голосів")
