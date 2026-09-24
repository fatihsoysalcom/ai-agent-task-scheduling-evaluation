import time
from collections import namedtuple

# Define a Task structure for our AI agent to process
Task = namedtuple('Task', ['id', 'priority', 'effort'])

class AIAgent:
    """Simulates an AI agent that schedules tasks based on internal logic."""
    def __init__(self, name="TaskSchedulerAgent"):
        self.name = name
        self.processed_tasks = []

    def process_tasks(self, tasks):
        print(f"--- {self.name} - Observability Phase ---")
        print(f"Agent received {len(tasks)} tasks.")
        print("Initial tasks:")
        for task in tasks:
            print(f"  - Task {task.id}: Priority={task.priority}, Effort={task.effort}")

        # --- OBSERVABILITY: The agent logs its internal decision-making process ---
        # This section shows *what* the agent is doing and its internal state.
        # Agent's internal logic: Sort by priority (Critical > High > Medium > Low),
        # then by effort (lower effort first) within the same priority.
        priority_order_map = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        sorted_tasks = sorted(tasks, key=lambda t: (
            priority_order_map.get(t.priority, 99), # Higher priority = lower number
            t.effort # Lower effort first
        ))

        print("\nAgent's decision: Processing tasks in the following order:")
        total_effort_spent = 0
        max_effort_budget = 20 # Simulate a resource constraint for processing
        for task in sorted_tasks:
            if total_effort_spent + task.effort <= max_effort_budget:
                print(f"  - Processing Task {task.id} (P:{task.priority}, E:{task.effort}). Current effort: {total_effort_spent + task.effort}")
                self.processed_tasks.append(task)
                total_effort_spent += task.effort
                time.sleep(0.05) # Simulate work
            else:
                print(f"  - Skipping Task {task.id} due to effort budget constraint. (P:{task.priority}, E:{task.effort})")
                break # Stop if budget exceeded

        print(f"\nAgent finished. Total tasks processed: {len(self.processed_tasks)}. Total effort spent: {total_effort_spent}")
        # --- End of Observability Phase ---
        return self.processed_tasks

class AgentEvaluator:
    """Evaluates the performance of an AI agent against defined goals and metrics."""
    def __init__(self, target_priority_order):
        self.target_priority_order = target_priority_order
        # Assign scores based on target priority order (higher score for higher priority)
        self.priority_scores = {p: len(target_priority_order) - i for i, p in enumerate(target_priority_order)}

    def evaluate(self, original_tasks, agent_processed_tasks, max_effort_budget):
        print("\n--- Agent Evaluation Phase ---")
        print("Evaluating agent's performance against defined goals.")

        # --- EVALUATION: Measuring *how well* the agent performed ---
        # This section introduces metrics and comparisons to assess performance.
        # Metric 1: Total priority score achieved by the agent
        agent_total_score = sum(self.priority_scores.get(task.priority, 0) for task in agent_processed_tasks)
        agent_effort_spent = sum(task.effort for task in agent_processed_tasks)

        print(f"\nAgent's Performance:")
        print(f"  - Tasks Processed: {len(agent_processed_tasks)}")
        print(f"  - Total Effort Spent: {agent_effort_spent} (Budget: {max_effort_budget})")
        print(f"  - Total Priority Score (higher is better): {agent_total_score}")

        # Calculate an 'optimal' baseline for comparison
        # Optimal strategy: Sort by highest priority score, then lowest effort
        optimal_sorted_tasks = sorted(original_tasks, key=lambda t: (
            -self.priority_scores.get(t.priority, 0), # Higher score first
            t.effort # Lower effort first
        ))

        optimal_processed_tasks = []
        optimal_effort_spent = 0
        for task in optimal_sorted_tasks:
            if optimal_effort_spent + task.effort <= max_effort_budget:
                optimal_processed_tasks.append(task)
                optimal_effort_spent += task.effort
            else:
                break

        optimal_total_score = sum(self.priority_scores.get(task.priority, 0) for task in optimal_processed_tasks)

        print(f"\nOptimal Baseline Performance (for comparison):")
        print(f"  - Tasks Processed: {len(optimal_processed_tasks)}")
        print(f"  - Total Effort Spent: {optimal_effort_spent} (Budget: {max_effort_budget})")
        print(f"  - Total Priority Score: {optimal_total_score}")

        # Provide feedback based on comparison
        if agent_total_score >= optimal_total_score:
            print("\nEvaluation Result: Agent performed optimally or very close to optimal!")
        else:
            print(f"\nEvaluation Result: Agent could improve. Optimal score was {optimal_total_score}, agent achieved {agent_total_score}.")
            print("  Recommendation: Consider refining agent's prioritization logic to better align with high-value tasks.")

        # Additional evaluation: Check if all critical tasks were processed (if possible within budget)
        critical_tasks_in_original = [t for t in original_tasks if t.priority == 'Critical']
        critical_tasks_processed_by_agent = [t for t in agent_processed_tasks if t.priority == 'Critical']

        if len(critical_tasks_in_original) > 0 and len(critical_tasks_processed_by_agent) < len(critical_tasks_in_original):
            print(f"  - Warning: Not all Critical tasks were processed by the agent ({len(critical_tasks_processed_by_agent)}/{len(critical_tasks_in_original)}).")
        elif len(critical_tasks_in_original) > 0:
            print(f"  - All Critical tasks were processed by the agent ({len(critical_tasks_processed_by_agent)}/{len(critical_tasks_in_original)}). Yay!")
        # --- End of Evaluation Phase ---

# Main execution block
if __name__ == "__main__":
    # Define a set of tasks for the agent to process
    tasks_to_process = [
        Task(id="A", priority="High", effort=5),
        Task(id="B", priority="Critical", effort=8),
        Task(id="C", priority="Medium", effort=3),
        Task(id="D", priority="Critical", effort=4),
        Task(id="E", priority="Low", effort=2),
        Task(id="F", priority="High", effort=6),
        Task(id="G", priority="Medium", effort=7),
    ]

    agent = AIAgent()
    # Phase 1: The AI agent runs, demonstrating its actions (observability).
    # At this point, we only see *what* it does, not *how well* it does it.
    processed_by_agent = agent.process_tasks(tasks_to_process)

    # Phase 2: Introduce an evaluation mechanism to assess the agent's performance.
    # We define goals and metrics to understand if the agent achieved its objectives.
    target_priority_order = ['Critical', 'High', 'Medium', 'Low']
    evaluator = AgentEvaluator(target_priority_order)
    # The max_effort_budget is passed to the evaluator to ensure consistency with agent's constraints
    evaluator.evaluate(tasks_to_process, processed_by_agent, max_effort_budget=20)
