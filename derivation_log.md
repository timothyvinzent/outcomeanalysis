# Derivation of a set of rules for the Road Fines event log explaining no credit collection for unresolved cases

- Generate enriched case log from event log, enriched with attributes and predicates from outcome flow diagram
- Initial baseline filter: baseline = lambda row: row['paid_full']=='True' or row['dismissed']=='True'
- Outcome target: outcome = lambda row: row['Send for Credit Collection.count'] <= 0.0
- Initial attribute hiding: r'Send for Credit Collection.*', credit_collection, unresolved, 'event_count'

1. Rule induction (37 sec): 
- Select rule: ([duration <= 269.0])
Precision: 1.0 1.0
Recall: 0.929 0.9291968286797656
True positives: 26956
False positives: 0
- Hide feature: duration

2. Rule induction (65 sec):
- Select rule: ([Insert Fine Notification.count <= 0.0])
Precision: 1.0 1.0
Recall: 0.727 0.7269562219924164
True positives: 21089
False positives: 0
- Add rule to baseline filter

3. Rule induction (53 sec):
- select rule: ([Final.paymentAmount::sum >= 25.49] ^ [Add penalty:Payment.delay <= 3.0] ^ [Final.outstanding_balance <= 37.55] ^ [Payment.count >= 2.0])
Precision: 1.0 1.0
Recall: 0.106 0.10617028610823853
True positives: 3080
False positives: 0
- Case inspection: S49055, S44571: cases are related to unpaid expense and unpaid penalty
- Attribute enrichment: outstanding_balance_without_expense, outstanding_balance_without_penalty

4. Rule induction (24 sec)
- Select rule: ([Add penalty:Payment.delay <= 3.0] ^ [Final.outstanding_balance_without_penalty <= 0.01])
Precision: 0.999 0.9991310392770246
Recall: 0.198 0.1981730437780076
True positives: 5749
False positives: 5

--- BEGIN Additional investigation---
- Subsetting for clarification: rule = row['Add penalty:Payment.delay'] <= 3.0 and row['Payment.count'] >= 2 and row['Final.outstanding_balance_without_penalty'] <= 0.01
Precision: 1.0 1.0
Recall: 0.122 0.12185453291968287
True positives: 3535
False positives: 0
- Double Check: row['Add penalty:Payment.delay'] <= 3.0 and row['Payment.count'] == 1 and row['Final.outstanding_balance_without_penalty'] <= 0.01
Precision: 0.998 0.9977467327625056
Recall: 0.076 0.07631851085832471
True positives: 2214
False positives: 5
- Checking when second or further payments happen
- More subsetting: row['Add penalty:Payment.delay'] <= 3.0 and row['Payment.count'] == 2 and row['Add penalty:Payment:2.delay'] > 3.0 and row['Final.outstanding_balance_without_penalty'] <= 0.01
Precision: 1.0 1.0
Recall: 0.114 0.11427094105480869
True positives: 3315
False positives: 0
This shows that 3315 have not paid in time. (A) How much did they trangress? and (B) how much money is missing at the deadline?
(A) dist = true_pos['Payment:2.start'] - true_pos['Add penalty.start']; dist.describe()
count    3315.000000
mean       88.673303
std        99.879087
min         4.000000
25%        24.000000
50%        49.000000
75%       108.000000
max       957.000000
(B) amount = true_pos['Payment.outstanding_balance_without_expense_and_penalty']; amount.describe()
count    3.315000e+03
mean     1.200307e+03
std      4.911687e+04
min     -2.154000e+01
25%     -1.100000e+01
50%     -6.710000e+00
75%      0.000000e+00
max      1.999966e+06
- Adding row['Payment.outstanding_balance_without_expense_and_penalty'] > 0.0 shows that there are only 9 cases who have messed up their amount in the first attempt, an example is S112084
--- END Additional investigation---

- Add rule to baseline filter

5. Rule induction (30 sec)
- select rule: ([appeal == True] ^ [Insert Date Appeal to Prefecture.expense_sum <= 15.16] ^ [Notify Result Appeal to Offender.count <= 0.0])
Precision: 1.0 1.0
Recall: 0.04 0.03967597380213719
True positives: 1151
False positives: 0
- rewrite rule: row['appeal'] and row['Insert Date Appeal to Prefecture.count'] >= 1.0 and row['Notify Result Appeal to Offender.count'] <= 0.0
Precision: 1.0 1.0
Recall: 0.044 0.04426059979317477
True positives: 1284
False positives: 0
- simplify rule: row['Insert Date Appeal to Prefecture.count'] >= 1.0 and row['Notify Result Appeal to Offender.count'] <= 0.0
Precision: 1.0 1.0
Recall: 0.044 0.04426059979317477
True positives: 1284
False positives: 0
- drop from baseline

6. Rule induction (14 sec)
- select rule: ([Send Fine:Payment.delay >= 69.0] ^ [Final.outstanding_balance <= 7.5])
Precision: 1.0 1.0
Recall: 0.017 0.017304377800758358
True positives: 502
False positives: 0
- simplify rule: row['Final.outstanding_balance'] <= 7.5
Precision: 1.0 1.0
Recall: 0.029 0.029334712168217855
True positives: 851
False positives: 0
- threshold optimization: row['Final.outstanding_balance'] <= 10.0
Precision: 1.0 1.0
Recall: 0.037 0.03667700792830059
True positives: 1064
False positives: 0
- Add rule to baseline filter

7. Rule induction (22 sec)
- select rule: ([Send Fine:Payment.delay >= 54.0] ^ [start_time_rel >= 4401.0])
Precision: 0.996 0.9955555555555555
Recall: 0.008 0.0077214753533264395
True positives: 224
False positives: 1
- simplify rule: row['start_time_rel'] >= 4401.0
Precision: 0.947 0.9473969631236443
Recall: 0.06 0.06022061358152361
True positives: 1747
False positives: 97
- threshold optimization: row['start_time_rel'] >= 4481.0
Precision: 1.0 1.0
Recall: 0.058 0.0583936573595312
True positives: 1694
False positives: 0
- Add rule to baseline filter

8. Rule induction (39 sec)
- select rule: ([appeal == True] ^ [Payment.outstanding_balance_without_penalty <= 2.3])
Precision: 0.994 0.9938144329896907
Recall: 0.017 0.01661496035849707
True positives: 482
False positives: 3
- Add rule to baseline filter

9. Rule induction (10 sec)
- select rule ([Send Fine:Payment.delay >= 71.0] ^ [start_time_rel >= 4401.0])
Precision: 0.995 0.9949238578680203
Recall: 0.007 0.006756290934160634
True positives: 196
False positives: 1
- rewrite rule (Payment.count >= 1 ^ [start_time_rel >= 4401.0])
Precision: 0.996 0.9956331877729258
Recall: 0.008 0.007859358841778697
True positives: 228
False positives: 1

10. Rule induction (19 sec)
- No more results
- Recurse: change target to no insert
- keep baseline filter including rules (apart from first)
- hide Penalty* and InsertFine* from attributes

11. Rule Induction (30 sec)
- top results refer to FINAL amounts, which have information about Penalty
- hide *FINAL*

12. Rule Induction (8 sec)
- bad results
Predictive:
Precision: 0.570588
Recall: 0.025345
Descriptive: 
Precision: 0.570588
Recall: 0.025345
- switch over to CART:4 (use TRAIN_TEST_SPLIT = 0.1)
- pick rule if (start_time_rel <= 688.5) and (Send Fine.dismissal_last <= 14.5) and (Create Fine.dismissal > 3.5) then class: 1 (proba: 100.0%) | based on 270 samples
- simplify 
special_dismissal_codes = ['A', 'B', 'C', 'D', 'E', 'F', 'I', 'J', 'K', 'M', 'N', 'Q']
rule = lambda row: row['Create Fine.dismissal'] in special_dismissal_codes (3.5 < x < 14.5)
Precision: 0.985 0.9850746268656716
Recall: 0.005 0.0046801872074883
True positives: 330
False positives: 5
- threshold optimization 
special_dismissal_codes = ['2', '3', '5', 'A', 'B', 'E', 'F', 'I', 'J', 'K', 'M', 'N', 'Q', 'R', 'T', 'U', 'V']
Precision: 1.0 1.0
Recall: 0.006 0.006296979151893349
True positives: 444
False positives: 0
- Add rule to baseline filter

13. Rule Induction CART:4
- no more substantial recall 
- case inspection of remainder with knowledge of outcome flow, example: case N22405
- hypothesis lambda row: row['Create Fine.count'] == 1.0 and row['Send Fine.count'] == 1.0 and row['event_count'] == 2.0
Precision: 1.0 1.0
Recall: 0.703 w.r.t. no Collect, 0.967 w.r.t. no InsertFine
True positives: 20385
False positives: 0
