# Baseball Data Sorting

## Instructions:

### To run:
`python run.py`

### To test:
`pip -m pytest test_run.py`

### Requirements:
`setuptools==36.5.0.post20170921
pytest==3.0.6
pandas==0.20.3`

## Terminology
1. **Subject**: A field that is grouped on; analogous to SQL's "GROUP BY"  
clause.  
2. **Split**: A filter used to restrict a dataset; analogous to SQL's "WHERE"  
clause.  
    * **vs LHH**: "versus left-handed hitters"  
    * **vs RHH**: "versus right-handed hitters"  
    * **vs LHP**: "versus left-handed pitchers"  
    * **vs RHP**: "versus right-handed pitchers"  
3. **Stat**: A metric that is calculated from the aggregated data. There are  
four basic stats to be calculated that should be familiar to any baseball fan.
    * AVG
    * OBP
    * SLG
    * OPS


