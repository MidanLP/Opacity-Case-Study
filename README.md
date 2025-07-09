# Opacity Case Study

This project supports the case study and practical evaluation for the thesis **"Analyzing System Confidentiality: A Case Study of a Real-World System using Timed Automata"** submitted at TU Berlin. It includes simulation scripts, verification data, and a web system used to illustrate and benchmark opacity in discrete-timed systems.


## Project Structure

- `Testing/` – Contains files and scipts for testing of the Website
//- `Theory/` – Includes theoretical explanations and resources related to opacity.
- `Website/` – Holds the complete website files showcasing the case study and scipts to easily host and test the websites

## File Overview 
├── Testing/ # Scripts and datasets for runtime measurement and simulation
│ └── Times/ # Timing results, processed data, plots, and boxplots
├── Theory/ # Theoretical models used in the thesis
│ └── Automata.txt # Definition of the abstract timed automaton model
├── Website/ # Realistic case study web app
│ ├── Healthcare/ # Simulated healthcare system
│ └── Parachute/ # Simulated parachute deployment system
├── runWebsites.py # Script to launch both mock web apps simultaneously
├── README.md # This file
└── time_output.xlsx # Final output timing data

| File / Script                    | Description                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------------- |                 
| `runWebsites.py`                 | Backup scipt to launch both web servers through python (not recomended, see Setup).          |
| `health_server.py`               | backend for the Healthcare system.                                                           |
| `para_server.py`                 | backend for the Parachute system.                                                            | 
| `index.html` (under each system) | Frontend interface for the respective case study applications.                               |
| `createBoxplot.py`               | Generates performance comparison plots from recorded timing data.                            |
| `Test_Website.py`                | Used to programmatically test server response and simulate client behavior.                  |
| `time_data.xlsx`, etc.           | Raw and filtered timing measurements for various caching strategies.                         |
| `boxplot_*.png`                  | Visual runtime comparisons between configurations (cached, no cache, etc.).                  |
| `Comparison Server.png`          | Summary visualization comparing systems.                                                     |
| `time_output.xlsx`               | Final formatted timing results, used in Table \ref{tab\:case\_study\_results} of the thesis. |


##  Getting Started

To view the case study:

1. Clone the repository:
   ```bash
   git clone https://github.com/MidanLP/Opacity-Case-Study.git


##  Dependencies
Testing: 

-Python
-Pandas
-Selenium Webdriver (Chrome)
-Mathplot lib