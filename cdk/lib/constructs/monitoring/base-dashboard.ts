import { Construct } from 'constructs';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as apigwv2 from 'aws-cdk-lib/aws-apigatewayv2'; // Correct CDK v2 import
import * as cw_actions from 'aws-cdk-lib/aws-cloudwatch-actions'; // Import for SnsAction
import { Duration, Stack } from 'aws-cdk-lib';
import { ComparisonOperator, TreatMissingData } from 'aws-cdk-lib/aws-cloudwatch';
import { BaseDashboardProps } from './monitoring-base-props'; // Import props
import * as logs from 'aws-cdk-lib/aws-logs'; // Import logs
import { LogGroup } from 'aws-cdk-lib/aws-logs'; // Import LogGroup specifically
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as pipes from 'aws-cdk-lib/aws-pipes';
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class BaseDashboard extends Construct {
    public readonly dashboard: cloudwatch.Dashboard;
    public readonly alertTopic: sns.Topic;
    public readonly criticalAlarms: cloudwatch.Alarm[] = [];

    constructor(scope: Construct, id: string, props: BaseDashboardProps) {
        super(scope, id);

        const stack = Stack.of(this);
        const prefix = props.dashboardNamePrefix ? `${props.dashboardNamePrefix}-` : '';
        const dashboardName = `${prefix}${stack.stackName}-ServiceHealth-Overview`;
        const alarmPrefix = `${prefix}${stack.stackName}`;
        const anomalyStdDev = props.anomalyDetectionStandardDeviation ?? 2;

        // --- Central SNS Topic for Alerts ---
        this.alertTopic = new sns.Topic(this, 'AlertTopic', {
            displayName: `${alarmPrefix}-Alerts`,
            topicName: `${alarmPrefix}-Alerts`,
        });
        cdk.Tags.of(this.alertTopic).add('Component', 'Monitoring');


        this.dashboard = new cloudwatch.Dashboard(this, 'ServiceHealthOverviewDashboard', {
            dashboardName: dashboardName,
            periodOverride: cloudwatch.PeriodOverride.AUTO,
            start: '-PT3H',
        });
        cdk.Tags.of(this.dashboard).add('Component', 'Monitoring');

        // --- Define ALL potential Widgets (Declaration) ---
        // Array to collect widgets in order
        const widgetsToAdd: cloudwatch.IWidget[] = [];

        // API GW Widgets
        const titleWidget = new cloudwatch.TextWidget({
            markdown: `# ${dashboardName}
Key operational metrics and anomaly detection overview.`,
            width: 24,
            height: 2
        });

        // Define criticalAlarmStatusWidget with width 12
        const criticalAlarmStatusWidget = new cloudwatch.AlarmStatusWidget({
            title: 'Critical Alarm Status',
            alarms: this.criticalAlarms,
            width: 12,
            height: 6,
            sortBy: cloudwatch.AlarmStatusWidgetSortBy.STATE_UPDATED_TIMESTAMP,
            states: [cloudwatch.AlarmState.ALARM, cloudwatch.AlarmState.INSUFFICIENT_DATA, cloudwatch.AlarmState.OK]
        });

        // --- API Gateway Widgets ---
        const apiGwHeaderWidget = new cloudwatch.TextWidget({ markdown: `## API Gateway`, width: 24, height: 1 });

        const getApiMetric = (metricName: string, statistic: string, label?: string) => {
            return props.httpApi.metric(metricName, {
                statistic: statistic,
                period: Duration.minutes(5),
                label: label ?? metricName,
            });
        };

        const apiGwWidget = new cloudwatch.GraphWidget({
            title: 'API Req, Latency (Avg/p90/p99), 5xx Err',
            left: [
                getApiMetric('Count', 'Sum', 'Requests').with({ color: '#1f77b4' }),
                getApiMetric('5xx', 'Sum', '5xx Errors').with({ color: '#ff7f0e' }),
            ],
            right: [
                getApiMetric('Latency', 'Average', 'Latency Avg (ms)').with({ color: '#2ca02c' }),
                getApiMetric('Latency', 'p90', 'Latency p90 (ms)').with({ color: '#98df8a' }),
                getApiMetric('Latency', 'p99', 'Latency p99 (ms)').with({ color: '#ff9896' }),
            ],
            width: 12,
            height: 6,
            leftYAxis: { min: 0 },
            rightYAxis: { min: 0, label: 'Milliseconds' },
        });

        const apiLatencyP99Metric = getApiMetric('Latency', 'p99');
        const apiLatencyAnomalyWidget = new cloudwatch.GraphWidget({
            title: 'API Latency P99 & Anomaly Band',
            left: [
                 new cloudwatch.MathExpression({
                    expression: `ANOMALY_DETECTION_BAND(m1, ${anomalyStdDev})`,
                    usingMetrics: { m1: apiLatencyP99Metric },
                    label: `Anomaly Band (StdDev ${anomalyStdDev})`,
                    color: '#ffb74d',
                    period: Duration.minutes(5)
                }),
                 apiLatencyP99Metric.with({label: 'Latency P99', color: '#1f77b4', period: Duration.minutes(5) })
            ],
            width: 12,
            height: 6,
            leftYAxis: { label: 'Milliseconds', min: 0 },
            period: Duration.minutes(5)
        });

        // --- API Gateway Alarms ---
        const highApi5xxAlarm = new cloudwatch.Alarm(this, 'Api5xxCriticalAlarm', {
            alarmName: `${alarmPrefix}-Api5xxErrors-Critical`,
            alarmDescription: 'CRITICAL: High number of API Gateway 5xx errors',
            metric: getApiMetric('5xx', 'Sum'),
            threshold: 5,
            evaluationPeriods: 2,
            comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treatMissingData: TreatMissingData.NOT_BREACHING,
        });
        highApi5xxAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
        this.criticalAlarms.push(highApi5xxAlarm);

        const highApiLatencyWarning = new cloudwatch.Alarm(this, 'ApiLatencyP99Warning', {
            alarmName: `${alarmPrefix}-ApiLatencyP99-Warning`,
            alarmDescription: 'WARN: High API Gateway p99 latency',
            metric: apiLatencyP99Metric,
            threshold: 3000,
            evaluationPeriods: 3,
            comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treatMissingData: TreatMissingData.NOT_BREACHING,
        });
        highApiLatencyWarning.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));

        const apiLatencyAnomalyAlarm = new cloudwatch.CfnAlarm(this, 'ApiLatencyP99AnomalyAlarm', {
            alarmName: `${alarmPrefix}-ApiLatencyP99-Anomaly`,
            alarmDescription: `ANOMALY: Unusual spike in API Gateway p99 latency detected (StdDev: ${anomalyStdDev})`,
            comparisonOperator: 'GreaterThanUpperThreshold',
            evaluationPeriods: 2,
            treatMissingData: 'ignore',
            metrics: [
                {
                    id: 'm1',
                    metricStat: {
                        metric: {
                            namespace: apiLatencyP99Metric.namespace,
                            metricName: apiLatencyP99Metric.metricName,
                            dimensions: Object.entries(apiLatencyP99Metric.dimensions || {}).map(([name, value]) => ({ name, value: String(value) })),
                        },
                        period: apiLatencyP99Metric.period.toSeconds(),
                        stat: apiLatencyP99Metric.statistic,
                        unit: apiLatencyP99Metric.unit,
                    },
                    returnData: true,
                },
                {
                    id: 't1',
                    expression: `ANOMALY_DETECTION_BAND(m1, ${anomalyStdDev})`,
                    label: `Latency P99 Anomaly Band (StdDev ${anomalyStdDev})`,
                    returnData: true,
                },
            ],
            thresholdMetricId: 't1',
            alarmActions: [this.alertTopic.topicArn],
        });

        // --- Lambda Handler Widgets ---
        const lambdaHeaderWidget = new cloudwatch.TextWidget({ markdown: `## Lambda Handler: ${props.apiLambdaHandler.functionName}`, width: 24, height: 1 });

        const apiLambdaWidget = new cloudwatch.GraphWidget({
            title: 'Lambda Invokes, Duration (Avg/p90/p99), Err, Thrtl, Concurrency',
            left: [
                props.apiLambdaHandler.metricInvocations({ label: 'Invocations', period: Duration.minutes(5) }).with({ color: '#1f77b4' }),
                props.apiLambdaHandler.metricErrors({ label: 'Errors', period: Duration.minutes(5) }).with({ color: '#d62728' }),
                props.apiLambdaHandler.metricThrottles({ label: 'Throttles', period: Duration.minutes(5) }).with({ color: '#ff7f0e' }),
                props.apiLambdaHandler.metric('ConcurrentExecutions', {
                    label: 'Concurrency (Max)',
                    statistic: 'Maximum',
                    period: Duration.minutes(5),
                }).with({ color: '#9467bd' }),
            ],
            right: [
                props.apiLambdaHandler.metricDuration({ statistic: 'Average', label: 'Duration Avg (ms)', period: Duration.minutes(5) }).with({ color: '#2ca02c' }),
                props.apiLambdaHandler.metricDuration({ statistic: 'p90', label: 'Duration p90 (ms)', period: Duration.minutes(5) }).with({ color: '#98df8a' }),
                props.apiLambdaHandler.metricDuration({ statistic: 'p99', label: 'Duration p99 (ms)', period: Duration.minutes(5) }).with({ color: '#ff9896' }),
            ],
            width: 12,
            height: 6,
            leftYAxis: { min: 0 },
            rightYAxis: { min: 0, label: 'Milliseconds' },
        });

        const lambdaDurationP99Metric = props.apiLambdaHandler.metricDuration({ statistic: 'p99', period: Duration.minutes(5) });
        const lambdaDurationAnomalyWidget = new cloudwatch.GraphWidget({
            title: 'Lambda Duration P99 & Anomaly Band',
            left: [
                new cloudwatch.MathExpression({
                    expression: `ANOMALY_DETECTION_BAND(m1, ${anomalyStdDev})`,
                    usingMetrics: { m1: lambdaDurationP99Metric },
                    label: `Anomaly Band (StdDev ${anomalyStdDev})`,
                    color: '#ffb74d',
                    period: Duration.minutes(5)
                }),
                lambdaDurationP99Metric.with({ label: 'Duration P99', color: '#1f77b4', period: Duration.minutes(5) })
            ],
            width: 12,
            height: 6,
            leftYAxis: { label: 'Milliseconds', min: 0 },
            period: Duration.minutes(5)
        });

        // --- Lambda Handler Alarms ---
        const highLambdaErrorsAlarm = new cloudwatch.Alarm(this, 'LambdaErrorsCriticalAlarm', {
            alarmName: `${alarmPrefix}-LambdaErrors-Critical`,
            alarmDescription: `CRITICAL: High number of errors for Lambda ${props.apiLambdaHandler.functionName}`,
            metric: props.apiLambdaHandler.metricErrors({ period: Duration.minutes(5) }),
            threshold: 5,
            evaluationPeriods: 2,
            comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treatMissingData: TreatMissingData.NOT_BREACHING,
        });
        highLambdaErrorsAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
        this.criticalAlarms.push(highLambdaErrorsAlarm);

        const highLambdaDurationWarning = new cloudwatch.Alarm(this, 'LambdaDurationP99Warning', {
            alarmName: `${alarmPrefix}-LambdaDurationP99-Warning`,
            alarmDescription: `WARN: High p99 duration for Lambda ${props.apiLambdaHandler.functionName}`,
            metric: lambdaDurationP99Metric,
            threshold: 5000,
            evaluationPeriods: 3,
            comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treatMissingData: TreatMissingData.NOT_BREACHING,
        });
        highLambdaDurationWarning.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));

        const lambdaDurationAnomalyAlarm = new cloudwatch.CfnAlarm(this, 'LambdaDurationP99AnomalyAlarm', {
            alarmName: `${alarmPrefix}-LambdaDurationP99-Anomaly`,
            alarmDescription: `ANOMALY: Unusual spike in p99 duration for Lambda ${props.apiLambdaHandler.functionName} (StdDev: ${anomalyStdDev})`,
            comparisonOperator: 'GreaterThanUpperThreshold',
            evaluationPeriods: 2,
            treatMissingData: 'ignore',
            metrics: [
                {
                    id: 'm1',
                    metricStat: {
                        metric: {
                            namespace: lambdaDurationP99Metric.namespace,
                            metricName: lambdaDurationP99Metric.metricName,
                            dimensions: Object.entries(lambdaDurationP99Metric.dimensions || {}).map(([name, value]) => ({ name, value: String(value) })),
                        },
                        period: lambdaDurationP99Metric.period.toSeconds(),
                        stat: lambdaDurationP99Metric.statistic,
                        unit: lambdaDurationP99Metric.unit,
                    },
                    returnData: true,
                },
                {
                    id: 't1',
                    expression: `ANOMALY_DETECTION_BAND(m1, ${anomalyStdDev})`,
                    label: `Duration P99 Anomaly Band (StdDev ${anomalyStdDev})`,
                    returnData: true,
                },
            ],
            thresholdMetricId: 't1',
            alarmActions: [this.alertTopic.topicArn],
        });

        widgetsToAdd.push(lambdaHeaderWidget, apiLambdaWidget, lambdaDurationAnomalyWidget);
        // --- END API Lambda Handler ---

        // --- WebSocket Lambda Handler Widgets & Alarms (NEW SECTION) ---
        if (props.webSocketHandler) {
            const wsLambda = props.webSocketHandler;
            const wsLambdaName = wsLambda.functionName;
            const wsLambdaHeaderWidget = new cloudwatch.TextWidget({ markdown: `## WebSocket Lambda Handler: ${wsLambdaName}`, width: 24, height: 1 });
            const wsLambdaWidget = new cloudwatch.GraphWidget({
                title: 'WS Lambda Invokes, Duration (Avg/p90/p99), Err, Thrtl, Concurrency',
                 left: [
                     wsLambda.metricInvocations({ label: 'Invocations', period: Duration.minutes(5) }).with({ color: '#1f77b4' }),
                     wsLambda.metricErrors({ label: 'Errors', period: Duration.minutes(5) }).with({ color: '#d62728' }),
                     wsLambda.metricThrottles({ label: 'Throttles', period: Duration.minutes(5) }).with({ color: '#ff7f0e' }),
                     wsLambda.metric('ConcurrentExecutions', {
                         label: 'Concurrency (Max)',
                         statistic: 'Maximum',
                         period: Duration.minutes(5),
                     }).with({ color: '#9467bd' }),
                 ],
                 right: [
                     wsLambda.metricDuration({ statistic: 'Average', label: 'Duration Avg (ms)', period: Duration.minutes(5) }).with({ color: '#2ca02c' }),
                     wsLambda.metricDuration({ statistic: 'p90', label: 'Duration p90 (ms)', period: Duration.minutes(5) }).with({ color: '#98df8a' }),
                     wsLambda.metricDuration({ statistic: 'p99', label: 'Duration p99 (ms)', period: Duration.minutes(5) }).with({ color: '#ff9896' }),
                 ],
                width: 12, height: 6, leftYAxis: { min: 0 }, rightYAxis: { min: 0, label: 'Milliseconds' },
            });
            const wsLambdaDurationP99Metric = wsLambda.metricDuration({ statistic: 'p99', period: Duration.minutes(5) });
            const wsLambdaDurationAnomalyWidget = new cloudwatch.GraphWidget({
                title: 'WS Lambda Duration P99 & Anomaly Band',
                 left: [
                     new cloudwatch.MathExpression({
                         expression: `ANOMALY_DETECTION_BAND(m1, ${anomalyStdDev})`,
                         usingMetrics: { m1: wsLambdaDurationP99Metric },
                         label: `Anomaly Band (StdDev ${anomalyStdDev})`,
                         color: '#ffb74d',
                         period: Duration.minutes(5)
                     }),
                     wsLambdaDurationP99Metric.with({ label: 'Duration P99', color: '#1f77b4', period: Duration.minutes(5) })
                 ],
                width: 12, height: 6, leftYAxis: { label: 'Milliseconds', min: 0 }, period: Duration.minutes(5)
            });
            // WebSocket Lambda Alarms
            const highWsLambdaErrorsAlarm = new cloudwatch.Alarm(this, 'WsLambdaErrorsCriticalAlarm', {
                alarmName: `${alarmPrefix}-WsLambdaErrors-Critical`,
                alarmDescription: `CRITICAL: High number of errors for WebSocket Lambda ${wsLambdaName}`,
                metric: wsLambda.metricErrors({ period: Duration.minutes(5) }),
                threshold: 5, evaluationPeriods: 2, comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, treatMissingData: TreatMissingData.NOT_BREACHING,
            });
            highWsLambdaErrorsAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
            const highWsLambdaDurationWarning = new cloudwatch.Alarm(this, 'WsLambdaDurationP99Warning', {
                 alarmName: `${alarmPrefix}-WsLambdaDurationP99-Warning`,
                 alarmDescription: `WARN: High p99 duration for WebSocket Lambda ${wsLambdaName}`,
                 metric: wsLambdaDurationP99Metric,
                 threshold: 5000, evaluationPeriods: 3, comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, treatMissingData: TreatMissingData.NOT_BREACHING,
            });
            highWsLambdaDurationWarning.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
            const wsLambdaDurationAnomalyAlarm = new cloudwatch.CfnAlarm(this, 'WsLambdaDurationP99AnomalyAlarm', {
                 alarmName: `${alarmPrefix}-WsLambdaDurationP99-Anomaly`,
                 alarmDescription: `ANOMALY: Unusual spike in p99 duration for WebSocket Lambda ${wsLambdaName} (StdDev: ${anomalyStdDev})`,
                 comparisonOperator: 'GreaterThanUpperThreshold',
                 evaluationPeriods: 2,
                 treatMissingData: 'ignore',
                 metrics: [
                    {
                        id: 'm1',
                        metricStat: {
                            metric: {
                                namespace: wsLambdaDurationP99Metric.namespace,
                                metricName: wsLambdaDurationP99Metric.metricName,
                                dimensions: Object.entries(wsLambdaDurationP99Metric.dimensions || {}).map(([name, value]) => ({ name, value: String(value) })),
                            },
                            period: wsLambdaDurationP99Metric.period.toSeconds(),
                            stat: wsLambdaDurationP99Metric.statistic,
                            unit: wsLambdaDurationP99Metric.unit,
                        },
                        returnData: true,
                    },
                    {
                        id: 't1',
                        expression: `ANOMALY_DETECTION_BAND(m1, ${anomalyStdDev})`,
                        label: `Duration P99 Anomaly Band (StdDev ${anomalyStdDev})`,
                        returnData: true,
                    },
                 ],
                 thresholdMetricId: 't1',
                 alarmActions: [this.alertTopic.topicArn],
            });
            // Add WebSocket widgets to the general list
            widgetsToAdd.push(wsLambdaHeaderWidget, wsLambdaWidget, wsLambdaDurationAnomalyWidget);
        }
        // --- END WebSocket Lambda Handler ---

        // --- DynamoDB Widgets ---
        const ddbHeaderWidget = new cloudwatch.TextWidget({ markdown: `## DynamoDB Tables`, width: 24, height: 1 });

        const getDdbMetric = (table: dynamodb.ITable, metricName: string, statistic: string, label?: string) => {
            return table.metric(metricName, {
                statistic: statistic,
                period: Duration.minutes(5),
                label: label ?? `${table.tableName} ${metricName}`,
            });
        };

        const chatTableWidget = new cloudwatch.GraphWidget({
            title: `DDB - ${props.conversationTable.tableName} - RCU/WCU, Latency, Throttles`,
            left: [
                getDdbMetric(props.conversationTable, 'ConsumedReadCapacityUnits', 'Sum', 'Read Units').with({ color: '#1f77b4' }),
                getDdbMetric(props.conversationTable, 'ConsumedWriteCapacityUnits', 'Sum', 'Write Units').with({ color: '#aec7e8' }),
                getDdbMetric(props.conversationTable, 'ReadThrottleEvents', 'Sum', 'Read Throttles').with({ color: '#ff7f0e' }),
                getDdbMetric(props.conversationTable, 'WriteThrottleEvents', 'Sum', 'Write Throttles').with({ color: '#ffbb78' }),
            ],
            right: [
                getDdbMetric(props.conversationTable, 'SuccessfulRequestLatency', 'Average', 'Avg Latency (ms)').with({ color: '#2ca02c' }),
            ],
            width: 12,
            height: 6,
            leftYAxis: { min: 0, label: 'Various units' },
            rightYAxis: { min: 0, label: 'Milliseconds' },
        });

        const botsTableWidget = new cloudwatch.GraphWidget({
            title: `DDB - ${props.botsMetadataTable.tableName} - RCU/WCU, Latency, Throttles`,
            left: [
                getDdbMetric(props.botsMetadataTable, 'ConsumedReadCapacityUnits', 'Sum', 'Read Units').with({ color: '#1f77b4' }),
                getDdbMetric(props.botsMetadataTable, 'ConsumedWriteCapacityUnits', 'Sum', 'Write Units').with({ color: '#aec7e8' }),
                getDdbMetric(props.botsMetadataTable, 'ReadThrottleEvents', 'Sum', 'Read Throttles').with({ color: '#ff7f0e' }),
                getDdbMetric(props.botsMetadataTable, 'WriteThrottleEvents', 'Sum', 'Write Throttles').with({ color: '#ffbb78' }),
            ],
            right: [
                getDdbMetric(props.botsMetadataTable, 'SuccessfulRequestLatency', 'Average', 'Avg Latency (ms)').with({ color: '#2ca02c' }),
            ],
            width: 12,
            height: 6,
            leftYAxis: { min: 0, label: 'Various units' },
            rightYAxis: { min: 0, label: 'Milliseconds' },
        });

        // --- DynamoDB Alarms ---
        const ddbReadThrottleMetric = new cloudwatch.MathExpression({
            expression: "m1 + m2",
            usingMetrics: {
                m1: getDdbMetric(props.conversationTable, 'ReadThrottleEvents', 'Sum'),
                m2: getDdbMetric(props.botsMetadataTable, 'ReadThrottleEvents', 'Sum'),
            },
            label: 'Total Read Throttles',
            period: Duration.minutes(5),
        });
        const ddbReadThrottleAlarm = new cloudwatch.Alarm(this, 'DynamoDbReadThrottlesCriticalAlarm', {
            alarmName: `${alarmPrefix}-DynamoDbReadThrottles-Critical`,
            alarmDescription: 'CRITICAL: High number of DynamoDB read throttle events across tables',
            metric: ddbReadThrottleMetric,
            threshold: 10,
            evaluationPeriods: 3,
            comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treatMissingData: TreatMissingData.NOT_BREACHING,
        });
        ddbReadThrottleAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
        this.criticalAlarms.push(ddbReadThrottleAlarm);

        const ddbWriteThrottleMetric = new cloudwatch.MathExpression({
            expression: "m1 + m2",
            usingMetrics: {
                m1: getDdbMetric(props.conversationTable, 'WriteThrottleEvents', 'Sum'),
                m2: getDdbMetric(props.botsMetadataTable, 'WriteThrottleEvents', 'Sum'),
            },
            label: 'Total Write Throttles',
            period: Duration.minutes(5),
        });
        const ddbWriteThrottleAlarm = new cloudwatch.Alarm(this, 'DynamoDbWriteThrottlesCriticalAlarm', {
            alarmName: `${alarmPrefix}-DynamoDbWriteThrottles-Critical`,
            alarmDescription: 'CRITICAL: High number of DynamoDB write throttle events across tables',
            metric: ddbWriteThrottleMetric,
            threshold: 10,
            evaluationPeriods: 3,
            comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treatMissingData: TreatMissingData.NOT_BREACHING,
        });
        ddbWriteThrottleAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
        this.criticalAlarms.push(ddbWriteThrottleAlarm);

        // --- S3 Exporter Widgets & Alarms (Conditional) ---
        let s3ExporterHeaderWidget: cloudwatch.TextWidget | undefined;
        let s3ExporterWidget: cloudwatch.GraphWidget | undefined;
        let s3ExporterLogErrorsMetric: cloudwatch.Metric | undefined;
        let codeBuildLogErrorsMetric: cloudwatch.Metric | undefined;

        if (props.s3ExporterLambda) {
            s3ExporterHeaderWidget = new cloudwatch.TextWidget({ markdown: `## S3 Exporter Lambda: ${props.s3ExporterLambda.functionName}`, width: 24, height: 1 });
            s3ExporterWidget = new cloudwatch.GraphWidget({
                title: 'Exporter Lambda - Invocations, Duration, Errors, Throttles',
                left: [
                    props.s3ExporterLambda.metricInvocations({ label: 'Invocations', period: Duration.minutes(5) }).with({ color: '#1f77b4' }),
                    props.s3ExporterLambda.metricErrors({ label: 'Errors', period: Duration.minutes(5) }).with({ color: '#d62728' }),
                    props.s3ExporterLambda.metricThrottles({ label: 'Throttles', period: Duration.minutes(5) }).with({ color: '#ff7f0e' }),
                ],
                right: [
                    props.s3ExporterLambda.metricDuration({ statistic: 'Average', label: 'Duration Avg (ms)', period: Duration.minutes(5) }).with({ color: '#2ca02c' })
                ],
                width: 12,
                height: 6,
                leftYAxis: { min: 0 },
                rightYAxis: { min: 0, label: 'Milliseconds' },
            });

            const highS3ExporterErrorAlarm = new cloudwatch.Alarm(this, 'S3ExporterLambdaErrorsCriticalAlarm', {
                alarmName: `${alarmPrefix}-S3ExporterLambdaErrors-Critical`,
                alarmDescription: `CRITICAL: High number of errors for S3 Exporter Lambda ${props.s3ExporterLambda.functionName}`,
                metric: props.s3ExporterLambda.metricErrors({ period: Duration.minutes(5) }),
                threshold: 1,
                evaluationPeriods: 1,
                comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                treatMissingData: TreatMissingData.NOT_BREACHING,
            });
            highS3ExporterErrorAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
            this.criticalAlarms.push(highS3ExporterErrorAlarm);

            widgetsToAdd.push(s3ExporterHeaderWidget);
            widgetsToAdd.push(s3ExporterWidget);
        }

        // --- Step Function Widgets & Alarms (Conditional) ---
        let sfnHeaderWidget: cloudwatch.TextWidget | undefined;
        let stateMachineWidget: cloudwatch.GraphWidget | undefined;
        if (props.embeddingStateMachine) {
            const stateMachineIdentifier = props.embeddingStateMachine.stateMachineArn;
            sfnHeaderWidget = new cloudwatch.TextWidget({ markdown: `## Embedding Step Function: ${stateMachineIdentifier}`, width: 24, height: 1 });

            const getSfnMetric = (metricName: string, statistic: string, label?: string) => {
                return new cloudwatch.Metric({
                    namespace: 'AWS/States',
                    metricName: metricName,
                    dimensionsMap: { StateMachineArn: stateMachineIdentifier },
                    statistic: statistic,
                    period: Duration.minutes(5),
                    label: label ?? metricName,
                });
            };

            stateMachineWidget = new cloudwatch.GraphWidget({
                title: 'Step Function - Executions, Failed, Timed Out, Avg Time',
                left: [
                    getSfnMetric('ExecutionsStarted', 'Sum', 'Executions Started').with({ color: '#1f77b4' }),
                    props.embeddingStateMachine.metricFailed({ label: 'Failed', period: Duration.minutes(5), statistic: 'Sum' }).with({ color: '#d62728' }),
                    props.embeddingStateMachine.metricTimedOut({ label: 'Timed Out', period: Duration.minutes(5), statistic: 'Sum' }).with({ color: '#ff7f0e' }),
                ],
                right: [
                    getSfnMetric('ExecutionTime', 'Average', 'Execution Time Avg (ms)').with({ color: '#2ca02c' }),
                ],
                width: 12,
                height: 6,
                leftYAxis: { min: 0 },
                rightYAxis: { min: 0, label: 'Milliseconds' },
            });

            const stepFunctionFailureAlarm = new cloudwatch.Alarm(this, 'StepFunctionFailuresCriticalAlarm', {
                alarmName: `${alarmPrefix}-StepFunctionFailures-Critical`,
                alarmDescription: `CRITICAL: High number of failures for Step Function ${stateMachineIdentifier}`,
                metric: props.embeddingStateMachine.metricFailed({ period: Duration.minutes(5), statistic: 'Sum' }),
                threshold: 1,
                evaluationPeriods: 1,
                comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                treatMissingData: TreatMissingData.NOT_BREACHING,
            });
            stepFunctionFailureAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
            this.criticalAlarms.push(stepFunctionFailureAlarm);

            const stepFunctionTimeoutAlarm = new cloudwatch.Alarm(this, 'StepFunctionTimeoutsCriticalAlarm', {
                alarmName: `${alarmPrefix}-StepFunctionTimeouts-Critical`,
                alarmDescription: `CRITICAL: High number of timeouts for Step Function ${stateMachineIdentifier}`,
                metric: props.embeddingStateMachine.metricTimedOut({ period: Duration.minutes(5), statistic: 'Sum' }),
                threshold: 1,
                evaluationPeriods: 1,
                comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                treatMissingData: TreatMissingData.NOT_BREACHING,
            });
            stepFunctionTimeoutAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
            this.criticalAlarms.push(stepFunctionTimeoutAlarm);

            if (sfnHeaderWidget) widgetsToAdd.push(sfnHeaderWidget);
            if (stateMachineWidget) widgetsToAdd.push(stateMachineWidget);
        }

        // --- CodeBuild Widgets & Alarms (Conditional) ---
        let codeBuildHeaderWidget: cloudwatch.TextWidget | undefined;
        let codeBuildWidget: cloudwatch.GraphWidget | undefined;
        if (props.knowledgeBaseCodeBuild) {
            codeBuildHeaderWidget = new cloudwatch.TextWidget({ markdown: `## Knowledge Base Build: ${props.knowledgeBaseCodeBuild.projectName}`, width: 24, height: 1 });

            const getCodeBuildMetric = (metricName: string, statistic: string, label?: string) => {
                return new cloudwatch.Metric({
                    namespace: 'AWS/CodeBuild',
                    metricName: metricName,
                    dimensionsMap: { ProjectName: props.knowledgeBaseCodeBuild!.projectName },
                    statistic: statistic,
                    period: Duration.minutes(5),
                    label: label ?? metricName,
                });
            };

            codeBuildWidget = new cloudwatch.GraphWidget({
                title: 'CodeBuild - Builds, Failed Builds, Duration (Avg)',
                left: [
                    getCodeBuildMetric('Builds', 'Sum', 'Builds Started').with({ color: '#1f77b4' }),
                    getCodeBuildMetric('FailedBuilds', 'Sum', 'Failed Builds').with({ color: '#d62728' }),
                ],
                right: [
                    getCodeBuildMetric('Duration', 'Average', 'Duration Avg (s)').with({ color: '#2ca02c' })
                ],
                width: 12,
                height: 6,
                leftYAxis: { min: 0 },
                rightYAxis: { min: 0, label: 'Seconds' },
                period: Duration.minutes(5)
            });

            const codeBuildFailureAlarm = new cloudwatch.Alarm(this, 'CodeBuildFailuresCriticalAlarm', {
                alarmName: `${alarmPrefix}-CodeBuildFailures-Critical`,
                alarmDescription: `CRITICAL: High number of failures for CodeBuild Project ${props.knowledgeBaseCodeBuild.projectName}`,
                metric: getCodeBuildMetric('FailedBuilds', 'Sum'),
                threshold: 1,
                evaluationPeriods: 1,
                comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                treatMissingData: TreatMissingData.NOT_BREACHING,
            });
            codeBuildFailureAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
            this.criticalAlarms.push(codeBuildFailureAlarm);

            if (codeBuildHeaderWidget) widgetsToAdd.push(codeBuildHeaderWidget);
            if (codeBuildWidget) widgetsToAdd.push(codeBuildWidget);
        }

        // --- Log-Based Error Widgets (Define placeholder or graph) ---
        let logErrorWidget: cloudwatch.IWidget; // Changed type to IWidget to allow Text or Graph

        if (props.apiLambdaHandler) {
            // Use the passed-in apiLambdaLogGroup prop if available
            const apiLambdaLogGroup = props.apiLambdaLogGroup;

            // Use the passed-in s3ExporterLogGroup prop if available
            const s3ExporterLogGroup = props.s3ExporterLogGroup;


            // Use the passed-in codeBuildLogGroup prop if available
            const codeBuildLogGroup = props.codeBuildLogGroup;

            const logErrorMetrics: cloudwatch.Metric[] = [];

            let wsLogErrorsMetric: cloudwatch.Metric | undefined;

            // Only create API Lambda filters if the log group is provided
            if (apiLambdaLogGroup) {
                const authErrorFilter = new logs.MetricFilter(this, 'AuthenticationErrorFilter', {
                    logGroup: apiLambdaLogGroup, // Use prop
                    metricNamespace: 'QikrChat/Logs',
                    metricName: 'AuthenticationErrors',
                    filterPattern: logs.FilterPattern.literal('?"JWT Audience verification failed" ?"JWT Token has expired" ?"Permission action" ?"is not configured" ?"User not found in request state" ?"Invalid token"'),
                    metricValue: '1',
                });
                logErrorMetrics.push(authErrorFilter.metric({ label: 'Auth Errors', statistic: 'Sum', period: Duration.minutes(5), color: '#e41a1c' }));

                const dbErrorFilter = new logs.MetricFilter(this, 'DatabaseErrorFilter', {
                    logGroup: apiLambdaLogGroup, // Use prop
                    metricNamespace: 'QikrChat/Logs',
                    metricName: 'DatabaseErrors',
                    filterPattern: logs.FilterPattern.literal('?"DynamoDB" ?"error" ?"Failed to get table resource" ?"Failed to assume role" ?"TABLE_ACCESS_ROLE_ARN is not set"'),
                    metricValue: '1',
                });
                logErrorMetrics.push(dbErrorFilter.metric({ label: 'DB Errors', statistic: 'Sum', period: Duration.minutes(5), color: '#377eb8' }));

                const bedrockErrorFilter = new logs.MetricFilter(this, 'BedrockErrorFilter', {
                    logGroup: apiLambdaLogGroup, // Use prop
                    metricNamespace: 'QikrChat/Logs',
                    metricName: 'BedrockErrors',
                    filterPattern: logs.FilterPattern.literal('?"Error querying Bedrock Knowledge Base" ?"Error in content model conversion"'),
                    metricValue: '1',
                });
                logErrorMetrics.push(bedrockErrorFilter.metric({ label: 'Bedrock Errors', statistic: 'Sum', period: Duration.minutes(5), color: '#4daf4a' }));
            }

            // Only create S3 Exporter filter if the lambda AND log group are provided
            if (props.s3ExporterLambda && s3ExporterLogGroup) {
                const s3ExporterErrorFilter = new logs.MetricFilter(this, 'S3ExporterLogErrorFilter', {
                    logGroup: s3ExporterLogGroup, // Use prop
                    metricNamespace: 'QikrChat/Logs',
                    metricName: 'S3ExporterLogErrors',
                    filterPattern: logs.FilterPattern.literal('"- ERROR -"'),
                    metricValue: '1',
                });
                s3ExporterLogErrorsMetric = s3ExporterErrorFilter.metric({
                    label: 'S3 Exporter Log Errors',
                    statistic: 'Sum',
                    period: Duration.minutes(5),
                    color: '#FFC0CB', // Pink
                });
                logErrorMetrics.push(s3ExporterLogErrorsMetric);
            } else if (props.s3ExporterLambda && !s3ExporterLogGroup) {
                 console.warn(`s3ExporterLambda provided to BaseDashboard, but its logGroup prop was not.`);
            }

            // Only create CodeBuild filter if the project AND log group are provided
            if (props.knowledgeBaseCodeBuild && codeBuildLogGroup) {
                const codeBuildErrorFilter = new logs.MetricFilter(this, 'CodeBuildLogErrorFilter', {
                    logGroup: codeBuildLogGroup, // Use prop
                    metricNamespace: 'QikrChat/Logs',
                    metricName: 'CodeBuildLogErrors',
                    filterPattern: logs.FilterPattern.literal('?State ?= ?FAILED ?"Phase context status code:" ?"Message:" ?FAILED ?Error ?"Command did not exit successfully"'),
                    metricValue: '1',
                });
                codeBuildLogErrorsMetric = codeBuildErrorFilter.metric({
                    label: 'CodeBuild Log Errors',
                    statistic: 'Sum',
                    period: Duration.minutes(5),
                    color: '#800080', // Purple
                });
                logErrorMetrics.push(codeBuildLogErrorsMetric);
            } else if (props.knowledgeBaseCodeBuild && !codeBuildLogGroup) {
                 console.warn(`knowledgeBaseCodeBuild provided to BaseDashboard, but its logGroup prop was not.`);
            }

            // Only create WebSocket filter if the handler AND log group are provided
            if (props.webSocketHandler && props.webSocketLogGroup) {
                const wsLogErrorFilter = new logs.MetricFilter(this, 'WebSocketLogErrorFilter', {
                    logGroup: props.webSocketLogGroup,
                    metricNamespace: 'QikrChat/Logs', // Use consistent namespace
                    metricName: 'WebSocketLogErrors',
                    filterPattern: logs.FilterPattern.literal('"- ERROR -"'), // Generic error filter
                    metricValue: '1',
                });
                wsLogErrorsMetric = wsLogErrorFilter.metric({
                    label: 'WebSocket Log Errors',
                    statistic: 'Sum',
                    period: Duration.minutes(5),
                    color: '#FFA500', // Orange color for distinction
                });
                logErrorMetrics.push(wsLogErrorsMetric);
            } else if (props.webSocketHandler && !props.webSocketLogGroup) {
                console.warn(`webSocketHandler provided to BaseDashboard, but its logGroup prop was not.`);
            }

            if (logErrorMetrics.length > 0) {
                 // Create the graph widget if metrics exist
                 logErrorWidget = new cloudwatch.GraphWidget({
                    title: 'Log-Based Error Counts (Sum 5min)',
                    left: logErrorMetrics,
                    width: 12, // Ensure width is 12
                    height: 6,
                    leftYAxis: { min: 0, label: 'Count' },
                    period: Duration.minutes(5)
                });
            } else {
                // Create a placeholder TextWidget if no metrics
                logErrorWidget = new cloudwatch.TextWidget({
                    markdown: '### Log-Based Error Counts\n\nNo log metric filters configured or no errors found in the selected time range.',
                    width: 12,
                    height: 6
                });
            }
        } else {
             // Create a placeholder TextWidget if apiLambdaHandler is not provided
             logErrorWidget = new cloudwatch.TextWidget({
                markdown: '### Log-Based Error Counts\n\nLog monitoring requires apiLambdaHandler to be configured.',
                width: 12,
                height: 6
             });
        }
        // --- END Log-Based Error Widgets ---

        // --- S3 Bucket Metrics (Conditional) ---
        let s3HeaderWidget: cloudwatch.TextWidget | undefined;
        let s3DdbBucketWidget: cloudwatch.GraphWidget | undefined;
        let bedrockUsageHeaderWidget: cloudwatch.TextWidget | undefined;
        let s3QueryResultBucketWidget: cloudwatch.GraphWidget | undefined;
        let s3BotsBucketWidget: cloudwatch.GraphWidget | undefined;
        let s3KnowledgeBaseBucketWidget: cloudwatch.GraphWidget | undefined;
        let bedrockTokenWidget: cloudwatch.GraphWidget | undefined;

        const extendedProps = props as BaseDashboardProps & { 
            athenaWorkgroupName?: string;
            ddbExportBucket?: s3.IBucket;
            knowledgeBaseBucket?: s3.IBucket; // Added KB Bucket
            queryResultBucket?: s3.IBucket; // Added Athena results bucket
            botsBucket?: s3.IBucket;      // Added Bots analytics bucket
        };

        if (props.embeddingStateMachine) {
            // --- S3 Bucket Metrics (Conditional) ---
            // Add widgets for any provided S3 buckets
            if (extendedProps.ddbExportBucket || extendedProps.knowledgeBaseBucket || extendedProps.queryResultBucket || extendedProps.botsBucket) {
                s3HeaderWidget = new cloudwatch.TextWidget({ markdown: '## S3 Bucket Metrics', width: 24, height: 1 });
                widgetsToAdd.push(s3HeaderWidget); // Add the single S3 header

                const getS3Metric = (bucket: s3.IBucket, metricName: string, statistic: string, label?: string) => {
                    return new cloudwatch.Metric({
                        namespace: 'AWS/S3',
                        metricName: metricName,
                        dimensionsMap: {
                            BucketName: bucket.bucketName,
                            // StorageType dimension needed for size/object metrics
                            ...(metricName === 'BucketSizeBytes' || metricName === 'NumberOfObjects' ? { StorageType: 'StandardStorage', FilterId: 'EntireBucket' } : {})
                        },
                        statistic: statistic,
                        // Use daily period for size/object, 5 min for others
                        period: (metricName === 'BucketSizeBytes' || metricName === 'NumberOfObjects') ? Duration.days(1) : Duration.minutes(5),
                        label: label ?? `${bucket.bucketName} ${metricName}`,
                    });
                };

                const getS3RequestMetric = (bucket: s3.IBucket, metricName: string, statistic: string, label?: string) => {
                    // Request metrics are directly under AWS/S3 namespace, simpler dimensions
                    return new cloudwatch.Metric({
                        namespace: 'AWS/S3',
                        metricName: metricName,
                        dimensionsMap: {
                            BucketName: bucket.bucketName,
                            // StorageType dimension needed for size/object metrics
                            ...(metricName === 'BucketSizeBytes' || metricName === 'NumberOfObjects' ? { StorageType: 'StandardStorage', FilterId: 'EntireBucket' } : {})
                        },
                        statistic: statistic,
                        // Use daily period for size/object, 5 min for others
                        period: (metricName === 'BucketSizeBytes' || metricName === 'NumberOfObjects') ? Duration.days(1) : Duration.minutes(5),
                        label: label ?? `${bucket.bucketName} ${metricName}`,
                    });
                };

                // Widget for DynamoDB Export Bucket
                if (extendedProps.ddbExportBucket) {
                    s3DdbBucketWidget = new cloudwatch.GraphWidget({
                        title: `S3 DynamoDB Export - ${extendedProps.ddbExportBucket.bucketName}`,
                        left: [
                            getS3Metric(extendedProps.ddbExportBucket, 'BucketSizeBytes', 'Average', 'Size (Bytes)').with({ period: Duration.days(1), color: '#1f77b4' }),
                            getS3Metric(extendedProps.ddbExportBucket, 'NumberOfObjects', 'Average', 'Object Count').with({ period: Duration.days(1), color: '#aec7e8' }),
                        ],
                        right: [
                            getS3RequestMetric(extendedProps.ddbExportBucket, '4xxErrors', 'Sum', '4xx Errors').with({ color: '#ff7f0e' }),
                            getS3RequestMetric(extendedProps.ddbExportBucket, '5xxErrors', 'Sum', '5xx Errors').with({ color: '#d62728' }),
                        ],
                        width: 12,
                        height: 6,
                        leftYAxis: { min: 0 },
                        rightYAxis: { min: 0 },
                    });

                    const s3DdbBucketErrorsAlarm = new cloudwatch.Alarm(this, 'S3DdbBucketErrorsCriticalAlarm', {
                        alarmName: `${alarmPrefix}-S3-${extendedProps.ddbExportBucket.bucketName}-Errors-Critical`,
                        alarmDescription: `CRITICAL: High number of 5xx errors for S3 Bucket ${extendedProps.ddbExportBucket.bucketName}`,
                        metric: getS3RequestMetric(extendedProps.ddbExportBucket, '5xxErrors', 'Sum'),
                        threshold: 5, // Adjust threshold as needed
                        evaluationPeriods: 2,
                        comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                        treatMissingData: TreatMissingData.NOT_BREACHING,
                    });
                    s3DdbBucketErrorsAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
                    this.criticalAlarms.push(s3DdbBucketErrorsAlarm);

                    if (s3DdbBucketWidget) widgetsToAdd.push(s3DdbBucketWidget);
                }

                // Widget for Knowledge Base Bucket
                if (extendedProps.knowledgeBaseBucket) {
                    s3KnowledgeBaseBucketWidget = new cloudwatch.GraphWidget({
                        title: `S3 Knowledge Base - ${extendedProps.knowledgeBaseBucket.bucketName}`,
                        left: [
                            getS3Metric(extendedProps.knowledgeBaseBucket, 'BucketSizeBytes', 'Average', 'Size (Bytes)').with({ period: Duration.days(1), color: '#1f77b4' }),
                            getS3Metric(extendedProps.knowledgeBaseBucket, 'NumberOfObjects', 'Average', 'Object Count').with({ period: Duration.days(1), color: '#aec7e8' }),
                        ],
                        right: [
                            getS3RequestMetric(extendedProps.knowledgeBaseBucket, '4xxErrors', 'Sum', '4xx Errors').with({ color: '#ff7f0e' }),
                            getS3RequestMetric(extendedProps.knowledgeBaseBucket, '5xxErrors', 'Sum', '5xx Errors').with({ color: '#d62728' }),
                        ],
                        width: 12,
                        height: 6,
                        leftYAxis: { min: 0 },
                        rightYAxis: { min: 0 },
                    });

                    const s3KnowledgeBaseBucketErrorsAlarm = new cloudwatch.Alarm(this, 'S3KnowledgeBaseBucketErrorsCriticalAlarm', {
                        alarmName: `${alarmPrefix}-S3-${extendedProps.knowledgeBaseBucket.bucketName}-Errors-Critical`,
                        alarmDescription: `CRITICAL: High number of 5xx errors for S3 Bucket ${extendedProps.knowledgeBaseBucket.bucketName}`,
                        metric: getS3RequestMetric(extendedProps.knowledgeBaseBucket, '5xxErrors', 'Sum'),
                        threshold: 5, // Adjust threshold as needed
                        evaluationPeriods: 2,
                        comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                        treatMissingData: TreatMissingData.NOT_BREACHING,
                    });
                    s3KnowledgeBaseBucketErrorsAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
                    this.criticalAlarms.push(s3KnowledgeBaseBucketErrorsAlarm);

                    if (s3KnowledgeBaseBucketWidget) widgetsToAdd.push(s3KnowledgeBaseBucketWidget);
                }

                // Widget for Athena Query Result Bucket
                if (extendedProps.queryResultBucket) {
                     s3QueryResultBucketWidget = new cloudwatch.GraphWidget({
                        title: `S3 Athena Results - ${extendedProps.queryResultBucket.bucketName}`,
                        left: [
                            getS3Metric(extendedProps.queryResultBucket, 'BucketSizeBytes', 'Average', 'Size (Bytes)').with({ color: '#1f77b4' }),
                            getS3Metric(extendedProps.queryResultBucket, 'NumberOfObjects', 'Average', 'Object Count').with({ color: '#aec7e8' }),
                        ],
                        right: [
                            getS3RequestMetric(extendedProps.queryResultBucket, '4xxErrors', 'Sum', '4xx Errors').with({ color: '#ff7f0e' }),
                            getS3RequestMetric(extendedProps.queryResultBucket, '5xxErrors', 'Sum', '5xx Errors').with({ color: '#d62728' }),
                        ],
                        width: 12,
                        height: 6,
                        leftYAxis: { min: 0 },
                        rightYAxis: { min: 0 },
                    });

                    const s3QueryResultBucketErrorsAlarm = new cloudwatch.Alarm(this, 'S3QueryResultBucketErrorsCriticalAlarm', {
                        alarmName: `${alarmPrefix}-S3-${extendedProps.queryResultBucket.bucketName}-Errors-Critical`,
                        alarmDescription: `CRITICAL: High number of 5xx errors for S3 Bucket ${extendedProps.queryResultBucket.bucketName}`,
                        metric: getS3RequestMetric(extendedProps.queryResultBucket, '5xxErrors', 'Sum'),
                        threshold: 5, // Adjust threshold as needed
                        evaluationPeriods: 2,
                        comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                        treatMissingData: TreatMissingData.NOT_BREACHING,
                    });
                    s3QueryResultBucketErrorsAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
                    this.criticalAlarms.push(s3QueryResultBucketErrorsAlarm);

                    if (s3QueryResultBucketWidget) widgetsToAdd.push(s3QueryResultBucketWidget);
                }

                // Widget for Bots Analytics Bucket
                if (extendedProps.botsBucket) {
                     s3BotsBucketWidget = new cloudwatch.GraphWidget({
                        title: `S3 Bots Analytics - ${extendedProps.botsBucket.bucketName}`,
                        left: [
                            getS3Metric(extendedProps.botsBucket, 'BucketSizeBytes', 'Average', 'Size (Bytes)').with({ color: '#1f77b4' }),
                            getS3Metric(extendedProps.botsBucket, 'NumberOfObjects', 'Average', 'Object Count').with({ color: '#aec7e8' }),
                        ],
                        right: [
                            getS3RequestMetric(extendedProps.botsBucket, '4xxErrors', 'Sum', '4xx Errors').with({ color: '#ff7f0e' }),
                            getS3RequestMetric(extendedProps.botsBucket, '5xxErrors', 'Sum', '5xx Errors').with({ color: '#d62728' }),
                        ],
                        width: 12,
                        height: 6,
                        leftYAxis: { min: 0 },
                        rightYAxis: { min: 0 },
                    });

                    const s3BotsBucketErrorsAlarm = new cloudwatch.Alarm(this, 'S3BotsBucketErrorsCriticalAlarm', {
                        alarmName: `${alarmPrefix}-S3-${extendedProps.botsBucket.bucketName}-Errors-Critical`,
                        alarmDescription: `CRITICAL: High number of 5xx errors for S3 Bucket ${extendedProps.botsBucket.bucketName}`,
                        metric: getS3RequestMetric(extendedProps.botsBucket, '5xxErrors', 'Sum'),
                        threshold: 5, // Adjust threshold as needed
                        evaluationPeriods: 2,
                        comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                        treatMissingData: TreatMissingData.NOT_BREACHING,
                    });
                    s3BotsBucketErrorsAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
                    this.criticalAlarms.push(s3BotsBucketErrorsAlarm);

                    if (s3BotsBucketWidget) widgetsToAdd.push(s3BotsBucketWidget);
                }
            }
        }

        // --- Bedrock Model Usage (Placeholder for Custom Metrics) ---
        bedrockUsageHeaderWidget = new cloudwatch.TextWidget({ markdown: `## Bedrock Model Usage (Custom Metrics)`, width: 24, height: 1 });
        widgetsToAdd.push(bedrockUsageHeaderWidget); // Add header

        // Use search expressions to find all models dynamically
        const bedrockInputTokensExpression = new cloudwatch.MathExpression({
            // Search for all InputTokens metrics in the namespace, group by ModelId
            expression: `SEARCH('{QikrChat/Usage,ModelId} MetricName="InputTokens"', 'Sum', 300)`,
            usingMetrics: {}, // No specific metrics needed here for search
            label: 'Input Tokens:', // Simplified label
            period: Duration.minutes(5),
            color: '#1f77b4', // Base color, CloudWatch will cycle if multiple lines
        });

        const bedrockOutputTokensExpression = new cloudwatch.MathExpression({
            // Search for all OutputTokens metrics in the namespace, group by ModelId
            expression: `SEARCH('{QikrChat/Usage,ModelId} MetricName="OutputTokens"', 'Sum', 300)`,
            usingMetrics: {},
            label: 'Output Tokens:', // Simplified label
            period: Duration.minutes(5),
            color: '#aec7e8', // Base color
        });

        bedrockTokenWidget = new cloudwatch.GraphWidget({
            title: 'Bedrock Token Counts by Model (Sum 5min)',
            left: [bedrockInputTokensExpression, bedrockOutputTokensExpression], // Plot both input and output using search
            width: 12,
            height: 6,
            leftYAxis: { min: 0, label: 'Tokens' },
            period: Duration.minutes(5) // Set period on the widget as well
        });

        widgetsToAdd.push(bedrockTokenWidget); // Add the dynamic widget

        // --- EventBridge Pipe Widgets & Alarms (Conditional) ---
        let pipeHeaderWidget: cloudwatch.TextWidget | undefined;
        let pipeWidget: cloudwatch.GraphWidget | undefined;
        if (props.embeddingPipe) {
            pipeHeaderWidget = new cloudwatch.TextWidget({ markdown: `## EventBridge Pipe: ${props.embeddingPipe.ref}`, width: 24, height: 1 });

            const getPipeMetric = (metricName: string, statistic: string, label?: string) => {
                return new cloudwatch.Metric({
                    namespace: 'AWS/Events',
                    metricName: metricName,
                    dimensionsMap: { PipeName: props.embeddingPipe!.ref },
                    statistic: statistic,
                    period: Duration.minutes(5),
                    label: label ?? metricName,
                });
            };

            pipeWidget = new cloudwatch.GraphWidget({
                title: 'Pipe - Invocations, Failed (Target/Enrichment), Throttled',
                left: [
                    getPipeMetric('Invocation', 'Sum', 'Invocations').with({ color: '#1f77b4' }),
                    getPipeMetric('TargetInvocationFailed', 'Sum', 'Target Failures').with({ color: '#d62728' }),
                    getPipeMetric('EnrichmentInvocationFailed', 'Sum', 'Enrichment Failures').with({ color: '#e377c2' }),
                    getPipeMetric('TargetThrottled', 'Sum', 'Target Throttles').with({ color: '#ff7f0e' }),
                ],
                width: 12,
                height: 6,
                leftYAxis: { min: 0 },
            });

            const pipeTargetFailureAlarm = new cloudwatch.Alarm(this, 'PipeTargetFailuresCriticalAlarm', {
                alarmName: `${alarmPrefix}-PipeTargetFailures-Critical`,
                alarmDescription: `CRITICAL: High number of target invocation failures for Pipe ${props.embeddingPipe.ref}`,
                metric: getPipeMetric('TargetInvocationFailed', 'Sum'),
                threshold: 1,
                evaluationPeriods: 1,
                comparisonOperator: ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                treatMissingData: TreatMissingData.NOT_BREACHING,
            });
            pipeTargetFailureAlarm.addAlarmAction(new cw_actions.SnsAction(this.alertTopic));
            this.criticalAlarms.push(pipeTargetFailureAlarm);

            if (pipeHeaderWidget) widgetsToAdd.push(pipeHeaderWidget);
            if (pipeWidget) widgetsToAdd.push(pipeWidget);
        }

        // --- Athena Widgets & Alarms (Conditional) ---
        let athenaHeaderWidget: cloudwatch.TextWidget | undefined;
        let athenaUsageWidget: cloudwatch.GraphWidget | undefined;
        const extendedPropsForAthena = props as BaseDashboardProps & { athenaWorkgroupName?: string }; 
        if (extendedPropsForAthena.athenaWorkgroupName) {
            athenaHeaderWidget = new cloudwatch.TextWidget({ markdown: `## Athena Workgroup: ${extendedPropsForAthena.athenaWorkgroupName}`, width: 24, height: 1 });
 
            const getAthenaMetric = (metricName: string, statistic: string, label?: string) => {
                return new cloudwatch.Metric({
                    namespace: 'AWS/Athena',
                    metricName: metricName,
                    dimensionsMap: { WorkGroup: extendedPropsForAthena.athenaWorkgroupName! },
                    statistic: statistic,
                    period: Duration.minutes(5),
                    label: label ?? metricName,
                });
            };
 
            athenaUsageWidget = new cloudwatch.GraphWidget({
                title: 'Athena - Data Scanned, Execution Time, Failed Queries',
                left: [
                    getAthenaMetric('DataScanned', 'Sum', 'Data Scanned'),
                    getAthenaMetric('ExecutionTime', 'Average', 'Execution Time Avg (ms)'),
                    getAthenaMetric('FailedQueries', 'Sum', 'Failed Queries'),
                ],
                width: 12,
                height: 6,
                leftYAxis: { min: 0 },
            });

            if (athenaHeaderWidget) widgetsToAdd.push(athenaHeaderWidget);
            if (athenaUsageWidget) widgetsToAdd.push(athenaUsageWidget);
        }

        // --- Add Widgets to Dashboard in Order ---
        this.dashboard.addWidgets(titleWidget);

        // 2. Top Row (Always Alarms + Logs/Placeholder)
        // Assumes criticalAlarmStatusWidget and logErrorWidget are defined with width 12
        this.dashboard.addWidgets(criticalAlarmStatusWidget, logErrorWidget);

        this.dashboard.addWidgets(apiGwHeaderWidget);
        this.dashboard.addWidgets(apiGwWidget, apiLatencyAnomalyWidget);

        this.dashboard.addWidgets(ddbHeaderWidget);
        this.dashboard.addWidgets(chatTableWidget, botsTableWidget);

        // Add all collected conditional widgets
        for (let i = 0; i < widgetsToAdd.length; ) {
            const currentWidget = widgetsToAdd[i];

            // If it's a TextWidget (header), add it on its own row
            if (currentWidget instanceof cloudwatch.TextWidget) {
                this.dashboard.addWidgets(currentWidget);
                i++; // Advance by 1
                continue; // Move to the next widget
            }

            // If it's a GraphWidget or AlarmStatusWidget (or similar)
            const nextWidget = widgetsToAdd[i + 1];

            // Check if the next widget exists and is also *not* a TextWidget (i.e., can be paired)
            if (nextWidget && !(nextWidget instanceof cloudwatch.TextWidget)) {
                 // Add both widgets in a row
                 this.dashboard.addWidgets(currentWidget, nextWidget);
                 i += 2; // Advance by 2
            } else {
                 // Add the current widget by itself (either it's the last one, or the next is a header)
                 this.dashboard.addWidgets(currentWidget);
                 i++; // Advance by 1
            }
        }
    }
} 