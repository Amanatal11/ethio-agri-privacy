import numpy as np
from typing import List

class AccuracyEvaluator:
    """
    Compares the accuracy/utility of the federated approach vs. local-only.
    """

    def evaluate_utility(self, num_clients: int = 10, noise_scale: float = 0.1):
        """
        Simulates the benefit of federated learning.
        """
        # Ground truth regional trend (e.g., optimal planting day offset)
        ground_truth_trend = 15.0 
        
        # Local-only estimates (noisy and biased)
        local_estimates = [ground_truth_trend + np.random.normal(0, 5.0) for _ in range(num_clients)]
        local_error = np.mean([abs(e - ground_truth_trend) for e in local_estimates])
        
        # Federated estimate (averaged + DP noise)
        fed_mean = np.mean(local_estimates)
        fed_estimate = fed_mean + np.random.laplace(0, noise_scale)
        fed_error = abs(fed_estimate - ground_truth_trend)
        
        return local_error, fed_error

    def run_benchmark(self):
        print("--- Accuracy Benchmark: Federated vs. Local-Only Error ---")
        print(f"{'Clients':<10} | {'Local Error (Avg)':<20} | {'Federated Error':<20}")
        print("-" * 55)
        for n in [5, 20, 100]:
            l_err, f_err = self.evaluate_utility(num_clients=n)
            print(f"{n:<10} | {l_err:<20.4f} | {f_err:<20.4f}")
        print("\nNote: Federated error typically decreases as more clients participate, despite DP noise.")

if __name__ == "__main__":
    evaluator = AccuracyEvaluator()
    evaluator.run_benchmark()
