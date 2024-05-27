## Honeycomb Query Evals

### Overview

Evals for for Honeycomb Natural Langaguge Query generator from the [Fine Tuning LLMs](https://maven.com/parlance-labs/fine-tuning) course. Related notebooks from the course can be found at <https://github.com/parlance-labs/ftcourse>.

The [queries.csv](queries.csv) dataset contains \~ 2,300 example queries (along with per-query column schemas generated offline via RAG). There are two scoring methods supported
(corresponding to the two @task definitions below):

1. @validate - score using the validity checker from the course (utils.py)
2. @critique - score using the critique prompt from the course (critique.txt)

### Eval Script 

Use the `inspect eval` command with the eval script ([queries.py](queries.py)) to run evals on a variety of models.

To evaluate all of the queries using both scorers on Claude Opus:

```bash
$ inspect eval queries.py --model anthropic/claude-3-opus-20240229
```

To evaluate a random subset of 200 queries using both scorers on GPT 4 Turbo:

```bash
$ inspect eval queries.py --model openai/gpt-4-turbo --limit 200
```

To use the validate scorer only with a local Google Gemma 2B (via HF):

```bash
$ inspect eval queries.py@validate --model hf/google/gemma-2b
```

To use the critique scorer only with a local Ollma Lllama3 model

```bash
$ inspect eval queries.py@critique --model ollma/llama3
```

See `inspect eval --help` for details on all available options.

### Eval Notebook 

There is a also a notebook version of the evals ([queries.ipynb](queries.ipynb)). Rather than using `inspect eval` as it done with the script, the notebook uses Inspect's `eval()` function to execute evals within the notebok runtime.