'use client'

import { useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { EyeIcon, EyeSlashIcon, ShieldCheckIcon, SparklesIcon } from '@heroicons/react/24/outline'

export default function LoginForm() {
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    institution_name: '',
    role: 'teacher'
  })

  const { login, register } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (isLogin) {
        await login(formData.email, formData.password)
      } else {
        const success = await register({
          email: formData.email,
          password: formData.password,
          full_name: formData.full_name,
          institution_name: formData.institution_name,
          role: formData.role
        })
        if (success) {
          setIsLogin(true)
          setFormData({ ...formData, password: '' })
        }
      }
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="min-h-screen bg-slate-50 relative overflow-hidden flex items-center justify-center">
      {/* Background decorations */}
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-float" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-float" style={{ animationDelay: '2s' }} />
      <div className="absolute top-[20%] right-[10%] w-[30%] h-[30%] bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-float" style={{ animationDelay: '4s' }} />

      <div className="relative w-full max-w-5xl px-4 sm:px-6 lg:px-8 flex items-center justify-center animate-fade-in">
        <div className="w-full grid lg:grid-cols-2 bg-white/40 backdrop-blur-xl border border-white/60 shadow-[0_8px_40px_-12px_rgba(0,0,0,0.1)] rounded-[2rem] overflow-hidden">
          
          {/* Brand/Hero Section */}
          <div className="hidden lg:flex flex-col justify-between bg-gradient-to-br from-primary-600 to-indigo-900 p-12 text-white relative overflow-hidden">
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10" />
            <div className="relative z-10">
              <div className="flex items-center space-x-3 mb-16">
                <div className="h-12 w-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center border border-white/30">
                  <ShieldCheckIcon className="h-7 w-7 text-white" />
                </div>
                <span className="text-2xl font-outfit font-bold tracking-tight">CertifyAI</span>
              </div>
              
              <h1 className="text-4xl lg:text-5xl font-outfit font-bold leading-tight mb-6">
                Zero Fraud.<br/>
                <span className="text-primary-200">Absolute Trust.</span>
              </h1>
              <p className="text-indigo-100/80 text-lg max-w-md font-light leading-relaxed">
                Empower your institution with AI-driven, multi-layered certificate verification that scales effortlessly.
              </p>
            </div>
            
            <div className="relative z-10">
              <div className="flex items-center space-x-4 bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10">
                <div className="h-10 w-10 bg-primary-500/30 rounded-full flex items-center justify-center">
                  <SparklesIcon className="h-5 w-5 text-primary-200 animate-pulse-slow" />
                </div>
                <div>
                  <p className="text-sm font-medium text-white">AI Engine Active</p>
                  <p className="text-xs text-indigo-200">Processing with 99.5% accuracy</p>
                </div>
              </div>
            </div>
          </div>

          {/* Form Section */}
          <div className="p-8 sm:p-12 lg:p-16 flex flex-col justify-center bg-white/60">
            <div className="mb-10 lg:hidden flex justify-center">
              <div className="h-16 w-16 bg-primary-600 rounded-2xl flex items-center justify-center shadow-lg shadow-primary-500/30">
                <ShieldCheckIcon className="h-8 w-8 text-white" />
              </div>
            </div>

            <h2 className="text-3xl font-outfit font-bold text-slate-900 mb-2">
              {isLogin ? 'Welcome back' : 'Get started'}
            </h2>
            <p className="text-slate-500 font-medium mb-8">
              {isLogin ? 'Please enter your details to sign in.' : 'Create an account to verify certificates limitlessly.'}
            </p>

            <form className="space-y-5" onSubmit={handleSubmit}>
              {!isLogin && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-slide-up">
                  <div>
                    <label htmlFor="full_name" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                      Full Name
                    </label>
                    <input
                      id="full_name"
                      name="full_name"
                      type="text"
                      required={!isLogin}
                      value={formData.full_name}
                      onChange={handleChange}
                      className="glass-input w-full px-4 py-3 text-sm placeholder:text-slate-400"
                      placeholder="John Doe"
                    />
                  </div>

                  <div>
                    <label htmlFor="institution_name" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                      Institution
                    </label>
                    <input
                      id="institution_name"
                      name="institution_name"
                      type="text"
                      value={formData.institution_name}
                      onChange={handleChange}
                      className="glass-input w-full px-4 py-3 text-sm placeholder:text-slate-400"
                      placeholder="University Name"
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label htmlFor="role" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                      Role
                    </label>
                    <select
                      id="role"
                      name="role"
                      value={formData.role}
                      onChange={handleChange}
                      className="glass-input w-full px-4 py-3 text-sm text-slate-700"
                    >
                      <option value="teacher">Teacher</option>
                      <option value="admin">Administrator</option>
                      <option value="evaluator">Evaluator</option>
                    </select>
                  </div>
                </div>
              )}

              <div className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
                <label htmlFor="email" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                  Email Address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-sm placeholder:text-slate-400"
                  placeholder="name@example.com"
                />
              </div>

              <div className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
                <label htmlFor="password" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                  Password
                </label>
                <div className="relative">
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete={isLogin ? 'current-password' : 'new-password'}
                    required
                    value={formData.password}
                    onChange={handleChange}
                    className="glass-input w-full px-4 py-3 pr-12 text-sm placeholder:text-slate-400"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-4 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeSlashIcon className="h-5 w-5 text-slate-400 hover:text-slate-600 transition-colors" />
                    ) : (
                      <EyeIcon className="h-5 w-5 text-slate-400 hover:text-slate-600 transition-colors" />
                    )}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-primary-600 text-white py-3.5 px-4 rounded-xl font-semibold hover:bg-primary-700 hover:shadow-glow-primary hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none transition-all duration-200 mt-6 animate-slide-up"
                style={{ animationDelay: '0.3s' }}
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    {isLogin ? 'Signing in...' : 'Creating account...'}
                  </div>
                ) : (
                  isLogin ? 'Sign In' : 'Create Account'
                )}
              </button>

              <div className="text-center mt-8 animate-slide-up" style={{ animationDelay: '0.4s' }}>
                <p className="text-sm text-slate-500">
                  {isLogin ? "Don't have an account? " : 'Already have an account? '}
                  <button
                    type="button"
                    onClick={() => setIsLogin(!isLogin)}
                    className="font-semibold text-primary-600 hover:text-primary-500 transition-colors"
                  >
                    {isLogin ? 'Sign up' : 'Sign in'}
                  </button>
                </p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}