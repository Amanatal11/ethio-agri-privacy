import numpy as np
from tools.privacy_engine import PrivacyEngine
from typing import List, Dict

class PrivacyEvaluator:
    """
    Evaluates the privacy-preserving capabilities of the system.
    Simulates membership inference attacks and measures utility vs. privacy.
    """
    
    def __init__(self, epsilon_range: List[float] = [0.01, 0.1, 0.5, 1.0, 5.0]):
        self.epsilon_range = epsilon_range

    def simulate_membership_inference_attack(self, epsilon: float, iterations: int = 1000) -> float:
        """
        Simulates an attack where an adversary tries to guess if a specific data point 
        was part of the aggregate based on the DP output.
        Returns the success rate of the attack.
        """
        engine = PrivacyEngine(epsilon=epsilon)
        success_count = 0
        
        for _ in range(iterations):
            # True mean of a population
            population_data = np.random.normal(0.5, 0.1, 10)
            true_mean = np.mean(population_data)
            
            # DP output
            dp_mean = engine.add_differential_privacy_noise(np.array([true_mean]), sensitivity=0.1)[0]
            
            # Adversary guess: If dp_mean is close to true_mean, they might guess membership.
            # This is a highly simplified proxy for attack success.
            if abs(dp_mean - true_mean) < 0.01:
                success_count += 1
                
        return success_count / iterations

    def run_benchmark(self):
        print("--- Privacy Benchmark: Membership Inference Attack Success Rate ---")
        print(f"{'Epsilon':<10} | {'Attack Success Rate':<20}")
        print("-" * 35)
        for eps in self.epsilon_range:
            rate = self.simulate_membership_inference_attack(eps)
            print(f"{eps:<10} | {rate:<20.4f}")
        print("\nNote: Lower epsilon = higher privacy = lower attack success rate.")

if __name__ == "__main__":
    evaluator = PrivacyEvaluator()
    evaluator.run_benchmark()
