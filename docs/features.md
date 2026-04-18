# Supported Features

## MCP Tools (17 Total)

All tools support comprehensive error handling with `success` and `error` fields in responses.

### Clients (2 tools)

- **`get_all_clients`** - List all clients with filtering
  - Filters: types, owners, date ranges (created/modified), include inactive, search
  - Pagination: page, page_size
  - Sort support

- **`get_client_info`** - Get detailed information about a specific client
  - Returns: client details, addresses, contacts, files

### Projects (2 tools)

- **`get_all_projects`** - List all projects with comprehensive filtering
  - Filters: client_ids, stage_groups, stages, priorities, project_managers, date ranges (created/modified/completed), include archived, search
  - Pagination: page, page_size
  - Sort support

- **`get_project_info`** - Get detailed project information
  - Returns: full project details, items, locations, systems, phases, labor types, taxes, payment terms, files

### Change Orders (2 tools)

- **`get_all_change_orders`** - List change orders for a project
  - Requires: project_id
  - Returns: change orders list

- **`get_change_order_info`** - Get detailed change order information
  - Returns: full change order details, items, adjustments, payments, taxes

### Opportunities (2 tools)

- **`get_all_opportunities`** - List all opportunities with extensive filtering
  - Filters: types, client_ids, stages, stage_groups, priorities, owners, date ranges (estimated/actual close dates, created/modified), include archived, search
  - Pagination: page, page_size
  - Sort support

- **`get_opportunity_info`** - Get detailed opportunity information
  - Returns: full opportunity details, pricing, associated quotes, resources, files

### Products (2 tools)

- **`get_all_products`** - List all products with filtering
  - Filters: brands, categories, suppliers, stock_items_only, include_inactive, search
  - Pagination: page, page_size
  - Sort support

- **`get_product_info`** - Get detailed product information
  - Returns: product details, pricing, images, specifications, labor items, accessories, subscriptions, inventory

### Purchase Orders (2 tools)

- **`get_all_purchase_orders`** - List all purchase orders with filtering
  - Filters: suppliers, project_ids, statuses, date ranges (ordered/received/created/modified), include archived, search
  - Pagination: page, page_size
  - Sort support

- **`get_purchase_order_info`** - Get detailed purchase order information
  - Returns: PO details, supplier info, products, pricing, shipping, billing, contacts

### Quotes (2 tools)

- **`get_all_quotes`** - List all quotes for a specific opportunity
  - Requires: opportunity_id
  - Returns: quotes list with version info

- **`get_quote_info`** - Get detailed quote information
  - Returns: full quote details, line items, pricing, taxes, payment terms, service plans, files

### Service Contracts (2 tools)

- **`get_all_service_contracts`** - List all service contracts with filtering
  - Filters: client_ids, project_ids, date ranges (start/end/payment_due/canceled/created/modified), include archived, search
  - Pagination: page, page_size
  - Sort support

- **`get_service_contract_info`** - Get detailed service contract information
  - Returns: contract details, pricing, dates, payment terms, features, files, payment schedules

### Time Entries (1 tool)

- **`get_all_time_entries`** - List all time entries with comprehensive filtering
  - Filters: types, resources, client_ids, project_ids, service_call_ids, labor_types, overtimes_only, include_archived
  - Date range: from_date, to_date
  - Pagination: page, page_size
  - Search and sort support

### Files (1 tool)

- **`get_file_info`** - Get detailed file information
  - Returns: file name, URL, parent object type/ID

## API Endpoints (GET operations)

### Implemented ✅

- [x] **Clients**
  - [x] GetClients - List with filters and pagination
  - [x] GetClient - Get single client details

- [x] **Projects**
  - [x] GetProjects - List with filters and pagination
  - [x] GetProject - Get single project details

- [x] **Change Orders**
  - [x] GetChangeOrders - List by project with pagination
  - [x] GetChangeOrder - Get single change order details

- [x] **Opportunities**
  - [x] GetOpportunities - List with filters and pagination
  - [x] GetOpportunity - Get single opportunity details

- [x] **Products**
  - [x] GetProducts - List with filters and pagination
  - [x] GetProduct - Get single product details

- [x] **Purchase Orders**
  - [x] GetPurchaseOrders - List with filters and pagination
  - [x] GetPurchaseOrder - Get single purchase order details

- [x] **Quotes**
  - [x] GetQuotes - List by opportunity
  - [x] GetQuote - Get single quote details

- [x] **Service Contracts**
  - [x] GetServiceContracts - List with filters and pagination
  - [x] GetServiceContract - Get single service contract details

- [x] **Time Entries**
  - [x] GetTimeEntries - List with filters and pagination

- [x] **Files**
  - [x] GetFile - Get single file details

### Not Implemented

- [ ] Create/Update operations (POST, PUT endpoints)
- [ ] Delete operations

## Common Features

### Parameter Support

- **Filtering**: Most list endpoints support filtering by relevant fields
- **Date Ranges**: Support for filtering by creation, modification, and domain-specific dates
- **Pagination**: Configurable page number and page size (default: page 1, 20 items)
- **Search**: Full-text search on applicable resources
- **Sorting**: Sort by field name on list endpoints
- **Archive Filtering**: Option to include/exclude archived items

### Error Handling

All tools return consistent error responses:

- `success: false` with `error` field for failures
- `success: true` with `data` field for successful responses
- Validation errors for missing required parameters
- API errors with detailed messages

### Authentication

Supports two authentication methods:

1. **API Key**: `DTOOLS_API_KEY` environment variable
2. **Auth Token**: `DTOOLS_AUTH_TOKEN` environment variable

Both methods are automatically handled by the server.

## Architecture

### API Endpoints Layer

Each resource has an endpoint file in `src/dtools_mcp/api_endpoints/`:

- Core functions for each endpoint (e.g., `list_clients()`, `get_client_details()`)
- Parameter validation and error handling
- Query builder for constructing filter parameters

### MCP Tools Layer

`src/dtools_mcp/server.py` wraps endpoints as MCP tools:

- Tool registration with descriptions
- Parameter schemas for LLM integration
- Consistent response format (success/data or success/error)
- Centralized logging

### Utilities

- **QueryBuilder**: Constructs complex query parameters for API calls
- **Config**: Centralized environment variable and configuration management
- **Shared**: Common utilities (BASE_API_URL, authentication headers)
- **Logger**: Centralized logging configuration
