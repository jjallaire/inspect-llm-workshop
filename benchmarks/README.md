## Benchmarks

This directory contains evals for several benchmarks. Note that some benchmark datasets are included in the `datasets/` directory and some are downloaded from Hugging Face (you should be sure to `pip install datasets` before attempting to run these benchmarks).

| Benchmark                                                          | Reference                          |                             Code | Dataset      |
|-----------------------------|---------------|--------------:|---------------|
| MMLU: Measuring Massive Multitask Language Understanding           | <https://arxiv.org/abs/2009.03300> |               [mmlu.py](mmlu.py) | Local        |
| MATH: Measuring Mathematical Problem Solving With the MATH Dataset | <https://arxiv.org/abs/2103.03874> | [mathematics.py](mathematics.py) | Local        |
| GPQA: A Graduate-Level Google-Proof Q&A Benchmark                  | <https://arxiv.org/abs/2311.12022> |               [gpqa.py](gpqa.py) | Hugging Face |
| ARC: AI2 Reasoning Challenge                                       | <https://arxiv.org/abs/1803.05457> |                 [arc.py](arc.py) | Hugging Face |
| GSM8K: Training Verifiers to Solve Math Word Problems              | <https://arxiv.org/abs/2110.14168> |             [gsm8k.py](gsm8k.py) | Hugging Face |