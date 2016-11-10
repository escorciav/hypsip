# HypSip

Welcome to HypSip!!!

It's a minimal set of tools simplify the creation of a wrapper around your python program.

> *Reader*: Why would you do that?

In short, hyper-parameter search in a distributed scenario where you submit your jobs to a head-node.

> *Reader*: feeling it... Does it creates the wrapper based on my program?

Unfortunately, it does not do that (yet or maybe never).

Certainly, it id possible with a little bit of template and/or functional programming.
I did not intend that when I wrote the code.
I thought that it could be possible at the cost of adding an abstraction for some cases.
I still do not know the cases that I should to target so I just *keep it simple* :smile:.

> *Reader*: What does it do?

It provides templates and a couple of utilities in order to write your wrapper for hyper-parameter search with minimal effort.

> *Reader*: OK. I'm in. What should I do?

Check the [simple wrapper](example/wrapper_simple.py) using our tools for a [simple program](example/simple.py).
Do you have a program that needs similar [resources]()?
Let's say [this one](example/simple_similar.py), go ahead and try to write a wrapper for it (call it *new_wrapper.py*).

As you may notice, by copy-paste the example and replace [these lines]() with the functions of the new program. You did it.

> *Reader*: What did I suppose to do?

You create your wrapper! Run it in "generator" mode:

```bash
python new_wrapper.py gen
```

Check your execution folder, you just created a bash file for your scheduler.
Submit it and you will explore hyper-parameters for a [simple program](example/simple_similar.py).

> *Reader*: Where is the catch?

There is not catch :stuck_out_tongue_winking_eye: ... OK, you have to use [argparse]() to simplify things out. After that, it's just:

1. Identify a template for the scheduler in your head-node.

2. Replace [this line]() with the template that you found.

3. Replace [this line]() with the argument parser of your program.

4. Replace [this line]() with the main of your program.

5. Run it and check that you are not using the same name for multiple variables after merging all the parsers :blush:.

> *Reader*: Where should I define my hyper-parameters?

Hyper-parameters are defined in a JSON-file similar to [this]().

The search strategy is random search and you define the sampling of your hyper-parameters.
You can reproduce your search by seeding the random number generator.

So far, you can perform uniform sampling from a list of values or sampling from a distribution of [scipy.stats.distributions]().

In our examples, the wrapper just reads this file in "execution" mode. In "generator" mode, it stamps it in the bash script of your scheduler. It is your wrapper so you can define whatever behavior.

> *Reader*: What does it mean HypSip?

It's kind of hyper-parameter + gossip. BTW, there is not too much gossip in our execution. The only gossip source is the head-node who talks about your program in different ways.
