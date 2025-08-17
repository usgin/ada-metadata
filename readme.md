# Metadata for Astromat Data Archive products


Approach: ADA products correspond to bundles delivered by O-REx/SAMIS. A product is the result of one analytical techique and one analysis session.  Generally, data from a single sample is included in the product, but some analysis sessions get results from multiple samples. 


The product consists of a set of files. Each file MUST have an accompanying YAML metadata file, with the simple content set out in the SAMIS DTD and BDD documents. There are a limited number of file types allowed:


Images: png, tiff, jpeg preferred.   Cameca .im images, and tiff stacks. are also allowed
ImageMap: png, tiff, jpeg
Tabular Data: csv format preferred; other delimited text formats may be used with adequate documentation
Data Cube: NetCDF, HDF5, .emd, .mzml 
Document: ASCII or UTF-8 text, or PDF/A.  These are for narrative text, and data visualizations
Metadata: yaml or JSON
otherTypes: there are several other specialized file types in common usage that O-REx is allowing. .obj and .stl files for representing 3-D models of particles; 


Each analysis method has an abbreviation; data products for that method consist of one or components, each of which is delivered as a single file.  These components include at least one data file and one or more supplementary files.  Most techniques require an accompanying analytical procedure documentation file. 


The ADA-AnalyticalMethodsAndAttributes.xlsx workbook, componentList worksheet lists the components currently in products submitted to the ADA (there are some components with no instances in the repository listed as well, for future use)  The column on the left lists the component names assigned in the SAMIS Bundle Delivery Documents (https://osiris-rex.atlassian.net/wiki/spaces/SDPD/pages/449544195/Bundle+Delivery+Documents+BDD, might need a confluence acccount to access...).  Some of the SAMIS-defined components have component parts, ADA assigns names to these as well so that files containing that information can be identified; the ADA names are listed in the notes column of the worksheet.  This is a temporary arrangement while the system is being refined. 


Component names are constructed with a prefix that identifes the analytical method, and a suffix for the kind of content. For example the 'DSCResultsTabular' is a file containing delimited tabular text with result data from a Differential Scanning Calorimetry (DSC) Analysis session. 


Each file type has a set of required metadata properties describing the file.  In addition, many of the components require additional metadata to document the file content supporting search and data assessment. Attributes associated with each filetype and component are listed in the columns of the attributes worksheet in the The ADA-AnalyticalMethodsAndAttributes.xlsx workbook. Currently, 23 of the component types have associated additional attributes. Determination if additional attributes are needed for other components, and what the mandatory requirements remains to be done.


## JSON schema

To improve the utility of the metadata serialization for information exchange, a modified schema for ADA meta has been drafted for review and consideration.  The schema is in adaMetadataSchema.json.


Other files in this directory contain summaries of unique values from some ADA metadata fields

AstromatMetadataFieldsMapping.xlsx contain mapping of metadata fields for material samples to the iSamples schema.

astromatPDSquestions.txt contains questions for discussion with PDS curators.
notes.txt contains notes and questions for internal ADA discussion.


## ADA-api-json 
folder contain example ADA metadata downloaded via the ADA API. 

## schemaTexts
folder for example metadata conforming to the new draft schema.


## TestPDSLabels2025
folder for example XML PDS label (metadata) documents 