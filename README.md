# Introduction
Application suite for WDME performance and energy efficiency monitoring. This proof of concept Docker composition of components to monitor and analyse performance and therefore energy efficiency of different tools deployed as Docker containers. Solution is based around Prometheus telemetry collection suite and takes advantage of existing data collection tools existing with Prometheus.
# Components
This is a summary of components used in the suite
## cAdvisor
A container that monitors resource usage and performance characteristics of other containers.
|Port	| Description |
| 8090:8080	| Exposes the cAdvisor interface |

## Redis
Provides a caching and message-queuing system for other services to use for storing and managing data.

## idrac
An iDRAC (Integrated Dell Remote Access Controller) exporter for Prometheus, collecting server hardware metrics.

## metric-adapter
Adapts and collects metrics for Prometheus scraping, acting as a custom metrics collector.

## event-parser
Parses event data and prepares it for metric collection or further processing.
| Environment Variable | Description                                |
|----------------------|--------------------------------------------|
| ADAPTER_PORT         |                                            |
| CLUSTERABILITY_HOST  |                                            |
| CLUSTERABILITY_PORT  |                                            |
| PARAM1               |                                            |
| PARAM2               |                                            |
| PARAM3               |                                            |
| PARAM4               |                                            |
| PARAM5               |                                            |
| PARAM6               |                                            |
| PARAM7               |                                            |


## Prometheus
Collects and stores metrics data for analysis.

## Prometheus pushgateway
Acts as an intermediary for batch jobs to push metrics to Prometheus.

## Grafana
Provides a UI for visualizing and analyzing metrics collected by Prometheus.

## Clusterability tool
Custerize the performance data

### API
| Endpoint        | Method | Description                                |
|-----------------|--------|--------------------------------------------|
| /clusterability | POST   | Asses the clusterability of provided data  |

Supported algorithms are: 
- dip-test
- silverman
- dbcm
- mcnn


Parameters:
````
algorithmType="<algorithm>"
jsonPathVariable="{<path1>, <path2>,…, <pathN>}"
````

Data format:
````
{
    "<Index1>": {
        "<param1>": <float>,
        "<param2>": <float>,
        "<param3>": <float>,
        ...
        "<paramN>": <float>
    },
    "<Index2>": {},
    "<Index3>": {},
    ...
    "<IndexN>": {},
}
````
To test the tool you can use following curl -command with provided dummy data JSON:
````
curl 'http://localhost:8000/clusterability?algorithmType=silverman&jsonPathVariable={$.cpu_usage,$.memory_usage,$.disk_io,$.net_receive,$.net_transmit}' -H 'Content-Type: application/json' -H 'accept: application/json' -d@testdata.json
````


### How to Use

## Stresstest
Generates dummy load to the environment for testing the tool suite
| Environment Variable | Description                                |
|----------------------|--------------------------------------------|
| TESTER_PORT          | Port on which the tool runs                |
| TIME_PERIOD          | Configures time period for testing         |
| TIME_SLICE           | Configures time slice for stress intervals |

### API
| Endpoint | Method | Description                                |
|----------|--------|--------------------------------------------|
| /start   | POST   | Start the load generator                   |

### How to Use




