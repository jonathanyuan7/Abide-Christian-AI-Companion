'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Clock, BookOpen, Loader2 } from 'lucide-react'

interface DevotionGeneratorProps {
  onGenerate: (theme?: string) => void
  loading: boolean
}

const devotionThemes = [
  { id: 'peace', name: 'Peace', emoji: '🕊️', description: 'Find inner calm and tranquility' },
  { id: 'hope', name: 'Hope', emoji: '🌟', description: 'Discover renewed optimism and faith' },
  { id: 'comfort', name: 'Comfort', emoji: '🤗', description: 'Receive solace and encouragement' },
  { id: 'strength', name: 'Strength', emoji: '💪', description: 'Build resilience and courage' },
  { id: 'love', name: 'Love', emoji: '❤️', description: 'Experience God\'s unconditional love' },
  { id: 'gratitude', name: 'Gratitude', emoji: '🙏', description: 'Cultivate thankfulness and joy' },
]

export function DevotionGenerator({ onGenerate, loading }: DevotionGeneratorProps) {
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null)

  const handleGenerate = () => {
    onGenerate(selectedTheme || undefined)
  }

  const handleRandomGenerate = () => {
    const randomTheme = devotionThemes[Math.floor(Math.random() * devotionThemes.length)]
    onGenerate(randomTheme.id)
  }

  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <p className="text-gray-600 dark:text-gray-400">
          Get a structured 10-minute devotion plan with scripture, reflection, and action steps
        </p>
      </div>

      {/* Theme Selection */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {devotionThemes.map((theme) => (
          <button
            key={theme.id}
            onClick={() => setSelectedTheme(theme.id)}
            className={`p-4 rounded-xl border-2 transition-all duration-200 text-center hover:shadow-md ${
              selectedTheme === theme.id
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
            }`}
          >
            <div className="text-2xl mb-2">{theme.emoji}</div>
            <div className="font-medium text-gray-900 dark:text-white">
              {theme.name}
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {theme.description}
            </div>
          </button>
        ))}
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3 justify-center">
        <Button
          onClick={handleGenerate}
          disabled={loading}
          size="lg"
          className="flex-1 sm:flex-none px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white shadow-lg hover:shadow-xl transition-all duration-200"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <BookOpen className="w-5 h-5 mr-2" />
              Generate Devotion
            </>
          )}
        </Button>

        <Button
          onClick={handleRandomGenerate}
          disabled={loading}
          variant="outline"
          size="lg"
          className="flex-1 sm:flex-none px-6 py-3 border-2 border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 transition-all duration-200"
        >
          <Clock className="w-5 h-5 mr-2" />
          Surprise Me
        </Button>
      </div>

      {/* Info */}
      <div className="text-center text-sm text-gray-500 dark:text-gray-400 space-y-1">
        <p>⏱️ Each devotion takes approximately 10 minutes</p>
        <p>📖 Includes scripture, reflection, prayer, and action steps</p>
        <p>🎵 Plus a relevant YouTube video for worship or learning</p>
      </div>
    </div>
  )
}
