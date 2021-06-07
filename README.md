# Test Management System Intro

Test Management System (TMS) is a set of a web application (TMS App) where you can manage your test cases, plus a Python library (TMS Bus) which can hook your test suite up with TMS App. After TMS Bus is correctly used in your test suite, your test information (test name, date, result, log, etc) will be populated into TMS App DB automatically during your tests run so you can read and manage your tests easily via TMS App UI in real time.

# Test Management System Architecture

```
--- UI ---                           ---- import to ---
|         |                         |                  |
| TMS App | <--- RESTful API --- TMS Bus <--- Your Test Suite 
|         |
--- DB ---
```

# Setup

1. Clone this TMS repository to your local environment 

2. Create Python3 virtual environment in TMS root directory  

3. Install all dependencies in requirements.txt


