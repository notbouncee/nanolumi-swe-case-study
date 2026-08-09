# Product Brief
## Water Quality Monitoring & Analytics Platform

Thank you for taking the time to complete this technical assessment.

This technical assessment is designed to reflect a small but realistic piece of work that a full-stack software engineer might undertake during a sprint. We are interested not only in whether the application works, but also in how you interpret a product need, make engineering decisions, prioritise within a time constraint, verify your work, and prepare software for review and handover.

There is intentionally no single correct solution.

## Scenario

Our company develops software used alongside IoT devices deployed in the field. One product helps operators monitor water quality across multiple sites.

Each site contains one or more devices capable of taking measurements such as pH, temperature, turbidity, and dissolved oxygen. Operators use a web application to request measurements, monitor device responses, investigate unusual results, and review historical data.

You have been asked to build an initial usable version of this application.

## Product objective

Build a small full-stack web application that enables an operator to:

- view a fleet of water-quality monitoring devices;
- request a new measurement from a selected device;
- track the progress of that request;
- view completed measurement results;
- identify readings or devices that may require attention;
- review historical measurements and basic analytics.

A simulator representing the field devices is provided separately in this pack.

## Before you start

We recommend this order:

1. Start the simulator by following `simulator/README.md`.
2. Confirm you can call `GET /health` and `GET /api/devices`.
3. Create your application repository and choose a stack you can work quickly in.
4. Implement a backend callback endpoint that can receive and store simulator results.
5. Implement the backend action that sends measurement commands to the simulator.
6. Add the operator UI once the request/callback loop works end to end.

You do not need to use this exact order, but it is a good way to avoid spending too much time on frontend work before the simulator integration is proven.

## Device interaction

The backend initiates communication with the devices.

When an operator requests a measurement, your backend should send a command to the simulator. The simulator will acknowledge whether the command has been accepted. This acknowledgement confirms receipt of the request, but does not mean that the measurement has completed.

Once processing finishes, the simulator will send the result to a callback endpoint exposed by your application.

A typical flow is:

```text
Operator requests a measurement
            ↓
Backend sends a command to the device
            ↓
Device acknowledges the command
            ↓
Device performs the measurement
            ↓
Device sends a result to the backend
            ↓
Application updates the operator interface
```

Your application should associate acknowledgements and final results with the original request.

The exact request, acknowledgement, and callback formats are defined in `SIMULATOR_PROTOCOL.md`.

## Working with field devices

The behaviour of deployed devices is outside our direct control.

Devices may operate remotely, use unreliable connections, run different firmware versions, or interact with physical sensors under changing conditions. You should not assume that every device will:

- acknowledge a request immediately;
- complete every accepted request;
- respond within a predictable amount of time;
- return results in request order;
- deliver every callback only once;
- always return complete or expected data;
- always be available when requested.

The simulator approximates some of these realities.

You are not expected to solve every possible failure mode. Use your judgement to decide what should be handled within the available time, and document important assumptions or limitations.

## Minimum useful implementation

Within the timebox, aim to produce a working vertical slice rather than a broad unfinished system. A useful submission should include:

- a backend service that can list devices from the simulator or otherwise represent the simulator's devices;
- a way for an operator to request a measurement for a device;
- persistence for measurement requests and completed results;
- a callback endpoint that the simulator can call;
- enough UI to see devices, request status, received results, and readings that may need attention;
- setup instructions that allow an evaluator to run your application and connect it to the simulator;
- at least a few meaningful automated tests.

If you run out of time, prefer documenting a clear limitation over hiding incomplete behavior.

## Functional expectations

### Device fleet

Provide an operator-facing view of the available monitoring devices and enough information to understand their current state.

You may decide what information is useful, such as the device, site, latest communication, most recent measurement, current request state, or whether attention is required.

### Requesting a measurement

An operator should be able to request a new measurement from a selected device and receive suitable feedback as the request progresses.

Requests may be acknowledged, completed, rejected, failed, delayed, or remain incomplete. How these states are represented to the operator is left to your judgement.

### Measurement results and history

Completed measurements should be persisted and available for later review.

The application should make it possible to identify readings outside the expected operating ranges defined in the protocol. Historical measurements should be viewable for an individual device.

### Dashboard and analytics

The application should include an operator dashboard that helps a user understand the overall state of the deployment and identify where investigation may be required.

You should decide which information is most useful. Examples may include:

- total devices;
- devices requiring attention;
- requests awaiting completion;
- failed or incomplete requests;
- recent abnormal readings;
- latest reading for each device;
- measurements received over time;
- trends for selected parameters.

We are not assessing visual polish or the number of charts. We are interested in whether the interface presents useful information clearly and supports a sensible workflow.

## Scope and prioritisation

Please spend approximately **3–4 hours** on this technical assessment.

The product could be developed far beyond what is practical within that time. We do not expect a production-ready system or every possible feature.

Prioritisation is part of the assessment. A focused, reliable, understandable solution is preferable to a larger solution with many incomplete features.

Where requirements are unclear, make a reasonable decision and document it. If you intentionally leave something out, explain what you would do with additional time.

## Optional extensions

The core technical assessment is the working full-stack application described above. The following areas are optional. They are useful if you finish the main workflow early, or if you want to briefly document how you would evolve the system with more time.

Please do not sacrifice the core request/callback workflow, data integrity, or usability in order to add these extensions.

### Large-scale architecture

You may briefly describe how the application could evolve if the device fleet, request volume, number of sites, or historical data size became much larger.

### Performance engineering

You may briefly note performance considerations for the parts of your application most likely to grow, such as dashboard views, historical measurement data, or pending request workflows.

### Cloud and platform engineering

You may briefly describe how you would run, configure, observe, and maintain the application outside a local development environment.

Actual cloud deployment is not required.

### Deep security engineering

Authentication for the supplied simulator is out of scope, but you may briefly note security considerations that would matter for a production version of this product.

Implementing a full security model is not required for this timebox. Clear acknowledgement of important risks is sufficient.

## Technical freedom

You may use any language, framework, database, and frontend technology you are comfortable with.

You are free to choose the application architecture, project structure, testing strategy, and supporting tooling. Choose an approach proportionate to the technical assessment.

A polished visual design is not required, but the application should be usable enough for an evaluator to follow the main workflow.

## Configuration expectations

Your repository should make it clear how to configure:

- the simulator base URL, usually `http://localhost:9000` when running locally;
- the callback URL that your backend sends to the simulator;
- any database connection or local persistence settings.

If your backend runs on the host machine while the simulator runs in Docker, the callback URL sent to the simulator usually needs to use `host.docker.internal`, for example:

```text
http://host.docker.internal:8000/api/device-results
```

Replace the port and path with the route exposed by your backend.

## Testing and verification

Include automated tests that you consider meaningful for the solution.

We are more interested in the quality and relevance of the tests than in a particular coverage percentage.

At minimum, consider testing:

- creating a measurement request;
- processing a completed callback;
- avoiding duplicate records when the same callback is received more than once;
- identifying readings outside the expected operating ranges.

## AI-assisted development

You may use AI-assisted development tools during the implementation phase of the technical assessment. You remain responsible for the submitted work and should be able to explain your implementation, key decisions, verification approach, and known limitations.

The live implementation and pull-request review portions of the interview will be conducted without AI-assisted development tools. Official language and framework documentation may be consulted.

## Submission

Submit your work as a Git repository at least **24 hours before your scheduled interview**.

Treat the repository as work being handed over to another engineer. It should contain enough information for an evaluator to:

- understand the solution;
- configure and run the application;
- connect it to the simulator;
- execute the automated tests;
- evaluate the main workflow.

Use your judgement when deciding what documentation and supporting material to include. Do not commit secrets or real credentials.

Before submitting, please check that someone evaluating your work can:

- start your application from a clean checkout;
- start the simulator using this pack;
- configure your application to talk to the simulator;
- request a measurement through the UI;
- see the request move through acknowledgement and callback states;
- run your automated tests;
- understand your assumptions and known limitations.

## Live interview

The interview will build directly on your submission. We may ask you to:

- walk through the operator experience;
- explain the architecture and data flow;
- discuss assumptions and trade-offs;
- review a pull request;
- identify risks or defects in a proposed code change;
- implement a small enhancement or bug fix;
- discuss how the platform might evolve, including one or two optional-extension directions.

You are not expected to have implemented the optional extensions during the submitted implementation phase. The live discussion focuses on your reasoning, implementation approach, validation, and trade-offs.

## Evaluation

We evaluate submissions holistically. Areas considered may include:

- product thinking and prioritisation;
- frontend and backend implementation;
- API and external-system integration;
- data modelling and asynchronous workflow handling;
- correctness and resilience;
- code quality and maintainability;
- testing and verification;
- dashboard usability;
- ability to communicate design choices, trade-offs, and verification clearly;
- documentation and handover quality.

Strong engineers may make different technical choices while producing equally effective solutions. We are more interested in your reasoning and execution than in a particular stack or architecture.

## Final note

Software that interacts with field devices operates at the boundary between systems we control and systems we do not.

Build an application that remains understandable and useful even when that boundary is imperfect.

Copyright (c) 2026 Nanolumi. All rights reserved. See `LICENSE`.
