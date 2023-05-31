import subprocess
from config import STEPS
from execute_steps import run_steps

def main():
    print("Available step names:")
    for name in STEPS:
        print(name)
    print("Just press enter if you run all steps.")
    step_input = input("Enter the step names to execute (comma-separated): ")
    if not step_input:
        step_names = STEPS
    else:
        step_names = [step.strip() for step in step_input.split(",")]

    print("Selected steps to execute:")
    for name in step_names:
        print(name)

    subprocess.run(["python", "execute_steps.py"] + step_names)

    run_steps(step_names)

if __name__ == "__main__":
    main()