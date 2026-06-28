# Metadata-Extraction-Tool


🎯 Objective

To automate the discovery and analysis of embedded file metadata for use in digital forensics, incident response, and reconnaissance. Manual extraction using multiple tools (ExifTool, pdfinfo, etc.) is tedious and inconsistent. This tool provides a unified, automated pipeline that:

    Recursively scans files and directories.

    Extracts metadata from over 100+ file formats (JPEG, PNG, PDF, Office documents, audio, video).

    Flags high‑value artifacts (GPS coordinates, author usernames, software versions).

    Presents findings in a structured, searchable JSON format for easy integration with SIEMs, case management systems, or investigation reports.

🧠 How It Works – Technical Overview

The tool is built around the industry‑standard ExifTool by Phil Harvey—a powerful, battle‑tested metadata library. The Python script acts as a wrapper that:

    Accepts Input – A single file, a folder, or a glob pattern.

    Iterates Recursively – Walks through directories, processing each file.

    Calls ExifTool – Invokes exiftool -j <file> to extract metadata in JSON format.

    Parses & Normalises – Converts the raw JSON into a consistent schema, handling missing fields gracefully.

    Enriches & Flags – Applies heuristics to detect and highlight potentially sensitive or interesting fields (e.g., GPSLatitude, Creator, Company, LastModifiedBy).

    Exports Report – Saves a timestamped JSON report for the investigator.

Because ExifTool supports hundreds of file formats, this tool can handle everything from JPEG images to complex Microsoft Office documents, PDFs, and even audio/video containers.
✨ Advanced Features (Real‑World Upgrade)
Feature	Implementation
Batch Processing	Scans entire directories recursively – ideal for large‑scale data seizure reviews or pentesting engagement file dumps.
ExifTool Integration	Leverages ExifTool’s extensive format coverage (over 100 file types), ensuring consistent extraction across diverse file sets.
Sensitive Data Flagging	Automatically highlights and prioritises high‑value metadata: GPS coordinates, author usernames, organization names, software versions, and file editing history.
Structured JSON Output	Exports all findings to a timestamped JSON file, suitable for ingestion into Elasticsearch, Splunk, or custom analysis pipelines.
GeoIP Enrichment (Optional)	If GPS coordinates are found, the tool can optionally perform a reverse geocoding lookup to provide a human‑readable address (e.g., "London, UK").
Hash Calculation	Computes MD5, SHA1, and SHA256 hashes of scanned files to maintain forensic integrity and enable correlation with threat intelligence feeds.
Risk Scoring	Assigns a "Privacy Risk Score" to each file based on the presence of sensitive metadata (e.g., GPS + Author + Software Version = HIGH risk).
Stealth Mode	Can be run without writing any files to disk (stream output) for covert reconnaissance during pentesting.
🔬 Testing & Use Case

Scenario:
A penetration tester has been granted access to a corporate file share. They want to quickly identify which documents might contain sensitive employee information, internal network details, or software version information that could be used for targeted attacks.

Process:

    Run the tool against the file share:
    bash

python3 metadata_hunter.py /mnt/fileshare --gps --hash

    Scanning results:

        Invoice_2025.pdf → Extracted Author: John Smith, Company: Acme Corp, Software: Adobe Acrobat 10.1 (outdated, potentially vulnerable).

        Office_Photo.jpg → Extracted GPS: 40.7128° N, 74.0060° W (exact office location).

        Project_Plan.docx → Extracted LastModifiedBy: Admin, Total Edit Time: 47 hours.

        Internal_Network_Diagram.png → Extracted Creation Date: 2024-03-15, Software: Microsoft Visio 2021.

    Flags raised:

        HIGH Risk: GPS data found in Office_Photo.jpg – exposes physical office location.

        MEDIUM Risk: Outdated Adobe Acrobat version in Invoice_2025.pdf – suggests potential vulnerability.

        HIGH Risk: Internal_Network_Diagram.png contains internal network details – should not be accessible to all users.

Outcome:

    The penetration tester uses this intelligence to:

        Target Admin accounts (identified from document metadata).

        Exploit the outdated Adobe Acrobat version if discovered on a target system.

        Use GPS coordinates to tailor a phishing campaign with location‑specific references.

    The system administrator, upon reviewing the same report, initiates a data classification policy to remove metadata from externally shared documents and revoke access to sensitive files.

🛠️ Tools & Technologies

    Python 3 – core logic, file system interaction, and JSON generation.

    ExifTool (by Phil Harvey) – the underlying metadata extraction engine.

    subprocess – for invoking ExifTool from within Python.

    hashlib – for calculating file hashes (MD5, SHA1, SHA256) to maintain forensic integrity.

    json – for structured data export.

    requests – (optional) for reverse geocoding of GPS coordinates.

📁 Output Example (JSON Structure)

A typical report entry for a single file contains:

    Filename – The file name and path.

    File Size – In bytes.

    Hashes – MD5, SHA1, SHA256 (if enabled).

    Metadata – Full set of extracted fields (Author, Company, GPS, CreationDate, etc.).

    Risk Tags – List of flagged items (e.g., GPS present, Author name found, Outdated software).

    Risk Score – Numerical score indicating overall sensitivity.

📝 Conclusion

The Metadata Extraction Tool is a powerful addition to any digital forensics, incident response, or penetration testing toolkit. It transforms the tedious manual process of inspecting metadata into a fast, automated, and repeatable workflow. By surfacing hidden data such as author identities, GPS coordinates, and software versions, it provides critical context for investigations and adversarial reconnaissance. During testing, it successfully extracted sensitive metadata from a variety of file types, highlighting its versatility and real‑world applicability. It is a clear demonstration of how OSINT techniques can be automated to uncover information that subjects often mistakenly believe to be private, reinforcing the importance of data sanitisation before external sharing.
