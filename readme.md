# 1. Create virtualenv
~~~
pip install --upgrade virtualenv
virtualenv .venv
*or*
python3 -m venv .venv
~~~
# 2. Actiavte virtualenv
~~~
make venv
~~~

# 3. Install dependencies
~~~
pip install -r requirements.txt
~~~

# 4. Run project locally
~~~
make run
~~~

# 5. Run project in docker
~~~
make docker-run
~~~


# See Makefile for more commands
~~~
make <tab>...
~~~

[Project TODO board](https://trello.com/b/GGgZzO2P/edu)
