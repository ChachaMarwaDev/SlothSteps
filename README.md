# SlothSteps
A repository documenting my journey through Sloth Bytes weekly challenges. Every step, no matter how small, is growth. Here, I share solutions, learn from feedback, and prove that persistence beats speed. Open to all — no discrimination, just learning together

<details>
<summary><b>Big O Time Complexity</b><summary>
Big O describes **how long code takes to run as the input grows larger**.

Think of it like this: if you have a list of 10 items vs 1,000,000 items — how does that affect your code's speed?

---

**O(1) — Constant**
No matter how big the list, it takes the same time.
python
my_list[0]  # Always just grabs the first item

**O(n) — Linear**
Bigger list = proportionally more time.
python
for item in my_list:  # Loop through every item
    print(item)

**O(n²) — Quadratic**
A loop inside a loop. Gets slow fast.
python
for i in my_list:
    for j in my_list:  # For every item, loop again
        print(i, j)

**O(log n) — Logarithmic**
Each step cuts the problem in half. Very efficient.
Binary search is the classic example — you guess the middle, eliminate half, repeat.

---

### The simple mental model:

| Big O | Plain English |
|---|---|
| O(1) | Instant, always |
| O(log n) | Fast, gets barely slower |
| O(n) | Slows down evenly |
| O(n²) | Gets painful quickly |

The point isn't to memorize formulas — it's to ask yourself: "if my input doubles, what happens to my code?" That instinct is what interviewers are really testing