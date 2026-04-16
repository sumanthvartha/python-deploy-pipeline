# python-deploy-pipeline

a simple flask task API with a full CI/CD pipeline — automated tests, docker, and gated deployments across dev/staging/prod using github actions.

built this to understand how deployment pipelines actually work end to end, not just the theory.

## what this does

- flask REST API (task manager — create, list, mark done)
- `/health` endpoint for pipeline smoke tests
- pytest unit tests, flake8 linting, bandit security scanning
- dockerized
- github actions pipeline with environment gates (staging needs lead approval, prod needs manager approval)

## the flow

```
write code → open PR → automated checks run (pytest/flake8/bandit)
→ peer review + approval → merge to develop
→ auto-deploy to dev → lead approves → deploy to staging
→ manager approves → deploy to production
```

if any gate fails, everything after it is blocked. i learned this the hard way when flake8 caught a missing newline and killed the whole pipeline lol.

## structure

```
|--- .github/workflows/deploy-pipeline.yml
|--- src/
│   |-- __init__.py
│   |-- app.py
|-- tests/
│   |-- __init__.py
│   |-- test_app.py
|-- Dockerfile
|-- requirements.txt
|-- README.md
```

## api

| method | endpoint | what it does |
|--------|----------|-------------|
| GET | /health | health check (smoke tests hit this) |
| GET | /api/version | returns api version |
| GET | /api/tasks | list all tasks |
| POST | /api/tasks | create task — send `{"title": "something"}` |
| PUT | /api/tasks/\<id\> | mark task as done |

## running locally

```bash
git clone https://github.com/sumanthvartha/flask.git
cd flask
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py
# hit http://localhost:5000/health
```

## running with docker

```bash
docker build -t task-api .
docker run -p 5000:5000 task-api
```

## running tests

```bash
pip install pytest flake8 bandit
pytest tests/ -v
flake8 src/ --max-line-length=120
bandit -r src/ -ll
```

## pipeline setup

the pipeline lives in `.github/workflows/deploy-pipeline.yml`. it has 4 jobs:

1. **ci checks** — runs on every PR. pytest + flake8 + bandit. fails = PR blocked.
2. **deploy to dev** — auto runs after merge to develop. builds docker image.
3. **deploy to staging** — pauses and waits for lead to approve in github.
4. **deploy to prod** — pauses again, waits for manager approval.

to set up the approval gates:
- go to repo settings → environments
- create `dev`, `staging`, `production`
- add required reviewers for staging and production
- also set branch protection on `develop` (require PR + status checks)

## things i ran into while building this

- put app.py in the wrong folder at first — `src/src/app.py` instead of `src/app.py`. pipeline couldn't find it. project structure matters more than you think.
- forgot to add a newline at end of files. flake8 blocked the entire pipeline over it. small things break real pipelines.
- bandit flagged `debug=True` as a high severity security issue — makes sense, you don't want a debugger exposed in production. fixed it with an env variable.
- port 5000 was already in use when i tried to run docker because flask was still running from earlier. had to kill the process first.
- created a PR targeting master instead of develop — pipeline didn't trigger because the workflow only watches develop and main.

none of these were "hard" problems but they're the exact kind of stuff that eats your time if you don't know what to look for.

