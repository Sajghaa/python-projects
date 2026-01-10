class SimpleTod:
    def __init__(self):
        self.tasks =[]
        self.next_id =1

    def add(self, description: str):
        if description.strip():
            task = {"id":self.next_id, "description":description, "done":False}
            
            self.tasks.append(task)
            self.next_id += 1
            print(f"Added:{description}")
        else:
            print("Task cannot be empty")

    def view(self):

        if not self.tasks:
            print("No tasks")
            return
        
        print("\n Your Tasks: ")
        for task in self.tasks:
            status = "Yes" if task["done"] else "No"
            print(f"{task['id']}. [{status}] {task['description']}")

    def complete(self, task_id: int):
        for task in self.tasks:
            if task_id['id'] == task_id:
                task["done"] = True
                print(f" Completed task {task_id}")
                return
        print(f" Task{task_id} not found")

    def delete(self, task_id: int):
        for task in self.tasks:
            if task['id'] == task_id:
                self.tasks.remove(task)
                print(f"Deleted task {task_id}")
                return
        print(f"Task {task_id} not found")

def main():
    todo =  SimpleTod()
    while True:
        print("\n1. Add 2. View 3. complete 4. Delete 5. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
           task =input("Task: ").strip()
           todo.add(task)
        elif choice == "2":
            todo.view()
        elif choice == "3":
            try:
                task_id = int(input("Task ID to complete: "))
                todo.complete(task_id)
            except:
                print("Enter a number")
        elif choice == "4":
            try:
                task_id = int(input("Task ID to delete: "))
                todo.delete(task_id)
            except:
                print("Enter a number")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Choose 1-5")

if __name__ == "__main__":
    main()