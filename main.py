# TODO:
"""
* read about docker-compose networks.

1. Clean up code: Comments, unused imports(* use lib): python black, pylint, ...
1.1. Add make command or make some pre-commit hook (git hooks)


2. Adjust unit tests to match new module structure: handlers.



3. Add background tasks

--------------------------
4. Message brokers



"""


import uvicorn

if __name__ == '__main__':
        uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=4)
