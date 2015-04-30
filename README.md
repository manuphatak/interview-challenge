# interview-challenge

**A web API scavenger hunt, programmatically search for the next clue!**

----------

This is an interview-style coding challenge used by [redacted] to screen applicants.

This repository includes a web server that hosts the challenge. **You can run the server and solve the problem**.

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

### Install

```sh
git clone git@github.com:bionikspoon/interview-challenge.git && \
cd interview-challenge
mkvirtualenv interview # optional for virtual env users
make setup # pip install -r requirements.txt
```

If `redis` or `redislite` fails, don't worry about it.  There's a fallback option for caching.  `redislite` requires "python dev headers", google that phrase if you want to make it work.


### Migrate

There is no actual database, `.json` is perfectly fine for this. The original puzzle likely used `MongoDB` and `migrate.py` simulates the results. The `json` file  is built and used by the server to serve pages.  The logic is dynamic, it can encode your own custom message.  

```sh
make migrate # python migrate.py
```

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

If you come with a wildly different or cleaner solution then my own, feel free to send a `pull request` with a name, I'm happy to add it in and give creds.

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