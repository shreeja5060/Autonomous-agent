from pipelines.task_pipeline import TaskPipeline

def print_evaluation(eval_data):
    """Pretty print evaluation"""
    if not eval_data:
        return
    
    print("\n QUALITY EVALUATION:")
    print(f"  Overall Score: {eval_data.get('overall_score', 'N/A')}/10")
    print(f"  Completeness: {eval_data.get('completeness', 'N/A')}/10")
    print(f"  Accuracy: {eval_data.get('accuracy', 'N/A')}/10")
    print(f"  Clarity: {eval_data.get('clarity', 'N/A')}/10")
    print(f"  Usefulness: {eval_data.get('usefulness', 'N/A')}/10")
    
    if "strengths" in eval_data:
        print("\n   Strengths:")
        for strength in eval_data["strengths"]:
            print(f"    • {strength}")
    
    if "improvements" in eval_data:
        print("\n   Suggested Improvements:")
        for improvement in eval_data["improvements"]:
            print(f"    • {improvement}")

def main():
    pipeline = TaskPipeline()
    
    # Test cases
    test_topics = [
        "AI in Healthcare",
        "Quantum Computing applications",
        "Climate Change solutions using technology"
    ]
    
    for i, topic in enumerate(test_topics, 1):
        print(f"\n{'#'*70}")
        print(f"TEST CASE {i}/{len(test_topics)}")
        print(f"{'#'*70}")
        
        result = pipeline.run(topic, max_iterations=2)
        
        print("\n" + "="*70)
        print(" FINAL OUTPUT:")
        print("="*70)
        print(result["final_output"])
        
        print_evaluation(result["final_evaluation"])
        
        print("\n" + "-"*70)
        input("Press Enter to continue to next test...")
    
    # Show overall metrics
    pipeline.show_metrics()

if __name__ == "__main__":

    main()
