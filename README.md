
EMIS XML SNOMED CONCEPT EXTRACTOR
===================================
Extract and categorise SNOMED codes from EMIS search exports as XML.

Features:
- Supports multiple XML files containing many search definitions.
- Produces an Excel workbook for each EMIS search.
- For each workbook, creates tabs for each codeset.
- Extracts child codes used in EMIS, unless excluded.
- Identifies inactive SNOMED concepts; providing updated IDs.

Instructions:
1. Set file paths on the right.
2. Need the 3 Microsoft Access databases? 
Obtain from NHS TRUD: search for 'SNOMED CT UK Data Migration Workbench' subscirbe and choose the latest version.
3. Place XML file(s) from EMIS in the XML directory.
4. Click 'Run'.

Debugging:
If the script is slow, ensure the databases have indexes configured.

Author:
Eddie Davison | eddie.davison@nhs.net | NHS North Central London ICB