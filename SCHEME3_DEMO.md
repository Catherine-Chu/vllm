# Scheme 3 structured output integration

This branch publishes the vLLM source changes used by the approved centralized T04 demo. The native base is **v0.32.0**, commit `5df63a7203cdb9328d824a27b682e77c7b9928be`. This is an independent Scheme 3 branch, with no Scheme 3.1 changes and no upstream pull request.

The grammar integration is a separate commit from the historical CPU fallback fix. Ascend integration can select the grammar commit without automatically taking the CPU fix. The complete branch includes both to preserve the source content used in the local CPU verification.

## Integration scope

- `vllm/sampling_params.py`: the mixed grammar handle parameter, validation and explicit rejection of unsupported combinations.
- `vllm/v1/structured_output/backend_types.py`: the handle constraint type.
- `vllm/v1/structured_output/request.py`: mapping the handle into the existing structured-output request key.
- `vllm/v1/structured_output/backend_xgrammar.py`: delegating mixed compilation to the external package while retaining the native matcher and stop behavior.
- `vllm/utils/cpu_triton_utils.py`: a separately committed, historical CPU fallback argument binding and unused-slot PAD fix; not an Ascend adaptation.

The runtime also needs the `mixed_tokenizer` package and the modified XGrammar from [demo/schema3-grammar](https://github.com/Catherine-Chu/xgrammar/tree/demo/schema3-grammar). This branch alone does not provide the offline tokenizer or Grammar artifact builder.

## Design and validation

The companion project is [vllm-mixed-tokenizer-demo](https://github.com/Catherine-Chu/vllm-mixed-tokenizer-demo/tree/demo/scheme3); access to that private repository is required. The approved T04 implementation is fixed by its `demo-t04-optimized` tag.

- [Handoff and pinned versions](https://github.com/Catherine-Chu/vllm-mixed-tokenizer-demo/blob/demo/scheme3/docs/T04_HANDOFF.md)
- [Module map](https://github.com/Catherine-Chu/vllm-mixed-tokenizer-demo/blob/demo/scheme3/docs/SYSTEM_MODULE_MAP.md)
- [Bridge contract tests](https://github.com/Catherine-Chu/vllm-mixed-tokenizer-demo/blob/demo/scheme3/tests/test_task03_vllm_bridge.py)
- [Complete T04 regression driver](https://github.com/Catherine-Chu/vllm-mixed-tokenizer-demo/blob/demo/scheme3/scripts/run_task04opt_regression.py)
- [Approved regression evidence](https://github.com/Catherine-Chu/vllm-mixed-tokenizer-demo/blob/demo/scheme3/docs/results/task04opt/review-manifest.json)

The approved run passed 219 unit tests, 180 real-model HTTP functional requests and 82 lifecycle calls according to their expected-success/rejection/disconnection contracts. Validation used a local CPU and a fixed random one-block model with the full target vocabulary. Formal 27B weights, 910B3, MTP and device asynchronous model scheduling were not validated by this run. The recent T04 performance changes reside in the companion package, not in new vLLM patches.

The published source files are byte-identical to the approved patched checkout. Publication itself did not rebuild vLLM or create a new platform validation result. Fork checkouts already contain these patches: do not apply them twice. The existing companion E2E drivers deliberately require the original base HEAD plus the exact uncommitted patch scope; a new fork HEAD will not satisfy that provenance assertion. Follow the handoff's base-plus-patch reproduction route without deleting its assertions.
