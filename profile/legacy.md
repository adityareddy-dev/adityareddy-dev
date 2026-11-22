# Aditya Reddy

I'm a senior software engineer in Milwaukee, and I work on browser performance and observability. I write TypeScript and Go. I'm looking for my next role in browser engineering or web performance, Denver preferred.

## Recent

- The OpenTelemetry Browser SDK can [join the server trace on page load](https://github.com/open-telemetry/opentelemetry-browser/pull/564) using context from HTML meta tags. I also added [the B3 example](https://github.com/open-telemetry/opentelemetry-browser/pull/574) to the README.
- The [OpenTelemetry Ecosystem Explorer](https://github.com/open-telemetry/opentelemetry-ecosystem-explorer/pull/1437) now shows events on Java agent instrumentation pages.
- My [Faro exporter fix](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/52068) in the OpenTelemetry Collector contrib repo merged October 16, 2026 and shipped in [v0.164.0](https://github.com/open-telemetry/opentelemetry-collector-contrib/releases/tag/v0.164.0). The Faro translator [fuzz tests](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/52646) and fix that [returns the meta encoding error](https://github.com/open-telemetry/opentelemetry-collector-contrib/pull/52647) have merged too.
- More Go work includes [mdatagen README markers](https://github.com/open-telemetry/opentelemetry-collector/pull/16193) in the Collector, Alloy [CORS headers for the Faro receiver](https://github.com/grafana/alloy/pull/7618) and [goroutine stack traces in support bundles](https://github.com/grafana/alloy/pull/7629), and [list_alerts truncation](https://github.com/prometheus/prometheus-mcp/pull/210) in the Prometheus MCP server. The k6 [navigation check](https://github.com/grafana/k6/pull/6577) merged. My Collector fix to [preserve the connection's remote address](https://github.com/open-telemetry/opentelemetry-collector/pull/16305) is approved.
- My work in [Grafana Faro](https://github.com/grafana/faro-web-sdk/pulls?q=is%3Apr+author%3Aadityareddy-dev) covers hard page load navigations ([#2359](https://github.com/grafana/faro-web-sdk/pull/2359)), custom web vitals labels ([#2361](https://github.com/grafana/faro-web-sdk/pull/2361)), custom text masking for session replay ([#2362](https://github.com/grafana/faro-web-sdk/pull/2362)), and tracing setup for the OpenTelemetry SDK 3.0 upgrade ([#2358](https://github.com/grafana/faro-web-sdk/pull/2358), [#2363](https://github.com/grafana/faro-web-sdk/pull/2363), [#2364](https://github.com/grafana/faro-web-sdk/pull/2364)).
- Safari: the browser SDK wouldn't start on Safari 17 because of `URL.parse`. [#447](https://github.com/open-telemetry/opentelemetry-browser/pull/447) fixed it, and I wrote up why below.
- My [section on computing INP](https://github.com/w3c/event-timing/pull/175) merged into the W3C Event Timing spec. My [layout-instability change](https://github.com/WICG/layout-instability/pull/131) links to the CLS session-window explanation. Google's web-vitals has merged eight of my pull requests.
- [Client-side semantic conventions v0.1.0-dev](https://github.com/open-telemetry/semantic-conventions-client-side/releases/tag/v0.1.0-dev), the first dev release of the browser and mobile registry, came out October 27, 2026. It has [#33](https://github.com/open-telemetry/semantic-conventions-client-side/pull/33) in it, which moved `enduser.id` and `enduser.pseudo.id` over from core.
- In OpenTelemetry JS, [#7262](https://github.com/open-telemetry/opentelemetry-js/pull/7262) fixed B3 trace ID length validation, and [#7253](https://github.com/open-telemetry/opentelemetry-js/pull/7253) documented that API 1.10.0 needs SDK 3.x.
- [OpenTelemetry JS #7153](https://github.com/open-telemetry/opentelemetry-js/pull/7153) removed the `pagehide` listener from the trace and log SDKs, and shipped in [3.0.0](https://github.com/open-telemetry/opentelemetry-js/releases/tag/v3.0.0).
- [OpenTelemetry demo #3966](https://github.com/open-telemetry/opentelemetry-demo/pull/3966) replaced the Python recommendation service with Java on Spring Boot 4 and merged October 13, 2026. On November 3 [#4232](https://github.com/open-telemetry/opentelemetry-demo/pull/4232) gave its catalog calls a deadline. The [companion Helm chart change](https://github.com/open-telemetry/opentelemetry-helm-charts/pull/2398) is still open.

## Judging and certification

- Judge at HackOHI/O 2026, The Ohio State University's hackathon. I scored seven student teams on October 25, 2026.
- I judged [Kendor Build Day](https://kendor.io/hackathons/kendor-build-day) in November 2026. I'm also a judge for DSH Hacks V2, November 15 to 22, 2026.
- Virtual judge for Diamond Challenge 2027.
- Scorer for the San Mateo County STEM Fair, March 3 to 12, 2027.
- Judge for the 2027 American Business Awards.
- OpenTelemetry Certified Associate, passed October 30, 2026.

## Writing

- [The pagehide listener that never ran](https://dev.to/adityareddy_dev/the-pagehide-listener-that-never-ran-3k3e), November 7, 2026.
- [What broke when I moved Grafana Faro to OpenTelemetry JS 3.0](https://dev.to/adityareddy_dev/what-broke-when-i-moved-grafana-faro-to-opentelemetry-js-30-imb), November 3, 2026.
- [Why your INP can fall after one more click](https://dev.to/adityareddy_dev/why-your-inp-can-fall-after-one-more-click-2p2k), November 2, 2026.
- [How one Desk Studio job gets from roughs to sign-off](https://dev.to/adityareddy_dev/how-one-desk-studio-job-gets-from-roughs-to-sign-off-4h22), October 20, 2026.
- [Why the OpenTelemetry browser SDK wouldn't start on Safari 17](https://dev.to/adityareddy_dev/why-the-opentelemetry-browser-sdk-wouldnt-start-on-safari-17-55j5), October 2, 2026.
- Preprint: [The judge cannot see the margin](https://doi.org/10.5281/zenodo.23778627), a paired ablation study, posted on Zenodo October 29, 2026.

## Projects

- [Desk Studio](https://deskstudio.ai) runs inside the coding agent you already use. I released [v1.1.1 on GitHub](https://github.com/adityareddy-dev/deskstudio/releases/tag/v1.1.1) on November 18.
- [System Designer](https://systemdesigner.io): a free browser game for practicing system design. Pick a real problem, draw the system, then watch a full day of traffic hit it.
- [adityareddy.dev](https://adityareddy.dev) is a small 3D browser game about one working day. The resume is in the phone.
- [react-inp-blame](https://github.com/adityareddy-dev/react-inp-blame): connects slow browser interactions to React renders and handlers when it can identify them.
- [otel-js-upgrade](https://github.com/adityareddy-dev/otel-js-upgrade): reviewable migration diffs for OpenTelemetry JavaScript. It applies supported SDK 2.12 changes and previews SDK 3 migrations.
- [otel-zoneless-context](https://github.com/adityareddy-dev/otel-zoneless-context): browser context manager without zone.js.
- [otel-cluster-metrics](https://github.com/adityareddy-dev/otel-cluster-metrics): cumulative OpenTelemetry metrics from Node cluster workers through one Prometheus endpoint, 0.1.0 is on [npm](https://www.npmjs.com/package/@adityareddy-dev/otel-cluster-metrics).

## Upstream

Member of the [OpenTelemetry GitHub org](https://github.com/open-telemetry/community/issues/3758) and an [OpenTelemetry Browser approver](https://github.com/open-telemetry/opentelemetry-browser#approvers).

I contribute to OpenTelemetry's [browser SDK](https://github.com/open-telemetry/opentelemetry-browser), [client-side semantic conventions](https://github.com/open-telemetry/semantic-conventions-client-side), [GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/pull/680), [Collector](https://github.com/open-telemetry/opentelemetry-collector), [JavaScript SDK](https://github.com/open-telemetry/opentelemetry-js), [ecosystem explorer](https://github.com/open-telemetry/opentelemetry-ecosystem-explorer), [demo](https://github.com/open-telemetry/opentelemetry-demo), [Helm charts](https://github.com/open-telemetry/opentelemetry-helm-charts) and [docs](https://github.com/open-telemetry/opentelemetry.io). Also [Grafana Alloy](https://github.com/grafana/alloy), [k6](https://github.com/grafana/k6) and [Faro](https://github.com/grafana/faro-web-sdk), the [Prometheus MCP server](https://github.com/prometheus/prometheus-mcp), and [frontend load time in GitLab](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/267455).

I have seven merged pull requests in [PostHog's JavaScript SDK](https://github.com/PostHog/posthog-js/pulls?q=is%3Apr+author%3Aadityareddy-dev+is%3Amerged). My [datastore reporting docs change](https://github.com/newrelic/node-newrelic/pull/4434) merged in New Relic's Node.js agent, and my fix for [browser test fixtures on Windows](https://github.com/grafana/k6/pull/6635) merged in k6.

## Contact

[adityareddy.dev](https://adityareddy.dev), [LinkedIn](https://www.linkedin.com/in/adityareddy-dev), [X @adityareddydev](https://x.com/adityareddydev).
