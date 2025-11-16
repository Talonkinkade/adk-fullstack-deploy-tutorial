"""
File handler module for intelligent file routing and processing.

This module handles file processing for various file types including images, documents,
code files, and data files. It provides intelligent routing based on file type detection.
"""

import base64
import io
from typing import Dict, List, Optional, Any
from enum import Enum


class FileCategory(str, Enum):
    """File category enumeration"""
    IMAGE = "image"
    DOCUMENT = "document"
    CODE = "code"
    DATA = "data"
    OTHER = "other"


class FileHandler:
    """
    Handles file processing and intelligent routing based on file type.

    This class provides methods to:
    - Validate file data
    - Decode base64 encoded files
    - Detect file categories
    - Process different file types appropriately
    """

    # Supported MIME types by category
    MIME_TYPE_MAP = {
        FileCategory.IMAGE: [
            'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'
        ],
        FileCategory.DOCUMENT: [
            'application/pdf', 'text/plain', 'text/markdown',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ],
        FileCategory.CODE: [
            'text/javascript', 'text/typescript', 'text/x-python', 'text/x-java',
            'text/x-go', 'text/x-rust', 'text/x-c', 'text/x-c++',
            'application/json', 'text/html', 'text/css'
        ],
        FileCategory.DATA: [
            'application/json', 'text/csv', 'application/xml', 'text/xml',
            'application/yaml'
        ],
    }

    # File extension mapping
    EXTENSION_MAP = {
        # Images
        'jpg': FileCategory.IMAGE, 'jpeg': FileCategory.IMAGE,
        'png': FileCategory.IMAGE, 'gif': FileCategory.IMAGE,
        'webp': FileCategory.IMAGE, 'svg': FileCategory.IMAGE,

        # Documents
        'pdf': FileCategory.DOCUMENT, 'txt': FileCategory.DOCUMENT,
        'md': FileCategory.DOCUMENT, 'doc': FileCategory.DOCUMENT,
        'docx': FileCategory.DOCUMENT,

        # Code
        'js': FileCategory.CODE, 'ts': FileCategory.CODE,
        'jsx': FileCategory.CODE, 'tsx': FileCategory.CODE,
        'py': FileCategory.CODE, 'java': FileCategory.CODE,
        'go': FileCategory.CODE, 'rs': FileCategory.CODE,
        'cpp': FileCategory.CODE, 'c': FileCategory.CODE,
        'h': FileCategory.CODE, 'css': FileCategory.CODE,
        'html': FileCategory.CODE,

        # Data
        'json': FileCategory.DATA, 'csv': FileCategory.DATA,
        'xml': FileCategory.DATA, 'yaml': FileCategory.DATA,
        'yml': FileCategory.DATA, 'sql': FileCategory.DATA,
    }

    def __init__(self, max_file_size: int = 10 * 1024 * 1024):
        """
        Initialize FileHandler.

        Args:
            max_file_size: Maximum file size in bytes (default: 10MB)
        """
        self.max_file_size = max_file_size

    def validate_file(self, file_data: Dict[str, Any]) -> bool:
        """
        Validate file data structure and size.

        Args:
            file_data: Dictionary containing file metadata and data

        Returns:
            True if file is valid, False otherwise
        """
        required_fields = ['name', 'type', 'size', 'data', 'category']

        # Check required fields
        for field in required_fields:
            if field not in file_data:
                print(f"❌ File validation failed: missing field '{field}'")
                return False

        # Check file size
        if file_data['size'] > self.max_file_size:
            print(f"❌ File validation failed: size {file_data['size']} exceeds max {self.max_file_size}")
            return False

        return True

    def decode_file(self, base64_data: str) -> bytes:
        """
        Decode base64 encoded file data.

        Args:
            base64_data: Base64 encoded file content

        Returns:
            Decoded file bytes
        """
        try:
            return base64.b64decode(base64_data)
        except Exception as e:
            print(f"❌ Error decoding base64 file: {e}")
            raise

    def detect_category(self, mime_type: str, filename: str) -> FileCategory:
        """
        Detect file category from MIME type or filename extension.

        Args:
            mime_type: MIME type of the file
            filename: Name of the file

        Returns:
            Detected file category
        """
        # Check MIME type first
        for category, types in self.MIME_TYPE_MAP.items():
            if mime_type in types:
                return category

        # Fallback to extension
        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        return self.EXTENSION_MAP.get(extension, FileCategory.OTHER)

    def process_image(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process image file for vision-capable models.

        Args:
            file_data: File metadata and data

        Returns:
            Processed file information suitable for vision models
        """
        return {
            'type': 'image',
            'name': file_data['name'],
            'mime_type': file_data['type'],
            'size': file_data['size'],
            'base64_data': file_data['data'],
            'description': f"Image file: {file_data['name']}"
        }

    def process_document(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process document file (text extraction).

        Args:
            file_data: File metadata and data

        Returns:
            Processed document information
        """
        try:
            # Decode file
            file_bytes = self.decode_file(file_data['data'])

            # For text files, decode content
            if file_data['type'] in ['text/plain', 'text/markdown']:
                text_content = file_bytes.decode('utf-8')
                return {
                    'type': 'document',
                    'name': file_data['name'],
                    'mime_type': file_data['type'],
                    'content': text_content,
                    'description': f"Text document: {file_data['name']}"
                }

            # For other documents (PDF, DOCX), return metadata for now
            # In production, you'd use libraries like PyPDF2, python-docx, etc.
            return {
                'type': 'document',
                'name': file_data['name'],
                'mime_type': file_data['type'],
                'size': file_data['size'],
                'description': f"Document file: {file_data['name']} ({file_data['type']})",
                'note': 'Binary document - content extraction not yet implemented'
            }
        except Exception as e:
            print(f"❌ Error processing document: {e}")
            return {
                'type': 'document',
                'name': file_data['name'],
                'error': str(e),
                'description': f"Error processing document: {file_data['name']}"
            }

    def process_code(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process code file.

        Args:
            file_data: File metadata and data

        Returns:
            Processed code file information
        """
        try:
            # Decode file
            file_bytes = self.decode_file(file_data['data'])
            code_content = file_bytes.decode('utf-8')

            # Extract file extension for language detection
            extension = file_data['name'].split('.')[-1].lower()

            return {
                'type': 'code',
                'name': file_data['name'],
                'language': extension,
                'content': code_content,
                'lines': len(code_content.split('\n')),
                'description': f"Code file ({extension}): {file_data['name']}"
            }
        except Exception as e:
            print(f"❌ Error processing code file: {e}")
            return {
                'type': 'code',
                'name': file_data['name'],
                'error': str(e),
                'description': f"Error processing code file: {file_data['name']}"
            }

    def process_data_file(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data file (JSON, CSV, XML, YAML).

        Args:
            file_data: File metadata and data

        Returns:
            Processed data file information
        """
        try:
            # Decode file
            file_bytes = self.decode_file(file_data['data'])
            data_content = file_bytes.decode('utf-8')

            # Determine data format
            extension = file_data['name'].split('.')[-1].lower()

            return {
                'type': 'data',
                'name': file_data['name'],
                'format': extension,
                'content': data_content,
                'size': len(data_content),
                'description': f"Data file ({extension}): {file_data['name']}"
            }
        except Exception as e:
            print(f"❌ Error processing data file: {e}")
            return {
                'type': 'data',
                'name': file_data['name'],
                'error': str(e),
                'description': f"Error processing data file: {file_data['name']}"
            }

    def process_file(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intelligently route and process file based on its category.

        Args:
            file_data: File metadata and data

        Returns:
            Processed file information
        """
        # Validate file
        if not self.validate_file(file_data):
            return {
                'error': 'File validation failed',
                'name': file_data.get('name', 'unknown')
            }

        category = file_data.get('category', FileCategory.OTHER)

        print(f"📁 Processing file: {file_data['name']} (category: {category})")

        # Route to appropriate processor
        if category == FileCategory.IMAGE:
            return self.process_image(file_data)
        elif category == FileCategory.DOCUMENT:
            return self.process_document(file_data)
        elif category == FileCategory.CODE:
            return self.process_code(file_data)
        elif category == FileCategory.DATA:
            return self.process_data_file(file_data)
        else:
            return {
                'type': 'other',
                'name': file_data['name'],
                'mime_type': file_data['type'],
                'size': file_data['size'],
                'description': f"Unsupported file type: {file_data['name']}"
            }

    def process_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple files.

        Args:
            files: List of file data dictionaries

        Returns:
            List of processed file information
        """
        if not files:
            return []

        print(f"📦 Processing {len(files)} file(s)...")

        processed_files = []
        for file_data in files:
            processed = self.process_file(file_data)
            processed_files.append(processed)

        return processed_files

    def create_file_context_message(self, processed_files: List[Dict[str, Any]]) -> str:
        """
        Create a context message summarizing uploaded files for the LLM.

        Args:
            processed_files: List of processed file information

        Returns:
            Formatted context message
        """
        if not processed_files:
            return ""

        context_parts = ["📎 **Attached Files:**\n"]

        for file_info in processed_files:
            file_type = file_info.get('type', 'unknown')
            name = file_info.get('name', 'unknown')
            description = file_info.get('description', '')

            context_parts.append(f"\n- **{name}** ({file_type})")

            if 'content' in file_info and file_info['content']:
                # Truncate long content
                content = file_info['content']
                if len(content) > 500:
                    content = content[:500] + '...\n[Content truncated]'
                context_parts.append(f"\n  Content:\n  ```\n  {content}\n  ```")

            if 'error' in file_info:
                context_parts.append(f"\n  ⚠️ Error: {file_info['error']}")

        return "\n".join(context_parts)


# Singleton instance
_file_handler: Optional[FileHandler] = None


def get_file_handler() -> FileHandler:
    """
    Get or create the singleton FileHandler instance.

    Returns:
        FileHandler instance
    """
    global _file_handler
    if _file_handler is None:
        _file_handler = FileHandler()
    return _file_handler
