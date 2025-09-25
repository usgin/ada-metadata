from django.http import JsonResponse
from django.template.loader import render_to_string
import json
import pandas
from pathlib import Path
import hashlib
from .models import *
import re
# for xml response
from django.shortcuts import render
from django.http import HttpResponse

global FILEEXT_LKUP
global METADATA_DATA_LKUP
global INSTRUMENT_LKUP
FILEEXT_LKUP = {}
METADATA_DATA_LKUP = {}
INSTRUMENT_LKUP = {}

schemadict = {
    "1": "sample",
    "2": "analysis.general",
    "3": "technique",
    "4": "instrument",
    "5": "laboratory",
    "6": "unknown",
    "34": "mission"
}
def cleanKey(inkey: str) -> str:
    #  regular expression to replace all non-alphanumeric characters (\W) with an period ('.')
    return re.sub(r'\W+', '', inkey).lower()[:254]

def clean_string(input_string):
    if input_string:
        cleaned_string = input_string.replace("'", "")  # Remove single quotes
        cleaned_string = cleaned_string.replace('"', "")  # Remove double quotes
        cleaned_string = cleaned_string.replace("\n", "")  # Remove newline characters
        cleaned_string = cleaned_string.replace("\r", "")
    else:
        cleaned_string = ""
    return cleaned_string


FILEEXT_LOOKUP =  '../ADA-FileExtensions.xlsx'
print('File Extension lookup')
lkup = pandas.read_excel(FILEEXT_LOOKUP,
                         sheet_name='adaFileExtensions',
                         na_filter=False)
print('file extension lookup columns: %s', ', '.join(lkup.columns))
for index, row in lkup.iterrows():
    theKey = (row['extension']).lstrip(".")
    FILEEXT_LKUP[theKey] = row
lkup = {}


METADATA_DATA_LOOKUP =  '../MetadataToDataMapping.xlsx'
print('Metadata-data component lookup')
lkup = pandas.read_excel(METADATA_DATA_LOOKUP,
                         sheet_name='MetadataToDataMapping',
                         na_filter=False)
print('Metadata-data mapping lookup columns: %s', ', '.join(lkup.columns))
# columns are: record_id -- the ada database PK for the product
# stem -- root of product file names as provide by SAMIS; not products from other sources likely don't follow this convention
# metadata_file -- name of yaml file from ada database record_files
# data_file -- name of the data file described by the Yaml file; match based on grouping by product and stem
# specificType -- the dataComponentType or supDocType for the  data file
# type -- dataComponent or supDocType; each product has exactly one dataComponent file, the supDocs have related link
#         to the data file
for index, row in lkup.iterrows():
    theKey = (row['data_file'])
    METADATA_DATA_LKUP[theKey] = row
lkup = {}

INSTRUMENT_LOOKUP =  '../Instruments.xlsx'
print('Instruments  lookup')
lkup = pandas.read_excel(INSTRUMENT_LOOKUP,
                         sheet_name='Instruments',
                         na_filter=False)
print('Instruments lookup columns: %s', ', '.join(lkup.columns))
for index, row in lkup.iterrows():
    theKey = cleanKey(row['instrument'])
    INSTRUMENT_LKUP[theKey] = row
lkup = {}


def getRecordItems(data):
    # data is records table content for one product
    doi_id = data.doi
    print(f"bundle_id DOI: {doi_id}")
    #record items is a dictionary passed to render_to_string with the JSON (or XML) template to generate the
    #   output file
    conformance = ["CDIF_basic_1.0"]
    recorditems = {'doi': doi_id,
                   'title': data.title,
                   'description': clean_string(data.description),
                   'publication_date': data.publication_date.date().isoformat(),
                   'publication_year': data.publication_date.year,
                   'specific_type': data.specific_type,
                   'fundingdescription':data.funding_description,
                   'created': data.created_at.date().isoformat(),
                   'updated': data.updated_at.date().isoformat()
                   }
    recorditems['record_id'] = data.id
    rec_id = data.id

    #read the relation tables and filter for records related to this product....

    contribs = RecordContributors.objects.all()
    bundlecontribs = contribs.filter(record_id=rec_id)

    creators = RecordCreators.objects.all()
    bundlecreators = creators.filter(record_id=rec_id)

    #note record_fundings table in ada db copy I have is emmpty
    fundings = RecordFundings.objects.all()
    bundlefundings = fundings.filter(record_id=rec_id)

    licenses = RecordLicenses.objects.all()
    bundlelicenses = licenses.filter(record_id=rec_id)

    relations = RecordRelations.objects.all()
    bundlerelations = relations.filter(source_record_id=rec_id)

    files = RecordFiles.objects.all()
    bundlefiles = files.filter(record_id=rec_id)

    subjects = RecordSubjects.objects.all()
    bundlesubjects = subjects.filter(record_id=rec_id)


    agentIDs = NameEntityIdentifiers.objects.all()


#handle creator
    creatorarray = []
    creatorids = []
    for  cname in bundlecreators:
        agentitem =[]
        # cname is a RecordCreator
        creatorFullName = cname.name_entity.full_name
        print("a creator " + creatorFullName)
        creatorid = cname.name_entity
        creatorids.append(creatorid) # keep track of creators, don't duplicate these as contributors
        cids = agentIDs.filter(name_entity_id = creatorid)
        # distinguish e-mail as id from https:// as ide
        theid = ''
        theemail = ''
        for anid in cids:
            if 'http' in anid.identifier:
                theid = anid.identifier
            elif '@' in anid.identifier:
                theemail = anid.identifier

        agentitem = {
            "name": creatorFullName,
            "identifier": theid,
            "email": theemail,
        }
        creatorarray.append(agentitem)
    recorditems['creator'] = creatorarray

# handle contributors  bundlecontribs
    contribarray = []
    contribids = []
    for  cname in bundlecontribs:
        agentitem =[]
        # cname is a RecordContributor
        fullName = cname.name_entity.full_name
        theRole = cname.contributor_type
        contribid = cname.name_entity
        if contribid in creatorids or contribid in contribids:
            continue    # don't put creators in contributor section
        cids = agentIDs.filter(name_entity_id = contribid)
        contribids.append(contribid)
        # distinguish e-mail as id from https:// as ide
        theid = ''
        theemail = ''
        for anid in cids:
            if 'http' in anid.identifier:
                theid = anid.identifier
            elif '@' in anid.identifier:
                theemail = anid.identifier

        agentitem = {
            "name": fullName,
            "identifier": theid,
            "email": theemail,
            "role": theRole
        }
        contribarray.append(agentitem)
    recorditems['contributor'] = contribarray

# handle funding  2025-08-31, my ADA db dump record_funding table is empty.
    fundingarray = []
    for fitem in bundlefundings:
        funditem = []
        # cname is a RecordContributor

        funder = fitem.funder
        # If fitem and funder are dicts use this:  "awardnumber": fitem.get("award_number", ""),
        funditem = {
            "awardnumber": getattr(fitem, "award_number", "") or "",
            "awardtitle" : getattr(fitem, "award_title", "") or "",
            "awardurl" : getattr(fitem, "award_number", "") or "",
            "fundername" : getattr(funder, "name", "") or "",
            "funderabbrev" : getattr(funder, "abbreviation", "") or "",
            "funderurl" : getattr(funder, "url", "") or "",
        }
        fundingarray.append(funditem)
    recorditems['funding'] = fundingarray

# first iterate through subjects with schemaID <> 6 to grab the properties they assert.
    for asubj in bundlesubjects:
        if asubj.subject_schema_id == 6:
            continue
        if asubj.subject_schema_id == 1:
            # sample identifier {"identifier"}
            recorditems['sampleid'] = asubj.subject.get('identifier',"")
        if asubj.subject_schema_id == 2:
            # analysis general {"sessionId", "analysisDate"}
            recorditems['sessionid'] = asubj.subject.get('sessionId',"")
            recorditems['analysisDate'] = (asubj.subject.get('analysisDate',"")
                                           or asubj.subject.get('analysis_date',""))

        if asubj.subject_schema_id == 3:
            # analysis technique {"name","identifier"}
            recorditems['technique'] = asubj.subject.get('name',"")
            recorditems['techniqueid'] = asubj.subject.get('identifier',"")
        if asubj.subject_schema_id == 4:
            # analysis instrument {"name", "identifier"}
            aninstrument = asubj.subject.get('name',"")
            recorditems['instrument'] = aninstrument
            recorditems['instrumentid'] = asubj.subject.get('identifier',"")
            recorditems['instrumenttype'] = INSTRUMENT_LKUP[cleanKey(aninstrument)]['type']
        if asubj.subject_schema_id == 5:
            # analysis laboratory {"name",  "abbreviation", "ror"}
            recorditems['laboratory'] = asubj.subject.get('name',"")
            recorditems['lab_abbrev'] = asubj.subject.get('abbreviation',"")
            recorditems['laboratoryid'] = asubj.subject.get('ror',"")
        if asubj.subject_schema_id == 34:
            # Mission {"mission"}
            recorditems['mission'] = asubj.subject.get('mission',"")

# handle description of files in bundle
    # each file is a component in the bundle and should conform to
    #        a file type DTD (e.g. image, tabular, cube, image, document),
    #       and to an ADA component profile that dictates expected properties.
    filearray = []

    for afile in bundlefiles:
        theFileName = getattr(afile, "name", "") or ""
        theStem = Path(theFileName).stem
        fileitem = {}

        if theFileName:
            fileext = Path(theFileName).suffix.lstrip(".")
            fileType = FILEEXT_LKUP[fileext]['media_type']
        else:
            fileType = "unknown"

        # if afile.general_type = 'Metadata', this is a yaml file documenting another file in the bundl with the
        #  same stem but a different extension.

        if afile.general_type == 'Metadata':
            # get the full file name for the file this is about
            targetfile = bundlefiles.filter(name__contains=theStem).exclude(name__endswith=fileext)
            targetfilename = targetfile[0].name
            #targethash = hash(targetfilename.encode('utf-8'))
            targethash = hashlib.md5(targetfilename.encode('utf-8')).hexdigest()
            conformance.append('ada:metadata')
            fileitem['keyset'] = {
                "id_": hashlib.md5(theFileName.encode('utf-8')).hexdigest(),
                'type_': ["schema:Dataset"],
                "componentType": "ada:metadata",
                "name": theFileName,
                "description": "",
                "about": targethash,
                "checksum": getattr(afile, "checksum", "") or "",
                "size":  getattr(afile, "size_bytes", "") or "",
                "encodingFormat": fileType
            }
            filearray.append(fileitem)
        else:

            for asubj in bundlesubjects.filter(subject_schema_id=6):
                print( asubj)
                # asubj.source_file.name is a yaml file, need to figure out what it targets
                sourcef = Path(asubj.source_file.name).stem
                # check that the subject object is about the current file
                if sourcef != theStem:
                    continue
                subjcontent = getattr(asubj, "subject", "") or ""  # this is a json object, content varies depending
                #  on the data file that its about

                # get the schema names for subject items
                dtype = METADATA_DATA_LKUP[theFileName]['DataType']
                detail = METADATA_DATA_LKUP[theFileName]['MethodDetail']
                spatial = METADATA_DATA_LKUP[theFileName]['spatialRefset']
                specificType = METADATA_DATA_LKUP[theFileName]['specificType']

                if dtype == 'collection_type':
                    conformance.append("ada:collection")
                    conformance.append("ada:" + specificType)
                    fileitem['keyset'] = {
                        "id_": hashlib.md5(theFileName.encode('utf-8')).hexdigest(),
                        'type_': ["ada:collection", "https://schema.org/Collection"],
                        'componentType':  "ada:" + specificType,
                        "name": theFileName,
                        "description": clean_string(subjcontent.get('description')),
                        "checksum": getattr(afile, "checksum", "") or "",
                        "size": getattr(afile, "size_bytes", "") or "",
                        "encodingFormat": fileType
                    }
                    # SAMIS metadata doesn't have information about what's in the zip archives
                    fileitem['thedetail'] = {
                        'memberType': [],
                        'nfiles': None,
                        'fileList': []
                    }
                    if detail == 'argt_detail':
                        fileitem['thedetail'] = fileitem['thedetail'] | {
                            'phaseAnalyzed': subjcontent.get('phaseAnalyzed'),
                            'isotopeType': subjcontent.get('isotopeType')
                        }
                    # get rid of null values
                    fileitem['thedetail'] = {k: v for k, v in fileitem["thedetail"].items() if v}

                elif dtype == 'dataCube_type':
                    fileitem['datastructure'] = "cdi:DimensionalDataStructure"
                    fileitem['thedetail'] = {}
                    conformance.append("ada:dataCube")
                    conformance.append("ada:" + specificType)
                    fileitem['keyset'] = {
                        "id_": hashlib.md5(theFileName.encode('utf-8')).hexdigest(),
                        'type_': ["cdi:PhysicalDataSet", "ada:dataCube"],
                        'componentType': 'ada:' + specificType,
                        "name": theFileName,
                        "description": clean_string(subjcontent.get('description')),
                        #                "about": [""],
                        "checksum": getattr(afile, "checksum", "") or "",
                        "size": getattr(afile, "size_bytes", "") or "",
                        "encodingFormat": fileType
                    }
                    if subjcontent['dimensions']:
                        fileitem['dataStructureComponents'] = []
                        for dim in subjcontent['dimensions']:
                            thisdim = {
                                'type_': "cdi:DimensionComponent",
                                # with current ada data can't identify component types
                                'name': dim.get('dimension'),
                                'token': cleanKey(dim.get('dimension')),
                                'description': clean_string(dim.get('fieldDescription')),
                                'index': dim.get('colNum') or "",
                                'unitOfMeasure': dim.get('unitOfMeasure'),
                                'fieldType': dim.get('fieldType'),
                                'length':  -1  # missing, should be the length of the dimension array;
                            }
                            fileitem['dataStructureComponents'].append(thisdim)
                        # samis metadata is missing description of  the measureComponents
                        #  so there is no dimensionalMeasureComponent loaded
                    if detail == 'l2ms_detail':
                        fileitem['thedetail'] = {
                            'sampleName': subjcontent.get('sampleName'),
                            'ionizationTimeDelay': subjcontent.get('ionizationTimeDelay'),
                            'massGate': subjcontent.get('massGate'),
                            'photoionizationWavelength': subjcontent.get('photoionizationWavelength'),
                            'plasmaShutter': subjcontent.get('plasmaShutter'),
                            'timeDelayUnits': subjcontent.get('timeDelayUnits'),
                            'wavelengthUnits': subjcontent.get('wavelengthUnits')
                        }
                    # get rid of null values
                    fileitem['thedetail'] = {k: v for k, v in fileitem["thedetail"].items() if v}

                elif dtype == 'document_type':
                    fileitem['thedetail'] = {}
                    conformance.append("ada:document")
                    conformance.append("ada:" + specificType)
                    fileitem['keyset'] = {
                        "id_": hashlib.md5(theFileName.encode('utf-8')).hexdigest(),
                        'type_': ["ada:document","schema:DigitalDocument"],
                        'componentType': 'ada:' + specificType,
                        "name": theFileName,
                        "description": clean_string(subjcontent.get('description')),
                        #                "about": [""],
                        "checksum": getattr(afile, "checksum", "") or "",
                        "size": getattr(afile, "size_bytes", "") or "",
                        "encodingFormat": fileType
                    }
                    fileitem['thedetail'] = {
                        'version': subjcontent.get('version'),
                        'isBasedOn': subjcontent.get('_originalName')
                    }
                    if detail == 'argt_detail':
                        fileitem['thedetail'] = fileitem['thedetail'] | {
                            'phaseAnalyzed': subjcontent.get('phaseAnalyzed'),
                            'isotopeType': subjcontent.get('isotopeType')
                        }
                    # get rid of null values
                    fileitem['thedetail'] = {k: v for k, v in fileitem["thedetail"].items() if v}

                elif dtype == 'image_type':
                    fileitem['thedetail'] = {}
                    conformance.append("ada:image")
                    conformance.append("ada:" + specificType)
                    fileitem['keyset']= {
                        "id_": hashlib.md5(theFileName.encode('utf-8')).hexdigest(),
                        'type_': ["ada:image", "schema:ImageObject"],
                        'componentType': 'ada:' + specificType,
                        "name": theFileName,
                        "description": clean_string(subjcontent.get('description')),
                        #                "about": [""],
                        "checksum": getattr(afile, "checksum", "") or "",
                        "size": getattr(afile, "size_bytes", "") or "",
                        "encodingFormat": fileType
                    }
                    fileitem['thedetail'] = {
                        'acquisitionTime': subjcontent.get('acquisitionTime'),
                        'channel1': subjcontent.get('channel1'),
                        'channel2': subjcontent.get('channel2'),
                        'channel3': subjcontent.get('channel3'),
                        'pixelSize': subjcontent.get('pixelSize'),
                        'illuminationType': subjcontent.get('illuminationType'),
                        'imageType': subjcontent.get('imageType')
                    }
                    # get rid of null values
                    fileitem['thedetail'] = {k: v for k, v in fileitem["thedetail"].items() if v}

                elif dtype == 'imageMap_type':
                    fileitem['thedetail'] = {}
                    conformance.append("ada:imageMap")
                    conformance.append("ada:" + specificType)
                    fileitem['keyset'] = {
                        "id_": hashlib.md5(theFileName.encode('utf-8')).hexdigest(),
                        'type_': ["ada:imageMap", "schema:ImageObject"],
                        'componentType': 'ada:' + specificType,
                        "name": theFileName,
                        "description": clean_string(subjcontent.get('description')),
                        #                "about": [""],
                        "checksum": getattr(afile, "checksum", "") or "",
                        "size": getattr(afile, "size_bytes", "") or "",
                        "encodingFormat": fileType
                    }
                    if spatial == 'spatialRegistration_type':
                        fileitem['thedetail'] = {
                           'basemap':subjcontent.get('basemap'),
                            'originX': subjcontent.get('originX'),
                            'originY': subjcontent.get('originY'),
                            'originZ': subjcontent.get('originZ'),
                            'coordDef': subjcontent.get('coordDef'),
                            'coordUnits': subjcontent.get('coordUnits'),
                            'pixelUnits': (subjcontent.get('pixelUnits')
                                                       or subjcontent.get('pxUnits')), # note alternate label pxUnits
                            'pixelScaleX': (subjcontent.get('pixelScaleX')
                                                        or subjcontent.get('pxScaleX')),  # note alternate label pxScaleX
                            'pixelScaleY': (subjcontent.get('pixelScaleY')
                                                        or subjcontent.get('pxScaleY')),  # note alternate label pxScaleY
                            'originLocation': subjcontent.get('originLocation')
                        }

                    fileitem['thedetail'] = fileitem['thedetail'] | {
                        'acquisitionTime':  subjcontent.get('acquisitionTime'),
                        'channel1':  subjcontent.get('channel1'),
                        'channel2':  subjcontent.get('channel2'),
                        'channel3':  subjcontent.get('channel3'),
                        'illuminationType':  subjcontent.get('illuminationType'),
                        'imageType':  subjcontent.get('imageType'),
                        'numPixelsX':  subjcontent.get('numPixelsX'),
                        'numPixelsY':  subjcontent.get('numPixelsY')
                        }
                    if detail == 'empa_detail':
                        fileitem['thedetail']['spectrometerUsed']: subjcontent.get('spectrometerUsed')
                        fileitem['thedetail']['signalUsed']: subjcontent.get('signalUsed')
                    # get rid of null values
                    fileitem['thedetail'] = {k: v for k, v in fileitem["thedetail"].items() if v}

                elif dtype == 'other_type':
                    fileitem['thedetail'] = {}
                    conformance.append("ada:otherFileType")
                    conformance.append("ada:" + specificType)
                    fileitem['keyset'] = {
                        "id_": hashlib.md5(theFileName.encode('utf-8')).hexdigest(),
                        'type_': ["ada:otherFileType"],
                        'componentType': 'ada:' + specificType,
                        "name": theFileName,
                        "description": clean_string(subjcontent.get('description')),
                        #                "about": [""],
                        "checksum": getattr(afile, "checksum", "") or "",
                        "size": getattr(afile, "size_bytes", "") or "",
                        "encodingFormat": fileType
                    }
                    fileitem['thedetail'] = {
                        'formatDescription': clean_string(subjcontent.get('formatDescription'))
                    }
                    if detail == 'slsshapemodel_detail':
                        fileitem['thedetail'] = fileitem['thedetail'] | {
                            'countScans': subjcontent.get('countScans'),
                            'facets': subjcontent.get('facets'),
                            'version': subjcontent.get('version'),
                            'vertices': subjcontent.get('vertices'),
                            'watertight': subjcontent.get('watertight'),
                            'unitsOfMeasurement': subjcontent.get('unitsOfMeasurement')
                            }
                    # get rid of null values
                    fileitem['thedetail'] = {k: v for k, v in fileitem["thedetail"].items() if v}

                elif dtype == 'supDocImage_type':
                    fileitem['thedetail'] = {}
                    conformance.append("ada:image")
                    conformance.append("ada:" + specificType)
                    fileitem['keyset'] = {
                        "id_": hashlib.md5(theFileName.encode('utf-8')).hexdigest(),
                        'type_': ["ada:image", "schema:DigitalDocument"],
                        'componentType': 'ada:' + specificType,
                        "name": theFileName,
                        "description": clean_string(subjcontent.get('description')),
                        #                "about": [""],
                        "checksum": getattr(afile, "checksum", "") or "missing",
                        "size": getattr(afile, "size_bytes", "") or -1,
                        "encodingFormat": fileType
                    }
                    fileitem['thedetail'] = {
                        'numPixelsX': subjcontent.get('numPixelsY'),
                        'numPixelsY': subjcontent.get('numPixelsY'),
                        'schema:isBasedOn': subjcontent.get('_originalName')
                    }
                    # get rid of null values
                    fileitem['thedetail'] = {k: v for k, v in fileitem["thedetail"].items() if v}

                elif dtype == 'tabularData_type':
                    fileitem['datastructure']="cdi:WideDataStructure"
                    fileitem['thedetail'] = {}
                    conformance.append("ada:tabularData")
                    conformance.append("ada:" + specificType)
                    fileitem['keyset'] = {
                        "id_": hashlib.md5(theFileName.encode('utf-8')).hexdigest(),
                        'type_': ["cdi:PhysicalDataSet", "ada:tabularData"],
                        'componentType': 'ada:' + specificType,
                        "name": theFileName,
                        "description": clean_string(subjcontent.get('description')),
                        #                "about": [""],
                        "checksum": getattr(afile, "checksum", "") or "",
                        "size": getattr(afile, "size_bytes", "") or "",
                        "encodingFormat": fileType
                    }
                    fileitem['thedetail'] = {
                        'headerRowCount': subjcontent.get('headerRowCount'),
                        'countRows': subjcontent.get('countRows'),
                        'countColumns': subjcontent.get('countColumns'),
                        'xCoordCol': subjcontent.get('xCoordCol'),
                        'yCoordCol': subjcontent.get('yCoordCol'),
                        'zCoordCol': subjcontent.get('zCoordCol'),
                        'coordUnits': subjcontent.get('coordUnits'),
                        'allowsDuplicates': False
                        }
                    # construct the column descriptions
                    if subjcontent['columns']:
                        fileitem['dataStructureComponents'] = []
                        for col in subjcontent['columns']:
                            thiscol = {
                            'type_': "cdi:MeasureComponent",
                            # with current ada data can't identify component types
                            'name': col.get('label'),
                            'token':cleanKey(col.get('label')),
                            'description':  clean_string(col.get('fieldDescription')),
                            'index':  col.get('colNum') or -1,
                            'fieldType':  col.get('fieldType'),
                            'unitOfMeasure': col.get('unitOfMeasure')
                            }
                            fileitem['dataStructureComponents'].append(thiscol)
                    # Then other properties for the table
                    if  detail == 'dsc_detail':
                        fileitem['thedetail']['analysisType'] = subjcontent.get('analysisType')

                    elif detail == 'eairms_detail':
                        fileitem['thedetail']['massConsumed'] = subjcontent.get('massConsumed')
                        fileitem['thedetail']['elementType'] = subjcontent.get('elementType')

                    elif detail == 'empa_detail':
                        fileitem['thedetail']['spectrometersUsed'] = subjcontent.get('spectrometersUsed')
                        fileitem['thedetail']['signalUsed'] = subjcontent.get('signalUsed')

                    elif detail == 'laf_detail':
                        fileitem['thedetail']['elementAnalyzed'] = subjcontent.get('elementAnalyzed')
                        fileitem['thedetail']['sampleMassConsumed'] = subjcontent.get('sampleMassConsumed')
                        fileitem['thedetail']['sampleType'] = subjcontent.get('sampleType')

                    elif detail == 'nanosims_detail':
                        fileitem['thedetail']['phaseAnalyzed'] = subjcontent.get('phaseAnalyzed')
                        fileitem['thedetail']['isotopeAnalyzed'] = subjcontent.get('isotopeAnalyzed')

                    elif detail == 'nanoir_detail':
                        fileitem['thedetail']['phaseAnalyzed'] = subjcontent.get('phaseAnalyzed')

                    elif detail == 'psfd_detail':
                        fileitem['thedetail']['imageName'] = subjcontent.get('imageName')  # list of strings
                        fileitem['thedetail']['imageViewingConditions'] = subjcontent.get('imageViewingConditions')

                    elif detail == 'put in correct place':
                        # subject line contains Instrument and Laborator
                        if len(recorditems['instrument'])>0:
                            recorditems['instrument'] = recorditems['instrument'] + "; " + subjcontent.get('Instrument')
                        else:
                            recorditems['instrument'] =  subjcontent.get('Instrument')

                        if len(recorditems['laboratory'])>0:
                            recorditems['laboratory'] = recorditems['laboratory'] + "; " + subjcontent.get('Laboratory')
                        else:
                            recorditems['laboratory'] =  subjcontent.get('Laboratory')

                    elif detail == 'vnmir_detail':
                        fileitem['thedetail'] = fileitem['thedetail'] |  {
                            'detector': subjcontent.get('detector'),
                            'beamsplitter': subjcontent.get('beamsplitter'),
                            'calibrationStandards': subjcontent.get('calibrationStandards'),
                            'comments': subjcontent.get('comments'),
                            'numberOfScans': subjcontent.get('numberOfScans'),
                            'eMaxFitRegionMax': subjcontent.get('eMaxFitRegionMax'),
                            'eMaxFitRegionMin': subjcontent.get('eMaxFitRegionMin'),
                            'emissionAngle': subjcontent.get('emissionAngle'),
                            'emissivityMaximum': subjcontent.get('emissivityMaximum'),
                            'environmentalPressure': subjcontent.get('environmentalPressure'),
                            'incidenceAngle': subjcontent.get('incidenceAngle'),
                            'measurement': subjcontent.get('measurement'),
                            'measurementEnvironment': subjcontent.get('measurementEnvironment'),
                            'phaseAngle': subjcontent.get('phaseAngle'),
                            'samplePreparation': subjcontent.get('samplePreparation'),
                            'sampleTemperature': subjcontent.get('sampleTemperature'),
                            'spectralRangeMax': subjcontent.get('spectralRangeMax'),
                            'spectralRangeMin': subjcontent.get('spectralRangeMin'),
                            'spectralResolution': subjcontent.get('spectralResolution'),
                            'spectralSampling': subjcontent.get('spectralSampling'),
                            'spotSize': subjcontent.get('spotSize'),
                            'uncertaintyNoise': subjcontent.get('uncertaintyNoise'),
                            'vacuumExposedSample': subjcontent.get('vacuumExposedSample'),
                            'sampleHeated': subjcontent.get('sampleHeated')
                            }

                    elif detail == 'xrd_detail':
                        fileitem['thedetail'] = fileitem['thedetail'] | {
                            'geometry': subjcontent.get('geometry'),
                            'sampleMount': subjcontent.get('sampleMount'),
                            'stepSize': subjcontent.get('stepSize'),
                            'timePerStep': subjcontent.get('timePerStep'),
                            'wavelength': subjcontent.get('wavelength')
                        }
                    # get rid of null values
                    fileitem['thedetail'] = {k: v for k, v in fileitem["thedetail"].items() if v}

            filearray.append(fileitem)
    recorditems['fileparts'] = filearray
    recorditems['conformsto'] = list(set(conformance))


    return recorditems

def recordJSONByDOIView(request):
    thedoi = request.GET.get('doi')
    print(f"doi: {thedoi}")
    data = Records.objects.get(doi=thedoi)
    print(f"data: {data}")
    recorditems = getRecordItems(data)
    print(f'record items: {recorditems}')
    json_string = render_to_string('adatemplate/adaJSONLD.json',
                                   { "recorditems": recorditems})
    print(f'json_string: {json_string}')
    # Parse the rendered template as JSON
    try:
        json_data = json.loads(json_string)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format in template"}, status=400)

    return JsonResponse(json_data)

def pdsLabel(request):
    thedoi = request.GET.get('doi')
    print(f"doi: {thedoi}")
    data = Records.objects.get(doi=thedoi)
    #print(f"data: {data}")
    recorditems = getRecordItems(data)
    #print(f'record items: {recorditems}')

    # Use render_to_string to get the XML content as a string
    xml_content = render_to_string('adatemplate/pdslabel.xml',
                                   { "recorditems": recorditems})
    return HttpResponse(xml_content, content_type='application/xml')