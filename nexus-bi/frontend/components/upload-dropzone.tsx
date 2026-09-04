"use client";

import { useCallback, useRef, useState } from "react";
import { UploadCloud, FileSpreadsheet, Loader2 } from "lucide-react";
import { ApiError, uploadDataset } from "@/lib/api";
import type { DatasetUploadResponse } from "@/lib/types";

const ACCEPTED_EXTENSIONS = [".csv", ".xlsx"];

interface UploadDropzoneProps {
  onUploaded: (result: DatasetUploadResponse) => void;
}

type UploadState =
  | { status: "idle" }
  | { status: "uploading"; percent: number; filename: string }
  | { status: "error"; message: string };

function isAcceptedFile(file: File): boolean {
  const lower = file.name.toLowerCase();
  return ACCEPTED_EXTENSIONS.some((ext) => lower.endsWith(ext));
}

export function UploadDropzone({ onUploaded }: UploadDropzoneProps) {
  const [state, setState] = useState<UploadState>({ status: "idle" });
  const [isDragActive, setIsDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(
    async (file: File) => {
      if (!isAcceptedFile(file)) {
        setState({
          status: "error",
          message: `"${file.name}" isn't a .csv or .xlsx file.`,
        });
        return;
      }

      setState({ status: "uploading", percent: 0, filename: file.name });
      try {
        const result = await uploadDataset(file, (percent) =>
          setState({ status: "uploading", percent, filename: file.name }),
        );
        setState({ status: "idle" });
        onUploaded(result);
      } catch (err) {
        const message = err instanceof ApiError ? err.message : "Upload failed. Try again.";
        setState({ status: "error", message });
      }
    },
    [onUploaded],
  );

  const onDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setIsDragActive(false);
      const file = event.dataTransfer.files?.[0];
      if (file) void handleFile(file);
    },
    [handleFile],
  );

  const onInputChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) void handleFile(file);
      event.target.value = ""; // allow re-uploading the same filename
    },
    [handleFile],
  );

  const isUploading = state.status === "uploading";

  return (
    <div className="w-full">
      <div
        role="button"
        tabIndex={0}
        onClick={() => !isUploading && inputRef.current?.click()}
        onKeyDown={(e) => {
          if ((e.key === "Enter" || e.key === " ") && !isUploading) inputRef.current?.click();
        }}
        onDragOver={(e) => {
          e.preventDefault();
          if (!isUploading) setIsDragActive(true);
        }}
        onDragLeave={() => setIsDragActive(false)}
        onDrop={isUploading ? undefined : onDrop}
        className={`flex flex-col items-center justify-center gap-3 rounded-panel border-2 border-dashed px-6 py-14 text-center transition-colors ${
          isDragActive
            ? "border-mint bg-mint/5"
            : "border-border bg-navy/[0.02] dark:bg-white/[0.02]"
        } ${isUploading ? "cursor-default opacity-80" : "cursor-pointer hover:border-mint/60"}`}
      >
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED_EXTENSIONS.join(",")}
          className="hidden"
          onChange={onInputChange}
          disabled={isUploading}
        />

        {isUploading ? (
          <>
            <Loader2 className="h-8 w-8 animate-spin text-mint" />
            <div className="w-full max-w-xs">
              <div className="mb-1 flex justify-between text-xs text-muted">
                <span className="truncate">{state.filename}</span>
                <span>{state.percent}%</span>
              </div>
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-border">
                <div
                  className="h-full rounded-full bg-mint transition-all"
                  style={{ width: `${state.percent}%` }}
                />
              </div>
            </div>
          </>
        ) : (
          <>
            <UploadCloud className="h-8 w-8 text-muted" />
            <div>
              <p className="font-medium">Drop a CSV or XLSX file here, or click to browse</p>
              <p className="mt-1 flex items-center justify-center gap-1 text-sm text-muted">
                <FileSpreadsheet className="h-4 w-4" /> .csv and .xlsx, up to 50MB
              </p>
            </div>
          </>
        )}
      </div>

      {state.status === "error" && (
        <p className="mt-3 text-sm text-red-500" role="alert">
          {state.message}
        </p>
      )}
    </div>
  );
}
