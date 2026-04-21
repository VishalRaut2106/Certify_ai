import type { Metadata } from 'next'
import { Inter, Outfit } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '../contexts/AuthContext'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const outfit = Outfit({ subsets: ['latin'], variable: '--font-outfit' })

export const metadata: Metadata = {
  title: 'CertifyAI • Premium Verification System',
  description: 'AI-powered bulk certificate verification system with zero fraud tolerance.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${outfit.variable} font-sans bg-slate-50 text-slate-900 antialiased selection:bg-indigo-500 selection:text-white`}>
        <AuthProvider>
          {children}
          <Toaster 
            position="top-right"
            toastOptions={{
              className: 'font-inter text-sm shadow-xl border border-slate-100 rounded-xl',
              duration: 4000,
            }} 
          />
        </AuthProvider>
      </body>
    </html>
  )
}