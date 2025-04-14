import subprocess
import sys

def run_docker_command(command):
    try:
        result = subprocess.run(
            f'docker exec exam_planning_backend {command}',
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        print(f"Error executing command: {e}")
        return None

def main():
    print("Retrieving user credentials from the database...")
    
    # Run Python command inside the backend container to query users
    python_command = 'python -c "from app.db.session import SessionLocal; from app.models.user import User; db = SessionLocal(); users = db.query(User).all(); print(\\"\\\\n=== Available Users ===\\\\n\\"); print(f\\"{\\'ID\\':<5} {\\'Email\\':<30} {\\'Name\\':<30} {\\'Role\\':<15}\\"); print(\\"-\\" * 80); [print(f\\"{user.id:<5} {user.email:<30} {user.name:<30} {user.role:<15}\\") for user in users]; print(\\"\\\\nNote: Default password is \\'password\\' unless otherwise specified.\\");"'
    
    output = run_docker_command(python_command)
    
    if output:
        print(output)
    else:
        print("Failed to retrieve user information.")

if __name__ == "__main__":
    main()
