# Selene: Programming for Everyone

Selene is a revolutionary programming language designed to make coding accessible to everyone, especially beginners. It bridges the gap between natural language and traditional programming, allowing you to write code by simply having a conversation. Selene is an ideal tool for students and teachers in the world of programming education.

## The Problem: Making Programming Accessible

Traditional programming languages often have a steep learning curve, filled with complex syntax and abstract concepts. This can be intimidating for newcomers and create a barrier to entry for those who want to bring their ideas to life through code. Many students are introduced to programming through visual block-based languages but find the transition to text-based languages like Python challenging. Selene provides a stepping stone, easing this transition. Selene aims to solve this by providing a more intuitive and user-friendly approach to programming.

## Features

Selene empowers users with a range of features designed for ease of use and flexibility, making it an excellent choice for learning and teaching programming:

*   **Conversational Programming:** Write code in plain Spanish or English. Its syntax is so natural that it looks like a dialogue, making it easy for those who have never programmed to understand and use. Selene understands your instructions and translates them into executable actions.
*   **Python-Based Execution:** Under the hood, Selene leverages the power and versatility of Python, giving you access to a vast ecosystem of libraries and tools. This allows students to gradually become familiar with Python's capabilities.
*   **Common Programming Constructs:** Selene supports essential programming concepts, including:
    *   Importing libraries
    *   Defining and calling functions
    *   Working with lists
    *   Implementing loops
    *   Introducing pauses or delays in execution
*   **Command-Line Interpreter (REPL):** Experiment with Selene interactively through its Read-Eval-Print Loop, perfect for quick tests and learning.
*   **`.se` Script Execution:** Write your Selene programs in `.se` files and execute them directly, allowing for the creation of more complex projects.
*   **Luna Wizard - Graphical IDE:** For a more visual experience, Selene offers the Luna Wizard, a graphical integrated development environment with features like:
    *   Automatic input windows for user interaction, simplifying how programs get data.
    *   A welcoming splash screen.
    *   Support for custom icons.
    *   Future integration with Arduino for physical computing projects, opening doors to robotics and electronics education.
*   **Single Executable Distribution:** Selene is distributed as a single executable, making it easy to install and run without complex setup procedures, ideal for classroom environments.

## Features of this Version

This version of Selene offers a robust set of capabilities for aspiring programmers:

*   **Dual Interaction Modes:**
    *   Engage with Selene through its conversational **text-based REPL** (Read-Eval-Print Loop).
    *   Write and execute longer programs using **`.se` script files**.
*   **Luna Wizard Graphical IDE:** A user-friendly graphical interface featuring:
    *   Automatic pop-up windows for `entrada` (input) commands.
    *   An initial splash screen for a pleasant startup experience.
    *   Support for custom application icons.
*   **Core Programming Constructs Supported:**
    *   **Variables:** Define variables using natural syntax (e.g., `toma x = 10`, `let y = "hello"`).
    *   **Loops:** Implement `mientras` (while) loops for repetitive tasks.
    *   **Conditionals:** Use `si` (if) statements for decision-making.
    *   **Lists:** Create and manipulate lists of items (e.g., `lista my_items = "apple", "banana", "orange"`).
    *   **Module Imports:** Access Python's standard library modules with commands like `de math importa sqrt`.
    *   **Pauses:** Introduce delays into your programs (e.g., `espera 1` for a 1-second pause).
*   **Python 3.12+ Compatibility:** Built to run on modern Python versions.
*   **Windows Executable:** Can be packaged into a single `SeleneIDE.exe` using PyInstaller, allowing it to run on Windows machines without a separate Python installation.

## Libraries and Dependencies

Selene's core is designed to be lightweight and accessible. Internally, it relies only on the Python standard library. The key modules used are:
*   `re` (for parsing natural language commands)
*   `importlib` (for dynamically importing modules)
*   `time` (for functions like pausing execution)
*   `pathlib` (for file system interactions)
*   `tkinter` (powering the Luna Wizard graphical IDE)
*   `zipfile` (primarily relevant for the PyInstaller packaging process to create the single executable)

No third-party modules are mandatory for Selene to run from its Python scripts.

One of Selene's powerful features is its ability to leverage the broader Python ecosystem through natural language commands. Users can import standard Python modules using Selene's intuitive syntax. For example:

*   To use functions from the `math` module, you can write:
    `de math importa sqrt`
    (This effectively allows Selene to access `math.sqrt`)
*   To use the `random` module, you might say:
    `de módulos importa random`
    (This allows Selene to use functions from the `random` module)

This approach means that users can access a vast range of functionalities available in Python's standard library without needing to manage complex installation steps for external libraries, as long as they have a standard Python environment set up.

## Getting Started

To get started with Selene, follow these instructions:

**Prerequisites:**
*   Python 3.12 or higher. Make sure your Python installation includes Tkinter (it's usually included by default).

**Project Structure:**
*   Clone or unzip the project so that the top-level directory contains `selene.py`, `start_luna.py`, and the `Functions/` and `Luna/` folders.

**Running Selene:**

You can run Selene in several ways from your terminal or command prompt, navigated to the project's top-level directory:

*   **Text REPL (Read-Eval-Print Loop):** For interactive coding.
    ```bash
    python selene.py
    ```
*   **Running a Selene Script:** To execute a script saved with a `.se` extension.
    ```bash
    python selene.py your_script_name.se
    ```
*   **Launching Luna Wizard (GUI):** To use the graphical interface.
    ```bash
    python selene.py --ide
    ```

**Single Executable for Windows (SeleneIDE.exe):**
*   If you have the `SeleneIDE.exe` (packaged with PyInstaller), simply double-clicking it on any Windows PC will launch the Luna Wizard GUI directly. This version does not require Python to be installed on the user's machine as it includes everything needed.

## Example Code / Testing in IDE

Here are a few simple examples to get you started with Selene. You can type these directly into the Selene REPL or the Luna Wizard IDE.

**Hello, World!**
```selene
muestra "Hello, World!"
```

**Echo your name:**
```selene
entrada name
muestra "Hi", name, "welcome to Selene!"
```

**Countdown:**
```selene
toma n = 5
mientras n > 0:
    muestra n
    espera 1
    toma n = n - 1
muestra "Lift-off!"
```

**Random number guess:**
```selene
de módulos importa random
toma secret = random.randint(1, 10)
entrada guess
si int(guess) == secret: muestra "Correct!"
si int(guess) != secret: muestra "Nope, the number was", secret
```

**Average of a list:**
```selene
lista scores = 8, 9, 10, 7, 9
toma avg = sum(scores) / len(scores)
muestra "Average:", avg
```

These examples cover user input, variables, loops, conditions, pauses, list handling and module import—the core building blocks a beginner needs to feel productive in Selene. You can copy and paste these directly into the Luna Wizard IDE to see them in action!

## Contributing

**This is a Public Beta / Testing Version!**

We are thrilled to share Selene with the community at this stage. We encourage you to **download, run, and thoroughly test** all aspects of the language and the Luna Wizard IDE.

**Found a Bug?**
Please let us know! Your bug reports and feedback on any issues you encounter are invaluable.

**Current State of the Code:**
Selene is functional but not yet fully optimized. We are actively working on improving it. Specific areas where we anticipate further development include:
*   Refinement of logical conditions and their parsing.
*   Enhancements to how Selene interacts with and adapts Python modules.
*   General code structure improvements and performance optimizations.

**We Welcome Your Contributions!**
Selene is an open project, and we believe in the power of community collaboration. Your input can significantly shape its future.

**Our Vision & Your Impact:**
Our long-term vision is to implement Selene in classrooms across Mexico and the United States, making programming more accessible to students. Your feedback, bug reports, and contributions are vital to achieving this goal and ensuring Selene is a robust and effective learning tool.

**How You Can Contribute:**
There are many ways to help:
*   **Provide Feedback:** Share your experiences, what you like, and what could be better.
*   **Report Bugs:** Detailed bug reports help us identify and fix issues quickly.
*   **Suggest Features:** Have ideas for new features or improvements? Let us know!
*   **Improve Code:** If you're a developer, contributions to the codebase are welcome.
*   **Send us an email:** If you are passionate about the project and found bugs or improvements that you think will improve the project and help us reach our goal, send us an email to: inovation.of.the.pear@gmail.com

We are excited to hear from you and build a better Selene together!

**Created with ❤️ from Mexico by: Elian Alfonso López Preciado**
