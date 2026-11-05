# Aditya Reddy

I'm a senior software engineer in Milwaukee, and I work on browser performance and observability. I write TypeScript and Go. I'm looking for my next role in browser engineering or web performance, Denver preferred.

## Recent

- My [Faro exporter fix](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/52068) in the OpenTelemetry Collector contrib repo merged October 16, 2026 and shipped in [v0.164.0](https://github.com/open-telemetry/opentelemetry-collector-contrib/releases/tag/v0.164.0). The Faro translator [fuzz tests](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/52646) and fix that [returns the meta encoding error](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/52647) have merged too. I now have four merged pull requests in collector-contrib.
- More Go work is open: [mdatagen README markers](https://github.com/open-telemetry/opentelemetry-collector/pull/16193) in the Collector, Alloy [CORS headers for the Faro receiver](https://github.com/grafana/alloy/pull/7618) and [goroutine stack traces in support bundles](https://github.com/grafana/alloy/pull/7629), a k6 [navigation check](https://github.com/grafana/k6/pull/6577), and [list_alerts truncation](https://github.com/prometheus/prometheus-mcp/pull/210) in the Prometheus MCP server. My Collector fix to [preserve the connection's remote address](https://github.com/open-telemetry/opentelemetry-collector/pull/16305) is approved.
- Grafana Faro: one merged pull request and six open pull requests in [faro-web-sdk](https://github.com/grafana/faro-web-sdk/pulls?q=is%3Apr+author%3Aadityareddy-dev), covering hard page load navigations ([#2359](https://github.com/grafana/faro-web-sdk/pull/2359)), custom web vitals labels ([#2361](https://github.com/grafana/faro-web-sdk/pull/2361)), custom text masking for session replay ([#2362](https://github.com/grafana/faro-web-sdk/pull/2362)), and the move of tracing setup onto the OpenTelemetry trace SDK ([#2358](https://github.com/grafana/faro-web-sdk/pull/2358), [#2363](https://github.com/grafana/faro-web-sdk/pull/2363), [#2364](https://github.com/grafana/faro-web-sdk/pull/2364) for the SDK 3.0 upgrade).
- OpenTelemetry browser SIG: I'm nominated as an approver on [#549](https://github.com/open-telemetry/opentelemetry-browser/pull/549), still open. I have 8 merged pull requests in [opentelemetry-browser](https://github.com/open-telemetry/opentelemetry-browser/pulls?q=is%3Apr+author%3Aadityareddy-dev+is%3Amerged), and I've reviewed 75 pull requests across nine OpenTelemetry repos.
- Safari: the browser SDK wouldn't start on Safari 17 because of `URL.parse`. [#447](https://github.com/open-telemetry/opentelemetry-browser/pull/447) fixed it, and I wrote up why below.
- Web performance specs: I opened a non-normative section on computing INP for the W3C Event Timing spec ([#175](https://github.com/w3c/event-timing/pull/175)) and moved the CLS explanation in WICG layout-instability to session windows ([#131](https://github.com/WICG/layout-instability/pull/131)). Both are open. Google's web-vitals took three of my fixes.
- [Client-side semantic conventions v0.1.0-dev](https://github.com/open-telemetry/semantic-conventions-client-side/releases/tag/v0.1.0-dev), the first dev release of the browser and mobile registry, came out October 27, 2026. It has [#33](https://github.com/open-telemetry/semantic-conventions-client-side/pull/33) in it, which moved `enduser.id` and `enduser.pseudo.id` over from core.
- I now have four merged pull requests in OpenTelemetry JS. This week, [#7262](https://github.com/open-telemetry/opentelemetry-js/pull/7262) fixed B3 trace ID length validation, and [#7253](https://github.com/open-telemetry/opentelemetry-js/pull/7253) documented that API 1.10.0 needs SDK 3.x.
- [OpenTelemetry JS #7153](https://github.com/open-telemetry/opentelemetry-js/pull/7153) removed the `pagehide` listener from the trace and log SDKs, and shipped in [3.0.0](https://github.com/open-telemetry/opentelemetry-js/releases/tag/v3.0.0).
- [OpenTelemetry demo #3966](https://github.com/open-telemetry/opentelemetry-demo/pull/3966) replaced the Python recommendation service with Java on Spring Boot 4 and merged October 13, 2026. On November 3 [#4232](https://github.com/open-telemetry/opentelemetry-demo/pull/4232) gave its catalog calls a deadline. The [companion Helm chart change](https://github.com/open-telemetry/opentelemetry-helm-charts/pull/2398) is still open.

## Judging and certification

- Judge at HackOHI/O 2026, The Ohio State University's hackathon. I scored seven student teams on October 25, 2026.
- I'll judge Kendor Build Day, November 8 to 13, 2026, and DSH Hacks V2, November 15 to 22, 2026.
- Virtual judge for Diamond Challenge 2027.
- Scorer for the San Mateo County STEM Fair, March 3 to 12, 2027.
- Judge for the 2027 American Business Awards.
- OpenTelemetry Certified Associate, passed October 30, 2026.

## Writing

- [What broke when I moved Grafana Faro to OpenTelemetry JS 3.0](https://dev.to/adityareddy_dev/what-broke-when-i-moved-grafana-faro-to-opentelemetry-js-30-imb), November 3, 2026.
- InfoQ accepted my article on Spring Boot 4 and OpenTelemetry. I'm still working on it.
- [Why your INP can fall after one more click](https://dev.to/adityareddy_dev/why-your-inp-can-fall-after-one-more-click-2p2k), November 2, 2026.
- [How one Desk Studio job gets from roughs to sign-off](https://dev.to/adityareddy_dev/how-one-desk-studio-job-gets-from-roughs-to-sign-off-4h22), October 20, 2026.
- [Why the OpenTelemetry browser SDK wouldn't start on Safari 17](https://dev.to/adityareddy_dev/why-the-opentelemetry-browser-sdk-wouldnt-start-on-safari-17-55j5), October 2, 2026.
- Preprint: [The judge cannot see the margin](https://doi.org/10.5281/zenodo.23778627), a paired ablation study, posted on Zenodo October 29, 2026.

## Projects

- [Desk Studio](https://deskstudio.ai): a design studio inside the coding agent you already use. Free, and nothing leaves your machine but the model calls you already make.
- [System Designer](https://systemdesigner.io): a free browser game for practicing system design. Pick a real problem, draw the system, then watch a full day of traffic hit it.
- [adityareddy.dev](https://adityareddy.dev) is a small 3D browser game about one working day. The resume is in the phone.
- [react-inp-blame](https://github.com/adityareddy-dev/react-inp-blame): connects slow browser interactions to React renders and handlers when it can identify them.
- [otel-js-upgrade](https://github.com/adityareddy-dev/otel-js-upgrade): reviewable migration diffs for OpenTelemetry JavaScript. It applies supported SDK 2.12 changes and previews SDK 3 migrations.
- [otel-zoneless-context](https://github.com/adityareddy-dev/otel-zoneless-context): browser context manager without zone.js.
- [otel-cluster-metrics](https://github.com/adityareddy-dev/otel-cluster-metrics): cumulative OpenTelemetry metrics from Node cluster workers through one Prometheus endpoint, 0.1.0 is on [npm](https://www.npmjs.com/package/@adityareddy-dev/otel-cluster-metrics).

## Upstream

Member of the [OpenTelemetry GitHub org](https://github.com/open-telemetry/community/issues/3758).

I contribute to OpenTelemetry's [browser SDK](https://github.com/open-telemetry/opentelemetry-browser), [client-side semantic conventions](https://github.com/open-telemetry/semantic-conventions-client-side), [Collector](https://github.com/open-telemetry/opentelemetry-collector), [JavaScript SDK](https://github.com/open-telemetry/opentelemetry-js), [ecosystem explorer](https://github.com/open-telemetry/opentelemetry-ecosystem-explorer), [demo](https://github.com/open-telemetry/opentelemetry-demo), [Helm charts](https://github.com/open-telemetry/opentelemetry-helm-charts) and [docs](https://github.com/open-telemetry/opentelemetry.io). Also [Grafana Alloy](https://github.com/grafana/alloy), [k6](https://github.com/grafana/k6) and [Faro](https://github.com/grafana/faro-web-sdk), the [Prometheus MCP server](https://github.com/prometheus/prometheus-mcp), and three open merge requests to [GitLab](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/267455) on frontend load time.

I have 12 merged pull requests in the [OpenTelemetry ecosystem explorer](https://github.com/open-telemetry/opentelemetry-ecosystem-explorer/pulls?q=is%3Apr+author%3Aadityareddy-dev+is%3Amerged). I also have three merged in [PostHog's JavaScript SDK](https://github.com/PostHog/posthog-js/pulls?q=is%3Apr+author%3Aadityareddy-dev+is%3Amerged). My [datastore reporting docs change](https://github.com/newrelic/node-newrelic/pull/4434) merged in New Relic's Node.js agent, and my fix for [browser test fixtures on Windows](https://github.com/grafana/k6/pull/6635) merged in k6.

## Contact

[adityareddy.dev](https://adityareddy.dev), [LinkedIn](https://www.linkedin.com/in/adityareddy-dev), [X @adityareddydev](https://x.com/adityareddydev).
