Since I wanted to learn languages ​​based on frequency lists, this repository documents my process of refining prompt-generation methods to design effective data for LLM-based RAG systems.

Below are two examples of frequency list outputs—one for English and one for Chinese—that I have created.

[English_learning.txt](https://github.com/chungngocthien/vocab-explorer/blob/main/english_learning.txt)
Example: 1: to, 2: is, 3: was, 4: work, 5: those, 6: every, 7: another, 8: next, 9: means, 10: started,...

[Chinese_learning.txt](https://github.com/chungngocthien/vocab-explorer/blob/main/chinese_learning.txt)
Example: 1: 的, 2: 是, 3: 在, 4: 不, 5: 我, 6: 一, 7: 有, 8: 这, 9: 他, 10: 个,...

Currently, I am studying effectively by feeding information into NotebookLM, which also allows me to compile a collection of prompts for future review.

I plan to identify tags related to the learning process. So far, I have established an English-learning taxonomy comprising: [KNOWLEDGE_CONSTRUCTION]
[RETRIEVAL_INTERLEAVED_RECOMBINATION]
[SCENARIO_SITUATED_ROLEPLAY_INJECTION]
[AFFECTIVE_TONE_VARIANT_MAPPING]
[LEXEME_BOUND_USAGE_SET]
[L1_SYNTAX_SCAFFOLD_SUBSTITUTION]
[VARIABLE_ISOLATION]

If you would like to see how I derived the algorithm, you can copy the content from [narrative-log.md](https://github.com/chungngocthien/vocab-explorer/blob/main/narrative-log.md) and have any LLM analyze it; it will explain how I created these two files. You can also provide the content to an AI agent—such as GLM—to execute the file generation.
