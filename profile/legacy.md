# Aditya Reddy

I work on browser performance and OpenTelemetry.

## Recent

- [Client-side semantic conventions v0.1.0-dev](https://github.com/open-telemetry/semantic-conventions-client-side/releases/tag/v0.1.0-dev), the first dev release of the browser and mobile registry, came out October 27, 2026. It has [#33](https://github.com/open-telemetry/semantic-conventions-client-side/pull/33) in it, which moved `enduser.id` and `enduser.pseudo.id` over from core.
- [browser-instrumentation 0.9.0](https://github.com/open-telemetry/opentelemetry-browser/releases/tag/browser-instrumentation-v0.9.0) and [browser-sdk 0.6.0](https://github.com/open-telemetry/opentelemetry-browser/releases/tag/browser-sdk-v0.6.0) went out October 22, 2026 with four of my fixes: middle and right clicks ([#448](https://github.com/open-telemetry/opentelemetry-browser/pull/448)), a `reportAllChanges` option for web vitals ([#450](https://github.com/open-telemetry/opentelemetry-browser/pull/450)), resource timing entries when the idle callback times out ([#453](https://github.com/open-telemetry/opentelemetry-browser/pull/453)), and a session store that doesn't throw when storage is blocked ([#451](https://github.com/open-telemetry/opentelemetry-browser/pull/451)).
- [OpenTelemetry demo #3966](https://github.com/open-telemetry/opentelemetry-demo/pull/3966): replaced the Python recommendation service with Java on Spring Boot 4. Merged October 13, 2026, and the [docs update](https://github.com/open-telemetry/opentelemetry.io/pull/11667) merged that day too. The [companion Helm chart change](https://github.com/open-telemetry/opentelemetry-helm-charts/pull/2398) is still open, waiting for a demo release.
- OpenTelemetry Helm charts: merged fixes for [conflicting event presets](https://github.com/open-telemetry/opentelemetry-helm-charts/pull/2421) and the [operator metrics Helm test](https://github.com/open-telemetry/opentelemetry-helm-charts/pull/2423). The [demo's Prometheus memory change](https://github.com/open-telemetry/opentelemetry-helm-charts/pull/2422) merged October 21, 2026 and is in [opentelemetry-demo chart 0.42.6](https://github.com/open-telemetry/opentelemetry-helm-charts/releases/tag/opentelemetry-demo-0.42.6).
- [OpenTelemetry JS #7153](https://github.com/open-telemetry/opentelemetry-js/pull/7153): removed the `pagehide` listener from the trace and log SDKs. Shipped in [3.0.0](https://github.com/open-telemetry/opentelemetry-js/releases/tag/v3.0.0).
- [OpenTelemetry browser #467](https://github.com/open-telemetry/opentelemetry-browser/pull/467): fixed sibling counting in CSS `nth-child` selectors. Shipped in [browser-instrumentation 0.8.2](https://github.com/open-telemetry/opentelemetry-browser/releases/tag/browser-instrumentation-v0.8.2).

## Libraries

- [react-inp-blame](https://github.com/adityareddy-dev/react-inp-blame): connects slow browser interactions to React renders and handlers when it can identify them.
- [otel-js-upgrade](https://github.com/adityareddy-dev/otel-js-upgrade): reviewable migration diffs for OpenTelemetry JavaScript. It applies supported SDK 2.12 changes and previews SDK 3 migrations.
- [otel-zoneless-context](https://github.com/adityareddy-dev/otel-zoneless-context): browser context manager without zone.js, with a bundler plugin that restores context across the native `await` calls it rewrites.
- [otel-cluster-metrics](https://github.com/adityareddy-dev/otel-cluster-metrics): cumulative OpenTelemetry metrics from Node cluster workers through one Prometheus endpoint, for the old [cluster mode issue](https://github.com/open-telemetry/opentelemetry-js/issues/1252). 0.1.0 is on [npm](https://www.npmjs.com/package/@adityareddy-dev/otel-cluster-metrics).

## Upstream

Member of the [OpenTelemetry GitHub org](https://github.com/open-telemetry/community/issues/3758).

I contribute to OpenTelemetry's [demo](https://github.com/open-telemetry/opentelemetry-demo), [JavaScript SDK](https://github.com/open-telemetry/opentelemetry-js), [browser SDK](https://github.com/open-telemetry/opentelemetry-browser), [client-side semantic conventions](https://github.com/open-telemetry/semantic-conventions-client-side), [Helm charts](https://github.com/open-telemetry/opentelemetry-helm-charts), [docs](https://github.com/open-telemetry/opentelemetry.io), and [ecosystem explorer](https://github.com/open-telemetry/opentelemetry-ecosystem-explorer). Also [Prometheus Helm charts](https://github.com/prometheus-community/helm-charts/pull/7344).

## Contact

[adityareddy.dev](https://adityareddy.dev), [LinkedIn](https://www.linkedin.com/in/adityareddy-dev), [X @adityareddydev](https://x.com/adityareddydev).
