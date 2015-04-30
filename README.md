# interview-challenge
A web API scavenger hunt, programmatically search for the next clue!

This is an interview-style coding challenge used by [redacted] to screen applicants.

This repository includes a web server hosting the challenge that you can run and try to solve for yourself.

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

**Note on programming languages:** the server and my solution is in `Python` 2.7.  The challenge is entirely web-based, you can solve the puzzle using any language you want. 

## Description

This repository is the puzzle reverse-engineered from the ground up. Mostly, I wanted to post my solution, that simple. However, I feel a need to protect the company that's still using this to screen applicants, so by reverse-engineering the puzzle I'm able to hide their identity and hopefully not show up in related google search results.

## Getting started

**Note:** If you get lost, there's a simple makefile with commands and description, take a look at it.

Windows users: The makefile is a small convenience. Copy and paste the commands, they should be familiar, e.g. `pip install -r requirements.txt`, `python migrate.py`, etc etc etc.

### Install

```sh
git clone git@github.com:bionikspoon/interview-challenge.git && \
cd interview-challenge
mkvirtualenv interview # optional for virtual env users
make setup # pip install -r requirements.txt
```

If `redis` or `redislite` fails, don't worry about it.  There's a fallback option for caching.  `redislite` requires "python dev headers", google that phrase if you're interested.


### Migrate

Does not use an actual database, `.json` is perfectly fine for this.  Migrate builds the `json` file which is used by the server to serve pages.  The logic is dynamic, it will encode any message to be used by the `challenge_server.py`.  

```sh
make migrate # python migrate.py
```

### Server

```sh
make start
```

and 

```sh
make stop
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
make solve
```

and 

```sh
make solve-clean
```

This second option is there simply to delete the cache file it creates.  Persistent caching got setup very early on, I was not sure if it part of the puzzle.  So that needs deleted to prove its actually solving the problem and not cheating.

## Credits

**Lead reverse-engineer** - **Manu Phatak** - bionikspoon@gmail.com

**Puzzle designers** - **[redacted]** - [redacted]@[redacted].com Let's find a way to get you proper credit.

# Good luck, have fun.  