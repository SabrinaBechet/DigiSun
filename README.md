
# Introduction
## DigiSun: a software to transform sunspot drawings into exploitable data
It allows to scan drawings, extract its information and store it in a database.
Copyright (C) 2019 Sabrina Bechet at Royal Observatory of Belgium (ROB)

This file is part of DigiSun.

DigiSun is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DigiSun is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DigiSun.  If not, see <https://www.gnu.org/licenses/>.

---------------
<br />

# Requirements and Installation
To run this version of Digisun, you will need:
* **Python 3.x** (tested on 3.9.1)
* **PIP** (should be installed automatically with Python)

Which can be downloaded and installed from https://www.python.org. <br />
You will also need the following libraries:

* pyqt5 
* pymysql
* configparser
* numpy
* pillow 
* shapely 

Which can be installed with PIP in a shell with the command:

`pip install pyqt5 pymysql configparser numpy pillow shapely`

**Note:** make sure you're installing packages for Python 3 and not 2, you can check this with:

`pip --version`

which should output something like:

`pip 20.3.1 from /usr/lib/python3.9/site-packages/pip (python 3.9)`

If you haven't already, clone this repository:

`git clone https://gitlab.com/locarno/digisun_2018.git`

<br />

# Running Digisun
After the installation of Python 3, Digisun and its dependencies (libraries), the program can be run in its folder (the one you cloned) as follows:

`python3 digisun.py`

Make sure you configure the settings for your use case in the file in `digisun_2018/data/digisun.ini`.
