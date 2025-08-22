'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Send, Loader2 } from 'lucide-react'

interface FeelingInputProps {
  onSubmit: (text: string) => void
  loading: boolean
}

const quickFeelings = [
  'anxious', 'lonely', 'overwhelmed', 'grateful', 'peaceful',
  'hopeful', 'stressed', 'joyful', 'sad', 'angry',
  'confused', 'excited', 'tired', 'inspired', 'worried'
]

export function FeelingInput({ onSubmit, loading }: FeelingInputProps) {
  const [text, setText] = useState('')
  const [selectedChips, setSelectedChips] = useState<string[]>([])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (text.trim() || selectedChips.length > 0) {
      const fullText = selectedChips.length > 0 
        ? `${text} ${selectedChips.join(', ')}`.trim()
        : text.trim()
      onSubmit(fullText)
      setText('')
      setSelectedChips([])
    }
  }

  const toggleChip = (feeling: string) => {
    setSelectedChips(prev => 
      prev.includes(feeling)
        ? prev.filter(f => f !== feeling)
        : [...prev, feeling]
    )
  }

  const addChipToText = (feeling: string) => {
    if (!text.includes(feeling)) {
      setText(prev => prev ? `${prev} ${feeling}` : feeling)
    }
  }

  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
          How are you feeling today?
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Share your heart and receive personalized spiritual guidance
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-3">
          <Textarea
            placeholder="Tell me how you're feeling... (e.g., 'I feel anxious about my upcoming presentation and need some peace')"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="min-h-[120px] resize-none text-lg"
            disabled={loading}
          />
          
          <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
            <span>Or choose from common feelings:</span>
            <span>{selectedChips.length} selected</span>
          </div>
        </div>

        {/* Quick Select Chips */}
        <div className="flex flex-wrap gap-2">
          {quickFeelings.map((feeling) => (
            <button
              key={feeling}
              type="button"
              onClick={() => toggleChip(feeling)}
              className={`px-3 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                selectedChips.includes(feeling)
                  ? 'bg-blue-500 text-white shadow-md'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {feeling}
            </button>
          ))}
        </div>

        {/* Selected chips display */}
        {selectedChips.length > 0 && (
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-600 dark:text-gray-400 mr-2">
              Selected:
            </span>
            {selectedChips.map((feeling) => (
              <span
                key={feeling}
                className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-md text-sm flex items-center space-x-1"
              >
                {feeling}
                <button
                  type="button"
                  onClick={() => toggleChip(feeling)}
                  className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-center">
          <Button
            type="submit"
            size="lg"
            disabled={loading || (!text.trim() && selectedChips.length === 0)}
            className="px-8 py-3 text-lg font-medium bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white shadow-lg hover:shadow-xl transition-all duration-200"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Getting guidance...
              </>
            ) : (
              <>
                <Send className="w-5 h-5 mr-2" />
                Get Guidance
              </>
            )}
          </Button>
        </div>
      </form>

      {/* Help text */}
      <div className="text-center text-sm text-gray-500 dark:text-gray-400">
        <p>
          💡 Tip: Be specific about your feelings for more personalized guidance
        </p>
      </div>
    </div>
  )
}
