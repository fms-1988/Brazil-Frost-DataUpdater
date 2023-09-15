# GitHub Action to Collect Frost Data in Brazil

The National Institute of Meteorology (INMET) releases daily information about the intensity of frosts occurring in Brazilian municipalities. Here's what we've done:

1. **Data Collection**: Collect data from the specified site ([linked here](https://portal.inmet.gov.br/paginas/geadas#)).
2. **Data Organization**: Organize the collected data in an appropriate database format and store it in 'data/data.csv'.
3. **Automation with GitHub Action**: Create a GitHub Action that automatically updates this database every 15 days. This action runs the 'scraper.py' file to perform the update.

## Objective

Our goal is to keep this frost database continuously updated. This way, the data is available for various purposes, such as map creation.

