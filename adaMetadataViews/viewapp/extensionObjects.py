import decimal
from dataclasses import dataclass, asdict
from typing import ClassVar, List, Dict, Any, Literal, Union, Optional
from decimal import Decimal
import json


@dataclass
class image_type:
    type_: ClassVar[List[str]] = ["ada:image", "schema:ImageObject"]
    acquisitionTime: Optional[str] 
    componentType: Literal[ "ada:AIVAImage",
                                "ada:EMPAImage",
                                "ada:LITImage",
                                "ada:STEMImage",
                                "ada:TEMImage",
                                "ada:TEMPatternsImage",
                                "ada:UVFMImage",
                                "ada:VLMImage",
                                "ada:SEMEBSDGrainImage",
                                "ada:SEMEDSElementalMap",
                                "ada:SEMHRCLImage",
                                "ada:SEMImageCollection",
                                "ada:TEMEDSImageCollection",
                                "ada:NanoSIMSImage",
                                "ada:XANESImageStack",
                                "ada:XANESStackOverviewImage",
                                "ada:XRDDiffractionPattern",
                                "ada:ShapeModelImage"
    ]
    channel1: Optional[str] 
    channel2: Optional[str] 
    channel3: Optional[str] 
    pixelSize: Optional[str] 
    illuminationType: Optional[str] 
    imageType: Optional[str] 


@dataclass
class empa_detail:
    type_: Literal[ "ada:EMPAImage",
                    "ada:EMPAQEATabular",
                    "ada:EMPAImageCollection"]
    spectrometersUsed: Optional[str] 
    signalUsed: Optional[str] = None

@dataclass
class spatialRegistration_type:
    basemap: Optional[str] 
    originX: Optional[decimal.Decimal]
    originY: Optional[decimal.Decimal]
    originZ: Optional[decimal.Decimal]
    coordDef: Optional[str] 
    coordUnits: Optional[str] 
    pixelUnits: Optional[str] # note alterrnater label pxUnits
    pixelScaleX: Optional[decimal.Decimal]  # note alterrnater label pxScaleX
    pixelScaleY: Optional[decimal.Decimal]  # note alterrnater label pxScaleY
    originLocation: Optional[str] 


@dataclass
class imageMap_type:
    type_: ClassVar[List[str]] = ["ada:imageMap", "schema:ImageObject"]
    componentType: Union [Literal[ "basemap",
                            "supplementalBasemap",
                            "L2MSOverviewImage",
                            "NanoIRMap",
                            "LITImage",
                            "UVFMImage",
                            "VLMImage",
                            "SEMEBSDGrainImageMap",
                            "SEMEDSElementalMap",
                            "SEMHRCLMap",
                            "SEMImageMap",
                            "STEMImage",
                            "TEMImage",
                            "TEMPatternsImage",
                            "VLMImage",
                            "NanoSIMSMap",
                            "XANESimage",
                            "VNMIROverviewImage"
                            ],
                            empa_detail ]
    acquisitionTime: Optional[str] 
    channel1: Optional[str] 
    channel2: Optional[str] 
    channel3: Optional[str] 
    illuminationType: Optional[str] 
    imageType: Optional[str] 
    numPixelsX: Optional[int] 
    numPixelsY: Optional[int] 
    spatialRegistration: spatialRegistration_type


@dataclass
class supDocImage_type:
    type_: ClassVar[List[str]] = ["ada:image","schema:DigitalDocument"]
    componentType: Literal[ "ada:analysisLocation",
                            "ada:annotatedProduct",
                            "ada:contextPhotography",
                            "ada:areaOfInterest",
                            "ada:instrumentMetadata",
                            "ada:supplementalBasemap",
                            "ada:plot",
                            "ada:quickLook",
                            "ada:report",
                            "ada:visImage"
                            ]
    numPixelsX: Optional[int] 
    numPixelsY: Optional[int] 
    original_name: Optional[str] 


@dataclass
class dsc_detail:
    type_: Literal["ada:DSCHeatTabular"]
    analysisType: Optional[str] 

@dataclass
class eairms_detail:
    type_: Literal["ada:EAIRMSCollection"]
    massConsumed: Optional[str] 
    elementType: Optional[str] 

@dataclass
class  laf_detail:
    type_: Literal[ "ada:LAFProcessed",
                    "ada:LAFRaw"]
    elementAnalyzed: Optional[str] 
    sampleMassConsumed: Optional[str] 
    sampleType: Optional[str] 


@dataclass
class nanosims_detail:
    type_: Literal[ "ada:NanoSIMSCollection",
                    "ada:NanoSIMSImageCollection",
                    "ada:NanoSIMSTabular",
                    "ada:NanoSIMSMap"  ]
    phaseAnalyzed: List[str]
    isotopeAnalyzed: List[str]

@dataclass
class nanoir_detail:
    type_: Literal[ "ada:NanoIRBackground",
                    "ada:NanoIRMapCollection",
                    "ada:NanoIRPointCollection"  ]
    phaseAnalyzed: List[str]

@dataclass
class psfd_detail:
    type_: Literal["ada:PSFDTabular"]
    imageName: List[str]
    imageViewingConditions: Optional[str] 

@dataclass
class vnmir_detail:
    type_: Literal["ada:VNMIRSpectralPoint",
                    "ada:VNMIROverviewImage",
                    "ada:VNMIRSpectralMap"]
    detector: Optional[str] 
    beamsplitter: Optional[str] 
    calibrationStandards: Optional[str] 
    comments: Optional[str] 
    numberOfScans: Optional[int] 
    eMaxFitRegionMax: Optional[str] 
    eMaxFitRegionMin: Optional[str] 
    emissionAngle: decimal.Decimal
    emissivityMaximum: Optional[str] 
    environmentalPressure: Optional[decimal.Decimal]
    incidenceAngle: Optional[decimal.Decimal]
    measurement: Optional[str] 
    measurementEnvironment: Optional[str] 
    phaseAngle: Optional[decimal.Decimal]
    samplePreparation: Optional[str] 
    sampleTemperature: Optional[int] 
    spectralRangeMax: Optional[str] 
    spectralRangeMin: Optional[str] 
    spectralResolution: Optional[str] 
    spectralSampling: Optional[str] 
    spotSize: Optional[str] 
    uncertaintyNoise: Optional[decimal.Decimal]
    vacuumExposedSample: bool = False
    sampleHeated: bool = False

@dataclass
class xrd_detail:
    type_:  Literal["ada:XRDTabular"]
    geometry: Optional[str] 
    sampleMount: Optional[str] 
    stepSize: decimal.Decimal
    timePerStep: decimal.Decimal
    wavelength: decimal.Decimal


@dataclass
class DataStructureComponent:
    type_:Literal["cdi:IdentifierComponent",
                "cdi:MeasureComponent",
                "cdi:AttributeComponent"]
    name: Optional[str] 
    instanceVariable: Optional[str] 
    index: Optional[int] 
    length: Optional[int] 
    physicalDataType: Optional[str]
    unitOfMeasure: Optional[str]
    qualifies: Optional[str]        # only applicable to attribute component

@dataclass
class tabularData_type:
    type_: ClassVar[List[str]] = ["cdi:PhysicalDataSet","ada:tabularData"]
    componentType: Union[Literal["ada:AMSRawData",
                                        "ada:AMSProcessedData",
                                        "ada:DSCResultsTabular",
                                        "ada:FTICRMSTabular",
                                        "ada:GPYCProcessedTabular",
                                        "ada:GPYCRawTabular",
                                        "ada:HRICPMSProcessed",
                                        "ada:HRICPMSRaw",
                                        "ada:ICPOESIntermediateTabular",
                                        "ada:ICPOESProcessedTabular",
                                        "ada:ICPOESRawTabular",
                                        "ada:ICTabular",
                                        "ada:MCICPMSTabular",
                                        "ada:NGNSMSRaw",
                                        "ada:NGNSMSProcessed",
                                        "ada:QICPMSProcessedTabular",
                                        "ada:QICPMSRawTabular",
                                        "ada:RAMANRawTabular",
                                        "ada:RITOFNGMSTabular",
                                        "ada:RITOFNGMSCollection",
                                        "ada:SEMEDSPointData",
                                        "ada:SIMSTabular",
                                        "ada:STEMEDSTabular",
                                        "ada:STEMEELSTabular",
                                        "ada:SVRUECTabular",
                                        "ada:XANESRawTabular",
                                        "ada:XANESProcessedTabular"
                                ],
                                dsc_detail,
                                eairms_detail,
                                empa_detail,
                                laf_detail,
                                nanosims_detail,
                                nanoir_detail,
                                psfd_detail,
                                vnmir_detail,
                                xrd_detail
                            ]
    has_DataStructureComponent: list[DataStructureComponent]
    headerRowCount: Optional[int]
    countRows: Optional[int] 
    countColumns: Optional[int] 
    xCoordCol: Optional[str] 
    yCoordCol: Optional[str] 
    zCoordCol: Optional[str] 
    coordUnits: Optional[str]
    delimiter: Optional[str] = ','
    isDelimited: bool = True
    allowsDuplicates: bool = False

@dataclass
class l2ms_detail:
    type_: Literal["ada:L2MSCube"]
    sampleName: Optional[str] 
    ionizationTimeDelay: Optional[int] 
    massGate:bool
    photoionizationWavelength: Optional[int] 
    plasmaShutter: bool
    timeDelayUnits: Optional[str] 
    wavelengthUnits: Optional[str] 

@dataclass
class dimensionComponent:
    type_:Literal["cdi:DimensionComponent"]
    name: Optional[str] 
    instanceVariable: Optional[str] 
    physicalDataType: Optional[str] 
    index: Optional[int] 
    length: Optional[int] 
    valueDomainMin: float
    valueDomainMax: float
    enumeratedValueDomain: Optional[str]   # URI for resoruce enumerated values on this dimension
    valueDomainDescription: Optional[str] 
    valuePath: Optional[str]    # depending on the encodingFormat for the dataCube,
    #       different syntax might be used. The string provided here
    #       should be what is needed to access values of this dimension
    #       using tools appropriate to the particular cube format.
    #       Development of conventions here is still under way.

@dataclass
class dimensionalMeasureComponent:
    type_:Literal[ "cdi:MeasureComponent",
                "cdi:AttributeComponent"]
    # use for measures and attibutes
    name: Optional[str] 
    instanceVariable: Optional[str] 
    physicalDataType: Optional[str]   # could be object, vector, tensor, list.
    #                           as well as standard scalar data types
    qualifies: Optional[str]   # only applicable to attribute component
    valueDomainMin: float
    valueDomainMax: float
    enumeratedValueDomain: Optional[str] 
    valueDomainDescription: Optional[str] 
    valueDataStructureDescription: Optional[str] 
    valuePath: Optional[str]    # depending on the encodingFormat for the dataCube,
    #       different syntax might be used. The string provided here
    #       should be what is needed to access values of this dimension
    #       using tools appropriate to the particular cube format.
    #       Development of conventions here is still under way.

@dataclass
class dataCube_type:
    type_: ClassVar[List[str]] = [ "ada:dataCube","cdi:DimensionalDataStructure"]
    componentType: Union[Literal["ada:GCMSCollection",
                                "ada:GCMSCube",
                                "ada:FTICRMSCube",
                                "ada:LCMSCollection",
                                "ada:SEMEBSDGrainImageMapCube",
                                "ada:SEMEDSElementalMapsCube",
                                "ada:SEMEDSPointDataCube",
                                "ada:SEMHRCLCube",
                                "ada:STEMEDSCube",
                                "ada:STEMEDSTomo",
                                "ada:STEMEELSCube",
                                "ada:VNMIRSpectralMap"
                                ],
                            l2ms_detail
                            ]
    dataComponentResource: Optional[str] 
    has_DataComponent:dimensionalMeasureComponent
    has_DimensionComponent:dimensionComponent

@dataclass
class argt_detail:
    type_: Literal ["ada:ARGTDocument"]
    phaseAnalyzed: Optional[str] 
    isotopeType: Optional[str] 

@dataclass
class document_type:
    type_: ClassVar[List[str]] = [ "ada:document","schema:DigitalDocument"]
    componentType: Union[Literal["ada:calibrationFile",
                                        "ada:contextVideo",
                                        "ada:logFile",
                                        "ada:methodDescription",
                                        "ada:peaks",
                                        "ada:processingDescription",
                                        "ada:QRISCalibrationFile",
                                        "ada:samplePreparation",
                                        "ada:shapefiles"],
                    argt_detail
                    ]
    version: Optional[str] 
    isBasedOn: Optional[str]  #same as ada/samis '_originalName'

@dataclass
class file_type:
    name: Optional[str] 
    namePattern: Optional[str]   # if the collection contains multiple files of the same
    # type (described by the same file object), e.g.
    # '20240227_SLS_UAZ_OREX-800014-0_1_contextPhotography_*.jpeg'.
    # The text at the '*' is a parameter that differentes members of the
    # collection; the remainder of the pattern is constant for all members of the
    # collection
    extension: Optional[str] 
    componentType: Optional[str] 
    encodingFormat: Optional[str] 


@dataclass
class collection_type:
    type_: ClassVar[List[str]] = [ "ada:collection", "https://schema.org/Collection"]
    componentType: Literal["ada:AIVAImageCollection",
                                "ada:ARGTCollection",
                                "ada:EAIRMSCollection",
                                "ada:EMPAImageCollection",
                                "ada:GCMSCollection",
                                "ada:GCGCMSCollection",
                                "ada:LCMSCollection",
                                "ada:LCMSMSCollection",
                                "ada:LIT2DDataCollection",
                                "ada:LITPolarDataCollection",
                                "ada:MCICPMSCollection",
                                "ada:NanoIRMapCollection",
                                "ada:NanoIRPointCollection",
                                "ada:NanoSIMSCollection",
                                "ada:NanoSIMSImageCollection",
                                "ada:QRISCalibratedCollection",
                                "ada:QRISRawCollection",
                                "ada:RITOFNGMSCollection",
                                "ada:SEMEDSElementalMaps",
                                "ada:SEMEDSPointDataCollection",
                                "ada:SEMImageCollection",
                                "ada:SIMSCollection",
                                "ada:TEMEDSImageCollection",
                                "ada:TOFSIMSCollection",
                                "ada:UVFMImageCollection",
                                "ada:VLMImageCollection",
                                "ada:XANESCollection",
                                "ada:XCTImageCollection"]

    memberType:List[str]
    nFiles: Optional[int] 
    fileList:List[file_type]


@dataclass
class slsshapemodel_detail:
    type_: Literal [ "ada:SLSShapeModel","ada:SLSPartialScan"]
    countScans: Optional[int] = None
    facets: Optional[int]= None
    version: Optional[str] = None
    vertices: Optional[int] = None
    watertight: bool = False
    unitsOfMeasurement: str='missing'

@dataclass
class other_type:
    type_: ClassVar[List[str]] = [ "ada:otherFileType"]
    componentType: Union[Literal["ada:other"],
                         slsshapemodel_detail
                        ]
    encodingFormat:Literal[ "Spectral Data Exchange File (.emsa)",
                        "3D model file (.obj)",
                        "Standard Triangle Language (.stl)",
                        "Open XML workbook (.xlsx)",
                        "Neptune Plus export (.exp)"]
    formatDescription: Optional[str] = None



# testing code
shape_model_instance = slsshapemodel_detail(
    type_="ada:SLSShapeModel",
    countScans=12,
    facets=5000,
    version="v1.0",
    vertices=2502,
    watertight=True,
    unitsOfMeasurement="millimeter"
)

other_instance = other_type( componentType =shape_model_instance,
                             encodingFormat= "Spectral Data Exchange File (.emsa)")

# Serialize with the custom function
doc_dict = asdict(other_instance)

doc_dict['type_'] = other_instance.type_


doc_json = json.dumps(doc_dict, indent=2)

print(doc_json)