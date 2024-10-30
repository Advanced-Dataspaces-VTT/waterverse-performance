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

### API
| Endpoint        | Method | Description                                |
|-----------------|--------|--------------------------------------------|
| /entry          | POST   | entry of the function or monitoring point  |
| /exit           | POST   | exit of the function or monitoring point   |

Endpoints require data in payload in JSON format that conforms to this format:
````
Entry payload
{
    "entryPoint":"<identifying entry point>", 
    "observedAt":<UTC Timestamp>
}
Exit payload
{
    "exitPoint":"<identifying exit point>", 
    "observedAt":<UTC Timestamp>
}

````

## event-parser
Parses event data and prepares it for metric collection or further processing.
| Environment Variable | Description                                |
|----------------------|--------------------------------------------|
| ADAPTER_PORT         | Port in which the event-parser is running  |
| TARGET_NAME          | Container name that is monitored           |
| CLUSTERABILITY_HOST  | Clusterability tool host name              |
| CLUSTERABILITY_PORT  | Clusterability tool host port              |
| PROMETHEUS_URL       | URL to the Prometheus telemetry server     |
| PROMETHEUS_PORT      | Port in which rometheus telemetry server runs |
| PARAM1               | Monitored metrics                          |
| PARAM2               |                                            |
| PARAM3               |                                            |
| PARAM4               |                                            |
| PARAM5               |                                            |
| PARAM6               |                                            |
| PARAM7               |                                            |

Example data is provided in testdata.json file

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
Example:
````
algorithmType=silverman&jsonPathVariable={$.cpu_usage,$.memory_usage,$.disk_io,$.net_receive,$.net_transmit}
````
Payload data is an array of JSON objects that conform to this data format:

````
{
    "type": <Entity Type, e.g. PerformanceMetrics>,
    "dateObserved": <UTC Timestamp of the event>,
    "cpu_usage": <CPU usage (sec/sec)>,
    "memory_usage": <bytes/sec>,
    "disk_io": <bytes/sec>,
    "net_receive": <bytes/sec>,
    "net_transmit": <bytes/sec>
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

# Notes

Creating perfomance datasets can be achieved with these tools, but to do off-line analysis additional tools are neede. Prometheus is not timeseries database in traditional sense so making data available offline is necessary. Tools exist for that purpose like
- PromQueen [https://github.com/Cleafy/promqueen/]



