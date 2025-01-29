# Introduction

Accessing AI has never been easier than it is today - this site is here to help you get started, both for the novice and the eager coder. This is, however, mainly an introduction and a way to get started - there's plenty of resources available if you have already started using AI.

# QR code to get here

![QR code!](gettingstarted_github.png "QR code to get to this page")

# Easiest to use - online general AI

## [ChatGPT](https://chatgpt.com/) 

OpenAI's ChatGPT is likely the most well known and easily accessible AI. It has the advantage of being meant for natural language use, so you can literally just chat away with it and ask it to do things for you, and it will most likely work.

It is also very capable, and can process text in various ways (and generate images if logged in), and doesn't require a login/account to use (although free use will be restricted in some ways).

## [Copilot](https://copilot.microsoft.com)

Microsoft's Copilot is similar to ChatGPT, having free access to text processing but requires an account to do image processing. It's currently considered to be slightly less capable than ChatGPT, but do have a lot of code-based knowledge thanks to Microsoft's purchase of GitHub.

## [DeepSeek](https://chat.deepseek.com/)

New challenger to ChatGPT from a Chinese firm. Astoundingly powerful in spite of not allegedly not having the huge budget that ChatGPT has had.

NOTE: *Requires* registration, but not payment.

# Online specialized AI

## [Claude](https://claude.ai/)

Claude is meant to help with software development assistance, and has an interface that reflects that (being better at handling a workspace with several files etc).

Can be used for adjacent tasks - for instance to create an HTML presentation, including populating the content. It is good at creating new projects from natural language, but can not be used to edit a project forever - it will eventually run out of 'memory' (or tokens, as it's called in the AI world).

NOTE: *Requires* registration, but not payment.

## [Cursor](https://www.cursor.com)

Another AI that is intended to help with software development, and is more of an auto-complete and analysis tool than a natural language project maker.

NOTE: *Requires* registration, but not payment - free account is time limited.

# Local AI

## [LM Studio](https://lmstudio.ai/)

LM Studio is an easy way to get started with running AI on your local computer - just go to the site and install the program, choose the default (pretty small) model and then start typing away to it.

Do note that a local AI tends to require a lot more care and feeding than the online versions, but has the advantage of allowing you full control of what you request out of it.

NOTE: Entirely free, and no data leaks out from your computer.

## [Fooocus](https://github.com/lllyasviel/Fooocus?tab=readme-ov-file#download)

Local image generation with a simple web-based UI. The prompt to generate images is more technical, a bit fiddly and less natural than using the online general AI tools; the benefit being better control over the actual prompt and being able to manipulate the tools directly using e.g. image prompts or LoRA:s.

NOTE: Entirely free. Can result in NSFW images.

## Python installation

For the refined developer who's willing to invest time and effort. 

This section is under development, but a starting point is to install Python 3.12 (not 3.13).

Grab this git repository by cloning it like this:

`git clone https://github.com/cmanderskronquist/getting_started_with_ai.git`

Then swap to the text summarizer demo directory:

`cd getting_started_with_ai/python_text_summarizer`

Set up the python virtual environment:
`python -m venv env`

Depending on whether you are on Windows or Unix, use the proper command from below:

`.\env\Scripts\activate`
or

`source ./env/bin/activate`

Run the following to get the packages needed in the virtual environment:

`pip install transformers sumy torch torchvision torchaudio`

And finally run the summarizer on the supplied text file:

`python transformer_summarize.py king_in_yellow_chapter_1.txt`

# General guidelines when using AI

Current generation AI is just large language models who takes in input and generate output. This means that while the output can look reasonable, and even look well-reasoned (if a text), it is in fact just text from a program *that does not itself know what it is writing*. 

You, as the user of an AI, have to check its output. This can cause problems if setting up AI programmatic responses, such as chatbots or knowledge agents, which are used by people without knowledge of how AI works and its limitations.

In short, trust but verify. Most available AI is not designed to lie to you, but they are often made to answer questions even if the questions are in areas in which the AI lacks good data - very few models of AI are designed to outright stop their processing when they reach areas that are beyond their scope and training data. This leads to what is called "AI hallucinations" but the important point is that for the AI there is no real difference between a good answer and a hallucination.

# IP / immaterial rights / lawyer

Using AI in your day to day business can lead to the business being liable for actions taken by the AI.

A useful site to check out in regards to AI governance is [anch.ai](https://anch.ai/).

[IBM has an AI offering](https://www.ibm.com/watsonx), which can provide some limited liability when used out of the box.
