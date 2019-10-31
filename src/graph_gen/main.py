from src.graph_gen import generate_free_scale_graph, graph2txt

n = 500
for k in [1, 3, 5, 10]:
    g = generate_free_scale_graph(n, k, ['a', 'b', 'c', 'd'])
    graph2txt(g, f'graphs/directed_free_scale_net_{n}_{k}.txt')
