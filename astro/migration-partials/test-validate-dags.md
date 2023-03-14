Determine a strategy to test and validate DAGs, and determine what DAGs will need more or less caution in being monitored and run.

Some workloads are idempotent and can easily run twice, or rerun.
Workloads that are non-idempotent and have state that can become invalid if they are rerun should be migrated with more caution and potentially downtime.
