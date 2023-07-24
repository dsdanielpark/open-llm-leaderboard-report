import subprocess
from config import STEPS
from execute_steps import run_steps

SEPERATE_LINE = "=" * 55


def main():
    # Start 
    print("Available step names:")
    for name in STEPS:
        print(name)
    print(SEPERATE_LINE)
    print("Just press enter if you run all steps.")
    print(SEPERATE_LINE)

    # Set steps
    step_input = input("Enter the step names to execute (comma-separated): ")
    print(SEPERATE_LINE)
    if not step_input:
        step_names = STEPS
    else:
        step_names = [step.strip() for step in step_input.split(",")]
    print("Selected steps to execute:")
    for name in step_names:
        print(name)

    # Run stepss
    subprocess.run(["python", "execute_steps.py"] + step_names)
    run_steps(step_names)

    # Finish
    print("Process Done.")


if __name__ == "__main__":
    main()
