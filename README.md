# interview-challenge

**A fun web API scavenger hunt and brain teaser. Programmatically search for the next clue!**

----------

This is an interview-style coding challenge used by [redacted] to screen applicants.

This repository includes a web server that hosts the challenge. **You can run the server and solve the problem**.

![interview-challenge](https://cloud.githubusercontent.com/assets/5052422/7423470/12a31a68-ef5b-11e4-9cad-4203d7f1ffc3.png)

## Skills Tested

The solution requires a number of good programming skills, including the following:

- API `requests`
- custom request payloads and headers
- error handling
- recursion
- traversing tree structures
- sanitizing data with typos, and
- general problem solving skills

In my own solution, in working with uncertainty, I leveraged the following:

- decorators
- local response caching, and
- monkey patching `requests` to be more specialized

## Description

In this repository I reverse-engineered from the ground up a puzzle I found on the internet..

**Note on programming languages:** The server and provided solution is in `Python`.  The actual puzzle is entirely web-based, you can solve the puzzle using any language you want.

## Getting started

**Note:** If you get lost, there's a simple makefile with commands and description, take a look at it. Or type `make`


### Summary

1. clone the repo
2. `make setup` to install dependencies and optional dependencies
3. `make migrate` to create the JSON mock database
4. `make serve` and `make stop` to control the server
5. solve the challenge.
6. rage quit. `make solve` to see what a solution looks like.

### Install

```sh
git clone git@github.com:bionikspoon/interview-challenge.git && \
cd interview-challenge
brew install poetry
make setup # poetry install
```


### Migrate

Create a JSON document to serve page data.

```sh
make migrate # python migrate.py
```

There is no actual database, `.json` is perfectly fine for this. The original puzzle likely used `MongoDB`.  `migrate.py` creates a json file that mocks the original structure. Once the `json` file  is built, the server can use it serve pages.  The logic is dynamic, it can encode your own custom message.

### Server

```sh
make start # python challenge_server.py
```

and

```sh
make stop # curl -X POST http://127.0.0.1:5000/shutdown
```
Hopefully self explanatory.

**Note:** `make start` runs the server in the background using `&`, this hangs the line, hit `return` to get your prompt back.

`make stop` cleverly sends a `curl` post request to the server to shut it down.

### Solve the puzzle

Navigate your browser to: `http://127.0.0.1:5000/`

There's not much there.  But it's all you get, so **good luck**.

If you come up with a wildly different solution, a cleaner solution, or you do it in a different language, definitely share it. Send a `pull request` with a named file, and add yourself to the credits. Make up a title for your role--just make sure it sounds slightly less important then mine `:)`. Kidding, you can be CEO of the ninja convention, but you have to solve the puzzle--honor system.  I'm happy to add it, give 'creds'.

### Run the included solution

```sh
make solve # python solution/solution.py
```

## Credits

**Lead reverse-engineer** - **Manu Phatak** - bionikspoon@gmail.com

**Puzzle designers** - **[redacted]** - [redacted]@[redacted].com *Let's find a way to get you proper credit.*

# Good luck, have fun.
