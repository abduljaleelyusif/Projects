def hillclimb(domain):
    # Create a random solution
    sol = [random.randint(domain[i][0], domain[i][1])
           for i in range(len(domain))]

    # Main loop
    while True:
        # Create list of neighboring solutions
        neighbors = []
        for j in range(len(domain)):
            # One away in each direction
            if sol[j] > domain[j][0]:
                neighbors.append(sol[0:j] + [sol[j] - 1] + sol[j + 1:])
            if sol[j] < domain[j][1]:
                neighbors.append(sol[0:j] + [sol[j] + 1] + sol[j + 1:])

        # See what the best solution amongst the neighbors is
        # current = costf(sol)
        # best = current
        # for j in range(len(neighbors)):
        #     cost = costf(neighbors[j])
        #     if cost < best:
        #         best = cost
        #         sol = neighbors[j]
        #
        # if best == current:
        #     break

    return sol