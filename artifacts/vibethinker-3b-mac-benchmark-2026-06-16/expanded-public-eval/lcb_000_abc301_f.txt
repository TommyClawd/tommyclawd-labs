<think>We need to count number of ways to replace each '?' with any letter (uppercase A-Z, lowercase a-z) i.e., 52 possibilities per '?', such that the resulting string contains no DDoS-type string as a subsequence.

Definition: DDoS-type string: length 4 pattern: positions i1 < i2 < i3 < i4 (not necessarily contiguous, subsequence) such that characters satisfy:

- positions 1,2,4 are uppercase letters (A-Z)
- position 3 is a lowercase letter (a-z)
- first and second characters are equal (i.e., char at i1 = char at i2). So pattern is: X X y Z where X uppercase, y lowercase, Z uppercase, with X same for first two.

Thus we need to avoid any subsequence of this form.

We need to count strings over alphabet (uppercase, lowercase) that avoid this pattern as a subsequence.

Given S with known letters and '?', we need to count assignments that avoid pattern.

Length up to 300k, so need O(N) or O(N * small constant). We need DP.

We can treat this as counting sequences that avoid a forbidden subsequence pattern. This is similar to counting strings that avoid a given pattern as a subsequence (not substring). For a pattern of length 4 with constraints on character categories and equality constraints.

We need to consider the process scanning the string left to right, maintaining state representing the "progress" towards forming a DDoS subsequence. Since pattern has constraints: we need to track possible partial matches.

But because pattern includes equality between first two characters, we need to consider that the first two characters are same uppercase letter X. So the pattern is: pick an uppercase letter X, then later another same uppercase X (must be after first), then a lowercase y (any lowercase?), then an uppercase Z (any uppercase, possibly equal to X or not). Actually constraints: first and second characters are equal uppercase letters; third is any lowercase; fourth is any uppercase (no relation to others). So pattern is: choose an uppercase X, then later same X, then any lowercase y, then any uppercase Z.

Thus to have a DDoS subsequence, we need to find indices i<j<k<l such that S[i]=S[j]=X uppercase, S[k]=y lowercase, S[l]=Z uppercase.

Thus it's like a pattern with constraints: two equal uppercase letters, then a lowercase, then an uppercase.

Goal: avoid any such subsequence.

We can think of DP that tracks the "state" of the longest prefix of the pattern we can match as a subsequence given the processed prefix, but due to equality constraints it's a bit more complex.

One approach: treat each possible uppercase letter X separately? There are 26 possibilities, maybe DP per letter? But N up to 3e5, 26 factor okay.

We can think of counting assignments where there is no DDoS subsequence. Equivalent to for each uppercase letter X, the string does not contain a subsequence X X (lowercase) (uppercase). However, the subsequence could involve any X; we need to avoid any X.

Thus we need to ensure that for all uppercase letters X, we cannot find two X's (with positions i<j) such that after the second X there is a lowercase somewhere, and after that lowercase there is an uppercase anywhere.

But it's not enough to just avoid for each X individually because the subsequence could involve any X; we can consider the union of events across X. Inclusion-exclusion across 26 letters might be possible but might be complex.

Better to design DP that tracks some global state capturing the existence of a partial pattern.

Observation: The pattern only cares about existence of two equal uppercase letters earlier. So we need to know if we have seen a pair of equal uppercase letters that could serve as the first two positions. However, we also need to know whether after such a pair we have seen a lowercase, and then later an uppercase. So we can track the earliest stage of building the pattern.

Simplify: Let's define states representing the "status" of partial subsequence detection:

State 0: No partial pattern (i.e., no uppercase seen, or no pair of equal uppercase seen). Actually we need to know if we have seen at least one uppercase letter, maybe to potentially start a pair later? Let's think.

We need to detect if there exist i<j such that S[i]=S[j]=uppercase X. So as we scan, when we see an uppercase letter, we might form a pair with a previously seen same uppercase. So we need to remember for each uppercase letter whether we have seen it before (single occurrence) to later be able to form a pair.

But we also need to consider that after we have formed a pair (i.e., we have at least one pair of equal uppercase letters), then if later we see a lowercase and then later an uppercase, we have a DDoS subsequence.

Thus we need to track if we have at least one pair of equal uppercase letters seen so far. Let's call that "pairSeen" boolean.

But also we need to track if we have seen a lowercase after a pair? Actually the pattern requires pair (two equal uppercase) then a lowercase then an uppercase. So after we have a pair, we need to see a lowercase (any) then later an uppercase. So we need to track the stage: after pair, have we seen a lowercase? Then after that, have we seen an uppercase? If we see uppercase after pair and before lowercase, does it affect? The pattern can skip characters; i.e., after pair we can ignore any uppercase until we see a lowercase; then after seeing a lowercase we can ignore any uppercase until we see an uppercase to complete pattern. So the detection is monotonic: once we have pairSeen, the next time we see a lowercase we move to state "lowercaseSeenAfterPair". Then the next time we see any uppercase after that moves to full pattern -> forbidden.

Thus we can define DP states:

0: no pair yet (i.e., we have not yet seen two equal uppercase letters). In this state, we haven't started pattern.

1: pairSeen (i.e., we have seen at least one pair of equal uppercase letters). But we haven't yet seen a lowercase after the pair.

2: pairSeen + lowercaseSeen (i.e., we have seen pair and then at least one lowercase later). Not yet seen uppercase after that.

If we ever see an uppercase while in state 2, we complete the pattern -> invalid.

Thus we need to count assignments that avoid reaching state 2 then uppercase.

But we also need to handle that pair detection depends on which uppercase letters we have seen; we need to know for each uppercase letter if we have seen it once before, to know when we get a pair.

Thus state 0 is more complex: we need to know for each uppercase letter whether we have seen it at least once, because encountering a uppercase that we've seen before creates a pair and moves to state 1.

But we cannot track 26 bits for each position due to large state.

But maybe we can compress: we only need to know whether we have seen any uppercase at all? Not enough: we need to know if we have seen a specific uppercase before to detect a pair of same letter. For a pair to occur, we