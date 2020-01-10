# TeXerBase Exercise Database

## What is this?

TeXerBase is a database to create and manage exercises.

Exercises have to be coded in Markdown with the special enhancement, that you can write Formulas in TeX/LaTeX, resolvind the problem that formulas are not natively supported by Markdown.

You could write this code for an exercise:

```
### $pq$-formula

1. Describe what the $pq$-Formula $x_{1,2} = -\frac{p}{2} \pm \sqrt{(\frac{p}{2})^2-q}$ is for.
2. Solve the quadratic equation $f(x)= 3x^2 - 2x + 1$
```

Unfortunately GitHub doesn't allow html in this readme so I can't show you the result here :-(

In addition to assistin you in creating your exercises TeXerBase will manage your solution as well as some meta-information like the source, the license, author, skill-level and, most important, lets you categorize your exercises in subjects and topics.

## Just need LaTeX-Support in Markdown?

Just check out the `modules/mdTeX2html.py`-file that uses the `latex2mathml`-python-library.

You can also use the entire thing, the TeXerBase-Server will return HTML with MathML for any Markdown-TeX-Mixture send to `<server>/mdtex2html` with a `POST`-Request. By default your `<server>` will be `localhost:8081`.

Have a Look at the file `template\cheatsheetMdTeX.tpl` for reference or run TeXerBase and see the sandbox in `<server>/cheatsheetMdTeX`).

## Installation and running

- clone the repository
- make sure the external __dependencies__ are installed:
  - python3.7 and up (comes with Ubuntu 19.10 and up, not default in Ubuntu 18.04!)
  - python3-jinja2
- run `TeXerBase.py`
- point your browser to `localhost:8081`

### customize subjects and topics

The structure is in the file `structure.yaml` which can be changed to your needs. Just make sure you __don't change any subjects or topics afer your first run__, since they are included, but not removed to your database on startup! __Adding new subjects and topics is fine__ though.

## Limitations

- It's in german Language so far - let me know if you want to make a translation!
- the browser needs to support `MathML`
- only SqLite-Database supported, but feel free to add i.e. `postges`-support to the `modules/dbio.py` and the `modules/dbInit.py` if you need it to scale.
- for secure/limited/external access I recommend using `nginx` as reverse proxy

## Further Ideas

Maybe I will extend TeXerBase in the future, depending on my needs, with some of the following:

- allow formulas in `\[ \]` and `\( \)`- enviroments in addition to the already supported `$ $` and `$$ $$`-environments
- include an option to assemble handsets of exercises
- ...tell me about your ideas or make a nice pull-request!
