# What is a Load Balancing, its need & how it works ?
<!-- 'Load balancing is the method of distributing network traffic equally across a pool of resources that support an application. Modern applications must process millions of users simultaneously and return the correct text, videos, images, and other data to each user in a fast and reliable manner. To handle such high volumes of traffic, most applications have many resource servers with duplicate data between them. A load balancer is a device that sits between the user and the server group and acts as an invisible facilitator, ensuring that all resource servers are used equally.' $^1$ -->

# Getting Started

## WINDOWS
| Step | Command | Effect |
| -- | -- | -- |
| **Cloning the Github Repo** | `git clone https://github.com/Coder-Harshit/LoadBalancer-Viz.git` | LoadBalancer Repo Cloned to Local system |
| **Navigating to Project Dir** | `cd LoadBalancer-Viz` | WorkingDir switched to `LoadBalancer-Viz` | 
| **Switching to Dev branch** | `git checkout dev` | Switched to Dev branch | 
| **Creating Python Virtual Env** | `python -m venv .venv` | Virtual Env `.venv` created *(using venv)* |
| **Activating the Env** | `.venv\Scripts\Activate` | Virtual Env activated |
| **Installing Dependencies** | `pip install -r requirements.txt` | Necessary requirements installed |
| **Executing the program** | `python main.py` | Program up & running |


## LINUX
| Step | Command | Effect |
| -- | -- | -- |
| **Cloning the Github Repo** | `git clone https://github.com/Coder-Harshit/LoadBalancer-Viz.git` | LoadBalancer Repo Cloned to Local system |
| **Navigating to Project Dir** | `cd LoadBalancer-Viz` | WorkingDir switched to `LoadBalancer-Viz` | 
| **Switching to Dev branch** | `git checkout dev` | Switched to Dev branch | 
| **Creating Python Virtual Env** | `python -m venv .venv` | Virtual Env `.venv` created *(using venv)* |
| **Activating the Env** | `source .venv/bin/activate` | Virtual Env activated |
| **Installing Dependencies** | `pip install -r requirements.txt` | Necessary requirements installed |
| **Executing the program** | `python main.py` | Program up & running |



# References:
1. [Amazon-AWS](https://aws.amazon.com/what-is/load-balancing/)