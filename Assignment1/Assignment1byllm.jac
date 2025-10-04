"""An AI-Powered To-Do List Assistant in Jac Ai Model"""

import random;
import from byllm.llm { Model }

# Initialize a lightweight LLM model
glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);

"""Use AI to summarize or suggest next action"""
def summarize_tasks(tasks: list[str]) -> str by llm();

# Node to represent a single task
node Task {
    has description: str;
    has done: bool = False;
}

# Walker to manage the to-do list
walker TaskManager {
    can start with root entry;
    can add_task with root entry;
    can show_tasks with root entry;
    can mark_done with Task entry;
    can summarize with root entry;

    has task_list: list[str] = [];

    # Create tasks dynamically
    impl start {
        print("🧠 AI To-Do Assistant Started!");
        print("Use commands: add, list, done, summarize, or exit.");
        while True {
            choice = input("Enter command: ");
            if choice == "add":
                visit --> add_task;
            elif choice == "list":
                visit --> show_tasks;
            elif choice == "done":
                if not here.outgo(Task):
                    print("No tasks yet!");
                else:
                    name = input("Enter task description to mark done: ");
                    for t in here.outgo(Task):
                        if t.description == name:
                            visit t;
                            break;
            elif choice == "summarize":
                visit --> summarize;
            elif choice == "exit":
                print("Goodbye! 👋");
                disengage;
            else:
                print("Invalid command!");
        }
    }

    impl add_task {
        desc = input("Enter new task description: ");
        new_task = here ++> Task(description=desc);
        print(f"✅ Added task: {desc}");
    }

    impl show_tasks {
        print("\n📋 Current Tasks:");
        for t in here.outgo(Task):
            status = "✔️ Done" if t.done else "❌ Not done"
            print(f" - {t.description} ({status})");
    }

    impl mark_done {
        here.done = True;
        print(f"🎯 Marked '{here.description}' as done.");
    }

    impl summarize {
        self.task_list = [t.description for t in here.outgo(Task)];
        result = summarize_tasks(self.task_list);
        print("\n🤖 AI Summary:");
        print(result);
    }
}

# Entry point
with entry:__main__ {
    root spawn TaskManager();
}
