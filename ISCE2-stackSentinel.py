@ ISCE2-stackSentinel.py的相关命令及其用法
@ https://github.com/isce-framework/isce2/blob/main/contrib/stack/topsStack/README.md
usage: stackSentinel.py [-h] [-H] -s SLC_DIRNAME -o ORBIT_DIRNAME -a
                        AUX_DIRNAME [-w WORK_DIR] -d DEM [-p POLARIZATION]
                        [-W {slc,correlation,interferogram,offset}]
                        [-n SWATH_NUM] [-b BBOX] [-x EXCLUDE_DATES]
                        [-i INCLUDE_DATES] [--start_date STARTDATE]
                        [--stop_date STOPDATE] [-C {geometry,NESD}]
                        [-m REFERENCE_DATE]
                        [--snr_misreg_threshold SNRTHRESHOLD]
                        [-e ESDCOHERENCETHRESHOLD]
                        [-O NUM_OVERLAP_CONNECTIONS] [-c NUM_CONNECTIONS]
                        [-z AZIMUTHLOOKS] [-r RANGELOOKS] [-f FILTSTRENGTH]
                        [-u {icu,snaphu}] [-rmFilter] [--param_ion PARAM_ION]
                        [--num_connections_ion NUM_CONNECTIONS_ION] [-useGPU]
                        [--num_proc NUMPROCESS]
                        [--num_proc4topo NUMPROCESS4TOPO] [-t TEXT_CMD]
                        [-V {True,False}]

Preparing the directory structure and config files for stack processing of
Sentinel-1 TOPS data

optional arguments:
  -h, --help            show this help message and exit
  -H, --hh              Display detailed help information.
  -s SLC_DIRNAME, --slc_directory SLC_DIRNAME
                        Directory with all Sentinel SLCs
  -o ORBIT_DIRNAME, --orbit_directory ORBIT_DIRNAME
                        Directory with all orbits
  -a AUX_DIRNAME, --aux_directory AUX_DIRNAME
                        Directory with all aux files
  -w WORK_DIR, --working_directory WORK_DIR
                        Working directory (default: ./).
  -d DEM, --dem DEM     Path of the DEM file
  -p POLARIZATION, --polarization POLARIZATION
                        SAR data polarization (default: vv).
  -W {slc,correlation,interferogram,offset}, --workflow {slc,correlation,interferogram,offset}
                        The InSAR processing workflow (default:
                        interferogram).

Area of interest:
  -n SWATH_NUM, --swath_num SWATH_NUM
                        A list of swaths to be processed. -- Default : '1 2 3'
  -b BBOX, --bbox BBOX  Lat/Lon Bounding SNWE. -- Example : '19 20 -99.5
                        -98.5' -- Default : common overlap between stack

Dates of interest:
  -x EXCLUDE_DATES, --exclude_dates EXCLUDE_DATES
                        List of the dates to be excluded for processing. --
                        Example : '20141007,20141031' (default: None).
  -i INCLUDE_DATES, --include_dates INCLUDE_DATES
                        List of the dates to be included for processing. --
                        Example : '20141007,20141031' (default: None).
  --start_date STARTDATE
                        Start date for stack processing. Acquisitions before
                        start date are ignored. format should be YYYY-MM-DD
                        e.g., 2015-01-23
  --stop_date STOPDATE  Stop date for stack processing. Acquisitions after
                        stop date are ignored. format should be YYYY-MM-DD
                        e.g., 2017-02-26

Coregistration options:
  Configurations for stack coregistartion of SLCs

  -C {geometry,NESD}, --coregistration {geometry,NESD}
                        Coregistration options (default: NESD).
  -m REFERENCE_DATE, --reference_date REFERENCE_DATE
                        Directory with reference acquisition
  --snr_misreg_threshold SNRTHRESHOLD
                        SNR threshold for estimating range misregistration
                        using cross correlation (default: 10).
  -e ESDCOHERENCETHRESHOLD, --esd_coherence_threshold ESDCOHERENCETHRESHOLD
                        Coherence threshold for estimating azimuth
                        misregistration using enhanced spectral diversity
                        (default: 0.85).
  -O NUM_OVERLAP_CONNECTIONS, --num_overlap_connections NUM_OVERLAP_CONNECTIONS
                        number of overlap interferograms between each date and
                        subsequent dates used for NESD computation (for
                        azimuth offsets misregistration) (default: 3).

Interferogram options:
  Configurations for interferogram generation

  -c NUM_CONNECTIONS, --num_connections NUM_CONNECTIONS
                        number of interferograms between each date and
                        subsequent dates (default: 1).
  -z AZIMUTHLOOKS, --azimuth_looks AZIMUTHLOOKS
                        Number of looks in azimuth for interferogram multi-
                        looking (default: 3).
  -r RANGELOOKS, --range_looks RANGELOOKS
                        Number of looks in range for interferogram multi-
                        looking (default: 9).
  -f FILTSTRENGTH, --filter_strength FILTSTRENGTH
                        Filter strength for interferogram filtering (default:
                        0.5).

Phase unwrapping options:
  Configurations for phase unwrapping

  -u {icu,snaphu}, --unw_method {icu,snaphu}
                        Unwrapping method (default: snaphu).
  -rmFilter, --rmFilter
                        Make an extra unwrap file in which filtering effect is
                        removed

Ionosphere options:
  Configurations for ionospheric delay estimation

  --param_ion PARAM_ION
                        ionosphere estimation parameter file. if provided,
                        will do ionosphere estimation.
  --num_connections_ion NUM_CONNECTIONS_ION
                        number of interferograms between each date and
                        subsequent dates for ionosphere estimation (default:
                        3).

Computing options:
  Configurations for computing environment and resource

  -useGPU, --useGPU     Allow App to use GPU when available
  --num_proc NUMPROCESS, --num_process NUMPROCESS
                        number of tasks running in parallel in each run file
                        (default: 1).
  --num_proc4topo NUMPROCESS4TOPO, --num_process4topo NUMPROCESS4TOPO
                        number of parallel processes (for topo only) (default:
                        1).
  -t TEXT_CMD, --text_cmd TEXT_CMD
                        text command to be added to the beginning of each line
                        of the run files (default: ''). Example: 'source
                        ~/.bash_profile;'
  -V {True,False}, --virtual_merge {True,False}
                        Use virtual files for the merged SLCs and geometry
                        files. Default: True for correlation / interferogram
                        workflow, False for slc / offset workflow
