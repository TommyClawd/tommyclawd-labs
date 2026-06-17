<think>We need to solve the problem "Overall Winner". The problem is straightforward: given N and a string S of length N consisting of characters 'T' and 'A', representing results of N games where each character indicates who won that game (T for Takahashi, A for Aoki). We need to determine the overall winner according to the following rule:

- The overall winner is the player who won more games than the other.
- If they have the same number of wins (i.e., the total counts are equal), then the overall winner is the one who reached that number of wins first during the sequence.

Thus we need to output 'T' if Takahashi is the overall winner, else 'A'.

The problem is essentially the AtCoder problem "Overall Winner" (ABC072 A? Actually something like that). The solution is simple: count the total number of 'T' and 'A'. If count_T > count_A, answer 'T'; if count_A > count_T, answer 'A'; else (counts equal) we need to simulate the games and see which player reaches count_T (which equals count_A) first. Since counts are equal, we need to find the first time the cumulative count of 'T' > cumulative count of 'A' (or the cumulative count of 'A' > cumulative count of 'T')? Actually, the rule: "If they had the same number of wins, the overall winner is the one who reached that number of wins first." Let's parse: Suppose total wins for each player are equal, say k. Then both reached k wins eventually at the end (both have k). However, we need to determine who reached k wins earlier in the sequence. Since at the end both have k, but we need to see which player's cumulative wins reached k earlier. Actually, we need to see which player reached the final total count first. For example, sample 2: N=6, S=ATTATA. Let's compute: total T count = 3, A count = 3. The sequence: positions:
1: A => A:1, T:0
2: T => A:1, T:1
3: T? Wait S[2] = T? Actually S = A T T A T A? No, S = "ATTATA". So characters: 1:A, 2:T, 3:T? Actually "ATTATA": index: 0:A, 1:T, 2:T? Wait "ATTATA": letters: A, T, T, A, T, A? Let's write: A (0), T (1), T (2), A (3), T (4), A (5). Yes, that's correct. So the cumulative counts:
i=1 (A): A=1, T=0.
i=2 (T): A=1, T=1.
i=3 (T): A=1, T=2.
i=4 (A): A=2, T=2.
i=5 (T): A=2, T=3.
i=6 (A): A=3, T=3.
The final counts are both 3. Who reached 3 first? Takahashi reaches 3 at i=5; Aoki reaches 3 at i=6. So Takahashi wins. That matches sample.

Thus the rule: If total counts equal, find the smallest index i where cumulative_T > cumulative_A? Not exactly. Actually we need to find who reaches the final total count first. Since final total count = k, we need to find the index where cumulative_T becomes k (i.e., T's count reaches total_T) and the index where cumulative_A becomes k (i.e., A's count reaches total_A). The player whose index is smaller wins. However, since total_T = total_A = k, we can simply simulate and keep cumulative counts, and when either cumulative_T == total_T or cumulative_A == total_A, we check which occurs first. But we can also just check when cumulative_T > cumulative_A? Not exactly, because at the moment when cumulative_T becomes equal to total_T (k), cumulative_A might be less than k. But the condition cumulative_T > cumulative_A might happen earlier or later. For example, consider S = "TTAA". N=4. total_T=2, total_A=2. Sequence:
i1: T => T=1, A=0.
i2: T => T=2, A=0. At i2, T reaches total_T=2. At this point, A hasn't reached total_A=2. So T wins. Note that at i2, cumulative_T > cumulative_A (2 > 0). So the condition cumulative_T > cumulative_A holds at i2. But is it always the case that the winner is the one who first leads (cumulative_T > cumulative_A) at some point? Let's test with some other sequences. Consider S = "TATA". total_T=2, total_A=2. Sequence:
i1: T => T=1, A=0 (T leads)
i2: A => T=1, A=1 (tie)
i3: T => T=2, A=1 (T leads)
i4: A => T=2, A=2 (tie). Who reaches total count first? T reaches total_T=2 at i3; A reaches total_A=2 at i4. So T wins. The first time cumulative_T > cumulative_A is at i1 (T leads) and also at i3. But the rule is about reaching total count first, not about leading at any point. However, the first lead might not correspond to reaching total count first? Let's try to find a counterexample. Suppose S = "ATTA". total_T=2, total_A=2. Sequence:
i1: A => A=1, T=0 (A leads)
i2: T => A=1, T=1 (tie)
i3: T => A=1, T=2 (T reaches total_T=2 at i3)
i4: A => A=2, T=2 (A reaches total_A=2 at i4). So T wins. The first lead is at i1 (A leads). So the first lead is not the winner. So we cannot just check who leads at any point. Instead, we need to find who reaches total count first.

Simplify: compute total_T = S.count('T'), total_A = N - total_T (or count('A')). If total_T != total_A, answer the one with larger count. If equal, iterate over S, maintain cumulative_T, cumulative_A, and when cumulative_T == total_T (i.e., after we have seen total_T T's), note the index for T; similarly when cumulative_A == total_A, note index for A. Since both will happen at some point (the final index N will satisfy both, but the earlier one determines winner). So we can just iterate and after each character increment the appropriate cumulative count, check if cumulative_T == total_T or cumulative_A == total_A. As soon as either condition is met, we can break and output the corresponding player. Actually we need to check which occurs first. So we can break when we see either condition; whichever we see first is the