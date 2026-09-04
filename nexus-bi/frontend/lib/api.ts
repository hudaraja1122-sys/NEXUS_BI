import type { ApiErrorBody, DatasetSummary, DatasetUploadResponse } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function checkHealth(): Promise<{ status: string; environment: string }> {
  const res = await fetch(`${API_BASE_URL}/health`, { cache: "no-store" });
  if (!res.ok) throw new ApiError(res.status, "Health check failed");
  return res.json();
}

export async function listDatasets(): Promise<DatasetSummary[]> {
  const res = await fetch(`${API_BASE_URL}/api/datasets`, { cache: "no-store" });
  if (!res.ok) throw new ApiError(res.status, "Failed to list datasets");
  const body: { datasets: DatasetSummary[] } = await res.json();
  return body.datasets;
}

export async function getDataset(datasetId: string): Promise<DatasetUploadResponse> {
  const res = await fetch(`${API_BASE_URL}/api/datasets/${datasetId}`, { cache: "no-store" });
  if (!res.ok) {
    const body: ApiErrorBody = await res.json().catch(() => ({ detail: "Failed to fetch dataset" }));
    throw new ApiError(res.status, body.detail);
  }
  return res.json();
}

/**
 * Uploads a dataset with progress reporting. Uses XHR (not fetch) because
 * fetch has no cross-browser upload-progress event as of Next.js 15 / the
 * runtimes this targets.
 */
export function uploadDataset(
  file: File,
  onProgress?: (percent: number) => void,
): Promise<DatasetUploadResponse> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append("file", file);

    xhr.open("POST", `${API_BASE_URL}/api/datasets/upload`);

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable && onProgress) {
        onProgress(Math.round((event.loaded / event.total) * 100));
      }
    };

    xhr.onload = () => {
      let body: unknown;
      try {
        body = JSON.parse(xhr.responseText);
      } catch {
        reject(new ApiError(xhr.status, "Server returned an invalid response."));
        return;
      }
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(body as DatasetUploadResponse);
      } else {
        const detail = (body as ApiErrorBody | undefined)?.detail ?? "Upload failed.";
        reject(new ApiError(xhr.status, detail));
      }
    };

    xhr.onerror = () => reject(new ApiError(0, "Network error — is the backend running?"));

    xhr.send(formData);
  });
}
