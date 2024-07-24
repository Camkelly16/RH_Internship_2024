- question: What PromQL expression calculates the rate of HTTP requests over the last
    1 minute?
  options:
    A: rate(http_requests_total[1m])
    B: increase(http_requests_total[1m])
    C: sum(http_requests_total[1m])
    D: avg(http_requests_total[1m])
  correct_answer: 1
- question: How do you filter metrics by the label 'job' with the value 'api-server'?
  options:
    A: http_requests_total{job="api-server"}
    B: http_requests_total[job="api-server"]
    C: http_requests_total(job="api-server")
    D: http_requests_total@job="api-server"
  correct_answer: 1
- question: How do you filter metrics by the labelWhich PromQL expression calculates
    is the correct way to apply a simple rate function?"
  options:
    A: (metric_name)
    B: rate(metric_name[5m])
    C: rate(metric_name) by (instance)
    D: rate(5m)(metric_name)
  correct_answer: 2
- question: Which PromQL expression filters metrics to those where the label 'status'
    is not equal to '200'?
  options:
    A: http_requests_total{status!="200"}
    B: http_requests_total{status<>200}
    C: http_requests_total(status!="200")
    D: http_requests_total{status!200}
  correct_answer: 1
- question: How do you select the last value of a time series in PromQL?
  options:
    A: last_over_time(metric_name[5m])
    B: max(metric_name)
    C: metric_name
    D: metric_name[5m]
  correct_answer: 1
- question: How do you calculate the average CPU usage per instance over the last
    5 minutes?
  options:
    A: avg(rate(node_cpu_seconds_total[5m])) by (instance)
    B: sum(rate(node_cpu_seconds_total[5m])) by (instance)
    C: max(rate(node_cpu_seconds_total[5m])) by (instance)
    D: min(rate(node_cpu_seconds_total[5m])) by (instance)
  correct_answer: 1
- question: Which PromQL expression calculates the increase in HTTP requests over
    the last 1 hour?
  options:
    A: increase(http_requests_total[1h])
    B: rate(http_requests_total[1h])
    C: sum(http_requests_total[1h])
    D: delta(http_requests_total[1h])
  correct_answer: 1
- question: How do you combine two metrics using the sum operator?
  options:
    A: metric1 + metric2
    B: addition(metric1, metric2)
    C: combine(metric1, metric2)
    D: (metric1, metric2)
  correct_answer: 1
- question: Which function would you use to get the 95th percentile of response times?
  options:
    A: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
    B: quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
    C: percentile(0.95, rate(http_request_duration_seconds_bucket[5m]))
    D: topk(0.95, rate(http_request_duration_seconds_bucket[5m]))
  correct_answer: 1
- question: What is the correct way to calculate the sum of values grouped by 'job'
    and 'instance'?
  options:
    A: sum(metric_name) by (job, instance)
    B: sum(metric_name) by job, instance
    C: sum(metric_name) job instance
    D: sum(metric_name) over (job, instance)
  correct_answer: 1
- question: Which expression calculates the difference between the maximum and minimum
    values of a metric over the last 10 minutes?
  options:
    A: max_over_time(metric_name[10m]) - min_over_time(metric_name[10m])
    B: delta(metric_name[10m])
    C: range(metric_name[10m])
    D: increase(metric_name[10m])
  correct_answer: 1
- question: How do you filter metrics where the 'environment' label is either 'prod'
    or 'staging'?
  options:
    A: metric_name{environment=~"prod|staging"}
    B: metric_name{environment="prod|staging"}
    C: metric_name{environment!~"prod|staging"}
    D: metric_name{environment=="prod|staging"}
  correct_answer: 1
- question: What function do you use to calculate the number of time series in a metric?
  options:
    A: count(metric_name)
    B: sum(metric_name)
    C: avg(metric_name)
    D: rate(metric_name)
  correct_answer: 1
- question: Which nested query calculates the average CPU usage for instances with
    more than 2 cores?
  options:
    A: avg by (instance) (sum by (instance, cpu) (rate(node_cpu_seconds_total[5m])))
      > 2
    B: avg by (instance) (rate(node_cpu_seconds_total[5m])) > 2
    C: sum by (instance) (avg by (cpu) (rate(node_cpu_seconds_total[5m]))) > 2
    D: sum by (instance) (rate(node_cpu_seconds_total[5m])) / count by (instance)
      (node_cpu_seconds_total) > 2
  correct_answer: 1
- question: How do you calculate the ratio of failed HTTP requests to total HTTP requests
    over the last 5 minutes?
  options:
    A: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
    B: sum(rate(http_requests_total{status=~"5.."}[5m])) and sum(rate(http_requests_total[5m]))
    C: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])
    D: avg(rate(http_requests_total{status=~"5.."}[5m])) / avg(rate(http_requests_total[5m]))
  correct_answer: 1
- question: Which query optimizes the calculation of the 99th percentile of request
    durations in a high-cardinality environment?
  options:
    A: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m]))
      by (le))
    B: histogram_quantile(0.99, avg(rate(http_request_duration_seconds_bucket[5m]))
      by (le))
    C: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
    D: histogram_quantile(0.99, max(rate(http_request_duration_seconds_bucket[5m]))
      by (le))
  correct_answer: 1
- question: How do you efficiently compute the average memory usage per namespace,
    excluding the 'kube-system' namespace?
  options:
    A: avg_over_time(node_memory_MemTotal_bytes{namespace!="kube-system"}[5m]) by
      (namespace)
    B: avg_over_time(node_memory_MemTotal_bytes[5m]) by (namespace) != "kube-system"
    C: avg(rate(node_memory_MemTotal_bytes{namespace!="kube-system"}[5m])) by (namespace)
    D: avg(node_memory_MemTotal_bytes{namespace!="kube-system"}) by (namespace)
  correct_answer: 1
- question: How would you write a PromQL query to calculate the average memory usage
    across all pods in a Kubernetes cluster?
  options:
    A: avg(kube_pod_memory_usage_bytes)
    B: sum(kube_pod_memory_usage_bytes)
    C: avg_over_time(kube_pod_memory_usage_bytes[5m])
    D: rate(kube_pod_memory_usage_bytes[5m])
  correct_answer: 1
- question: To calculate the rate of increase of HTTP requests in the last 5 minutes
    for a web application, which query would you use?
  options:
    A: rate(http_requests_total[5m])
    B: sum(http_requests_total[5m])
    C: increase(http_requests_total[5m])
    D: (http_requests_total[5m])
  correct_answer: 1
- question: What does the histogram_quantile() function do in PromQL?
  options:
    A: Computes the quantile (e.g., 95th percentile) from a histogram
    B: Calculates the average of a histogram
    C: Computes the sum of all histogram values
    D: Returns the rate of change for histogram values
  correct_answer: 1
- question: Which function combination would you use to calculate the average CPU
    usage over the past 10 minutes?
  options:
    A: avg_over_time(cpu_usage[10m])
    B: rate(cpu_usage[10m])
    C: increase(cpu_usage[10m])
    D: sum_over_time(cpu_usage[10m])
  correct_answer: 1
- question: How would you write a PromQL query to calculate the sum of the rate of
    increase for multiple counter metrics?
  options:
    A: sum(rate(counter_metric[5m]))
    B: rate(sum(counter_metric[5m]))
    C: increase(sum(counter_metric[5m]))
    D: sum_over_time(rate(counter_metric[5m]))
  correct_answer: 1
- question: To find the minimum disk space used across all servers over the past hour,
    which query would be correct?
  options:
    A: min_over_time(disk_space_used[1h])
    B: sum(disk_space_used[1h])
    C: avg(disk_space_used[1h])
    D: min(disk_space_used)
  correct_answer: 1
- question: What does the sum_over_time() function do in PromQL?
  options:
    A: Sums the values of the time series over a specified range
    B: Sums the values of the time series at a single point in time
    C: Sums the rates of the time series over a specified range
    D: Sums the rates of the time series at a single point in time
  correct_answer: 1
- question: How would you calculate the 99th percentile latency of HTTP requests over
    the last 10 minutes?
  options:
    A: Xuantile_over_tie(0.99, http_request_duration_seconds[10m])
    B: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[10m]))
    C: Xercentile_ove_time(0.99, http_request_duration_seconds[10m])
    D: quantile(0.99, http_request_duration_seconds(10m)
  correct_answer: 2
- question: To analyze the 95th percentile latency for HTTP requests using histogram
    data, which PromQL query would you use?
  options:
    A: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m]))
      by (le))
    B: quantile(0.5, http_request_duration_seconds[5m])
    C: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
    D: percentile_over_time(0.95, http_request_duration_seconds[5m])
  correct_answer: 1
- question: How would you write a query to calculate the difference between the maximum
    and minimum memory usage for each pod over the past 15 minutes?
  options:
    A: max_over_time(memory_usage[15m]) - min_over_time(memory_usage[15m])
    B: max(memory_usage) - min(memory_usage)
    C: increase(max(memory_usage[15m]) - min(memory_usage[15m]))
    D: rate(max(memory_usage[15m]) - min(memory_usage[15m]))
  correct_answer: 1
- question: Which query would you use to find the top 3 nodes with the highest CPU
    usage over the past hour?
  options:
    A: topk(3, max_over_time(node_cpu_usage[1h]))
    B: topk(3, sum(rate(node_cpu_usage[1h])))
    C: topk(3, avg_over_time(node_cpu_usage[1h]))
    D: topk(3, increase(node_cpu_usage[1h]))
  correct_answer: 1
- question: How can you calculate the average number of active sessions per minute
    over the past day, assuming active_sessions is a gauge metric?
  options:
    A: avg_over_time(active_sessions[1d]) / 1440
    B: rate(active_sessions[1d]) / 1440
    C: avg(active_sessions) / 1440
    D: irate(active_sessions[1d]) / 1440
  correct_answer: 2
- question: Which of the following is the correct PromQL syntax for selecting data
    from the http_requests_total metric in the last 5 minutes?
  options:
    A: http_requests_total[5m]
    B: http_requests_total{5m}
    C: http_requests_total(5m)
    D: http_requests_total{5m}]
  correct_answer: 1
- question: How do you retrieve the average value of the cpu_usage metric over a 10-minute
    window?
  options:
    A: avg(cpu_usage[10m])
    B: cpu_usage_avg[10m]
    C: cpu_usage / 10m
    D: cpu_usage(avg)[10m]
  correct_answer: 1
- question: What is the correct syntax to filter data from the http_requests_total
    metric where the status code is 200?
  options:
    A: http_requests_total{status="200"}
    B: http_requests_total(status="200")
    C: http_requests_total{status:200}
    D: http_requests_total[status="200"]
  correct_answer: 1
- question: Which of the following PromQL expressions is written with correct syntax
    to calculate the 90th percentile of the latency metric?
  options:
    A: (latency, 90)
    B: '{quantile="0.90"}'
    C: quantile(0.90, latency)
    D: latency[90%)
  correct_answer: 3
- question: How would you select the maximum value of the memory_usage metric over
    a 1-hour time range?
  options:
    A: max(memory_usage) [1h]
    B: memory_usage{1h} max
    C: max(memory_usage) / 1h
    D: memory_usage / max[1h]
  correct_answer: 1
- question: Which PromQL syntax retrieves the sum of disk_space_used across all instances?
  options:
    A: sum(disk_space_used) by (instance)
    B: disk_space_used{sum by instance}
    C: sum(disk_space_used) without (instance)
    D: disk_space_used{sum(instance)}
  correct_answer: 1
- question: How do you correctly select data from the network_packets_received metric
    where the device is named "eth0"?
  options:
    A: network_packets_received{device="eth0"}
    B: network_packets_received(device="eth0")
    C: network_packets_received{device:"eth0"}
    D: network_packets_received[device="eth0"]
  correct_answer: 1
- question: Which PromQL expression correctly filters data from the http_requests_total
    metric where the method is "POST" and the status is 500?
  options:
    A: http_requests_total{method="POST", status="500"}
    B: http_requests_total{method:"POST", status:"500"}
    C: http_requests_total(method="POST", status="500")
    D: http_requests_total[method="POST"][status="500"]
  correct_answer: 1
- question: What is the correct syntax to retrieve the minimum value of the response_time
    metric over a 30-minute time range?
  options:
    A: min(response_time) [30m]
    B: response_time[min(30m)]
    C: min(response_time) / 30m
    D: response_time / min[30m]
  correct_answer: 1
- question: Which of the following PromQL expressions correctly selects data from
    the disk_usage metric where the mount point is "/var"?
  options:
    A: disk_usage{mountpoint="/var"}
    B: disk_usage[mountpoint="/var"]
    C: disk_usage(mountpoint="var")
    D: disk_usage["/var"]
  correct_answer: 1
- question: How would you calculate the rate of change of the requests_total metric
    over a 5-minute interval?
  options:
    A: increase(requests_total)[5m]
    B: rate(requests_total)[5m]
    C: increase(rate(requests_total))[5m]
    D: rate(increase(requests_total))[5m]
  correct_answer: 2
- question: What is the correct PromQL syntax to compute the difference in disk_space_used
    over the last 10 minutes?
  options:
    A: delta(disk_space_used)[10m]
    B: diff(disk_space_used)[10m]
    C: increase(disk_space_used)[10m]
    D: rate(disk_space_used)[10m]
  correct_answer: 1
- question: How do you find the percentage increase in the transactions metric over
    the last hour?
  options:
    A: increase(transactions) * 100 / transactions
    B: (transactions - increase(transactions)) increase(transactions) * 100
    C: 100 * increase(transactions) / transactions
    D: transactions / increase(transactions) * 100
  correct_answer: 3
- question: Which of the following PromQL expressions calculates the second derivative
    of the cpu_usage metric over a 5-minute period?
  options:
    A: rate(rate(cpu_usage)[5m])[5m]
    B: increase(increase(cpu_usage)[5m])[5m]
    C: derivative(derivative(cpu_usage)[5m])[5m]
    D: increase(derivative(cpu_usage)[5m])[5m]
  correct_answer: 3
- question: How do you calculate the ratio of success to failure in the http_requests
    metric?
  options:
    A: success / failure
    B: success(failure)
    C: success + count(failure)
    D: success / sum(failure)
  correct_answer: 1
- question: Which PromQL expression calculates the difference between the maximum
    and minimum values of the memory_usage metric over the last 30 minutes?
  options:
    A: range_max(memory_usage[30m]) - range_min(memory_usage[30m])
    B: delta(memory_usage)[30m]
    C: range_max(memory_usage) - range_min(memory_usage)[30m]
    D: increase(max(memory_usage) - min(memory_usage))[30m]
  correct_answer: 1
- question: How do you compute the moving average of the temperature metric over a
    15-minute window?
  options:
    A: avg_over_time(temperature[15m])
    B: avg(temperature, 15m)
    C: increase(avg(temperature))[15m]
    D: rate(avg(temperature))[15m]
  correct_answer: 1
- question: What is the correct PromQL syntax to find the median of the response_time
    metric over the last hour?
  options:
    A: median_over_time(response_time[1h])
    B: quantile(0.5, response_time)[1h]
    C: median(response_time)[1h]
    D: percentile(response_time, 50)[1h]
  correct_answer: 2
- question: Which of the following PromQL expressions calculates the per-second rate
    of increase of the network_traffic metric over a 10-minute window?
  options:
    A: rate(network_traffic[10m])
    B: ((network_traffic))[10m]
    C: increase(network_traffic) / 10m
    D: rate(network_traffic) / 10m
  correct_answer: 1
- question: How would you compute the standard deviation of the latency metric over
    the last 5 minutes?
  options:
    A: stddev(latency)[5m]
    B: quantile(0.5, latency)[5m]
    C: delta(latency)[5m]
    D: stdev(latency)[5m]
  correct_answer: 1
- question: Which PromQL function is used to calculate the increase of a counter metric
    over time?
  options:
    A: increase()
    B: rate()
    C: delta()
    D: difference()
  correct_answer: 1
- question: How do you calculate the sum of the http_requests_total metric grouped
    by the status label?
  options:
    A: sum(http_requests_total) by (status)
    B: sum(http_requests_total) group by status
    C: sum(http_requests_total) without (status)
    D: sum(http_requests_total) on (status)
  correct_answer: 1
- question: Which PromQL function is used to compute the moving average of a metric
    over time?
  options:
    A: moving_avg()
    B: avg_over_time()
    C: rate()
    D: increase()
  correct_answer: 2
- question: How would you calculate the rate of change of the errors metric over a
    5-minute interval, accounting for resets to zero?
  options:
    A: irate(errors[5m])
    B: increase(errors[5m])
    C: rate(errors[5m])
    D: delta(errors[5m])
  correct_answer: 1
- question: Which function is used to find the lowest value of a metric over a specified
    time range?
  options:
    A: min_over_time()
    B: lowest()
    C: min()
    D: minimum()
  correct_answer: 1
- question: How do you calculate the sum of the disk_space_used metric over a 10-minute
    window for each instance?
  options:
    A: sum by (instance)(disk_space_used)[10m]
    B: sum(disk_space_used) group by instance[10m]
    C: sum(disk_space_used) by (instance)[10m]
    D: sum(disk_space_used) without (instance)[10m]
  correct_answer: 1
- question: Which function is used to compute the range of values for a metric over
    a specified time range?
  options:
    A: range_over_time()
    B: metric_range()
    C: range()
    D: value_range()
  correct_answer: 1
- question: How would you calculate the sum of the memory_usage metric over the last
    30 minutes, taking into account only samples where the value is greater than 1000?
  options:
    A: sum_over_time(memory_usage > 1000)[30m]
    B: sum(memory_usage) > 1000[30m]
    C: sum(memory_usage{memory_usage > 1000})[30m]
    D: sum(memory_usage > 1000)[30m]
  correct_answer: 1
- question: Which PromQL function is used to compute the absolute difference between
    the maximum and minimum values of a metric over a specified time range?
  options:
    A: range_abs()
    B: abs_range()
    C: difference()
    D: delta_abs()
  correct_answer: 1
- question: How do you calculate the average of the response_time metric over a 15-minute
    window, ignoring any samples where the value is zero?
  options:
    A: avg_over_time(response_time != 0)[15m]
    B: avg(response_time) unless response_time == 0[15m]
    C: avg(response_time) unless response_time = 0[15m]
    D: avg(response_time != 0)[15m]
  correct_answer: 1
- question: What is the correct PromQL expression to calculate the rate of increase
    of the http_requests_total metric over the last 10 minutes, filtering for the
    status code 200?
  options:
    A: increase(http_requests_total{status="200"})[10m]
    B: rate(http_requests_total{status="200"})[10m]
    C: increase(rate(http_requests_total{status="200"}))[10m]
    D: rate(increase(http_requests_total{status="200"}))[10m]
  correct_answer: 2
- question: How would you find the 90th percentile of the latency metric over the
    last hour, accounting for resets to zero?
  options:
    A: irate(quantile(0.90, latency)[1h])
    B: quantile(0.90, irate(latency)[1h])
    C: irate(quantile(0.90, latency))[1h]
    D: quantile(0.90, irate(latency))[1h]
  correct_answer: 4
- question: What is the correct PromQL expression to compute the moving average of
    the temperature metric over the last 15 minutes, filtering out any instances where
    the value is negative?
  options:
    A: avg_over_time(temperature > 0)[15m]
    B: avg(temperature) temperature < 0[15m]
    C: avg(temperature) unless temperature = 0[15m]
    D: avg(temperature > 0)[15m]
  correct_answer: 1
- question: How do you calculate the rate of change of the disk_io metric over the
    last 5 minutes, excluding any samples where the value is less than 10?
  options:
    A: irate(io > 10)[5m]
    B: irate(disk_io) > 1.0[5m]
    C: irate(disk_io{disk_io > 10})[5m]
    D: irate(avg_disk_io > 10)[5m]
  correct_answer: 3
- question: Which PromQL expression correctly calculates the ratio of successful_requests
    to total_requests over a 10-minute interval, excluding any samples where total_requests
    is zero?
  options:
    A: successful_requests / total_requests > 0 [10m]
    B: (successful_requests) // rate(total_requests) total_requests = 0 [10m]
    C: increase(successful_requests) / increase(total_requests) unless total_requests
      == 0 [10m]
    D: successful_requests + total_requests unless total_requests == 0 [10m]
  correct_answer: 3
- question: How would you find the maximum value of the cpu_temperature metric over
    the last 30 minutes, taking into account only samples where the device label is
    "cpu1"?
  options:
    A: max_over_time(cpu_temperature{device="cpu1"})[30m]
    B: max(cpu_temperature{device="cpu1"})[30m]
    C: max(cpu_temperature{device="cpu1"}[30m])
    D: max_over_time(cpu_temperature{device="cpu1"}[30m])
  correct_answer: 1
- question: What is the correct PromQL expression to calculate the 95th percentile
    of the response_time metric over the last 1 hour, excluding any samples where
    response_time is greater than 500 milliseconds?
  options:
    A: quantile(0.95response_time < 500)[1h]
    B: quantile_over_time(0.95, response_time[1h] unless response_time > 500)
    C: quantile(0.95, response_time) > 500 [1h]
    D: quantile(0.95, response_time) unless response_time > 500ms [1h]
  correct_answer: 2
- question: How do you compute the moving average of the network_throughput metric
    over the last 15 minutes, considering only samples where the value is above 1000?
  options:
    A: avg_over_time(network_throughput > 1000)[15m]
    B: avg(network_throughput) unless network_throughput <= 1000 [15m]
    C: avg(network_throughput) unless network_throughput <= 1000 [15m]
    D: avg_over_time(network_throughput > 1000)[15m]
  correct_answer: 1
- question: What is the correct PromQL expression to find the sum of disk_io_bytes
    for each instance over the last 5 minutes, excluding any instances where the sum
    is less than 1000 bytes?
  options:
    A: sum by (instance)(disk_io_bytes > 1000)[5m]
    B: (disk_io_bytes{disk_io_bytes > 1000}) by (instance)[5m]
    C: sum(disk_io_bytes) (disk_io_bytes) <= 1000 [5m]
    D: sum by (instance)(disk_io_bytes) unless sum(disk_io_bytes) <= 1000 [5m]
  correct_answer: 4
- question: How would you calculate the rate of change of the temperature metric over
    the last 10 minutes, excluding any samples where the value is less than 20?
  options:
    A: irate(temperature > 20)[10m]
    B: irate(temperature) > 20 [10m]
    C: irate(temperature{temperature > 20})[10m]
    D: (temperature > 0)[10m]
  correct_answer: 3
- question: What is the metric name for the query 'histogram_quantile(0.99, sum(rate(apiserver_request_duration_seconds_bucket{verb=~"LIST|GET",
    subresource!="log"}[2m])) by (verb,resource,subresource,component,apiserver,le))
    > 0'?
  options:
    A: ' "APIRequestRate"'
    B: ' "API99thWriteRequestLatency"'
    C: ' "API99thReadRequestLatency"'
    D: ' "flowControlRejectedRequest"'
  correct_answer: 3
- question: What is the query used to determine the API99thWriteRequestLatency?
  options:
    A: ' "sum(increase(apiserver_request_total{}[5m])) by (verb,resource,subresource,apiserver,component,code)
      > 0"'
    B: ' "histogram(0.99, sum(rate(apiserver_flowcontrol_request_wait_duration_seconds_bucket{}[5m]
      (le, flow_schema, prioritylevel)"'
    C: ' "histogram_quantile(0.99, sum(rate(apiserver_request_duration_seconds_bucket{verb=~""POST|PUT|PATCH|DELETE"",
      subresource!=""log""}[2m])) by (verb,resource,subresource,component,apiserver,le))
      > 0"'
    D: ' "sum(rate(apiserver_flowcontrol_dispatched_requests_total[2m])) by (flow_schema,priority_level)
      > 0"'
  correct_answer: 3
- question: What metric name corresponds to the query 'sum(increase(apiserver_request_total{}[5m]))
    by (verb,resource,subresource,apiserver,component,code) > 0'?
  options:
    A: ' "flowControl99thRequestExecution"'
    B: ' "flowControlRate"'
    C: ' "APIRequestCount"'
    D: ' "APIInflightRequests"'
  correct_answer: 3
- question: Which query is used to monitor the rate of requests handled by flow control?
  options:
    A: ' "sum(apiserver_current_inflight_requests{}) by (request_kind) > 0"'
    B: ' "sum(rate(apiserver_flowcontrol_dispatched_requests_total[2m])) by (flow_schema,priority_level)
      > 0"'
    C: ' "histogram_quantile(0.99, sum(rate(apiserver_request_duration_seconds_bucket{verb=~""LIST|GET"",
      subresource!=""log""}[2m])) by (verb,resource,subresource,component,apiserver,le))
      > 0"'
    D: ' "sum(irate(apiserver_request_total{}[2m])) by (verb,resource,subresource,apiserver,component,code)
      > 0"'
  correct_answer: 2
- question: What is the correct metric name for the query 'sum(rate(apiserver_flowcontrol_rejected_requests_total{}[5m]))
    by (flowSchema,reason) > 0'?
  options:
    A: ' "flowControlRejectedRequest"'
    B: ' "API99thReadRequestLatency"'
    C: ' "APIInflightRequests"'
    D: ' "flowControl99thRequestWait"'
  correct_answer: 1
- question: What query is used to find the 99th percentile request wait duration in
    flow control?
  options:
    A: ' "sum(irate(apiserver_request_total{}[2m])) by (verb,resource,subresource,apiserver,component,code)
      > 0"'
    B: ' "histogram_quantile(0.99, sum(rate(apiserver_flowcontrol_request_execution_seconds_bucket{}[5m]))
      by (le, flow_schema, priority_level)) > 0"'
    C: ' "histogram_quantile(0.99, sum(rate(apiserver_flowcontrol_request_wait_duration_seconds_bucket{}[5m]))
      by (le, flow_schema, priority_level)) > 0"'
    D: ' "sum(rate(apiserver_request_duration_seconds_bucket{verb=~""LIST|GET"", subresource!=""log""}[2m]))
      by (verb,resource,subresource,component,apiserver,le)) > 0"'
  correct_answer: 3
- question: Which query is used to determine the API inflight requests?
  options:
    A: ' "sum(apiserver_current_inflight_requests{}) by (request_kind) > 0"'
    B: ' "histogram_quantile(0.99, sum(rate(apiserver_flowcontrol_request_execution_seconds_bucket{}[5m]))
      by (le, flow_schema, priority_level)) > 0"'
    C: ' "sum(rate(apiserver_flowcontrol_rejected_requests_total{}[5m])) by (flowSchema,reason)
      > 0"'
    D: ' "sum(irate(apiserver_request_total{}[2m])) by (verb,resource,subresource,apiserver,component,code)
      > 0"'
  correct_answer: 1
- question: What metric name is used for the query 'sum(rate(apiserver_flowcontrol_dispatched_requests_total[2m]))
    by (flow_schema,priority_level) > 0'?
  options:
    A: ' "APIRequestRate"'
    B: ' "flowControlRejectedRequest"'
    C: ' "flowControlRate"'
    D: ' "flowControl99thRequestExecution"'
  correct_answer: 3
- question: Which query determines the 99th percentile of request execution time in
    flow control?
  options:
    A: ' "sum(rate(apiserver_request_duration_seconds_bucket{verb=~""POST|PUT|PATCH|DELETE"",
      subresource!=""log""}[2m])) by (verb,resource,subresource,component,apiserver,le))
      > 0"'
    B: ' "histogram_quantile(0.99, sum(rate(apiserver_flowcontrol_request_execution_seconds_bucket{}[5m]))
      by (le, flow_schema, priority_level)) > 0"'
    C: ' "histogram_quantile(0.99, sum(rate(apiserver_flowcontrol_request_wait_duration_seconds_bucket{}[5m]))
      by (le, flow_schema, priority_level)) > 0"'
    D: ' "sum(apiserver_current_inflight_requests{}) by (request_kind) > 0"'
  correct_answer: 2
- question: Which of the following PromQL queries correctly calculates the rate of
    HTTP requests per job over the last 5 minutes?
  options:
    A: sum by (job) (rate(http_requests_total[5m]))
    B: rate(http_requests_total[5m]) by (job)
    C: rate(sum by (job) (http_requests_total[5m]))
    D: rate(http_requests_total{job}[5m])
  correct_answer: 1
- question: What is the correct PromQL query to select the CPU time in nanoseconds
    for a web process in a production environment for a specific application, revision,
    and job?
  options:
    A: instance_cpu_time_ns{app="tiger", proc="db", rev="34d0f99", env="dev", job="cluster-manager"}
    B: instance_cpu_time_ns{app="lion", proc="web", rev="34d0f99", env="prod", job="cluster-manager"}
    C: instance_cpu_time_ns{app="lion", proc="web", rev="34d0f99", env="staging",
      job="manager"}
    D: instance_cpu_time_ns{app="lion", proc="web", rev="1234abcd", env="prod", job="cluster-manager"}
  correct_answer: 2
