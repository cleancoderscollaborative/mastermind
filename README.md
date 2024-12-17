[//]: # (README.md)
[//]: # (Copyright © 2024 Clean Coders Collaborative. All rights reserved.)
[//]: #

![Banner Light](https://raw.githubusercontent.com/cleancoderscollaborative/cdn/main/banners/banner-mastermind-light.png#gh-light-mode-only)
![Banner Light](https://raw.githubusercontent.com/cleancoderscollaborative/cdn/main/banners/banner-mastermind-dark.png#gh-dark-mode-only)

# Mastermind

## Overview

Implementing the Mastermind game will allow plenty of opportunities to discuss and experiment with TDD, Agile, and development principles
and patterns.
The environment has been chosen to focus on those topics, and not create a high learning curve to participate:

1. The game because it offers multiple opportunities for discussion.
1. Python is chosen because of the common C-like syntax, the prevalence
of use, and that both object-oriented and functional programming topcis may be addressed.
1. Visual Studio Code will be the IDE, because of the price tag, the available extensions, and it is the interface for GitHub Codespaces.
1. The project is configured in such a way as to be developed using a local Python installation or in a Codespace at GitHub if
you prefer not to (or cannot) install Python on your computer.

## Process

1. The group will be led by *champions* for the project.
The champions will pick the topic of discussion, and the group will develop code and talk
about making it better.
1. Gather requirements and define priorities.
1. Use TDD to start the project.
Agile will be incorported; if you are a Scrum connoisseur each meetup is a sprint, complete with a planning meeting at the beginning
and a retrospective at the end.
Remember that Agile, and even TDD, are not the focus of this project.
The focus is *Clean Code*.

## Configuration

### Option 1: Local development environment (preferred)

1. At a terminal window or command prompt (all systems) check to see if you have Python 3.
$ is the command prompt, and there are two possible commands to check:
```
$ python --version
$ python3 --version
```

#### Apple MacOS

1. Install Python 3 if you do not have it; three options:
    1. Install with Homebrew ($ is the command prompt): <sup>[Install Homebrew](#homebrew)</sup>
        ```
        $ brew install python
        ```
    1. Download and install from python.org: https://docs.python.org/3/using/mac.html
    1. Download and install from Anaconda.com: https://www.anaconda.com/download
1. Install git if you do not have it; two options:
    1. Install with Homebrew:
        ```
        $ brew install git
        ```
    1. Download and install from git-scm: https://git-scm.com/downloads/mac
1. Install Visual Studio Code if you do not have it; two options:
    1. Install with Homebrew:
        ```
        $ brew install --cask visual-studio-code
        ```
    1. Download and install from Microsoft: https://code.visualstudio.com/
1. Continue with [*All Platforms*](#all-platforms) below.

#### Microsoft Windows

1. Install Python 3 if you do not have it; three possible options:
    1. Install with Chocolatey ($ is the command prompt):  <sup>[Install Chocolatey](#chocolatey)</sup>
        ```
        $ choco install -y python3
        ```
    1. Download and install from python.org: https://docs.python.org/3/using/windows.html
    1. Download and install from Anaconda.com: https://www.anaconda.com/download
1. Install Visual Studio Code, if necessary:
    1. Install with Homebrew:
        ```
        $ brew install --cask visual-studio-code
        ```
    1. Download and install from Microsoft: https://code.visualstudio.com/
1. Continue with [*All Platforms*](#all-platforms) below.

#### Linux

1. Install Python 3 if you do not have it:
    ```
    $ sudo apt update; sudo apt install python3          # Debian Linux (Ubuntu, etc.)
    $ sudo yum check-update; sudo yum install python3    # RHEL (Red Hat, Centos, etc.)
    ```
1. Install Visual Studio Code, if necessary:
    1. Install with Homebrew:
        ```
        $ brew install --cask visual-studio-code
        ```
    1. Download and install from Microsoft: https://code.visualstudio.com/
1. Continue with [*All Platforms*](#all-platforms) below.

#### All Platforms

1. Install the necessary extensions to the VSCode environment:
    1. Click the extensions icon on the toolbar. ![extensions](./.assets/extensions-button.png)
    2. Add (if not already installed) Microsoft Python, Microsoft Python Debugger, Microsoft Live Share, and
    Ritwik Dey Liver Server:
    ![Required Extensions](./.assets/extensions.png)
1. Fork this repository to your own GitHub account:
1. Clone your copy to your local machine using git at the command prompt/terminal:
    ```
    $ cd <your projects directory>
    $ git clone <your repository path>
    ```
1. Open VSCode and select the repository folder you just cloned.

## Option 2: Develop in a GitHub Codespace

GitHub Codespaces are Docker containers running on servers at GitHub.
When you launch a Codespace 

1. Fork this repository to your own GitHub account:
1. In the new repository, click the Code button, select the Codespaces tab, and create a new Codespace
on the *main* branch.
1. A 

## Footnotes

### Homebrew

Homebrew is a popular application and package manager for Apple MacOS.
Installation instructions are located here: https://brew.sh

### Chocolatey

Chocolatey is an application and package manager for Microsoft Windows.
Installation instructions are located here: https://chocolatey.org/install

## License

The code is licensed under the MIT license. You may use and modify all or part of it as you choose, as long as attribution to the source is provided per the license. See the details in the [license file](./LICENSE.md) or at the [Open Source Initiative](https://opensource.org/licenses/MIT).


<hr>
Copyright © 2024 Clean Coders Collaborative. All rights reserved.