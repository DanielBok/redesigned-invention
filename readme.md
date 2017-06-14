# Manual

## Conda setup

```
conda create --name <env> --file requirements.txt
```

Important to use a common environment when developing to ensure that we are all on the same page

## Initial Setup
```
activate <env>  # windows
source activate <env>  # mac / linux

python run.py -b  # build the local dashboard command
dashboard db reset  # resets and seed the database
```

Assuming you're in the environment `<env>` henceforth.

## Running
```
python run.py  # runs the application in local debug mode
dashboard test  # runs unit tests
dashboard test --cov  # runs unit tests with coverage
```

## Preparing for production
```
dashboard setup push_hook  # setup pre-push hook
dashboard setup freeze  # prints a heroku ready requirements.txt

git push <remote> <branch>
```

We set up the `prepush` hook to run all the unit tests before pushing to a cloud repo. This ensures that we don't push up stuff which have errors

We also have local packages which heroku cannot install. Thus we use the custom `freeze` command to simplify matters.
