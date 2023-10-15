# bRAG [WIP]
bRAG is an example repo how you can do Basic Retrieval Augmented Generation the alternative way. 
No langchain. No ORMs. No alembic/migration generation tools.
Instead we go with PDF. What in the world? pugsql, dbmate & fastapi. That's it. 

More coming.

Or to be more precise, we will use:

1. [plain python openai](https://github.com/openai/openai-python) client to interact with our LLM
2. [qdrant](https://qdrant.tech/) as our vector database of choice and their [client](https://github.com/qdrant/qdrant-client).
3.  For the embeddings we will use ~~openai~~ Qdrant's [fastembed](https://github.com/qdrant/fastembed) lib. 
4. the API will be written using [fastapi](https://github.com/tiangolo/fastapi)
5. no ORM for us, instead we will roll with [pugsql](https://github.com/mcfunley/pugsql)
6. migrations will be done using plain sql and [dbMate](https://github.com/mcfunley/pugsql).
7. instead of poetry, we will go for [pyenv](https://github.com/pyenv/pyenv) + [pip-tools](https://github.com/jazzband/pip-tools)
8. on the db front - [postgres](https://www.postgresql.org/)
9. lastly, the app will be containerised - [docker](https://www.docker.com/)

Does that sound weird to you? Because it is! Even more fun.

## Basics

### One click deployment
```bash
docker-compose up
```

### local development for the api + db & vdb in docker
```bash
docker-compose up -d database qdrant
make run-dev
```
that's it. Then head over to http://localhost:8000/docs to see the swagger docs.

To get run-dev working proceed through the following steps:

To start, let's make sure you have pyenv installed. What is pyenv? You can read a bit about it on my blog.
[Pyenv, poetry and other rascals - modern Python dependency and version management.](https://grski.pl/pyenv-en)

Long story short it's like a virtualenv but for python versions that keeps everything isolated, without polluting your system interpreter or interpreters of other projects, which would be bad. You don't need to know much more than that.

If you are on mac you can just 
```bash
brew install pyenv
```

or if you do not like homebrew/are linux based:

```bash
curl https://pyenv.run | bash
```

Remember to [set up your shell for pyenv.](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)..
In short you have to add some stuff to either your `.bashrc`, `.zshrc` or `.profile`. Why? So the proper 'commands' are available in your terminal and so that stuff works. How?

```bash
# For bash:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# For Zsh:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```
Done? Now you just need to get pyenv to get python 3.11 downloaded & installed locally (no worries it won't change your system interpreter):

```bash
pyenv install 3.11
```
When you are done installing pyenv, we can get going.

We will name our project **bRAG** - the name coming from **b**asic **R**etrieval **A**ugmented **G**eneration API.
First of all, let's create a directory of the project:

```bash
mkdir bRAG
cd bRAG
```

Now we can set up a python version we want to use in this particular directory. How? With pyenv and pyenv-virtualenv, which is nowadays installed by default with the basic pyenv installer. If you need to, check the article I referred before to understand what's happening.

```bash
pyenv virtualenv 3.11 bRAG-3-11  # this creates a 'virtualenv' based on python 3.11 named bRAG-3-11
pyenv local bRAG-3-11
```

after that just install stuff from requirements.txt.


## Project structure

The file structure is:
```
 |-- app/  # Main codebase directory
 |---- chat/
 |------ __init__.py
 |------ api.py
 |------ constants.py
 |------ message.py
 |------ models.py
 |------ streams.py
 
 |---- core/
 |------ __init__.py
 |------ api.py
 |------ logs.py
 |------ middlewares.py
 |------ models.py
 
 |---- __init__.py
 |---- db.py
 |---- main.py
 
 
 |-- db/  # Database/migration/pugsql related code
 |---- migrations/
 |---- queries/
 |---- schema.sql
 
 |-- settings/  # Settings files directory
 |---- base.py
 |---- gunicorn.conf.py
 |-- tests/  # Main tests directory
 |-- requirements/
 
 |-- .dockerignore
 |-- .env.example
 |-- .gitignore
 |-- pre-commit-config.yaml  # for linting in during development
 |-- docker-compose.yml
 |-- Dockerfile
 |-- Makefile  # useful shortcuts
 |-- README.md
```
