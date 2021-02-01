## Intro
A toy website status checker testing the current state of async Kafka and Postgres integration.


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
   
   **Important**: when setting up Kafka, make sure to create these topics:
   * check_websites
   * write_website_status

5. Make sure `websites.json` contains the websites you want to check.

6. Start the website status check collection, write and trigger as separate process:
   ```bash
   ./bin/run_check.sh
   ```
   ```bash
   ./bin/run_write.sh
   ```
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


## Tech stack

It's a very simple website availability checker using async integrations with:
* `Kafka` (aiokafka)
* `Postgres` (asyncpg)
