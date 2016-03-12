# interview-challenge

**A web API scavenger hunt, programmatically search for the next clue!**

----------

This is an interview-style coding challenge used by [redacted] to screen applicants.

This repository includes a web server that hosts the challenge. **You can run the server and solve the problem**.

![interview-challenge](https://cloud.githubusercontent.com/assets/5052422/7423470/12a31a68-ef5b-11e4-9cad-4203d7f1ffc3.png)

## Skills Tested

The solution requires a number of good intermediate level programming skills, including the following:

- API `requests` libraries
- custom request payloads and headers
- '404' error handling
- recursion
- traversing tree nodes
- normalizing data with typos, and
- general problem solving skills

In my own solution, in working with uncertainty, I leveraged the following:

- decorators
- local response caching, and
- monkey patching `requests` to be more specialized

## Description

This repository is the puzzle reverse-engineered from the ground up.  I wanted to post my solution, it's a good code sample. However, I feel a need to protect the company that's still using this to screen applicants, so by reverse-engineering the puzzle I'm able to hide their identity and hopefully not show up in related google search results.

**Note on programming languages:** The server and provided solution is in `Python` 2.7.  The actual puzzle is entirely web-based, you can solve the puzzle using any language you want. 

## Getting started

**Note:** If you get lost, there's a simple makefile with commands and description, take a look at it. Or type `make`

**Windows users:** The makefile is a minor convenience. Copy and paste the commands out of it, they should be familiar, e.g. `pip install -r requirements.txt`, `python migrate.py`, etc etc etc.

### Summary

1. clone the repo
2. `make setup` to install dependencies and optional dependencies
3. `make migrate` to create the JSON mock database
4. `make serve` and `make stop` to control the server
5. solve the challenge.
6. rage quit. `make solve` and `make-solve-clean` to see what a solution looks like.

### Install

```sh
git clone git@github.com:bionikspoon/interview-challenge.git && \
cd interview-challenge
mkvirtualenv interview # optional for virtual env users
make setup # pip install -r requirements.txt
```

If `redis` or `redislite` fails, don't worry about it.  There's a fallback option for caching.  `redislite` requires "python dev headers", google that phrase if you want to make it work.


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

and 

```sh
make solve-clean
```

`make solve-clean` is there simply to delete the cache file created by the solution.  Persistent caching got setup very early on, I was not sure if it part of the puzzle or not.  So that needs deleted to prove its actually solving the problem and not cheating.

## Credits

**Lead reverse-engineer** - **Manu Phatak** - bionikspoon@gmail.com

**Puzzle designers** - **[redacted]** - [redacted]@[redacted].com *Let's find a way to get you proper credit.*

# Good luck, have fun.
