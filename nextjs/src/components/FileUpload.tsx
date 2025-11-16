'use client';

import React, { useCallback, useState } from 'react';
import { X, Upload, FileText, Image, Code, Database, File } from 'lucide-react';

export interface UploadedFile {
  id: string;
  name: string;
  type: string;
  size: number;
  data: string; // base64 encoded
  category: FileCategory;
}

export type FileCategory = 'image' | 'document' | 'code' | 'data' | 'other';

interface FileUploadProps {
  files: UploadedFile[];
  onFilesChange: (files: UploadedFile[]) => void;
  maxFiles?: number;
  maxFileSize?: number; // in bytes
  maxTotalSize?: number; // in bytes
}

const FILE_CONFIG = {
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB per file
  MAX_TOTAL_SIZE: 50 * 1024 * 1024, // 50MB total
  MAX_FILES: 5,
  ALLOWED_TYPES: {
    image: ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'],
    document: ['application/pdf', 'text/plain', 'text/markdown', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    code: ['text/javascript', 'text/typescript', 'text/x-python', 'text/x-java', 'text/x-go', 'text/x-rust', 'text/x-c', 'text/x-c++', 'application/json', 'text/html', 'text/css'],
    data: ['application/json', 'text/csv', 'application/xml', 'text/xml', 'application/yaml'],
  },
};

// Intelligent file type detection
const detectFileCategory = (file: File): FileCategory => {
  const mimeType = file.type;
  const extension = file.name.split('.').pop()?.toLowerCase();

  // Check MIME type first
  for (const [category, types] of Object.entries(FILE_CONFIG.ALLOWED_TYPES)) {
    if (types.includes(mimeType)) {
      return category as FileCategory;
    }
  }

  // Fallback to extension-based detection
  const extensionMap: Record<string, FileCategory> = {
    // Images
    jpg: 'image', jpeg: 'image', png: 'image', gif: 'image', webp: 'image', svg: 'image',
    // Documents
    pdf: 'document', txt: 'document', md: 'document', doc: 'document', docx: 'document',
    // Code
    js: 'code', ts: 'code', jsx: 'code', tsx: 'code', py: 'code', java: 'code',
    go: 'code', rs: 'code', cpp: 'code', c: 'code', h: 'code', css: 'code', html: 'code',
    // Data
    json: 'data', csv: 'data', xml: 'data', yaml: 'data', yml: 'data', sql: 'data',
  };

  return extensionMap[extension || ''] || 'other';
};

const getCategoryIcon = (category: FileCategory) => {
  switch (category) {
    case 'image': return <Image className="w-4 h-4" />;
    case 'document': return <FileText className="w-4 h-4" />;
    case 'code': return <Code className="w-4 h-4" />;
    case 'data': return <Database className="w-4 h-4" />;
    default: return <File className="w-4 h-4" />;
  }
};

const getCategoryColor = (category: FileCategory): string => {
  switch (category) {
    case 'image': return 'bg-purple-100 text-purple-700 border-purple-300';
    case 'document': return 'bg-blue-100 text-blue-700 border-blue-300';
    case 'code': return 'bg-green-100 text-green-700 border-green-300';
    case 'data': return 'bg-orange-100 text-orange-700 border-orange-300';
    default: return 'bg-gray-100 text-gray-700 border-gray-300';
  }
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

export default function FileUpload({
  files,
  onFilesChange,
  maxFiles = FILE_CONFIG.MAX_FILES,
  maxFileSize = FILE_CONFIG.MAX_FILE_SIZE,
  maxTotalSize = FILE_CONFIG.MAX_TOTAL_SIZE,
}: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateFiles = (newFiles: File[]): string | null => {
    const currentTotalSize = files.reduce((sum, f) => sum + f.size, 0);
    const newTotalSize = newFiles.reduce((sum, f) => sum + f.size, 0);

    if (files.length + newFiles.length > maxFiles) {
      return `Maximum ${maxFiles} files allowed`;
    }

    for (const file of newFiles) {
      if (file.size > maxFileSize) {
        return `File "${file.name}" exceeds ${formatFileSize(maxFileSize)} limit`;
      }
    }

    if (currentTotalSize + newTotalSize > maxTotalSize) {
      return `Total file size exceeds ${formatFileSize(maxTotalSize)} limit`;
    }

    return null;
  };

  const processFiles = useCallback(
    async (fileList: FileList | null) => {
      if (!fileList || fileList.length === 0) return;

      const newFiles = Array.from(fileList);
      const validationError = validateFiles(newFiles);

      if (validationError) {
        setError(validationError);
        setTimeout(() => setError(null), 3000);
        return;
      }

      setError(null);

      const processedFiles: UploadedFile[] = await Promise.all(
        newFiles.map(
          (file) =>
            new Promise<UploadedFile>((resolve, reject) => {
              const reader = new FileReader();
              reader.onload = (e) => {
                const base64 = e.target?.result as string;
                resolve({
                  id: `${Date.now()}-${Math.random()}`,
                  name: file.name,
                  type: file.type || 'application/octet-stream',
                  size: file.size,
                  data: base64.split(',')[1], // Remove data:image/png;base64, prefix
                  category: detectFileCategory(file),
                });
              };
              reader.onerror = reject;
              reader.readAsDataURL(file);
            })
        )
      );

      onFilesChange([...files, ...processedFiles]);
    },
    [files, onFilesChange]
  );

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      processFiles(e.dataTransfer.files);
    },
    [processFiles]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      processFiles(e.target.files);
      e.target.value = ''; // Reset input
    },
    [processFiles]
  );

  const removeFile = useCallback(
    (fileId: string) => {
      onFilesChange(files.filter((f) => f.id !== fileId));
    },
    [files, onFilesChange]
  );

  const totalSize = files.reduce((sum, f) => sum + f.size, 0);

  return (
    <div className="w-full space-y-2">
      {/* Dropzone */}
      <div
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-6 transition-all duration-200
          ${isDragging
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-950'
            : 'border-gray-300 dark:border-gray-700 hover:border-gray-400 dark:hover:border-gray-600'
          }
          ${files.length >= maxFiles ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
        onClick={() => {
          if (files.length < maxFiles) {
            document.getElementById('file-input')?.click();
          }
        }}
      >
        <input
          id="file-input"
          type="file"
          multiple
          onChange={handleFileInput}
          className="hidden"
          disabled={files.length >= maxFiles}
        />

        <div className="flex flex-col items-center justify-center space-y-2 text-center">
          <Upload className={`w-8 h-8 ${isDragging ? 'text-blue-500' : 'text-gray-400'}`} />
          <div className="text-sm">
            <span className="font-medium text-gray-700 dark:text-gray-300">
              {isDragging ? 'Drop files here' : 'Drop files or click to upload'}
            </span>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Auto-detects images, documents, code & data
            </p>
          </div>
          <p className="text-xs text-gray-400">
            {maxFiles - files.length} of {maxFiles} slots available • {formatFileSize(maxFileSize)} max per file
          </p>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="text-xs text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-950 px-3 py-2 rounded">
          {error}
        </div>
      )}

      {/* File list */}
      {files.length > 0 && (
        <div className="space-y-1">
          {files.map((file) => (
            <div
              key={file.id}
              className="flex items-center justify-between gap-2 p-2 rounded bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-center gap-2 flex-1 min-w-0">
                <div className={`flex items-center gap-1 px-2 py-1 rounded border text-xs font-medium ${getCategoryColor(file.category)}`}>
                  {getCategoryIcon(file.category)}
                  <span className="capitalize">{file.category}</span>
                </div>
                <span className="text-sm truncate flex-1" title={file.name}>
                  {file.name}
                </span>
                <span className="text-xs text-gray-500 whitespace-nowrap">
                  {formatFileSize(file.size)}
                </span>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  removeFile(file.id);
                }}
                className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors"
                aria-label="Remove file"
              >
                <X className="w-4 h-4 text-gray-500" />
              </button>
            </div>
          ))}

          {/* Total size indicator */}
          <div className="text-xs text-gray-500 dark:text-gray-400 text-right">
            Total: {formatFileSize(totalSize)} / {formatFileSize(maxTotalSize)}
          </div>
        </div>
      )}
    </div>
  );
}
