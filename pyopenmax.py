#
# Copyright (c) 2012 Peter de Rivaz
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.
#
# Raspberry Pi Video decode demo using OpenMAX IL via Python

import ctypes
import time

# Set up constants from OMX_Core.h include files

OMX_VERSION_MAJOR=1
OMX_VERSION_MINOR=1
OMX_VERSION_REVISION=2
OMX_VERSION_STEP=0
OMX_ALL=0xFFFFFFFF

OMX_VERSION = ((OMX_VERSION_STEP<<24) | (OMX_VERSION_REVISION<<16) | (OMX_VERSION_MINOR<<8) | OMX_VERSION_MAJOR)

(OMX_StateInvalid,      
    OMX_StateLoaded,      
    OMX_StateIdle,        
    OMX_StateExecuting,   
    OMX_StatePause,       
    OMX_StateWaitForResources) = range(6)
    
(OMX_CommandStateSet,    
    OMX_CommandFlush,      
    OMX_CommandPortDisable, 
    OMX_CommandPortEnable,  
    OMX_CommandMarkBuffer) = range(5)
    
(OMX_EventCmdComplete,         #/**< component has sucessfully completed a command */
    OMX_EventError,            #   /**< component has detected an error condition */
    OMX_EventMark,             #   /**< component has detected a buffer mark */
    OMX_EventPortSettingsChanged,# /**< component is reported a port settings change */
    OMX_EventBufferFlag,         # /**< component has detected an EOS */ 
    OMX_EventResourcesAcquired,  # /**< component has been granted resources and is
                                 #      automatically starting the state change from
                                 #      OMX_StateWaitForResources to OMX_StateIdle. */
   OMX_EventComponentResumed,    # /**< Component resumed due to reacquisition of resources */
   OMX_EventDynamicResourcesAvailable, #/**< Component has acquired previously unavailable dynamic resources */
   OMX_EventPortFormatDetected) = range(9)
   

(   OMX_IndexComponentStartUnused,# = 0x01000000,
    OMX_IndexParamPriorityMgmt,             #< reference: OMX_PRIORITYMGMTTYPE */
    OMX_IndexParamAudioInit,                #< reference: OMX_PORT_PARAM_TYPE */
    OMX_IndexParamImageInit,                #< reference: OMX_PORT_PARAM_TYPE */
    OMX_IndexParamVideoInit,                #< reference: OMX_PORT_PARAM_TYPE */
    OMX_IndexParamOtherInit,                #< reference: OMX_PORT_PARAM_TYPE */
    OMX_IndexParamNumAvailableStreams,      #< reference: OMX_PARAM_U32TYPE */
    OMX_IndexParamActiveStream,             #< reference: OMX_PARAM_U32TYPE */
    OMX_IndexParamSuspensionPolicy,         #< reference: OMX_PARAM_SUSPENSIONPOLICYTYPE */
    OMX_IndexParamComponentSuspended,       #< reference: OMX_PARAM_SUSPENSIONTYPE */
    OMX_IndexConfigCapturing,               #< reference: OMX_CONFIG_BOOLEANTYPE */ 
    OMX_IndexConfigCaptureMode,             #< reference: OMX_CONFIG_CAPTUREMODETYPE */ 
    OMX_IndexAutoPauseAfterCapture,         #< reference: OMX_CONFIG_BOOLEANTYPE */ 
    OMX_IndexParamContentURI,               #< reference: OMX_PARAM_CONTENTURITYPE */
    OMX_IndexParamCustomContentPipe,        #< reference: OMX_PARAM_CONTENTPIPETYPE */ 
    OMX_IndexParamDisableResourceConcealment, #< reference: OMX_RESOURCECONCEALMENTTYPE */
    OMX_IndexConfigMetadataItemCount,       #< reference: OMX_CONFIG_METADATAITEMCOUNTTYPE */
    OMX_IndexConfigContainerNodeCount,      #< reference: OMX_CONFIG_CONTAINERNODECOUNTTYPE */
    OMX_IndexConfigMetadataItem,            #< reference: OMX_CONFIG_METADATAITEMTYPE */
    OMX_IndexConfigCounterNodeID,           #< reference: OMX_CONFIG_CONTAINERNODEIDTYPE */
    OMX_IndexParamMetadataFilterType,       #< reference: OMX_PARAM_METADATAFILTERTYPE */
    OMX_IndexParamMetadataKeyFilter,        #< reference: OMX_PARAM_METADATAFILTERTYPE */
    OMX_IndexConfigPriorityMgmt,            #< reference: OMX_PRIORITYMGMTTYPE */
    OMX_IndexParamStandardComponentRole,    #< reference: OMX_PARAM_COMPONENTROLETYPE */
    ) = [0x01000000 + i for i in range(24)]
    
(   OMX_IndexPortStartUnused, # = 0x02000000,
    OMX_IndexParamPortDefinition,           #< reference: OMX_PARAM_PORTDEFINITIONTYPE */
    OMX_IndexParamCompBufferSupplier,       #< reference: OMX_PARAM_BUFFERSUPPLIERTYPE */ 
    ) = [0x02000000 + i for i in range(3)]
    
OMX_IndexReservedStartUnused = 0x03000000


(   OMX_IndexAudioStartUnused, # = 0x04000000,
    OMX_IndexParamAudioPortFormat,          #< reference: OMX_AUDIO_PARAM_PORTFORMATTYPE */
    OMX_IndexParamAudioPcm,                 #< reference: OMX_AUDIO_PARAM_PCMMODETYPE */
    OMX_IndexParamAudioAac,                 #< reference: OMX_AUDIO_PARAM_AACPROFILETYPE */
    OMX_IndexParamAudioRa,                  #< reference: OMX_AUDIO_PARAM_RATYPE */
    OMX_IndexParamAudioMp3,                 #< reference: OMX_AUDIO_PARAM_MP3TYPE */
    OMX_IndexParamAudioAdpcm,               #< reference: OMX_AUDIO_PARAM_ADPCMTYPE */
    OMX_IndexParamAudioG723,                #< reference: OMX_AUDIO_PARAM_G723TYPE */
    OMX_IndexParamAudioG729,                #< reference: OMX_AUDIO_PARAM_G729TYPE */
    OMX_IndexParamAudioAmr,                 #< reference: OMX_AUDIO_PARAM_AMRTYPE */
    OMX_IndexParamAudioWma,                 #< reference: OMX_AUDIO_PARAM_WMATYPE */
    OMX_IndexParamAudioSbc,                 #< reference: OMX_AUDIO_PARAM_SBCTYPE */
    OMX_IndexParamAudioMidi,                #< reference: OMX_AUDIO_PARAM_MIDITYPE */
    OMX_IndexParamAudioGsm_FR,              #< reference: OMX_AUDIO_PARAM_GSMFRTYPE */
    OMX_IndexParamAudioMidiLoadUserSound,   #< reference: OMX_AUDIO_PARAM_MIDILOADUSERSOUNDTYPE */
    OMX_IndexParamAudioG726,                #< reference: OMX_AUDIO_PARAM_G726TYPE */
    OMX_IndexParamAudioGsm_EFR,             #< reference: OMX_AUDIO_PARAM_GSMEFRTYPE */
    OMX_IndexParamAudioGsm_HR,              #< reference: OMX_AUDIO_PARAM_GSMHRTYPE */
    OMX_IndexParamAudioPdc_FR,              #< reference: OMX_AUDIO_PARAM_PDCFRTYPE */
    OMX_IndexParamAudioPdc_EFR,             #< reference: OMX_AUDIO_PARAM_PDCEFRTYPE */
    OMX_IndexParamAudioPdc_HR,              #< reference: OMX_AUDIO_PARAM_PDCHRTYPE */
    OMX_IndexParamAudioTdma_FR,             #< reference: OMX_AUDIO_PARAM_TDMAFRTYPE */
    OMX_IndexParamAudioTdma_EFR,            #< reference: OMX_AUDIO_PARAM_TDMAEFRTYPE */
    OMX_IndexParamAudioQcelp8,              #< reference: OMX_AUDIO_PARAM_QCELP8TYPE */
    OMX_IndexParamAudioQcelp13,             #< reference: OMX_AUDIO_PARAM_QCELP13TYPE */
    OMX_IndexParamAudioEvrc,                #< reference: OMX_AUDIO_PARAM_EVRCTYPE */
    OMX_IndexParamAudioSmv,                 #< reference: OMX_AUDIO_PARAM_SMVTYPE */
    OMX_IndexParamAudioVorbis,              #< reference: OMX_AUDIO_PARAM_VORBISTYPE */
    OMX_IndexConfigAudioMidiImmediateEvent, #< reference: OMX_AUDIO_CONFIG_MIDIIMMEDIATEEVENTTYPE */
    OMX_IndexConfigAudioMidiControl,        #< reference: OMX_AUDIO_CONFIG_MIDICONTROLTYPE */
    OMX_IndexConfigAudioMidiSoundBankProgram, #< reference: OMX_AUDIO_CONFIG_MIDISOUNDBANKPROGRAMTYPE */
    OMX_IndexConfigAudioMidiStatus,         #< reference: OMX_AUDIO_CONFIG_MIDISTATUSTYPE */
    OMX_IndexConfigAudioMidiMetaEvent,      #< reference: OMX_AUDIO_CONFIG_MIDIMETAEVENTTYPE */
    OMX_IndexConfigAudioMidiMetaEventData,  #< reference: OMX_AUDIO_CONFIG_MIDIMETAEVENTDATATYPE */
    OMX_IndexConfigAudioVolume,             #< reference: OMX_AUDIO_CONFIG_VOLUMETYPE */
    OMX_IndexConfigAudioBalance,            #< reference: OMX_AUDIO_CONFIG_BALANCETYPE */
    OMX_IndexConfigAudioChannelMute,        #< reference: OMX_AUDIO_CONFIG_CHANNELMUTETYPE */
    OMX_IndexConfigAudioMute,               #< reference: OMX_AUDIO_CONFIG_MUTETYPE */
    OMX_IndexConfigAudioLoudness,           #< reference: OMX_AUDIO_CONFIG_LOUDNESSTYPE */
    OMX_IndexConfigAudioEchoCancelation,    #< reference: OMX_AUDIO_CONFIG_ECHOCANCELATIONTYPE */
    OMX_IndexConfigAudioNoiseReduction,     #< reference: OMX_AUDIO_CONFIG_NOISEREDUCTIONTYPE */
    OMX_IndexConfigAudioBass,               #< reference: OMX_AUDIO_CONFIG_BASSTYPE */
    OMX_IndexConfigAudioTreble,             #< reference: OMX_AUDIO_CONFIG_TREBLETYPE */
    OMX_IndexConfigAudioStereoWidening,     #< reference: OMX_AUDIO_CONFIG_STEREOWIDENINGTYPE */
    OMX_IndexConfigAudioChorus,             #< reference: OMX_AUDIO_CONFIG_CHORUSTYPE */
    OMX_IndexConfigAudioEqualizer,          #< reference: OMX_AUDIO_CONFIG_EQUALIZERTYPE */
    OMX_IndexConfigAudioReverberation,      #< reference: OMX_AUDIO_CONFIG_REVERBERATIONTYPE */
    OMX_IndexConfigAudioChannelVolume,      #< reference: OMX_AUDIO_CONFIG_CHANNELVOLUMETYPE */
    ) = [0x04000000 + i for i in range(121-74+1)] 
    

(   OMX_IndexImageStartUnused, # = 0x05000000,
    OMX_IndexParamImagePortFormat,          #< reference: OMX_IMAGE_PARAM_PORTFORMATTYPE */
    OMX_IndexParamFlashControl,             #< reference: OMX_IMAGE_PARAM_FLASHCONTROLTYPE */
    OMX_IndexConfigFocusControl,            #< reference: OMX_IMAGE_CONFIG_FOCUSCONTROLTYPE */
    OMX_IndexParamQFactor,                  #< reference: OMX_IMAGE_PARAM_QFACTORTYPE */
    OMX_IndexParamQuantizationTable,        #< reference: OMX_IMAGE_PARAM_QUANTIZATIONTABLETYPE */
    OMX_IndexParamHuffmanTable,             #< reference: OMX_IMAGE_PARAM_HUFFMANTTABLETYPE */
    OMX_IndexConfigFlashControl,            #< reference: OMX_IMAGE_PARAM_FLASHCONTROLTYPE */
    ) = [0x05000000 + i for i in range(8)] 
    
(   OMX_IndexVideoStartUnused, # = 0x06000000,
    OMX_IndexParamVideoPortFormat,          #< reference: OMX_VIDEO_PARAM_PORTFORMATTYPE */
    OMX_IndexParamVideoQuantization,        #< reference: OMX_VIDEO_PARAM_QUANTIZATIONTYPE */
    OMX_IndexParamVideoFastUpdate,          #< reference: OMX_VIDEO_PARAM_VIDEOFASTUPDATETYPE */
    OMX_IndexParamVideoBitrate,             #< reference: OMX_VIDEO_PARAM_BITRATETYPE */
    OMX_IndexParamVideoMotionVector,        #< reference: OMX_VIDEO_PARAM_MOTIONVECTORTYPE */
    OMX_IndexParamVideoIntraRefresh,        #< reference: OMX_VIDEO_PARAM_INTRAREFRESHTYPE */
    OMX_IndexParamVideoErrorCorrection,     #< reference: OMX_VIDEO_PARAM_ERRORCORRECTIONTYPE */
    OMX_IndexParamVideoVBSMC,               #< reference: OMX_VIDEO_PARAM_VBSMCTYPE */
    OMX_IndexParamVideoMpeg2,               #< reference: OMX_VIDEO_PARAM_MPEG2TYPE */
    OMX_IndexParamVideoMpeg4,               #< reference: OMX_VIDEO_PARAM_MPEG4TYPE */
    OMX_IndexParamVideoWmv,                 #< reference: OMX_VIDEO_PARAM_WMVTYPE */
    OMX_IndexParamVideoRv,                  #< reference: OMX_VIDEO_PARAM_RVTYPE */
    OMX_IndexParamVideoAvc,                 #< reference: OMX_VIDEO_PARAM_AVCTYPE */
    OMX_IndexParamVideoH263,                #< reference: OMX_VIDEO_PARAM_H263TYPE */
    OMX_IndexParamVideoProfileLevelQuerySupported, #< reference: OMX_VIDEO_PARAM_PROFILELEVELTYPE */
    OMX_IndexParamVideoProfileLevelCurrent, #< reference: OMX_VIDEO_PARAM_PROFILELEVELTYPE */
    OMX_IndexConfigVideoBitrate,            #< reference: OMX_VIDEO_CONFIG_BITRATETYPE */
    OMX_IndexConfigVideoFramerate,          #< reference: OMX_CONFIG_FRAMERATETYPE */
    OMX_IndexConfigVideoIntraVOPRefresh,    #< reference: OMX_CONFIG_INTRAREFRESHVOPTYPE */
    OMX_IndexConfigVideoIntraMBRefresh,     #< reference: OMX_CONFIG_MACROBLOCKERRORMAPTYPE */
    OMX_IndexConfigVideoMBErrorReporting,   #< reference: OMX_CONFIG_MBERRORREPORTINGTYPE */
    OMX_IndexParamVideoMacroblocksPerFrame, #< reference: OMX_PARAM_MACROBLOCKSTYPE */
    OMX_IndexConfigVideoMacroBlockErrorMap, #< reference: OMX_CONFIG_MACROBLOCKERRORMAPTYPE */
    OMX_IndexParamVideoSliceFMO,            #< reference: OMX_VIDEO_PARAM_AVCSLICEFMO */
    OMX_IndexConfigVideoAVCIntraPeriod,     #< reference: OMX_VIDEO_CONFIG_AVCINTRAPERIOD */
    OMX_IndexConfigVideoNalSize,            #< reference: OMX_VIDEO_CONFIG_NALSIZE */
    ) = [0x06000000 + i for i in range(161-135+1)]
    

(   OMX_IndexCommonStartUnused, # = 0x07000000,
    OMX_IndexParamCommonDeblocking,         #< reference: OMX_PARAM_DEBLOCKINGTYPE */
    OMX_IndexParamCommonSensorMode,         #< reference: OMX_PARAM_SENSORMODETYPE */
    OMX_IndexParamCommonInterleave,         #< reference: OMX_PARAM_INTERLEAVETYPE */
    OMX_IndexConfigCommonColorFormatConversion, #< reference: OMX_CONFIG_COLORCONVERSIONTYPE */
    OMX_IndexConfigCommonScale,             #< reference: OMX_CONFIG_SCALEFACTORTYPE */
    OMX_IndexConfigCommonImageFilter,       #< reference: OMX_CONFIG_IMAGEFILTERTYPE */
    OMX_IndexConfigCommonColorEnhancement,  #< reference: OMX_CONFIG_COLORENHANCEMENTTYPE */
    OMX_IndexConfigCommonColorKey,          #< reference: OMX_CONFIG_COLORKEYTYPE */
    OMX_IndexConfigCommonColorBlend,        #< reference: OMX_CONFIG_COLORBLENDTYPE */
    OMX_IndexConfigCommonFrameStabilisation,#< reference: OMX_CONFIG_FRAMESTABTYPE */
    OMX_IndexConfigCommonRotate,            #< reference: OMX_CONFIG_ROTATIONTYPE */
    OMX_IndexConfigCommonMirror,            #< reference: OMX_CONFIG_MIRRORTYPE */
    OMX_IndexConfigCommonOutputPosition,    #< reference: OMX_CONFIG_POINTTYPE */
    OMX_IndexConfigCommonInputCrop,         #< reference: OMX_CONFIG_RECTTYPE */
    OMX_IndexConfigCommonOutputCrop,        #< reference: OMX_CONFIG_RECTTYPE */
    OMX_IndexConfigCommonDigitalZoom,       #< reference: OMX_CONFIG_SCALEFACTORTYPE */
    OMX_IndexConfigCommonOpticalZoom,       #< reference: OMX_CONFIG_SCALEFACTORTYPE*/
    OMX_IndexConfigCommonWhiteBalance,      #< reference: OMX_CONFIG_WHITEBALCONTROLTYPE */
    OMX_IndexConfigCommonExposure,          #< reference: OMX_CONFIG_EXPOSURECONTROLTYPE */
    OMX_IndexConfigCommonContrast,          #< reference: OMX_CONFIG_CONTRASTTYPE */
    OMX_IndexConfigCommonBrightness,        #< reference: OMX_CONFIG_BRIGHTNESSTYPE */
    OMX_IndexConfigCommonBacklight,         #< reference: OMX_CONFIG_BACKLIGHTTYPE */
    OMX_IndexConfigCommonGamma,             #< reference: OMX_CONFIG_GAMMATYPE */
    OMX_IndexConfigCommonSaturation,        #< reference: OMX_CONFIG_SATURATIONTYPE */
    OMX_IndexConfigCommonLightness,         #< reference: OMX_CONFIG_LIGHTNESSTYPE */
    OMX_IndexConfigCommonExclusionRect,     #< reference: OMX_CONFIG_RECTTYPE */
    OMX_IndexConfigCommonDithering,         #< reference: OMX_CONFIG_DITHERTYPE */
    OMX_IndexConfigCommonPlaneBlend,        #< reference: OMX_CONFIG_PLANEBLENDTYPE */
    OMX_IndexConfigCommonExposureValue,     #< reference: OMX_CONFIG_EXPOSUREVALUETYPE */
    OMX_IndexConfigCommonOutputSize,        #< reference: OMX_FRAMESIZETYPE */
    OMX_IndexParamCommonExtraQuantData,     #< reference: OMX_OTHER_EXTRADATATYPE */
    OMX_IndexConfigCommonFocusRegion,       #< reference: OMX_CONFIG_FOCUSREGIONTYPE */
    OMX_IndexConfigCommonFocusStatus,       #< reference: OMX_PARAM_FOCUSSTATUSTYPE */
    OMX_IndexConfigCommonTransitionEffect,  #< reference: OMX_CONFIG_TRANSITIONEFFECTTYPE */
    ) = [0x07000000 + i for i in range(199-165+1)]
    
(   OMX_IndexOtherStartUnused, # = 0x08000000,
    OMX_IndexParamOtherPortFormat,          #< reference: OMX_OTHER_PARAM_PORTFORMATTYPE */
    OMX_IndexConfigOtherPower,              #< reference: OMX_OTHER_CONFIG_POWERTYPE */
    OMX_IndexConfigOtherStats,              #< reference: OMX_OTHER_CONFIG_STATSTYPE */
    ) = [0x08000000 + i for i in range(4)]


(   OMX_IndexTimeStartUnused, # = 0x09000000,
    OMX_IndexConfigTimeScale,               #< reference: OMX_TIME_CONFIG_SCALETYPE */
    OMX_IndexConfigTimeClockState,          #< reference: OMX_TIME_CONFIG_CLOCKSTATETYPE */
    OMX_IndexConfigTimeActiveRefClock,      #< reference: OMX_TIME_CONFIG_ACTIVEREFCLOCKTYPE */
    OMX_IndexConfigTimeCurrentMediaTime,    #< reference: OMX_TIME_CONFIG_TIMESTAMPTYPE (read only) */
    OMX_IndexConfigTimeCurrentWallTime,     #< reference: OMX_TIME_CONFIG_TIMESTAMPTYPE (read only) */
    OMX_IndexConfigTimeCurrentAudioReference, #< reference: OMX_TIME_CONFIG_TIMESTAMPTYPE (write only) */
    OMX_IndexConfigTimeCurrentVideoReference, #< reference: OMX_TIME_CONFIG_TIMESTAMPTYPE (write only) */
    OMX_IndexConfigTimeMediaTimeRequest,    #< reference: OMX_TIME_CONFIG_MEDIATIMEREQUESTTYPE (write only) */
    OMX_IndexConfigTimeClientStartTime,     #<reference:  OMX_TIME_CONFIG_TIMESTAMPTYPE (write only) */
    OMX_IndexConfigTimePosition,            #< reference: OMX_TIME_CONFIG_TIMESTAMPTYPE */
    OMX_IndexConfigTimeSeekMode,            #< reference: OMX_TIME_CONFIG_SEEKMODETYPE */
    ) = [0x09000000 + i for i in range(12)]

OMX_IndexKhronosExtensions = 0x6F000000 #< Reserved region for introducing Khronos Standard Extensions */ 

OMX_IndexVendorStartUnused = 0x7F000000

# OMX_VIDEO_CODINGTYPE 
(OMX_VIDEO_CodingUnused,     #< Value when coding is N/A */
    OMX_VIDEO_CodingAutoDetect, #< Autodetection of coding type */
    OMX_VIDEO_CodingMPEG2,      #< AKA: H.262 */
    OMX_VIDEO_CodingH263,       #< H.263 */
    OMX_VIDEO_CodingMPEG4,      #< MPEG-4 */
    OMX_VIDEO_CodingWMV,        #< all versions of Windows Media Video */
    OMX_VIDEO_CodingRV,         #< all versions of Real Video */
    OMX_VIDEO_CodingAVC,        #< H.264/AVC */
    OMX_VIDEO_CodingMJPEG,      #< Motion JPEG */
    ) = range(9)

OMX_DirInput = 0         
OMX_DirOutput = 1

(OMX_EventCmdComplete,            #< component has sucessfully completed a command */
    OMX_EventError,               #< component has detected an error condition */
    OMX_EventMark,                #< component has detected a buffer mark */
    OMX_EventPortSettingsChanged, #< component is reported a port settings change */
    OMX_EventBufferFlag,          #< component has detected an EOS */ 
    OMX_EventResourcesAcquired,   #< component has been granted resources and is
                                  #     automatically starting the state change from
                                  #     OMX_StateWaitForResources to OMX_StateIdle. */
   OMX_EventComponentResumed,     #< Component resumed due to reacquisition of resources */
   OMX_EventDynamicResourcesAvailable, #< Component has acquired previously unavailable dynamic resources */
   OMX_EventPortFormatDetected) = range(9)

# OMX_TIME_CLOCKSTATE
(OMX_TIME_ClockStateRunning,             #< Clock running. */
      OMX_TIME_ClockStateWaitingForStartTime, #< Clock waiting until the 
                                               #   prescribed clients emit their
                                               #   start time. */
      OMX_TIME_ClockStateStopped) = range(3)

(OMX_TIME_RefClockNone,    #< Use no references. */
      OMX_TIME_RefClockAudio,	#< Use references sent through OMX_IndexConfigTimeCurrentAudioReference */
      OMX_TIME_RefClockVideo) = range(3)


# Set up OpenMax types
class COMPONENTTYPE(ctypes.Structure):
    pass

    
c_appdata = ctypes.c_char_p
c_handle = ctypes.POINTER(COMPONENTTYPE)
c_buffer_p = ctypes.c_char_p
c_int_p = ctypes.POINTER(ctypes.c_int)
c_event_handler = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, c_appdata, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
c_empty_buffer_done = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, c_appdata, c_buffer_p)
c_fill_buffer_done = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, c_appdata, c_buffer_p)
c_get_component_version = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, ctypes.POINTER(ctypes.c_char*128), c_int_p, c_int_p, ctypes.POINTER(ctypes.c_char*128))
c_send_command = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, ctypes.c_int, ctypes.c_int, ctypes.c_int)
c_get_parameter = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, ctypes.c_int, ctypes.c_void_p)
c_get_config = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, ctypes.c_int, ctypes.c_void_p)
c_set_config = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, ctypes.c_int, ctypes.c_void_p)
c_set_parameter = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, ctypes.c_int, ctypes.c_void_p)
c_get_state = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, ctypes.POINTER(ctypes.c_int))  
c_setup_tunnel = ctypes.CFUNCTYPE(ctypes.c_int, c_handle, ctypes.c_int, c_handle, ctypes.c_int)


class CALLBACKS(ctypes.Structure):
    _fields_ = [("EventHandler", c_event_handler),
                ("EmptyBufferDone", c_empty_buffer_done),
                ("FillBufferDone", c_fill_buffer_done)]

                
class OMX_PORT_PARAM_TYPE (ctypes.Structure):
    _fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                ("nPorts", ctypes.c_int),
                ("nStartPortNumber", ctypes.c_int)]


class OMX_VIDEO_PARAM_PORTFORMATTYPE (ctypes.Structure):
    _fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                ("nPortIndex", ctypes.c_int),
                ("nIndex", ctypes.c_int),
                ("eCompressionFormat", ctypes.c_int),
                ("eColorFormat", ctypes.c_int),
                ("xFramerate", ctypes.c_int)]


class OMX_PARAM_PORTDEFINITIONTYPE (ctypes.Structure):
    _fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                ("nPortIndex", ctypes.c_int),
                ("eDir", ctypes.c_int),
                ("nBufferCountActual", ctypes.c_int),
                ("nBufferCountMin", ctypes.c_int),
                ("nBufferSize", ctypes.c_int),
                ("bEnabled", ctypes.c_int),
                ("bPopulated", ctypes.c_int),
                ("nBufferCountMin", ctypes.c_int),
                ("eDomain", ctypes.c_int),
                ("format", ctypes.c_int*12),
                ("bBuffersContiguous", ctypes.c_int),
                ("nBufferAlignment", ctypes.c_int)
                ]

# WARNING, in progress, c_send_command is a place holder for callbacks I haven't correctly specified yet                   
COMPONENTTYPE._fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                ("pComponentPrivate", ctypes.c_int),
                ("pApplicationPrivate", ctypes.c_int),
                ("GetComponentVersion",c_get_component_version),
                ("SendCommand", c_send_command),
                ("GetParameter", c_get_parameter),
                ("SetParameter", c_set_parameter),
                ("GetConfig", c_get_config),
                ("SetConfig", c_set_config),
                ("GetExtensionIndex", c_send_command),
                ("GetState", c_get_state),
                ("ComponentTunnelRequest", c_send_command),
                ("UseBuffer", c_send_command),
                ("AllocateBuffer", c_send_command),
                ("FreeBuffer", c_send_command),
                ("EmptyThisBuffer", c_send_command),
                ("FillThisBuffer", c_send_command),
                ("ComponentTunnelRequest", c_send_command),
                ("SetCallbacks", c_send_command),
                ("ComponentDeInit", c_send_command),
                ("UseEGLImage", c_send_command),
                ("ComponentRoleEnum", c_send_command)
                ]

    
class OMX_PARAM_CONTENTURITYPE (ctypes.Structure):
    _fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                ("contentURI", ctypes.c_char*256)]


class OMX_PARAM_U32TYPE (ctypes.Structure):
     _fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                 ("nPortIndex", ctypes.c_int),
                 ("nU32", ctypes.c_int)]


class OMX_TIME_CONFIG_CLOCKSTATETYPE (ctypes.Structure):
     _fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                 ("eState", ctypes.c_int),
                 ("nStartTime0", ctypes.c_int),
                 ("nStartTime1", ctypes.c_int),
                 ("nOffset0", ctypes.c_int),
                 ("nOffset1", ctypes.c_int),
                 ("nWaitMask", ctypes.c_int)]


class OMX_TIME_CONFIG_TIMESTAMPTYPE (ctypes.Structure):
     _fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                 ("nPortIndex", ctypes.c_int),
                 ("nTimestamp0", ctypes.c_int),
                 ("nTimestamp1", ctypes.c_int)]


class OMX_TIME_CONFIG_SCALETYPE (ctypes.Structure):
     _fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                 ("xScale", ctypes.c_int)] # Q16


class OMX_TIME_CONFIG_ACTIVEREFCLOCKTYPE (ctypes.Structure):
     _fields_ = [("nSize", ctypes.c_int),
                ("nVersion", ctypes.c_int),
                 ("eClock", ctypes.c_int)] 
     
    
def py_empty_buffer_done_callback(handle,appdata,data):
    print "Got empty buffer done callback!",handle
    return 0

    
def py_fill_buffer_done_callback(handle,appdata,data):
    print "Got empty buffer done callback!",handle
    return 0
    

empty_buffer_done_callback = c_empty_buffer_done(py_empty_buffer_done_callback)
fill_buffer_done_callback = c_fill_buffer_done(py_fill_buffer_done_callback)

def check(e):
    """Checks that error is zero"""
    if e==0: return
    print 'Error code',hex(e&0xffffffff)
    raise ValueError
    
class OMXComponent(object):
    
    def __init__(self,name,disable_all=True,output_zero=False):
        """Returns the OpenMax component of the given name

        If disable_all then all ports are disabled.
        If output_zero then the number of output buffers is set to 0."""
        appdata = ctypes.c_char_p("extra args")
        handle = c_handle()
        callbacks = CALLBACKS()
        def py_event_handler_callback(handle,appdata,event,data1,data2,pdata):
            if event == OMX_EventError:
                print 'Error:',hex(data1&0xffffffff),name
            elif event == OMX_EventCmdComplete:
                print 'Command complete',name
                self.command_complete = True
            elif event == OMX_EventPortSettingsChanged:
                print 'Port Settings Changed',name
                self.port_changed = True
            elif event == OMX_EventBufferFlag:
                print 'End of stream detected',name
                self.end_of_stream = True
            else:
                print "Got callback for",name,event,hex(data1&0xffffffff),data2
            
            return 0 
        event_handler_callback = c_event_handler(py_event_handler_callback)
        callbacks.EventHandler = event_handler_callback
        callbacks.EmptyBufferDone = empty_buffer_done_callback
        callbacks.FillBufferDone = fill_buffer_done_callback
        e = openmax.OMX_GetHandle(ctypes.byref(handle),"OMX.broadcom."+name,appdata,ctypes.byref(callbacks))
        check(e)
        self.port_changed = False
        self.command_complete = False
        self.handle = handle
        self.callbacks = callbacks
        if disable_all:
            self.disable_all_ports()
        if output_zero:
            self.output_zero()

    def close(self):
        e = openmax.OMX_FreeHandle(self.handle)
        check(e)
        del self.handle
        
    def get_ports(self, t):
        """Returns the OMX_PORT_PARAM_TYPE structure for a given type"""
        ports = OMX_PORT_PARAM_TYPE()
        ports.nSize = 4*4
        ports.nVersion = OMX_VERSION
        ports_p = ctypes.pointer(ports)
        e = self.handle[0].GetParameter(self.handle, t, ctypes.cast(ports_p,ctypes.c_void_p))
        check(e)
        assert ports.nSize == 4*4
        return ports
  
    def get_port_definition(self, port):
        """Returns the OMX_PARAM_PORTDEFINITIONTYPE structure"""
        portdef = OMX_PARAM_PORTDEFINITIONTYPE()
        portdef.nSize = 24*4
        portdef.nVersion = OMX_VERSION
        portdef.nPortIndex = port
        portdef_p = ctypes.pointer(portdef)
        e = self.handle[0].GetParameter(self.handle, OMX_IndexParamPortDefinition, ctypes.cast(portdef_p,ctypes.c_void_p))
        check(e)
        assert portdef.nSize == 24*4
        return portdef

    def portformattype(self,compression_format = OMX_VIDEO_CodingAVC):
        """Set the video format"""
        f = OMX_VIDEO_PARAM_PORTFORMATTYPE()
        f.nSize = 7*4
        f.nVersion = OMX_VERSION
        f.nPortIndex = 130
        f.eCompressionFormat = OMX_VIDEO_CodingAVC
        f_p = ctypes.pointer(f)
        e = self.handle[0].SetParameter(self.handle, OMX_IndexParamVideoPortFormat, ctypes.cast(f_p,ctypes.c_void_p)) 
        check(e)
        
    def disable_all_ports(self):
        """Runs through the different types of port and turns them off.  Needed in order to use tunneling"""
        for t in (OMX_IndexParamAudioInit, OMX_IndexParamVideoInit, OMX_IndexParamImageInit, OMX_IndexParamOtherInit):
            ports = self.get_ports(t)
            for x in xrange(ports.nPorts):
                self.disable_port(ports.nStartPortNumber + x)

    def output_zero_port(self,port):
        """Sets a specific port to have zero output buffers.

        This allows components such as read_media to start and work out which streams are inside them."""
        portdef = self.get_port_definition(port)
        #print 'Port %d is direction %d with %d buffers' % (portdef.nPortIndex,portdef.eDir,portdef.nBufferCountActual)
        if portdef.eDir != OMX_DirOutput or portdef.nBufferCountActual==0: return
        portdef.nBufferCountActual = 0
        portdef_p = ctypes.pointer(portdef)
        e = self.handle[0].SetParameter(self.handle, OMX_IndexParamPortDefinition, ctypes.cast(portdef_p,ctypes.c_void_p))
        check(e)
        self.enable_port(port)
                    
    def output_zero(self):
        """Runs through the different types of port and sets number of ouyput buffers to 0"""
        for t in (OMX_IndexParamAudioInit, OMX_IndexParamVideoInit, OMX_IndexParamImageInit, OMX_IndexParamOtherInit):
            ports = self.get_ports(t)
            for x in xrange(ports.nPorts):
                self.output_zero_port(ports.nStartPortNumber + x)
                
    def debug(self):
        """Runs through the different types of port and sets number of ouyput buffers to 0"""
        for t in (OMX_IndexParamAudioInit, OMX_IndexParamVideoInit, OMX_IndexParamImageInit, OMX_IndexParamOtherInit):
            ports = self.get_ports(t)
            for x in xrange(ports.nPorts):
                port = ports.nStartPortNumber + x
                portdef = self.get_port_definition(port)
                print 'Port %d is direction %d with %d buffers' % (port,portdef.eDir,portdef.nBufferCountActual)
                
    def disable_port(self,x):
        e = self.handle[0].SendCommand(self.handle, OMX_CommandPortDisable, x, 0)
        check(e)
        return self

    def enable_port(self,x):
        e = self.handle[0].SendCommand(self.handle, OMX_CommandPortEnable, x, 0)
        check(e)
        return self

    def flush_port(self,x):
        self.command_complete = False
        e = self.handle[0].SendCommand(self.handle, OMX_CommandFlush, x, 0)
        check(e)
        return self
        
    def stateset(self,state):
        """Moves the component to the requested state"""
        if self.getstate()==state:
            print 'skip stateset'
            return self
        print 'Moving to state',state
        e = self.handle[0].SendCommand(self.handle, OMX_CommandStateSet, state, 0)
        check(e)
        count=0
        for count in xrange(10):
            s = self.getstate()
            if s==state:
                break
            print 'Waiting...'
            time.sleep(0.2)
        else:
            raise ValueError("State not reached")
            
        return self
        
    def getstate(self):
        """Retrieves the current state"""
        state = ctypes.c_int(0xaffedead)
        e = self.handle[0].GetState(self.handle, ctypes.byref(state))
        check(e)
        print 'Getting state',state.value
        return state.value

    def check_idle(self):
        """Make sure that source component is idle, not loaded"""
        s = self.getstate()
        if s != OMX_StateLoaded:
            return
        self.stateset(OMX_StateIdle)

    def tunnel(self,srcport,sink,sinkport):
        """Sets up a tunnel from srcport on this component to dest:destport"""
        self.check_idle()
        self.disable_port(srcport)
        sink.disable_port(sinkport)
        ps = OMX_PARAM_U32TYPE()
        ps.nSize = 4*4
        ps.nVersion = OMX_VERSION
        ps.nPortIndex = srcport
        ps_p = ctypes.pointer(ps)
        e = self.handle[0].GetParameter(self.handle, OMX_IndexParamNumAvailableStreams, ctypes.cast(ps_p,ctypes.c_void_p))
        if e == 0:
            if ps.nU32 == 0:
                raise ValueError("No streams available")
            ps.nU32 = 0
            assert ps.nSize==16
            e = self.handle[0].SetParameter(self.handle, OMX_IndexParamActiveStream, ctypes.cast(ps_p,ctypes.c_void_p))
            check(e)

        e = openmax.OMX_SetupTunnel(self.handle, srcport, sink.handle, sinkport)
        check(e)

        self.enable_port(srcport)
        sink.enable_port(sinkport)
        return Tunnel(self,srcport,sink,sinkport)

    def teardown(self,port):
        e = openmax.OMX_SetupTunnel(self.handle, port, 0, 0)
        check(e)

        
class ReadMediaComponent(OMXComponent):
    """This component parses container formats and produces output streams (video/audio/text)"""
    
    def __init__(self):
        super(ReadMediaComponent,self).__init__("read_media")
        
    def open_uri(self,uri):
        """For a media reader component, tell it to open the given file"""
        uri += '\0'
        uri_s = OMX_PARAM_CONTENTURITYPE()
        uri_s.nSize = 8+len(uri)
        uri_s.nVersion= OMX_VERSION
        uri_s.contentURI = uri
        uri_p = ctypes.pointer(uri_s)
        e = self.handle[0].SetParameter(self.handle, OMX_IndexParamContentURI, ctypes.cast(uri_p,ctypes.c_void_p))
        check(e)

class VideoSchedulerComponent(OMXComponent):
    """This component generates clock signals to other components"""
    
    def __init__(self):
        super(VideoSchedulerComponent,self).__init__("video_scheduler")
        self.end_of_stream = False

class ClockComponent(OMXComponent):
    """This component generates clock signals to other components"""
    
    def __init__(self):
        super(ClockComponent,self).__init__("clock")
        
    def clock_wait(self,ports=1):
        """Tells a clock component to wait for the bitmask of ports to start"""
        cs = OMX_TIME_CONFIG_CLOCKSTATETYPE()
        cs.nSize = 8*4
        cs.nVersion = OMX_VERSION
        cs.eState = OMX_TIME_ClockStateWaitingForStartTime
        #cs.eState = OMX_TIME_ClockStateRunning
        cs.nWaitMask = 1
        #cs.nWaitMask = 0
        cs.nOffset0=-1000*200
        cs_p = ctypes.pointer(cs)
        e = self.handle[0].SetParameter(self.handle, OMX_IndexConfigTimeClockState, ctypes.cast(cs_p,ctypes.c_void_p))
        check(e)

    def clock_report(self):
        """Prints the current state of the clock"""
        cs = OMX_TIME_CONFIG_CLOCKSTATETYPE()
        cs.nSize = 8*4
        cs.nVersion = OMX_VERSION
        cs_p = ctypes.pointer(cs)
        e = self.handle[0].GetParameter(self.handle, OMX_IndexConfigTimeClockState, ctypes.cast(cs_p,ctypes.c_void_p))
        check(e)
        assert cs.nSize==8*4
        print 'Clock state=%d, wait=%d' % (cs.eState,cs.nWaitMask)

    def clock_time(self):
        """Prints the current time on the clock"""
        cs = OMX_TIME_CONFIG_TIMESTAMPTYPE()
        cs.nSize = 5*4
        cs.nVersion = OMX_VERSION
        cs.nPortIndex = OMX_ALL
        cs_p = ctypes.pointer(cs)
        e = self.handle[0].GetConfig(self.handle, OMX_IndexConfigTimeCurrentMediaTime, ctypes.cast(cs_p,ctypes.c_void_p))
        check(e)
        print 'Clock time=%d:%d us' % (cs.nTimestamp0,cs.nTimestamp1)
        assert cs.nSize == 5*4

    def clock_walltime(self):
        """Prints the current time on the clock"""
        cs = OMX_TIME_CONFIG_TIMESTAMPTYPE()
        cs.nSize = 5*4
        cs.nVersion = OMX_VERSION
        cs.nPortIndex = OMX_ALL
        cs_p = ctypes.pointer(cs)
        e = self.handle[0].GetConfig(self.handle, OMX_IndexConfigTimeCurrentWallTime, ctypes.cast(cs_p,ctypes.c_void_p))
        check(e)
        print 'Wall time=%d:%d us' % (cs.nTimestamp0,cs.nTimestamp1)
        assert cs.nSize == 5*4

        
    def clock_scale(self):
        """Prints the current scaling on the clock (Q16)"""
        cs = OMX_TIME_CONFIG_SCALETYPE()
        cs.nSize = 3*4
        cs.nVersion = OMX_VERSION
        cs_p = ctypes.pointer(cs)
        e = self.handle[0].GetConfig(self.handle, OMX_IndexConfigTimeScale, ctypes.cast(cs_p,ctypes.c_void_p))
        check(e)
        assert cs.nSize == 3*4
        print 'Clock scale=%d/65536' % (cs.xScale)

    def clock_activeref(self):
        """Prints the current scaling on the clock (Q16)"""
        cs = OMX_TIME_CONFIG_ACTIVEREFCLOCKTYPE()
        cs.nSize = 3*4
        cs.nVersion = OMX_VERSION
        cs_p = ctypes.pointer(cs)
        e = self.handle[0].GetConfig(self.handle, OMX_IndexConfigTimeActiveRefClock, ctypes.cast(cs_p,ctypes.c_void_p))
        check(e)
        assert cs.nSize == 3*4
        print 'Clock ref %d' % (cs.eClock)

    def clock_setactiveref(self,ref = OMX_TIME_RefClockVideo):
        cs = OMX_TIME_CONFIG_ACTIVEREFCLOCKTYPE()
        cs.nSize = 3*4
        cs.nVersion = OMX_VERSION
        cs.eClock = ref
        cs_p = ctypes.pointer(cs)
        e = self.handle[0].SetConfig(self.handle, OMX_IndexConfigTimeActiveRefClock, ctypes.cast(cs_p,ctypes.c_void_p))
        check(e)

class Tunnel:
    """Helper class to hold the details of a tunnel setup between OMX components"""
    def __init__(self,src,srcport,sink,sinkport):
        self.src = src
        self.srcport = srcport
        self.sink = sink
        self.sinkport = sinkport

    def flush(self):
        self.src.flush_port(self.srcport)
        self.sink.flush_port(self.sinkport)
        while self.src.command_complete == False or self.sink.command_complete == False:
            time.sleep(0.1)

    def disable(self):
        self.src.disable_port(self.srcport)
        self.sink.disable_port(self.sinkport)

    def teardown(self):
        self.src.teardown(self.srcport)
        self.sink.teardown(self.sinkport)        
              
# Setup addresses of known ports
PORT_MEDIA_READER_OUTPUT =  111
PORT_MEDIA_READER_CLOCK_INPUT = 113
PORT_VIDEO_DECODER_INPUT =  130
PORT_VIDEO_DECODER_OUTPUT = 131
PORT_RESIZE_INPUT =         60
PORT_RESIZE_OUTPUT =        61
PORT_WRITE_STILL_INPUT =    30
PORT_IMAGE_READ_OUTPUT =    310
PORT_IMAGE_DECODE_INPUT =   320
PORT_IMAGE_DECODE_OUTPUT =  321
PORT_VIDEO_SCHEDULER_INPUT = 10 
PORT_VIDEO_SCHEDULER_OUTPUT = 11 
PORT_VIDEO_SCHEDULER_CLOCK_INPUT = 12
PORT_VIDEO_RENDER_INPUT = 90

# Open the host communications
bcm = ctypes.CDLL('libbcm_host.so')
b = bcm.bcm_host_init()
check(b)

# Load the OMX library
openmax = ctypes.CDLL('libopenmaxil.so')
e = openmax.OMX_Init()
check(e)

# openmax.OMX_Deinit()
    
def play(videofile):
    """Plays the video stream for the given filename"""

    # Open the required components
    read_media = ReadMediaComponent()
    read_media.output_zero_port(PORT_MEDIA_READER_OUTPUT)

    # Open file
    read_media.disable_port(PORT_MEDIA_READER_CLOCK_INPUT)
        
    read_media.open_uri(videofile)

    read_media.stateset(OMX_StateIdle)
    while not read_media.port_changed:
        time.sleep(0.1)

    # Open components needed for playback
    video_decode = OMXComponent("video_decode",disable_all=False)
    video_render = OMXComponent("video_render")
    clock = ClockComponent()
    video_scheduler = VideoSchedulerComponent()

    # Connect up just read_media and video_decode to fill the pipeline with frames
    tunnels = []
    tunnels.append(read_media.tunnel(PORT_MEDIA_READER_OUTPUT,video_decode,PORT_VIDEO_DECODER_INPUT))
    video_decode.disable_port(131)

    # Start the video decode
    video_decode.stateset(OMX_StateIdle)
    video_decode.stateset(OMX_StateExecuting)
    read_media.stateset(OMX_StateIdle)
    read_media.stateset(OMX_StateExecuting)

    # Wait for video to fill with frames
    while not video_decode.port_changed:
        time.sleep(0.1)

    # Pause the media so we can set up more tunnels
    read_media.stateset(OMX_StateIdle)
        
    #Set up the rest of the render pipeline
    clock.clock_wait(1) # Wait only for video to be ready
    clock.clock_setactiveref()
    tunnels.append(video_decode.tunnel(PORT_VIDEO_DECODER_OUTPUT,video_scheduler,PORT_VIDEO_SCHEDULER_INPUT))
    tunnels.append(video_scheduler.tunnel(PORT_VIDEO_SCHEDULER_OUTPUT,video_render,PORT_VIDEO_RENDER_INPUT))
    tunnels.append(clock.tunnel(80,video_scheduler,PORT_VIDEO_SCHEDULER_CLOCK_INPUT))
    tunnels.append(clock.tunnel(81,read_media,PORT_MEDIA_READER_CLOCK_INPUT))
    video_render.stateset(OMX_StateIdle)

    # Start complete pipeline
    clock.stateset(OMX_StateExecuting)
    read_media.stateset(OMX_StateExecuting)
    video_scheduler.stateset(OMX_StateExecuting)
    video_render.stateset(OMX_StateExecuting)

    while not video_scheduler.end_of_stream:
        time.sleep(0.1)

    for t in tunnels:
        t.flush()
    for t in tunnels:
        t.disable()
    for t in tunnels:
        t.teardown()
    C=[read_media,video_decode,video_scheduler,video_render,clock]
    for c in C:
        c.stateset(OMX_StateIdle)
    for c in C:
        c.stateset(OMX_StateLoaded)
    for c in C:
        c.close()
        
    print 'Stream finished'
    return


if __name__ == "__main__":
    play("/home/pi/transformers.mp4")
    #play("/opt/vc/src/hello_pi/hello_video/test.h264") 
