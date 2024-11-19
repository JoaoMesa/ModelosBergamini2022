from docplex.mp.model import Model
model = Model(name='scalable_model')

x = [model.continuous_var(lb=0, ub=1, name=f'x{i}') for i in range(10)]

model.maximize(model.sum(x) + 2 * x[1] - 5*x[9])

model.add_constraint(model.sum(x) <= 7)
#model.add_constraint(x[1] + x[0] == 1.5)
model.add_constraint(x[9] >= 0.5)

solution = model.solve()

if solution:
    print("Initial Solution (Continuous Variables):")
    for var in x:
        print(f"{var} = {solution.get_value(var)}")

bin_indices = []

for index in range(10):
    bin_indices.append(index)
    for idx in bin_indices:
        x[idx].set_vartype(model.binary_vartype)

    solution = model.solve()

    if solution:
        print("New Solution (Selected Variables as Binary):", bin_indices)
        for var in x:
            print(f"{var} = {solution.get_value(var)}")
    else:
        print("No solution found")
