'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Menu, Transition } from '@headlessui/react'
import { Fragment } from 'react'
import { 
  UserCircleIcon, 
  Cog6ToothIcon, 
  ArrowRightOnRectangleIcon,
  BellIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline'

export default function Navbar() {
  const { user, logout } = useAuth()

  return (
    <nav className="sticky top-0 z-50 bg-white/70 backdrop-blur-lg border-b border-white/40 shadow-sm transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-[72px]">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center group">
              <div className="h-10 w-10 bg-gradient-to-br from-primary-600 to-indigo-800 rounded-xl flex items-center justify-center shadow-md shadow-primary-500/20 group-hover:shadow-glow-primary transition-all duration-300">
                <ShieldCheckIcon className="h-6 w-6 text-white" />
              </div>
              <div className="ml-3">
                <span className="text-xl font-outfit font-bold text-slate-900 tracking-tight">
                  Certify<span className="text-primary-600">AI</span>
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {/* Quick Stats */}
            <div className="hidden md:flex items-center space-x-6 mr-6 pointer-events-none">
              <div className="flex flex-col items-end">
                <div className="flex items-baseline space-x-1.5">
                  <span className="font-outfit font-semibold text-slate-900 text-lg leading-none">{user?.certificates_uploaded || 0}</span>
                  <span className="text-slate-500 text-xs font-medium uppercase tracking-wider">Uploaded</span>
                </div>
              </div>
              <div className="h-8 w-px bg-slate-200" />
              <div className="flex flex-col items-start">
                <div className="flex items-baseline space-x-1.5">
                  <span className="font-outfit font-semibold text-slate-900 text-lg leading-none">{user?.verifications_performed || 0}</span>
                  <span className="text-slate-500 text-xs font-medium uppercase tracking-wider">Verified</span>
                </div>
              </div>
            </div>

            {/* Notifications */}
            <button className="relative p-2.5 text-slate-400 hover:text-primary-600 hover:bg-primary-50/50 rounded-xl transition-all group">
              <BellIcon className="h-5 w-5 group-hover:-rotate-12 transition-transform" />
              <span className="absolute top-2 right-2.5 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
            </button>

            {/* User menu */}
            <Menu as="div" className="relative">
              <Menu.Button className="flex items-center space-x-3 rounded-xl p-2 pl-3 hover:bg-slate-50 border border-transparent hover:border-slate-100 transition-all focus:outline-none focus:ring-2 focus:ring-primary-500/20 group">
                <div className="hidden md:block text-right">
                  <div className="text-sm font-semibold text-slate-900 group-hover:text-primary-600 transition-colors">{user?.full_name}</div>
                  <div className="text-xs text-slate-500 font-medium">{user?.role?.charAt(0).toUpperCase() + user?.role?.slice(1)}</div>
                </div>
                <div className="h-9 w-9 bg-primary-100 text-primary-700 rounded-lg flex items-center justify-center font-bold font-outfit shadow-sm shadow-primary-500/10">
                  {user?.full_name?.charAt(0) || 'U'}
                </div>
              </Menu.Button>

              <Transition
                as={Fragment}
                enter="transition ease-out duration-200"
                enterFrom="transform opacity-0 scale-95 translate-y-2"
                enterTo="transform opacity-100 scale-100 translate-y-0"
                leave="transition ease-in duration-150"
                leaveFrom="transform opacity-100 scale-100 translate-y-0"
                leaveTo="transform opacity-0 scale-95 translate-y-2"
              >
                <Menu.Items className="absolute right-0 mt-3 w-64 rounded-2xl shadow-glass bg-white/90 backdrop-blur-xl ring-1 ring-slate-900/5 focus:outline-none z-50 overflow-hidden">
                  <div className="p-2">
                    <div className="px-4 py-3 bg-slate-50/50 rounded-xl mb-2">
                      <div className="text-sm font-semibold text-slate-900 truncate">{user?.full_name}</div>
                      <div className="text-xs text-slate-500 truncate mt-0.5">{user?.email}</div>
                      {user?.institution_name && (
                        <div className="mt-2 text-xs font-medium text-primary-600 bg-primary-50 inline-block px-2 py-1 rounded-md">
                          {user.institution_name}
                        </div>
                      )}
                    </div>
                    
                    <Menu.Item>
                      {({ active }) => (
                        <a
                          href="#"
                          className={`${
                            active ? 'bg-primary-50 text-primary-700' : 'text-slate-700'
                          } flex items-center px-4 py-2.5 text-sm font-medium rounded-xl transition-colors`}
                        >
                          <UserCircleIcon className={`mr-3 h-5 w-5 ${active ? 'text-primary-600' : 'text-slate-400'}`} />
                          Profile Settings
                        </a>
                      )}
                    </Menu.Item>
                    <Menu.Item>
                      {({ active }) => (
                        <a
                          href="#"
                          className={`${
                            active ? 'bg-primary-50 text-primary-700' : 'text-slate-700'
                          } flex items-center px-4 py-2.5 text-sm font-medium rounded-xl transition-colors mb-1`}
                        >
                          <Cog6ToothIcon className={`mr-3 h-5 w-5 ${active ? 'text-primary-600' : 'text-slate-400'}`} />
                          Preferences
                        </a>
                      )}
                    </Menu.Item>
                    <div className="h-px bg-slate-100 my-1"></div>
                    <Menu.Item>
                      {({ active }) => (
                        <button
                          onClick={logout}
                          className={`${
                            active ? 'bg-red-50 text-red-700' : 'text-slate-700'
                          } flex items-center w-full px-4 py-2.5 text-sm font-medium rounded-xl transition-colors`}
                        >
                          <ArrowRightOnRectangleIcon className={`mr-3 h-5 w-5 ${active ? 'text-red-500' : 'text-slate-400'}`} />
                          Sign out
                        </button>
                      )}
                    </Menu.Item>
                  </div>
                </Menu.Items>
              </Transition>
            </Menu>
          </div>
        </div>
      </div>
    </nav>
  )
}