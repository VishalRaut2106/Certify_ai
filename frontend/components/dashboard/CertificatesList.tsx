'use client'

import { useState } from 'react'
import { 
  DocumentTextIcon, 
  EyeIcon, 
  TrashIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import { certificateAPI } from '@/lib/api'
import toast from 'react-hot-toast'

interface Certificate {
  id: string
  file_name: string
  file_type: string
  file_size: number
  status: string
  trust_score?: number | null
  upload_date: string
}

interface CertificatesListProps {
  certificates: Certificate[]
  loading: boolean
  onRefresh: () => void
}

export default function CertificatesList({ certificates, loading, onRefresh }: CertificatesListProps) {
  const [filter, setFilter] = useState('all')
  const [deleting, setDeleting] = useState<string | null>(null)

  const getStatusBadge = (status: string) => {
    const baseClasses = "inline-flex items-center px-2 py-1 rounded text-xs font-medium"
    
    switch (status) {
      case 'valid':
        return <span className={`${baseClasses} bg-green-100 text-green-800`}>✅ Valid</span>
      case 'suspicious':
        return <span className={`${baseClasses} bg-yellow-100 text-yellow-800`}>⚠️ Suspicious</span>
      case 'fake':
        return <span className={`${baseClasses} bg-red-100 text-red-800`}>❌ Fake</span>
      case 'pending':
        return <span className={`${baseClasses} bg-blue-100 text-blue-800`}>⏳ Pending</span>
      default:
        return <span className={`${baseClasses} bg-slate-100 text-slate-800`}>⏳ Processing</span>
    }
  }

  const getTrustScoreColor = (score?: number | null) => {
    if (!score || score === null) return 'text-slate-500'
    if (score >= 85) return 'text-green-600'
    if (score >= 30) return 'text-yellow-600'
    return 'text-red-600'
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleDelete = async (certificateId: string) => {
    if (!confirm('Are you sure you want to delete this certificate?')) return
    
    setDeleting(certificateId)
    try {
      await certificateAPI.deleteCertificate(certificateId)
      toast.success('Certificate deleted successfully')
      onRefresh()
    } catch (error) {
      toast.error('Failed to delete certificate')
    } finally {
      setDeleting(null)
    }
  }

  const filteredCertificates = certificates.filter(cert => {
    if (filter === 'all') return true
    return cert.status === filter
  })

  const statusCounts = {
    all: certificates.length,
    valid: certificates.filter(c => c.status === 'valid').length,
    suspicious: certificates.filter(c => c.status === 'suspicious').length,
    fake: certificates.filter(c => c.status === 'fake').length,
    pending: certificates.filter(c => c.status === 'pending').length,
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
        <div className="animate-pulse">
          <div className="flex items-center justify-between mb-6">
            <div>
              <div className="h-5 bg-slate-200 rounded w-48 mb-2"></div>
              <div className="h-4 bg-slate-200 rounded w-64"></div>
            </div>
            <div className="h-8 bg-slate-200 rounded w-20"></div>
          </div>
          <div className="space-y-4">
            <div className="flex space-x-6 border-b border-slate-200 pb-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-6 bg-slate-200 rounded w-16"></div>
              ))}
            </div>
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="border border-slate-200 rounded-lg p-4">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-slate-200 rounded-lg"></div>
                    <div className="flex-1">
                      <div className="h-4 bg-slate-200 rounded w-3/4 mb-2"></div>
                      <div className="h-3 bg-slate-200 rounded w-1/2"></div>
                    </div>
                    <div className="w-16 h-12 bg-slate-200 rounded"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">My Certificates</h2>
            <p className="text-slate-600 text-sm mt-1">Manage and track your certificate verification status</p>
          </div>
          <button
            onClick={onRefresh}
            className="inline-flex items-center px-3 py-2 bg-slate-100 border border-slate-300 text-sm font-medium rounded-md text-slate-700 hover:bg-slate-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 transition-colors"
          >
            <ArrowPathIcon className="h-4 w-4 mr-2" />
            Refresh
          </button>
        </div>

        {/* Filter Tabs */}
        <div className="border-b border-slate-200 mb-6">
          <nav className="-mb-px flex space-x-6">
            {[
              { key: 'all', label: 'All', count: statusCounts.all },
              { key: 'valid', label: 'Valid', count: statusCounts.valid },
              { key: 'suspicious', label: 'Suspicious', count: statusCounts.suspicious },
              { key: 'fake', label: 'Fake', count: statusCounts.fake },
              { key: 'pending', label: 'Pending', count: statusCounts.pending },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setFilter(tab.key)}
                className={`${
                  filter === tab.key
                    ? 'border-slate-500 text-slate-900 bg-slate-50'
                    : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 hover:bg-slate-50'
                } whitespace-nowrap py-2 px-3 border-b-2 font-medium text-sm rounded-t-md transition-all`}
              >
                {tab.label}
                {tab.count > 0 && (
                  <span className={`${
                    filter === tab.key ? 'bg-slate-200 text-slate-800' : 'bg-slate-100 text-slate-600'
                  } ml-2 py-0.5 px-2 rounded-full text-xs font-medium`}>
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>

        {/* Certificates List */}
        {filteredCertificates.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-slate-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <DocumentTextIcon className="h-8 w-8 text-slate-400" />
            </div>
            <h3 className="text-base font-semibold text-slate-900 mb-2">No certificates found</h3>
            <p className="text-slate-500 max-w-sm mx-auto text-sm">
              {filter === 'all' ? 'Upload some certificates to get started with AI-powered verification.' : `No ${filter} certificates found. Try a different filter.`}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredCertificates.map((certificate) => (
              <div key={certificate.id} className="border border-slate-200 rounded-lg p-4 hover:bg-slate-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4 flex-1">
                    <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <DocumentTextIcon className="h-5 w-5 text-slate-600" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-3 mb-1">
                        <p className="text-sm font-medium text-slate-900 truncate">
                          {certificate.file_name}
                        </p>
                        {getStatusBadge(certificate.status)}
                      </div>
                      
                      <div className="flex items-center space-x-4 text-xs text-slate-500">
                        <span className="px-2 py-0.5 bg-slate-100 rounded font-medium text-slate-600">
                          {certificate.file_type.toUpperCase()}
                        </span>
                        <span>{formatFileSize(certificate.file_size)}</span>
                        <span>{formatDate(certificate.upload_date)}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    {certificate.trust_score !== undefined && certificate.trust_score !== null && (
                      <div className="text-right bg-slate-50 rounded-md p-2">
                        <div className={`text-lg font-semibold ${getTrustScoreColor(certificate.trust_score)}`}>
                          {certificate.trust_score.toFixed(1)}%
                        </div>
                        <div className="text-xs text-slate-500 font-medium">Trust Score</div>
                      </div>
                    )}
                    
                    <div className="flex items-center space-x-1">
                      <button
                        className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-md transition-colors"
                        title="View Details"
                      >
                        <EyeIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(certificate.id)}
                        disabled={deleting === certificate.id}
                        className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 disabled:opacity-50 rounded-md transition-colors"
                        title="Delete"
                      >
                        {deleting === certificate.id ? (
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-600"></div>
                        ) : (
                          <TrashIcon className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}