# **SQBFval**
A tool for Scalable QBF validation and Winning strategy equivalence


# QBF validation:

Accepts QBF instance in QCIR or QDIMACS format and allows interactive play for valiation with a QBF solver or a QBF Certificate.

Play with QBF certificate:

    python3 interactive_validation.py --certificate intermediate_files/LN_hein_04_3x3_05_SAT/certificate.aag --instance intermediate_files/LN_hein_04_3x3_05_SAT/qbf.qcir

Sample output:

![certficate_play](https://user-images.githubusercontent.com/37924323/215739115-0c161ee7-672b-4bee-bf26-cbf083cfde8f.png)

Play with QBF solver, for SAT instance:

    python3 interactive_validation.py --instance intermediate_files/LN_hein_04_3x3_05_SAT/qbf.qcir --status 1 --player user --validation dynamic

Sample output:

![user_qbf_play](https://user-images.githubusercontent.com/37924323/215741605-60972c6d-8904-4412-8004-bbea67d69e4e.png)

help:

    python3 interactive_validation.py -h

main options:
    --status [sat/unsat], needed to be specified for interactive play

    --player [random/user] random generates random assignments as an opponent, for user we can input the assignments

    --seed [int] random seed for reproducing results or counter examples

    --validation [static/dynamic] static is for playing with a certificate and dynamic is for playing with a QBF solver

_Input:_  certificate in aag format for static validation and instance in QCIR/QDIMACS format.

_Output:_  Paritial assignments in each layer for interactive valdiation and play


# Winning strategy equivalence of two QBFs:

Accepts
 - two QBF instances in QDIMACS, Q1 and Q2.
 - a certificate C1 of Q1
 - a file listing shared variables of Q1, Q2 with which there is a common winning strategy

Computes if C1 also holds for Q2 with respect to the shared variables.

Example equivalence check of Hein_12 instance:

    python3 winning_strategy_equivalence.py --instance1 intermediate_files/Hein_12_07_partial_equivalence/BOW_0.qdimacs --instance2 intermediate_files/Hein_12_07_partial_equivalence/BOW_1.qdimacs --certificate intermediate_files/Hein_12_07_partial_equivalence/cert_BOW_0.aag --shared_variables intermediate_files/Hein_12_07_partial_equivalence/shared_variables.txt

Sample output: Formulas are winning strategy equivalent

The above example essential checks if winning strategy of BOW_1.qdimacs instance holds for BOW_0.qdimacs.
The equivalence holds from BOW_1 to BOW_0.

However the equivalence does not hold from BOW_0 to BOW_1

Example:

    python3 winning_strategy_equivalence.py --instance1 intermediate_files/Hein_12_07_partial_equivalence/BOW_1.qdimacs --instance2 intermediate_files/Hein_12_07_partial_equivalence/BOW_0.qdimacs --certificate intermediate_files/Hein_12_07_partial_equivalence/cert_BOW_1.aag --shared_variables intermediate_files/Hein_12_07_partial_equivalence/shared_variables.txt

Sample output: Formulas are winning strategy NOT equivalent

## Dependencies:
Uses SAT solver from pysat

Install using:

    pip install python-sat

Or using the provided `requirements.txt` file:

    pip install -r requirements.txt

## Author:

    Irfansha Shaik
    Aarhus/Linz
