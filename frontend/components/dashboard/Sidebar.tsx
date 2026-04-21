'use client'

import { 
  CloudArrowUpIcon, 
  DocumentTextIcon, 
  ChartBarIcon
} from '@heroicons/react/24/outline'

interface SidebarProps {
  activeTab: string
  onTabChange: (tab: string) => void
}

const navigation = [
  { 
    name: 'Upload', 
    id: 'upload', 
    icon: CloudArrowUpIcon,
    description: 'Bulk verification'
  },
  { 
    name: 'Certificates', 
    id: 'certificates', 
    icon: DocumentTextIcon,
    description: 'View dashboard'
  },
  { 
    name: 'Analytics', 
    id: 'statistics', 
    icon: ChartBarIcon,
    description: 'Insights & data'
  },
]

export default function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  return (
    <div className="w-72 bg-white/50 backdrop-blur-sm border-r border-slate-200/60 min-h-[calc(100vh-72px)] flex flex-col">
      <div className="flex-1 px-4 py-8 space-y-8">
        
        <div>
          <h3 className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">
            Main Menu
          </h3>
          <nav className="space-y-2">
            {navigation.map((item) => {
              const isActive = activeTab === item.id
              return (
                <button
                  key={item.id}
                  onClick={() => onTabChange(item.id)}
                  className={`
                    group flex items-center w-full p-3 font-medium rounded-xl transition-all duration-300 relative overflow-hidden
                    ${isActive 
                      ? 'bg-primary-50 text-primary-700 shadow-sm shadow-primary-500/10' 
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900 border-transparent'}
                  `}
                >
                  {isActive && (
                    <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1.5 h-8 bg-primary-600 rounded-r-md"></span>
                  )}
                  
                  <div className={`p-2 rounded-lg mr-3 transition-colors ${isActive ? 'bg-primary-100' : 'bg-slate-100 group-hover:bg-white border border-transparent group-hover:border-slate-200'}`}>
                    <item.icon
                      className={`h-5 w-5 transition-transform ${
                        isActive ? 'text-primary-700 scale-110' : 'text-slate-500 group-hover:text-slate-700'
                      }`}
                    />
                  </div>
                  
                  <div className="text-left">
                    <div className="text-sm font-semibold">{item.name}</div>
                    <div className={`text-[11px] mt-0.5 font-medium ${
                      isActive ? 'text-primary-600/80' : 'text-slate-500'
                    }`}>
                      {item.description}
                    </div>
                  </div>
                </button>
              )
            })}
          </nav>
        </div>

      </div>

      {/* System Info Banner */}
      <div className="p-4 mx-4 mb-6 relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 to-indigo-900 text-white shadow-xl">
        <div className="absolute top-0 right-0 w-24 h-24 bg-primary-500 opacity-20 blur-2xl rounded-full" />
        <div className="relative z-10">
          <div className="flex items-center space-x-2 mb-3">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            <span className="text-xs font-semibold uppercase tracking-wider text-green-400">System Online</span>
          </div>
          <p className="text-sm font-medium mb-1 line-clamp-1">AI Engine v2.4 Active</p>
          <p className="text-xs text-slate-300 font-light">Processing verifications at 99.5% accuracy with zero down-time.</p>
        </div>
      </div>
    </div>
  )
}