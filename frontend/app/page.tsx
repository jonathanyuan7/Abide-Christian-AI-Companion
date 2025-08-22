'use client'

import { useState } from 'react'
import { Header } from '@/components/Header'
import { FeelingInput } from '@/components/FeelingInput'
import { ResponseDisplay } from '@/components/ResponseDisplay'
import { DevotionGenerator } from '@/components/DevotionGenerator'
import { CrisisBanner } from '@/components/CrisisBanner'
import { useToast } from '@/hooks/use-toast'

export default function HomePage() {
  const [response, setResponse] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [showDevotion, setShowDevotion] = useState(false)
  const { toast } = useToast()

  const handleFeelingSubmit = async (text: string) => {
    setLoading(true)
    try {
      const res = await fetch('/api/feel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      })

      if (!res.ok) {
        throw new Error('Failed to get response')
      }

      const data = await res.json()
      setResponse(data)
      setShowDevotion(false)
      
      toast({
        title: "Response received",
        description: "Here's your personalized spiritual guidance.",
      })
    } catch (error) {
      console.error('Error:', error)
      toast({
        title: "Error",
        description: "Failed to get response. Please try again.",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const handleDevotionGenerate = async (theme?: string) => {
    setLoading(true)
    try {
      const res = await fetch('/api/devotion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ theme }),
      })

      if (!res.ok) {
        throw new Error('Failed to generate devotion')
      }

      const data = await res.json()
      setResponse(data)
      setShowDevotion(true)
      
      toast({
        title: "Devotion generated",
        description: "Your 10-minute devotion plan is ready.",
      })
    } catch (error) {
      console.error('Error:', error)
      toast({
        title: "Error",
        description: "Failed to generate devotion. Please try again.",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Hero Section */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white">
              Abide
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300">
              Your gentle Christian AI companion
            </p>
            <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
              Share how you're feeling and receive relevant Bible verses, 
              pastoral reflection, and prayer. Find peace and guidance in God's Word.
            </p>
          </div>

          {/* Main Input Section */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 md:p-8">
            <FeelingInput 
              onSubmit={handleFeelingSubmit}
              loading={loading}
            />
          </div>

          {/* Quick Devotion Generator */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 md:p-8">
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
              Need a devotion?
            </h2>
            <DevotionGenerator 
              onGenerate={handleDevotionGenerate}
              loading={loading}
            />
          </div>

          {/* Response Display */}
          {response && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 md:p-8">
              {response.crisis_detected ? (
                <CrisisBanner 
                  message={response.message}
                  supportiveVerses={response.supportive_verses}
                  prayer={response.prayer}
                  resources={response.resources}
                />
              ) : (
                <ResponseDisplay 
                  response={response}
                  isDevotion={showDevotion}
                />
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
