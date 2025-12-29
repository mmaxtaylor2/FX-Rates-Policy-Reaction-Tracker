"""
FX & Rates Policy Reaction Tracker - Main Entry Point
Phase 1: Load events → fetch market data → build event windows
"""

from scripts.pipeline import run_event_reaction_pipeline

def main():
    print("\n==============================================")
    print("   FX & RATES POLICY REACTION TRACKER - RUN   ")
    print("==============================================\n")

    try:
        run_event_reaction_pipeline()
    except Exception as e:
        print("\nERROR OCCURRED:")
        print(e)
        print("")
        return
    
    print("\n----------------------------------------------")
    print("Pipeline completed successfully.")
    print("Output saved to data/event_reaction_output.csv")
    print("----------------------------------------------\n")

if __name__ == "__main__":
    print("\nStarting program...\n")
    main()
    print("\nProgram finished.\n")

