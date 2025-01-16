# As a user I should

## MVP

### data import
- be able to download an excel custom nrrm report and provide it as input to the application to store in a db
  - The report should be able to be variable meaning it might not have all the fields but should be able to update the fields it does have.
- process that data against the current data to drive actionable insights
  - did anything change?  Did we lose a sailor? Did we gain a sailor? Did any sailor fields change?
    - ```DODID```
- we preserve old data so that we can look at a sailor profile and observe changes over time

### Unit Metrics

#### Warfighting Readiness
- be able to see overrall deployability metrics based on the nrrm individual deployability status broken down by CAI/CAO/Local/IAP`
  - ```deployability```
- able to see overrall medical readiness metrics based on the nrrm individual deployability status broken down by CAI/CAO/Local/IAP
  - ```medical readiness```

### Individual Metrics
- be able to see and individual profile including historical values to identify changes over time.

### Actions
- be able to identiy actions based on the data changes
  - did we lose a sailor?  We owe that sailor a transfer eval.  
    - identified as a pending action item until completed
  - did a sailor phone number change in nrrm?  We might need to update the recall list
  - did we gain a sailor?  We owe that sailor a call from our sponsorship coordinator

### Reporting
- how do we get these reports and metrics into the hands of decision makers
  - email report bi-weekly?
  - last updated date for clarity and emails can run on regular cadence?
    - timestamp on unit-metric-snapshot table


### DB Design
#### tables
- sailor
  - dodid (PK)
  - last-name 
  - first-name
  - deployability
  - medical-readiness
  - prd
- sailor-historical
  - timestamp (PK)
  - dodid (PK, references(sailor(dodid)))
  - last-name 
  - first-name
  - deployability
  - medical-readiness
  - prd
- sailor-loss
  - dodid (PK, references(sailor(dodid)))
  - nrrm-loss-date
  - action-pending
- sailor-gain
  - dodid (PK, references(sailor(dodid)))
  - nrrm-gain-date
  - action-pending
- unit-metric-snapshot
  - timestamp (PK)
  - cai-count
  - local-count
  - cai-deployability-fd-count
  - cai-deplyability-pd-count
  - cai-deployability-nd-count
  - local-deployability-fd-count
  - local-deployability-pd-count
  - local-deployability-nd-count
  - cai-medical-fd-count
  - cai-medical-pd-count
  - cai-medical-nd-count
  - local-medical-fd-count
  - local-medical-pd-count
  - local-medical-nd-count
