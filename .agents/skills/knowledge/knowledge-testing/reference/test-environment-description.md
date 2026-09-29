## Environments
| Environment | Purpose | Host | Data set | Refresh | Access |
| --- | --- | --- | --- | --- | --- |
| local | Developer workstation | localhost | synthetic tree, 250k files | on demand | none |
| ci | Pull request verification | <CI_RUNNER_HOST> | fixture tree in repo | per run | CI service account |
| perf | Throughput benchmarking | <PERF_HOST_IP> | generated 5M-file tree | weekly | request via DEVEX-ACCESS |
| soak | Long-running stability | <SOAK_HOST> | mirror of perf | monthly | request via DEVEX-ACCESS |
|  |  |  |  |  |  |
| Connection string (perf) | <PERF_RESULTS_DB_CONNECTION_STRING> |  |  |  |  |
| Owner | QA lead - <QA_LEAD_NAME> (<QA_LEAD_EMAIL>) |  |  |  |  |
