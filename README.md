

FUTURE:
maximize geometric mean of each intersection table (+1 to avoid 0s)?
AT LEAST USE GMEAN AS A METRIC FOR HOW CLOSE WE ARE TO IDEAL.. TO COMPARE DIFFERENT METHODS

**may still need to weigh different intersection tables, based on the number of dims
- consider the number of panel members..?

**with >4 dimensions all intersection sizes will be 0/1 anyway... detect those cases and ignore those intersection tables
- much better than the MAX_DIMS_INTERSECTION_TO_OPTIMIZE_ON limitation we have now.