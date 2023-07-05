#############
TF-M profiler
#############

TF-M profiler is a tool for profiling and benchmarking TF-M. The developer can
leverage it to get the interested data of runtime.

Initially, TF-M profiler supports only count logging. You can add "checkpoint"
in the program. The timer count or CPU cycle count of this checkpoint can be
saved at runtime and be analysed in the future.

************************
How to use TF-M profiler
************************

1. Integrate profiler tool with TF-M

The profiler should be compiled together with TF-M, thus running in SPE.

The source file need to be compiled with TF-M is mainly `profiler.c`. The header
files are in `export` folder.

`export/prof_hal.h` defines the HAL that should be implemented by the platform.

* `prof_hal_init()`: Initialize the counter hardware.

* `prof_hal_get_count()`: Get current counter value.

The size of the database is determined by `PROF_DB_MAX` defined in
`export/prof_common.h`.

The developer can override the size by redefining `PROF_DB_MAX`.

2. Add checkpoints for secure side

The developer should identify the places in source code for adding the
checkpoints. The count value of the timer or CPU cycle will be saved into the
database for the checkpoints.

The interface APIs are defined in `export/prof_if_s.h` for secure side.

3. Add checkpoints for non-secure side

It's supported to add checkpionts in non-secure side. Add
`export/ns/prof_if_ns.c` to the source file list of non-secure side.

The interface APIs for non-secure side are defined in `export/ns/prof_if_ns.h`.

4. Run the program and collect data

After successfully run the program, the data should be saved into the database.

The developer can dump the data throught the interface defined in the header
files mentioned above.

A customized software or tool can be used to generate the analysis report based
on the data.

********************
Interface user guide
********************

Initialization
==============

`prof_data_init()` should be called in secure side before calling any API of
profiler.

Count logging
=============

The counter logging related APIs are defined in macros to keep the interface
consistent between secure and non-secure side.

`PROF_TIMING_LOG`: This API is used to log the counter value when calling this
macro. `topic_id` and `cp_id` are the parameters.

`topic_id`: Topic is used to gather a group of checkpoints. It's useful when
you have many checkpoints for different purposes. Topic can help to organize
them and filter the related information out. It's a 8-bit unsigned value.

`cp_id`: Checkpoint ID. Different topics can have same `cp_id`. It's a 16-bit
unsigned value.

Data fetching
=============

For the same consistent reason as counter logging, same macros are defined as
the interface for both secure and non-secure side.

The data fetching interface works as stream way. `PROF_FETCH_DATA_START` and
`PROF_FETCH_DATA_BY_XXX_START` search the data that matches the given pattern
from the beginning of the database. `PROF_FETCH_DATA_CONTINUE` and
`PROF_FETCH_DATA_BY_XXX_CONTINUE` search from the next data set of the
previous result.

The match condition of a search is controlled by the tag mask. It's `tag value`
& `tag_mask` == `tag_pattern`. To enumerate the whole database, set
`tag_mask` and `tag_pattern` both to `0`.

`PROF_FETCH_DATA_XXX`: The generic interface for getting data.

`PROF_FETCH_DATA_BY_TOPIC_XXX`: Get data for a specific `topic`.

`PROF_FETCH_DATA_BY_CP_XXX`: Get data for a specific checkpoint by specifying
both `topic` and `cp`.

The APIs return `false` if no matching data found until the end of the database.

Calibration
===========

The profiler itself has the tick or cycle cost. To get a more accurate data, a
calibration system is introduced. It's optional.

The counter logging APIs can be called from secure or non-secure side. And the
cost of calling functions from these two worlds are different. So, secure and
non-secure have different calibration data.

The system performance might float during the initialization, for example change
CPU frequency, enable cache, etc. So, it's recommendated that the calibration is
done just before the first checkpoint.

`PROF_DO_CALIBRATE`: Call this macro to get calibration value. The more `rounds`
the more accurate.

`PROF_GET_CALI_VALUE_FROM_TAG`: Get the calibration value from the tag. The
calibrated counter is "current_counter" - "previous_counter" -
"current_cali_value".
"current_cali_value" = PROF_GET_CALI_VALUE_FROM_TAG(current_tag).

Data analysis
=============

Data analysis interfaces can be used to do some basic analysis and the data
returned is calibrated already.

`PROF_DATA_DIFF`: Get the counter value difference for the two tags. Returning
`0` indicates errors.

If the checkpoints are logged by multi-times, you can get the following counter
value differences between two tags:

`PROF_DATA_DIFF_MIN`: Get the minimum counter value difference for the two tags.
Returning `UINT32_MAX` indicates errors.

`PROF_DATA_DIFF_MAX`: Get the maximum counter value difference for the two tags.
Returning `0` indicates errors.

`PROF_DATA_DIFF_AVG`: Get the average counter value difference for the two tags.
Returning `0` indicates errors.

--------------

*Copyright (c) 2022-2023, Arm Limited. All rights reserved.*
