
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
1. Launch `EMIS XML SNOMED CONCEPT EXTRACTOR.exe`
2. Set file paths to specify:
    - `XML Input Directory`: Where you will drop `.xml` files.
    - `DMWB NHS SNOMED.mdb`: Contains description IDs, concepts, and terms in SNOMED-CT.
    - `DMWB NHS SNOMED Transitive Closure.mdb`: Contains parent-child relationships.
    - `DMWB NHS SNOMED History.mdb`: Contains a list of inactive SNOMED concepts with updated IDs.
    - `Output Directory`: Where Excel workbooks and `log.txt` will be saved.
3. Obtain databases from [NHS TRUD] if you haven't.
4. Place XML file(s) from EMIS in the XML directory.
5. Click 'Run'.

Debugging:
If the script is slow, ensure the databases have indexes configured.

Notes:
- The program does not match concept IDs for EMIS Drug Groups or library items. For such cases, you can typically use QOF or PCD refsets to find these codes.

Author:
Eddie Davison | eddie.davison@nhs.net | NHS North Central London ICB
Copyright (C) 2023 - Eddie Davison

Licensing:
This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License v3. See [license.txt](./license.txt) or [GNU Licenses](https://www.gnu.org/licenses/) for full details..