Pronto Setup Documents
===

<!-- TOC -->

- [Setting up the application](#setting-up-the-application)
- [Downloading and Installing Conda](#downloading-and-installing-conda)
- [Checking Installation](#checking-installation)
- [Setting up the Environment](#setting-up-the-environment)
- [Installing the External Packages](#installing-the-external-packages)
- [Running the Development build](#running-the-development-build)
- [Other Information](#other-information)

<!-- /TOC -->


## Setting up the application

Please follow these steps to set up the application.

## Downloading and Installing Conda

Head over to [Conda](https://conda.io/miniconda.html) to download the latest version of Python. Download the Python 3.6 version based on your system. If you're unsure, you'll most likely need the Windows 64-bit version.

Conda is a package manager - in other words - it helps you manage all the background setup tasks related to the external libraries used relative to your system. This makes it simpler to use over the basic Python installation.

During installation, **REMEMBER to check the save conda to path option**.

## Checking Installation

Open your command prompt or terminal and go into the project's root folder. If you're on Windows, you can get the command prompt by:

1. Press \<Windows>+<R>
2. Type "cmd" into the box
3. Press \<Enter>
4. Type `cd PATH/TO/PROJECT/ROOT`

The project root folder is where you'll find this `Readme` document.

All commands that are typed are prepended with a `$` sign. If you installed the application correctly, type the following command. You should see the following output.

```
$ conda -V
conda 4.3.18
```

If the output is not something similar (an error), it is likely because you did not put/install `conda` into path just now.

## Setting up the Environment

After installing conda into your 
```
$ conda create --name <env> python=3.5

Example:
$ conda create --name SIA python=3.5
```

It is important to use a common environment when developing to ensure that we are all on the same page.

## Installing the External Packages

After creating the environment, we must go into that environment. To do so, type the following into the command prompt

```
Windows
$ activate <env>

Mac / Linux
$ source activate <env>

Example
$ activate SIA
```

To download all the external libraries that we use, type the following
```
$ conda config --append channels conda-forge --append channels anaconda
$ conda install --file requirements.txt
```

## Running the Development build

Before running the application, you'll need to do some minor setup. If you're running in production, you can skip this step. If you just want a demo version, we'll need to "seed" the database with some data, thus these steps.

```
$ python run.py -b
$ dashboard db reset
```
The first command creates locally some helper commands. The second command seeds the local database with some data. The second command will take a while to complete as we are pushing quite a lot of data (40Mb).

To run the development version of the application, type
```
$ python run.py
```

## Other Information

The test account credentials are as follows:
| User    | Username  | Password |
| :------ | :-------- | :------- |
| Manager | manager   | airport  |
| Driver  | driver0   | airport  |
| Driver  | driver`X` | airport  |

There are around 200 drivers. Thus you can use drivers from **driver0** to **driver199** for driver login.