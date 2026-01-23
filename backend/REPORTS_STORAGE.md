# Reports Storage Configuration

## Current Setup

The application stores generated PDF reports in a Fly.io volume mounted at `/data/reports`.

### Configuration

- **Volume Name**: `reports_data`
- **Mount Point**: `/data`
- **Reports Directory**: `/data/reports` (configured via `REPORTS_DIR` env var in `fly.toml`)
- **Multi-Region Deployment**: Deployed across 3 regions (iad, lax, syd)

### Current Architecture

```
fly.toml:
  [[mounts]]
    source = "reports_data"
    destination = "/data"
  
  [env]
    REPORTS_DIR = "/data/reports"
```

## Multi-Region Considerations

### Current Limitation

Fly.io volumes are **region-specific** and not automatically replicated across regions. This means:

1. Reports generated in one region are stored in that region's volume
2. If a user's request is routed to a different region, the report file may not be accessible
3. The `download_report` endpoint checks `os.path.exists(report.file_path)` which will fail if the file is in another region's volume

### Impact

- **Intermittent 404 errors**: Users may get "Report file not found" errors when their download request hits a different region than where the report was generated
- **After restarts**: If an instance restarts and is placed in a different region, previously generated reports become inaccessible

## Recommended Solutions

### Option 1: Shared Object Storage (Recommended for Production)

Migrate to a shared object storage service like AWS S3, Cloudflare R2, or Backblaze B2.

**Advantages:**
- Reports accessible from all regions
- No data loss on instance restarts
- Better scalability
- Lower cost for large volumes of reports

**Implementation:**
1. Add S3-compatible storage client (e.g., `boto3` or `aioboto3`)
2. Update `report_generator.py` to upload PDFs to object storage
3. Store object keys (not file paths) in `Report.file_path`
4. Update `download_report` to stream from object storage
5. Add environment variables for storage credentials

**Example Change:**
```python
# Instead of:
file_path = os.path.join(settings.REPORTS_DIR, filename)
HTML(string=html_content).write_pdf(file_path)

# Use:
pdf_bytes = HTML(string=html_content).write_pdf()
object_key = f"reports/{report_id}/{filename}"
s3_client.upload_fileobj(BytesIO(pdf_bytes), bucket, object_key)
report.file_path = object_key
```

### Option 2: Single-Region Deployment

Deploy all instances in a single region to ensure volume consistency.

**Advantages:**
- Simple, no code changes needed
- Works with current implementation

**Disadvantages:**
- Higher latency for users in other regions
- Single point of failure
- Doesn't leverage multi-region benefits

**Implementation:**
```toml
# fly.toml - Remove multi-region config
primary_region = "iad"

# Remove:
# [[regions]]
#   name = "lax"
# [[regions]]
#   name = "syd"
```

### Option 3: Volume Replication (Not Recommended)

Manually replicate volumes across regions using scheduled jobs.

**Disadvantages:**
- Complex to implement and maintain
- Replication lag can cause issues
- Increased storage costs
- Risk of sync conflicts

## Migration Path

If migrating to object storage:

1. **Phase 1**: Add object storage support alongside file storage
   - New reports go to object storage
   - Old reports remain on volume
   - Download endpoint checks both locations

2. **Phase 2**: Migrate existing reports
   - Background job to upload existing PDFs to object storage
   - Update database `file_path` values to object keys

3. **Phase 3**: Remove volume dependency
   - Remove volume mount from `fly.toml`
   - Remove file system code from `report_generator.py`

## Current Workaround

Until a permanent solution is implemented, consider:

1. **Primary region routing**: Configure Fly.io to prefer routing to the primary region (iad) where most reports are likely stored
2. **Retry logic**: Add retry logic in the frontend to attempt download from different regions
3. **Monitoring**: Set up alerts for 404 errors on report downloads to track the frequency of this issue

## Related Files

- `backend/fly.toml` - Volume and region configuration
- `backend/app/core/config.py` - REPORTS_DIR configuration
- `backend/app/services/report_generator.py` - Report generation and storage
- `backend/app/api/reports.py` - Report download endpoint
