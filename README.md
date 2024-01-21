# legendary-robot

## Task1 – Monitoring System Design

Scenario: Implement a robust system to monitor USDT transfer to the ZERO address
(https://etherscan.io/address/0x0000000000000000000000000000000000000000) on Ethereum
mainnet. In case the transfer happens, our team would like to be notified to take appropriate
actions.
Design the system, such that:
- Once the token transfer event happens, our team gets notified within 2 minutes.
- Resilient – No downtime
- Cost-effective
- Can easily be modified to add more token transfer monitorings (e.g. to other addresses,
or monitor other token addresses)

### Q1: Please provide technical details (can be as in-depth as pseudo-code and/or an
overview of the algorithm or approaches used), including the analysis of why the design
is good, compared to other possible designs.

### Q2: Please also state the analysis of potential loopholes / trade-offs that the design you
proposed may have (that may cause the monitoring to not function properly).


## Task 2 – Reward Distribution

### Q3: Write a Python3 code that calculates how much each user should receive the reward.
Please include any test cases to test the functionality, including normal and edge cases
as well.

Implement the Python function according to the format below:
def calculate_reward(events: list[tuple[str,int]]) -> dict[str, float]:
raise NotImplemented() 

#### TODO

Problem statement:
We have 10,000 USDT to be distributed to our users who use our lending protocol during the
timestamp 0 to 3600 (1 hour duration). The reward distribution algorithm is such that the 1000
tokens are distributed at the rate of ~2.778 USDT / sec, where at each point in time, the tokens
will be distributed proportionally based on the total number of user’s shares.
Each user’s action can either be:

1. Increase shares by XX, or
2. Decrease shares by YY (user’s shares can never be negative)

Example:
● User action events – format will be a list of tuples of (user, timestamp, share_adjust):
○ [ (“A”, 0, 2), (“B”, 2, 1), (“A”, 10, -1) ]
The above example list of events means that
- User A increases 2 shares at time t=0
- User B increases 1 share at time t=2
- User A decreases 1 share at time t=10

So,
- Between time t=0 & t=1, only user A is getting the rewards → A gets 2.778 USDT
- Between time t=1 & t=10, A has 2 shares, while B has 1 share
→ A gets 2⁄3 of what’s distributed, and B gets 1⁄3 of what’s distributed
→ A gets 16.667 USDT and B gets 8.333 USDT
- Between time t=10 & t=3600, A and B has 1 share each
→ A gets 1⁄2 of what’s distributed, and B gets 1⁄2 of what’s distributed
→ A and B each gets 4986.111 USDT
So, in total, A gets 5005.556 USDT and B gets 4994.444 USDT
Expected Output: a dictionary of {“A” : 5005.556, “B” : 4994.444 }