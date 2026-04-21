'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import Navbar from './Navbar'
import Sidebar from './Sidebar'
import UploadSection from './UploadSection'
import CertificatesList from './CertificatesList'
import Statistics from './Statistics'
import { certificateAPI } from '@/lib/api'

export default function Dashboard() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('upload')
  const [certificates, setCertificates] = useState([])
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)

  useEffect(() => {
    if (activeTab === 'certificates') {
      loadCertificates()
    } else if (activeTab === 'statistics') {
      loadStatistics()
    }
  }, [activeTab])

  const loadCertificates = async () => {
    setLoading(true)
    try {
      const response = await certificateAPI.getCertificates({ limit: 50 })
      setCertificates(response.data)
    } catch (error) {
      console.error('Failed to load certificates:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadStatistics = async () => {
    setLoading(true)
    try {
      const response = await certificateAPI.getStatistics(30)
      setStats(response.data)
    } catch (error) {
      console.error('Failed to load statistics:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleUploadSuccess = () => {
    if (activeTab === 'certificates') {
      loadCertificates()
    }
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'upload':
        return <UploadSection onUploadSuccess={handleUploadSuccess} />
      case 'certificates':
        return (
          <CertificatesList 
            certificates={certificates} 
            loading={loading}
            onRefresh={loadCertificates}
          />
        )
      case 'statistics':
        return <Statistics stats={stats} loading={loading} />
      default:
        return <UploadSection onUploadSuccess={handleUploadSuccess} />
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 relative">
      <div className="absolute top-0 right-0 w-[800px] h-[600px] bg-primary-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50 pointer-events-none -translate-y-1/2 translate-x-1/3" />
      <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-indigo-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50 pointer-events-none translate-y-1/2 -translate-x-1/4" />

      <Navbar />
      
      <div className="max-w-[1600px] mx-auto flex z-10 relative">
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
        
        <main className="flex-1 p-6 lg:p-10 min-h-[calc(100vh-72px)] overflow-x-hidden">
          <div className="max-w-6xl mx-auto space-y-6">
            <div className="mb-8 animate-slide-up">
              <h1 className="text-3xl font-outfit font-bold text-slate-900 tracking-tight">
                Welcome back, <span className="text-primary-600">{user?.full_name?.split(' ')[0]}</span>
              </h1>
              <p className="text-slate-500 font-medium py-1">
                {user?.institution_name && `${user.institution_name} • `}
                {user?.role?.charAt(0).toUpperCase() + user?.role?.slice(1)} Workspace
              </p>
            </div>
            
            <div className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
              {renderContent()}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}