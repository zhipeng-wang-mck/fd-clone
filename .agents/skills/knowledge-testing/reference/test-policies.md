# Test Policies

## Mandatory tests by change class

| Change class             | Required                          |
|--------------------------|-----------------------------------|
| Filter or matcher logic  | unit plus integration             |
| Traversal or concurrency | unit, integration, and a perf run |
| Output formatting        | unit plus snapshot                |
| Documentation only       | none                              |

## Coverage thresholds

Line coverage must not fall below 80 percent on the filter and walk modules. Branch coverage must not fall below 70 percent overall. A pull request that lowers either figure is rejected.

## Performance criteria

A traversal of the 5M-file perf tree must complete within 12 seconds. Regressions above 5 percent against the previous release block the merge.

## Regression scope

The full integration suite runs on every release branch. Snapshot tests for colour output run on Linux and macOS only.

## Exit criteria

No open critical or high defects. All mandatory suites green. Perf run within budget.
