"""
Week 7 Lab - Part 1: Zero-Knowledge Proof (ZKP) Simulation
Ali Baba Cave Protocol Implementation
"""

import random


def simulate_zkp_trial(knows_password):
    """
    Simulate a single ZKP trial

    Args:
        knows_password (bool): Whether the prover knows the password

    Returns:
        tuple: (path_entered, challenge, success)
    """
    path_entered = random.choice(['A', 'B'])
    challenge = random.choice(['A', 'B'])

    if knows_password:
        # Alice knows the password, so she can always exit from the challenged path
        success = True
    else:
        # Without password, Alice can only succeed if her random path matches the challenge
        success = (path_entered == challenge)

    return path_entered, challenge, success


def simulate_zkp(trials=20, knows_password=True, verbose=False):
    """
    Run multiple ZKP trials and track results

    Args:
        trials (int): Number of trials to run
        knows_password (bool): Whether the prover knows the password
        verbose (bool): Print detailed trial information

    Returns:
        dict: Results including success count and details
    """
    success_count = 0
    trial_details = []

    for i in range(trials):
        path, challenge, success = simulate_zkp_trial(knows_password)

        if success:
            success_count += 1

        trial_info = {
            'trial': i + 1,
            'path_entered': path,
            'challenge': challenge,
            'success': success
        }
        trial_details.append(trial_info)

        if verbose:
            status = "✓ SUCCESS" if success else "✗ FAILED"
            print(f"Trial {i + 1:2d}: Path={path}, Challenge={challenge} → {status}")

    return {
        'success_count': success_count,
        'total_trials': trials,
        'success_rate': (success_count / trials) * 100,
        'trial_details': trial_details
    }


def calculate_security_probability(trials):
    """Calculate the probability of fooling the verifier by random guessing"""
    probability = (0.5) ** trials
    return probability


def main():
    """Main function to run ZKP simulations"""

    print("=" * 70)
    print("ZERO-KNOWLEDGE PROOF SIMULATION - Ali Baba Cave Protocol")
    print("=" * 70)

    print("\nPROTOCOL DESCRIPTION:")
    print("-" * 70)
    print("1. Alice (Prover) enters the cave through path A or B")
    print("2. Bob (Verifier) randomly challenges her to exit through A or B")
    print("3. If Alice knows the secret password, she can always comply")
    print("4. Without the password, she can only guess (50% chance)")
    print("5. After multiple trials, Bob gains confidence Alice knows the secret")
    print("-" * 70)

    trials = 20

    # Simulation 1: Honest Prover (knows password)
    print(f"\n{'=' * 70}")
    print("SIMULATION 1: HONEST PROVER (Knows Password)")
    print("=" * 70)
    honest_results = simulate_zkp(trials=trials, knows_password=True, verbose=False)

    print(f"\nResults:")
    print(f"  Success: {honest_results['success_count']}/{honest_results['total_trials']}")
    print(f"  Success Rate: {honest_results['success_rate']:.2f}%")
    print(f"  Expected: 100% (Alice can always respond correctly with password)")

    # Simulation 2: Malicious Prover (no password - guessing)
    print(f"\n{'=' * 70}")
    print("SIMULATION 2: MALICIOUS PROVER (No Password - Guessing)")
    print("=" * 70)
    malicious_results = simulate_zkp(trials=trials, knows_password=False, verbose=False)

    print(f"\nResults:")
    print(f"  Success: {malicious_results['success_count']}/{malicious_results['total_trials']}")
    print(f"  Success Rate: {malicious_results['success_rate']:.2f}%")
    print(f"  Expected: ~50% (Random guessing has 1/2 probability per trial)")

    # Security Analysis
    print(f"\n{'=' * 70}")
    print("SECURITY ANALYSIS")
    print("=" * 70)

    probability = calculate_security_probability(trials)
    print(f"\nProbability of fooling verifier by luck ({trials} trials):")
    print(f"  (1/2)^{trials} = {probability:.2e}")
    print(f"  That's approximately 1 in {int(1 / probability):,}")

    print(f"\nSecurity for different trial counts:")
    for n in [10, 20, 30, 50]:
        prob = calculate_security_probability(n)
        print(f"  {n:2d} trials: 1 in {int(1 / prob):,}")

    print(f"\n{'=' * 70}")
    print("CONCLUSION")
    print("=" * 70)
    print("After 20 trials, it's computationally infeasible for a malicious")
    print("prover to succeed without knowing the password. This demonstrates")
    print("zero-knowledge: Alice proves she knows the password WITHOUT revealing")
    print("it, while making it nearly impossible for an attacker to fake knowledge.")
    print("=" * 70)

    # Additional Analysis: Run multiple simulations to show variance
    print(f"\n{'=' * 70}")
    print("ADDITIONAL ANALYSIS: Multiple Malicious Attempts")
    print("=" * 70)
    print("\nRunning 10 separate simulations of malicious provers:")

    malicious_rates = []
    for i in range(10):
        result = simulate_zkp(trials=20, knows_password=False, verbose=False)
        rate = result['success_rate']
        malicious_rates.append(rate)
        print(f"  Attempt {i + 1:2d}: {result['success_count']:2d}/20 ({rate:5.1f}%)")

    avg_rate = sum(malicious_rates) / len(malicious_rates)
    print(f"\nAverage success rate: {avg_rate:.1f}% (Expected: ~50%)")


if __name__ == "__main__":
    main()