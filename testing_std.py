from scipy.stats import kruskal, wilcoxon
import itertools

cluster_a = [0.108, 0.084, 0.1, 0.077]
cluster_b = [0.121, 0.117, 0.144, 0.122]
cluster_c = [0.123, 0.135, 0.117, 0.128]
cluster_d = [0.089, 0.076, 0.074, 0.065]

clusters = [cluster_a, cluster_b, cluster_c, cluster_d]

pairs = list(itertools.combinations(clusters, 2))

for pair in pairs:
    H, p_value = wilcoxon(pair[0], pair[1])
    formatted_p_value = format(p_value, ".10f")
    print(f"The pair {pair[0]} and {pair[1]} have a p-value of {formatted_p_value}")