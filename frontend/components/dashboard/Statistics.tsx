'use client'

import { ChartBarIcon, DocumentTextIcon, CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface StatisticsProps {
  stats: any
  loading: boolean
}

export default function Statistics({ stats, loading }: StatisticsProps) {
  if (loading) {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <div className="animate-pulse">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-8 h-8 bg-slate-200 rounded-md"></div>
              <div>
                <div className="h-5 bg-slate-200 rounded w-48 mb-2"></div>
                <div className="h-4 bg-slate-200 rounded w-32"></div>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                  <div className="animate-pulse">
                    <div className="flex items-center justify-between mb-3">
                      <div className="w-12 h-12 bg-slate-200 rounded-lg"></div>
                      <div className="h-6 bg-slate-200 rounded w-12"></div>
                    </div>
                    <div className="h-4 bg-slate-200 rounded w-3/4"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12">
        <div className="text-center">
          <div className="w-16 h-16 bg-slate-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <ChartBarIcon className="h-8 w-8 text-slate-400" />
          </div>
          <h3 className="text-lg font-semibold text-slate-900 mb-2">No statistics available</h3>
          <p className="text-slate-500 max-w-sm mx-auto">
            Upload some certificates to see detailed verification statistics and insights.
          </p>
        </div>
      </div>
    )
  }

  const statsData = {
    total: stats.total_processed || 0,
    valid: stats.valid_count || 0,
    suspicious: stats.suspicious_count || 0,
    fake: stats.fake_count || 0,
    pending: stats.pending_count || 0,
    avgTrustScore: stats.average_trust_score || 0,
    avgProcessingTime: stats.average_processing_time || 0
  }

  const statCards = [
    {
      title: 'Total Certificates',
      value: statsData.total,
      icon: DocumentTextIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Valid Certificates',
      value: statsData.valid,
      icon: CheckCircleIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Suspicious/Fake',
      value: statsData.suspicious + statsData.fake,
      icon: ExclamationTriangleIcon,
      color: 'text-red-600',
      bgColor: 'bg-red-100'
    },
    {
      title: 'Avg Trust Score',
      value: `${(statsData.avgTrustScore || 0).toFixed(1)}%`,
      icon: ChartBarIcon,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    }
  ]

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-8 h-8 bg-slate-900 rounded-md flex items-center justify-center">
            <ChartBarIcon className="h-5 w-5 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Verification Statistics
            </h2>
            <p className="text-slate-600 text-sm">
              Last {stats.period_days} days overview
            </p>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {statCards.map((stat, index) => (
            <div key={index} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
              <div className="flex items-center justify-between mb-3">
                <div className={`${stat.bgColor} rounded-lg p-3`}>
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="text-right">
                  <p className="text-2xl font-semibold text-slate-900">{stat.value}</p>
                </div>
              </div>
              <p className="text-sm font-medium text-slate-600">{stat.title}</p>
            </div>
          ))}
        </div>

        {/* Detailed Breakdown */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Status Breakdown */}
          <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
            <h3 className="text-base font-semibold text-slate-900 mb-4 flex items-center">
              <div className="w-6 h-6 bg-blue-100 rounded-md flex items-center justify-center mr-2">
                <DocumentTextIcon className="h-4 w-4 text-blue-600" />
              </div>
              Status Breakdown
            </h3>
            <div className="space-y-3">
              {Object.entries(stats.statistics_by_status || {}).map(([status, data]: [string, any]) => (
                <div key={status} className="flex items-center justify-between p-3 bg-white rounded-md border border-slate-100">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full mr-3 ${
                      status === 'valid' ? 'bg-green-500' :
                      status === 'suspicious' ? 'bg-yellow-500' :
                      status === 'fake' ? 'bg-red-500' : 'bg-slate-500'
                    }`}></div>
                    <span className="text-sm font-medium text-slate-700 capitalize">{status}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-base font-semibold text-slate-900">{data.count}</div>
                    <div className="text-xs text-slate-500">
                      {data.average_trust_score ? `${data.average_trust_score.toFixed(1)}% avg` : 'No data'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
            <h3 className="text-base font-semibold text-slate-900 mb-4 flex items-center">
              <div className="w-6 h-6 bg-purple-100 rounded-md flex items-center justify-center mr-2">
                <ChartBarIcon className="h-4 w-4 text-purple-600" />
              </div>
              Performance Metrics
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-white rounded-md border border-slate-100">
                <span className="text-sm font-medium text-slate-700">Avg Processing Time</span>
                <span className="text-base font-semibold text-slate-900">
                  {(statsData.avgProcessingTime || 0).toFixed(1)}s
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-white rounded-md border border-slate-100">
                <span className="text-sm font-medium text-slate-700">Verification Rate</span>
                <span className="text-base font-semibold text-green-600">
                  {statsData.total > 0 ? (((statsData.total - statsData.pending) / statsData.total * 100).toFixed(1)) : 0}%
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-white rounded-md border border-slate-100">
                <span className="text-sm font-medium text-slate-700">Fraud Detection Rate</span>
                <span className="text-base font-semibold text-red-600">
                  {statsData.total > 0 ? (((statsData.suspicious + statsData.fake) / statsData.total * 100).toFixed(1)) : 0}%
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Generated timestamp */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center px-3 py-1.5 bg-slate-100 rounded-md">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
            <span className="text-xs text-slate-600 font-medium">
              Last updated: {new Date(stats.generated_at).toLocaleString()}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}