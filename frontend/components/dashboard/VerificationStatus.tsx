'use client'

import { useState, useEffect } from 'react'
import { CheckCircleIcon, ClockIcon, ExclamationTriangleIcon, XCircleIcon } from '@heroicons/react/24/outline'

interface VerificationStatusProps {
  status: string
  trustScore?: number | null
  processingTime?: number | null
  showDetails?: boolean
}

export default function VerificationStatus({ 
  status, 
  trustScore, 
  processingTime, 
  showDetails = false 
}: VerificationStatusProps) {
  const [isAnimating, setIsAnimating] = useState(false)

  useEffect(() => {
    if (status === 'processing') {
      setIsAnimating(true)
    } else {
      setIsAnimating(false)
    }
  }, [status])

  const getStatusConfig = () => {
    switch (status) {
      case 'valid':
        return {
          icon: CheckCircleIcon,
          label: 'Valid Certificate',
          color: 'text-green-600',
          bgColor: 'bg-green-100',
          borderColor: 'border-green-200',
          description: 'AI verification confirms this certificate is authentic'
        }
      case 'suspicious':
        return {
          icon: ExclamationTriangleIcon,
          label: 'Suspicious Certificate',
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-100',
          borderColor: 'border-yellow-200',
          description: 'AI detected potential authenticity issues'
        }
      case 'fake':
        return {
          icon: XCircleIcon,
          label: 'Fake Certificate',
          color: 'text-red-600',
          bgColor: 'bg-red-100',
          borderColor: 'border-red-200',
          description: 'AI verification indicates this certificate is not authentic'
        }
      case 'processing':
        return {
          icon: ClockIcon,
          label: 'AI Verification in Progress',
          color: 'text-blue-600',
          bgColor: 'bg-blue-100',
          borderColor: 'border-blue-200',
          description: 'AI is analyzing the certificate using OCR, QR detection, and fraud patterns'
        }
      case 'pending':
        return {
          icon: ClockIcon,
          label: 'Queued for Verification',
          color: 'text-slate-600',
          bgColor: 'bg-slate-100',
          borderColor: 'border-slate-200',
          description: 'Certificate is queued for AI verification'
        }
      default:
        return {
          icon: ClockIcon,
          label: 'Unknown Status',
          color: 'text-slate-600',
          bgColor: 'bg-slate-100',
          borderColor: 'border-slate-200',
          description: 'Verification status unknown'
        }
    }
  }

  const config = getStatusConfig()
  const IconComponent = config.icon

  return (
    <div className={`rounded-lg border p-3 ${config.bgColor} ${config.borderColor}`}>
      <div className="flex items-center space-x-3">
        <div className={`flex-shrink-0 ${isAnimating ? 'animate-spin' : ''}`}>
          <IconComponent className={`h-5 w-5 ${config.color}`} />
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2">
            <p className={`text-sm font-medium ${config.color}`}>
              {config.label}
            </p>
            
            {trustScore !== null && trustScore !== undefined && (
              <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                trustScore >= 85 ? 'bg-green-200 text-green-800' :
                trustScore >= 30 ? 'bg-yellow-200 text-yellow-800' :
                'bg-red-200 text-red-800'
              }`}>
                {trustScore.toFixed(1)}% Trust
              </span>
            )}
            
            {processingTime && (
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-200 text-slate-700">
                ⚡ {processingTime.toFixed(1)}s
              </span>
            )}
          </div>
          
          {showDetails && (
            <p className="text-xs text-slate-600 mt-1">
              {config.description}
            </p>
          )}
        </div>
      </div>
      
      {status === 'processing' && (
        <div className="mt-2">
          <div className="w-full bg-slate-200 rounded-full h-1.5">
            <div className="bg-blue-600 h-1.5 rounded-full animate-pulse" style={{ width: '60%' }}></div>
          </div>
          <p className="text-xs text-slate-600 mt-1">
            AI analyzing: OCR extraction, QR validation, fraud detection...
          </p>
        </div>
      )}
    </div>
  )
}