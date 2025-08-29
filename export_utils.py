import csv, io
from fastapi.responses import StreamingResponse, JSONResponse

def to_csv_stream(filename: str, rows, headers):
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(headers)
    for r in rows:
        writer.writerow([r.get(h, "") for h in headers])
    stream.seek(0)
    return StreamingResponse(iter([stream.read()]), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})