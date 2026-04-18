# Testing

## Test Execution

Run tests with:

```bash
uv run pytest -v
```

## Current Test Suite

- `test_mcp_server.py` - tool registration and metadata

## What's NOT Tested (Future Improvements)

The improved tests focus on tool definition validation. For more comprehensive testing, consider adding:

1. **Integration Tests** - Call tools with real API (requires valid credentials)
2. **Mock API Tests** - Mock httpx calls to test error handling without hitting real API
3. **Parameter Validation Tests** - Verify invalid parameters are rejected appropriately
4. **End-to-End Tests** - Test complete flow from Claude input → tool call → API response

## Benefits

- ✅ **Tool Discovery**: Claude can see exactly what parameters each tool accepts
- ✅ **Type Safety**: Parameters have correct types for Claude to use them properly
- ✅ **Documentation**: Tool descriptions guide LLM usage
- ✅ **Validation**: Ensures all tools follow expected patterns
- ✅ **Regression Prevention**: Tests catch breaking changes to tool definitions
