# Constraint Satisfaction Problems
Author: Bansharee Ireen

## Map Coloring Problem

### Usage

The `MapColoringCSP` class takes a filename consisting of the domain values and adjacency information as input. You can then use `solve_csp()` method with _optional_ parameters for heuristics and inference to solve the problem. The parameters have default values of `False`, set a parameter to `True` to solve the csp using the respective heuristic/inference.

```python
mapColoringProblem = MapColoringCSP(filename)
solution = mapColoringProblem.solve_csp(MRV=True, DH=True, LCV=True, infer=True)
```

### Input Format

The first line should have the possible domain values, comma separeted with _no_ spaces in between them.
The second line onwards should have the following format, with _no_ spaces in between them:

```text
variable1,neighbor1,neighbor2,...,neighborx
variable2,neighbor1,neighbor2,...,neighborx
```

Example file input with vertices `a,b,c,d` and domains `domain1, domain2,domain3`:

```text
domain1,domain2,domain3
a,b,c
b,a,d
c,a
d,b
```

## Circuit Board Problem

### Usage

The `CircuitBoardCSP` class takes a filename consisting of the circuit board dimensions and component appearance. You can then use `solve_csp()` method with _optional_ parameters for heuristics and inference to solve the problem. The parameters have default values of `False`, set a parameter to `True` to solve the csp using the respective heuristic/inference.

```python
circuitProblem = CircuitBoardCSP(filename)
circuitProblem.solve_csp(MRV=True, DH=True, LCV=True, infer=True)
```

### Input Format

Example with 10x3 circuit board and the following components:

```text
10x3
aaa
aaa
bbbbb
bbbbb
cc
cc
cc
eeeeeee
```


## Further Examples

### Map Coloring

Check `mapcoloring_test.py` for test runs on the map coloring problem on the US map (input file in `us_states.txt`) and on the Australian map (input file in `aus_states.txt`). Edit the `boolean` variable `filename` at the top of the file to change the input file for the problem.

### Circuit Board

Check `circuit_test.py` for test runs on the circuit board problem on the base problem (input file in `circuit.txt`) and a harder problem I came up with (input file in `circuit2.txt`).