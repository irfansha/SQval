# **SQBFval**
A tool for Scalable QBF validation

Accepts QBF instance in QCIR or QDIMACS format and allows interactive play for valiation with a QBF solver or a QBF Certificate.

## Usage:

Play with QBF certificate:

    python3 main.py --certificate intermediate_files/LN_hein_04_3x3_05_SAT/certificate.aag --instance intermediate_files/LN_hein_04_3x3_05_SAT/qbf.qcir

Sample output:

![certficate_play](https://user-images.githubusercontent.com/37924323/215739115-0c161ee7-672b-4bee-bf26-cbf083cfde8f.png)

Play with QBF solver, for SAT instance:

    python3 main.py --instance intermediate_files/LN_hein_04_3x3_05_SAT/qbf.qcir --status 1 --player user --validation dynamic

Sample output:

![user_qbf_play](https://user-images.githubusercontent.com/37924323/215741605-60972c6d-8904-4412-8004-bbea67d69e4e.png)

help:

    python3 main.py -h

main options:
    --status [sat/unsat], needed to be specified for interactive play

    --player [random/user] random generates random assignments as an opponent, for user we can input the assignments

    --seed [int] random seed for reproducing results or counter examples

    --validation [static/dynamic] static is for playing with a certificate and dynamic is for playing with a QBF solver

_Input:_  certificate in aag format for static validation and instance in QCIR/QDIMACS format.

_Output:_  Paritial assignments in each layer for interactive valdiation and play



## Dependencies:
Uses SAT solver from pysat

Install using:

    pip install python-sat

## Author:

    Irfansha Shaik
    Aarhus/Linz
