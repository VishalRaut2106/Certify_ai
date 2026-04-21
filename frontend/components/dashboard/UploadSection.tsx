'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { certificateAPI } from '@/lib/api'
import toast from 'react-hot-toast'
import { 
  CloudArrowUpIcon, 
  DocumentIcon, 
  XMarkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  DocumentArrowUpIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'

interface UploadSectionProps {
  onUploadSuccess: () => void
}

interface UploadedFile {
  file: File
  status: 'pending' | 'uploading' | 'success' | 'error'
  progress: number
  error?: string
  certificateId?: string
}

export default function UploadSection({ onUploadSuccess }: UploadSectionProps) {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [uploading, setUploading] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map(file => ({
      file,
      status: 'pending' as const,
      progress: 0
    }))
    setFiles(prev => [...prev, ...newFiles])
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/tiff': ['.tiff', '.tif']
    },
    maxSize: 10 * 1024 * 1024,
  })

  const removeFile = (index: number) => {
    if (uploading) return;
    setFiles(prev => prev.filter((_, i) => i !== index))
  }

  const uploadFiles = async () => {
    if (files.length === 0) return
    setUploading(true)
    
    try {
      if (files.length === 1) {
        const fileData = files[0]
        setFiles(prev => prev.map((f, i) => i === 0 ? { ...f, status: 'uploading', progress: 50 } : f))
        
        const response = await certificateAPI.uploadSingle(fileData.file)
        
        setFiles(prev => prev.map((f, i) => i === 0 ? { 
          ...f, status: 'success', progress: 100, certificateId: response.data.certificate_id 
        } : f))
        
        toast.success('Certificate verified successfully!')
      } else {
        setFiles(prev => prev.map(f => ({ ...f, status: 'uploading', progress: 50 })))
        const fileList = files.map(f => f.file)
        const response = await certificateAPI.uploadBulk(fileList)
        
        setFiles(prev => prev.map((f, i) => ({
          ...f, status: 'success', progress: 100, certificateId: response.data.uploaded_certificates[i]?.certificate_id
        })))
        toast.success(`${files.length} certificates processed!`)
      }
      onUploadSuccess()
    } catch (error: any) {
      setFiles(prev => prev.map(f => ({ 
        ...f, status: 'error', error: error.response?.data?.detail || 'Upload failed' 
      })))
      toast.error('Verification failed. See details.')
    } finally {
      setUploading(false)
    }
  }

  const clearAll = () => {
    if (!uploading) setFiles([])
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="space-y-8">
      {/* Upload Zone */}
      <div className="glass-panel p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-outfit font-bold text-slate-900">Document Verification</h2>
            <p className="text-sm text-slate-500 font-medium mt-1">
              Upload certificates to verify authenticity with our AI engine.
            </p>
          </div>
          {files.length > 0 && !uploading && (
            <button onClick={clearAll} className="text-sm font-semibold text-slate-500 hover:text-red-500 transition-colors">
              Clear all
            </button>
          )}
        </div>

        <div
          {...getRootProps()}
          className={`relative border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center transition-all duration-300 cursor-pointer overflow-hidden
            ${isDragActive 
              ? 'border-primary-500 bg-primary-50/50 shadow-inner' 
              : 'border-slate-300 hover:border-primary-400 hover:bg-slate-50/50'}
          `}
        >
          <input {...getInputProps()} />
          <div className={`absolute inset-0 bg-gradient-to-r from-primary-500 to-indigo-500 opacity-0 transition-opacity duration-300 ${isDragActive ? 'opacity-5' : ''}`} />
          
          <div className="relative z-10 flex flex-col items-center">
            <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-6 transition-transform duration-300 shadow-sm ${
              isDragActive ? 'bg-primary-100 scale-110 shadow-glow-primary' : 'bg-white border border-slate-200'
            }`}>
              <CloudArrowUpIcon className={`h-8 w-8 ${
                isDragActive ? 'text-primary-600' : 'text-slate-400'
              }`} />
            </div>
            
            <p className="text-lg font-semibold text-slate-900 mb-2">
              {isDragActive ? 'Drop documents here' : 'Drag & drop certificates'}
            </p>
            <p className="text-sm text-slate-500 mb-6">
              or <span className="text-primary-600 font-semibold hover:underline">browse files</span> from your device
            </p>
            
            <div className="flex flex-wrap justify-center gap-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
              <span className="px-3 py-1 bg-white border border-slate-200 rounded-lg shadow-sm">PDF</span>
              <span className="px-3 py-1 bg-white border border-slate-200 rounded-lg shadow-sm">JPG</span>
              <span className="px-3 py-1 bg-white border border-slate-200 rounded-lg shadow-sm">PNG</span>
              <span className="px-3 py-1 bg-slate-100 border border-slate-200 rounded-lg">Max 10MB</span>
            </div>
          </div>
        </div>

        {/* File Queue */}
        {files.length > 0 && (
          <div className="mt-8 animate-fade-in">
            <div className="space-y-3 max-h-72 overflow-y-auto pr-2 custom-scrollbar">
              {files.map((fileData, index) => (
                <div key={index} className="flex items-center space-x-4 p-4 bg-white border border-slate-200/60 rounded-xl shadow-sm transition-all hover:shadow-md group">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-slate-50 rounded-lg border border-slate-100 flex items-center justify-center">
                      <DocumentIcon className="h-6 w-6 text-slate-400" />
                    </div>
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-sm font-semibold text-slate-900 truncate pr-4">
                        {fileData.file.name}
                      </p>
                      
                      <div className="flex items-center space-x-2">
                        {fileData.status === 'success' && <span className="flex items-center text-xs font-bold text-success-600 bg-success-50 px-2 py-1 rounded-md"><CheckCircleIcon className="w-4 h-4 mr-1" />Verified</span>}
                        {fileData.status === 'error' && <span className="flex items-center text-xs font-bold text-danger-600 bg-danger-50 px-2 py-1 rounded-md"><ExclamationTriangleIcon className="w-4 h-4 mr-1" />Failed</span>}
                        {fileData.status === 'uploading' && <span className="flex items-center text-xs font-bold text-primary-600 bg-primary-50 px-2 py-1 rounded-md"><div className="w-3 h-3 border-2 border-primary-600 border-t-transparent rounded-full animate-spin mr-1.5" />Processing</span>}
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3 text-xs text-slate-500 font-medium">
                      <span>{fileData.file.type.split('/')[1]?.toUpperCase() || 'FILE'}</span>
                      <span className="w-1 h-1 bg-slate-300 rounded-full" />
                      <span>{formatFileSize(fileData.file.size)}</span>
                    </div>
                    
                    {fileData.status === 'uploading' && (
                      <div className="mt-3">
                        <div className="progress-bar">
                          <div className="progress-fill" style={{ width: `${fileData.progress}%` }}></div>
                        </div>
                      </div>
                    )}
                    
                    {fileData.error && (
                      <p className="text-xs font-medium text-danger-600 mt-2">{fileData.error}</p>
                    )}
                  </div>
                  
                  {fileData.status === 'pending' && (
                    <button
                      onClick={() => removeFile(index)}
                      className="p-2 text-slate-400 hover:text-danger-500 hover:bg-danger-50 opacity-0 group-hover:opacity-100 rounded-lg transition-all"
                    >
                      <XMarkIcon className="h-5 w-5" />
                    </button>
                  )}
                </div>
              ))}
            </div>
            
            {files.some(f => f.status === 'pending') && (
              <div className="mt-6 flex justify-end">
                <button
                  onClick={uploadFiles}
                  disabled={uploading}
                  className="bg-slate-900 text-white py-3 px-6 rounded-xl font-semibold shadow-md shadow-slate-900/20 hover:bg-slate-800 hover:shadow-lg hover:-translate-y-0.5 focus:ring-2 focus:ring-offset-2 focus:ring-slate-900 disabled:opacity-70 disabled:transform-none transition-all duration-200 flex items-center"
                >
                  {uploading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white/50 border-t-white rounded-full animate-spin mr-3"></div>
                      Executing ML Pipeline
                    </>
                  ) : (
                    <>
                      <SparklesIcon className="h-5 w-5 mr-2" />
                      Verify {files.filter(f => f.status === 'pending').length} Document{files.length > 1 ? 's' : ''}
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Hero Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6">
          <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mb-4 border border-primary-200">
            <SparklesIcon className="h-6 w-6 text-primary-600" />
          </div>
          <h3 className="text-lg font-outfit font-bold text-slate-900 mb-2">AI Analysis</h3>
          <p className="text-sm text-slate-600 leading-relaxed font-medium">
            Advanced ML algorithms detect forged anomalies and manipulation instantly.
          </p>
        </div>
        
        <div className="glass-card p-6">
          <div className="w-12 h-12 bg-success-100 rounded-xl flex items-center justify-center mb-4 border border-success-200">
            <CheckCircleIcon className="h-6 w-6 text-success-600" />
          </div>
          <h3 className="text-lg font-outfit font-bold text-slate-900 mb-2">Instant Verification</h3>
          <p className="text-sm text-slate-600 leading-relaxed font-medium">
            Comprehensive trust scores and analysis generated under 30 seconds.
          </p>
        </div>
        
        <div className="glass-card p-6">
          <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mb-4 border border-indigo-200">
            <DocumentArrowUpIcon className="h-6 w-6 text-indigo-600" />
          </div>
          <h3 className="text-lg font-outfit font-bold text-slate-900 mb-2">Bulk Pipeline</h3>
          <p className="text-sm text-slate-600 leading-relaxed font-medium">
            Upload and process up to 100 documents simultaneously with concurrent workers.
          </p>
        </div>
      </div>
    </div>
  )
}