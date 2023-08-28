def header():
   return """EMIS XML SNOMED CONCEPT EXTRACTOR
==================================="""
def content():
   return  """Extract and categorise SNOMED codes from EMIS XML search exports to Excel.

Features:
- Supports multiple XML files containing many searches.
- Produces an Excel workbook for each EMIS search.
- For each workbook, creates tabs for each set of codes.
- Extracts child codes recursively, unless excluded.
- Identifies inactive SNOMED concepts, providing updated IDs.

Instructions:
1. Set file paths to specify:
    - `XML Input Directory`: Where you will drop `.xml` files.
    - `DMWB NHS SNOMED.mdb`: Contains descriptions, concepts, and terms.
    - `DMWB NHS SNOMED Transitive Closure.mdb`: Contains relationships.
    - `DMWB NHS SNOMED History.mdb`: Maps inactive concepts to new concepts.
    - `Output Directory`: Where Excel workbooks and `log.txt` will be saved.
2. Obtain databases above from NHS TRUD if you haven't.
3. Place XML file(s) from EMIS in the XML directory.
4. Click 'Run'.

Debugging:
If the script is slow, ensure the databases have indexes configured.

Notes:
The program does not match concept IDs for EMIS Drug Groups or library items. 
For such cases, you can typically use QOF or PCD refsets to find these codes.

Author:
Eddie Davison | eddie.davison@nhs.net | NHS North Central London ICB
"""