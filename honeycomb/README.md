## Honeycomb Query Evals

Evals for for Honeycomb Natural Langaguge Query generator from the [Fine Tuning LLMs](https://maven.com/parlance-labs/fine-tuning) course. Related notebooks from the course can be found at <https://github.com/parlance-labs/ftcourse>.

The [queries.csv](queries.csv) dataset contains \~ 2,300 example queries (along with per-query column schemas generated offline via RAG). The evaluation tasks are implemented in [queries.py](queries.py), to evaluate a random subset of 200 queries using a variety of models:

``` bash
inspect eval queries.py --model openai/gpt-4-turbo --limit 200 
inspect eval queries.py --model hf/google/gemma-2b --limit 200 
inspect eval queries.py --model ollma/llama3 --limit 200
```

By default, scoring is done using the validity checker presened in the course (see [validate.py](validate.py)). You can instead use the [critique prompt](https://hamel.dev/blog/posts/evals/#automated-evaluation-w-llms) presented in the course by specifying the `critique` task parameter, for example:

``` bash
inspect eval queries.py --model ollma/llama3 --limit 25 -T critique=true
```