## Intro
A toy website status checker testing the current state if async Kafka and Postgres integration.


## How to run

1. Make sure you have Python 3.8 installed, and you are in the project root folder.

2. Create and activate a virtual environment

   With the builtin `venv` module
   ```bash
   python3 -m venv ~/venvs/website-status
   source ~/venvs/website-status/bin/activate
   ```

   or with `virtualenv`
   ```bash
   mkvirtualenv website-status
   workon website-status
   ```

3. Install the dependencies and the project:
   ```bash
   pip install -r requirements.txt
   inv install
   ```

4. Create a `.env` file based on the `env_example`:
   
   This requires a Kafka and Postgres service running somewhere.
   [Aiven](https://console.aiven.io) is a great choice for this!

5. Make sure `websites.json` contains the websites you want to check.

6. Start the website status check collection process:
   ```bash
   ./bin/run_collect.sh
   ```

7. Start the website status check trigger process:
      ```bash
   ./bin/run_trigger.sh
   ```

You should see in your Postgres database the result of the status checks!


### Run code quality checks

```bash
inv check
```

### Run the tests

1. Install the dev requirements:
    ```bash
    inv deps
    ```
2. Run the tests with coverage report:
    ```bash
    inv test
    ```
3. Run the tests without coverage report:
    ```bash
    inv test --no-coverage
    ```

## Deploy on Heroku

1. Install Heroku CLI
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```
2. Login to Heroku
```bash
heroku login
heroku container:login
```

3. Create the Heroku app and database
```bash
heroku create website-status
```

4. Push & release the image to Heroku
```bash
heroku container:push worker --recursive --app website-status
heroku container:release woker --app website-status
```

## Tech stack

It's a very simple website availability checker using async integrations with:
* `Kafka` (aiokafka)
* `Postgres` (asyncpg)
