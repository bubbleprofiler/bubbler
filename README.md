This is a Python interface to AnyBubble, BubbleProfiler and CosmoTransitions for solving
the bounce action.

```
>>> from bubbler import bubblers
>>> bubblers("0.1*((-x + 2)^4 - 14*(-x + 2)^2 + 24*(-x + 2))")
```

For plotting the profiles,

```
>>> from bubbler import profiles
>>> profiles("0.1*((-x + 2)^4 - 14*(-x + 2)^2 + 24*(-x + 2))")
```

This requires you to set paths to the codes

```
export PYTHONPATH=Absolute/Path/To/CosmoTransitions
export BUBBLEPROFILER=Absolute/Path/To/BubbleProfiler
export ANYBUBBLE=Absolute/Path/To/AnyBubble
```

The tests I shared before can be repeated by

```
python n_fields.py
python alpha_tests.py
```

NB I test against the develop branch of CosmoTransitions.
